"""
Escáner Recursivo de Videos - Core Engine
Maneja el escaneo profundo de carpetas y validación de videos MP4
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import cv2
import ffmpeg

@dataclass
class VideoInfo:
    """Información completa de un video detectado"""
    ruta: str
    nombre: str
    subcarpeta: str
    tamano_mb: float
    duracion_segundos: float
    resolucion: str
    codec: str
    fps: float
    bitrate_kbps: float
    fecha_modificacion: str
    es_valido: bool
    error: Optional[str] = None

class VideoScanner:
    """Motor de escaneo recursivo de videos"""
    
    # Configuración por defecto
    EXTENSIONES_VALIDAS = ['.mp4']
    TAMANO_MIN_MB = 1.0
    TAMANO_MAX_MB = 50 * 1024  # 50 GB
    MAX_ARCHIVOS_WARNING = 10000
    
    def __init__(self, log_file: str = 'logs/scanner.log'):
        """Inicializar escáner con logging"""
        self.setup_logging(log_file)
        self.stats = {
            'carpetas_escaneadas': 0,
            'archivos_procesados': 0,
            'videos_validos': 0,
            'videos_invalidos': 0,
            'errores': 0,
            'tamano_total_mb': 0.0,
            'duracion_total_segundos': 0.0
        }
        self.paused = False
        self.cancelled = False
        
    def setup_logging(self, log_file: str):
        """Configurar sistema de logs"""
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def escanear_recursivo(
        self, 
        carpeta_raiz: str,
        callback_progreso: Optional[callable] = None
    ) -> List[VideoInfo]:
        """
        Escanear recursivamente toda la estructura de carpetas
        
        Args:
            carpeta_raiz: Carpeta inicial del escaneo
            callback_progreso: Función para reportar progreso (carpetas_total, carpetas_actual, archivo_actual)
            
        Returns:
            Lista de VideoInfo con todos los videos válidos encontrados
        """
        self.logger.info(f"Iniciando escaneo recursivo en: {carpeta_raiz}")
        
        # Resetear estadísticas
        self.stats = {key: 0 if isinstance(value, int) else 0.0 
                     for key, value in self.stats.items()}
        self.cancelled = False
        
        videos = []
        carpeta_raiz = Path(carpeta_raiz).resolve()
        
        # Fase 1: Contar total de carpetas (para progreso preciso)
        total_carpetas = sum(1 for _ in os.walk(carpeta_raiz))
        self.logger.info(f"Árbol a recorrer: {total_carpetas} carpetas")
        
        # Fase 2: Escanear archivos
        carpetas_procesadas = 0
        
        for root, dirs, files in os.walk(carpeta_raiz):
            if self.cancelled:
                self.logger.warning("Escaneo cancelado por usuario")
                break
            
            # Esperar si está pausado
            while self.paused and not self.cancelled:
                import time
                time.sleep(0.1)
            
            carpetas_procesadas += 1
            self.stats['carpetas_escaneadas'] = carpetas_procesadas
            
            # Filtrar directorios ocultos
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            root_path = Path(root)
            subcarpeta_relativa = str(root_path.relative_to(carpeta_raiz))
            
            # Reportar progreso
            if callback_progreso:
                callback_progreso(total_carpetas, carpetas_procesadas, root)
            
            # Procesar archivos en esta carpeta
            for file in files:
                if self.cancelled:
                    break
                
                # Filtrar por extensión
                if not any(file.lower().endswith(ext) for ext in self.EXTENSIONES_VALIDAS):
                    continue
                
                # Filtrar archivos ocultos y temporales
                if file.startswith('.') or file.startswith('~'):
                    continue
                
                ruta_completa = root_path / file
                self.stats['archivos_procesados'] += 1
                
                # Validar archivo
                video_info = self._validar_video(
                    str(ruta_completa),
                    file,
                    subcarpeta_relativa
                )
                
                if video_info:
                    if video_info.es_valido:
                        videos.append(video_info)
                        self.stats['videos_validos'] += 1
                        self.stats['tamano_total_mb'] += video_info.tamano_mb
                        self.stats['duracion_total_segundos'] += video_info.duracion_segundos
                    else:
                        self.stats['videos_invalidos'] += 1
                
                # Advertencia si hay demasiados archivos
                if len(videos) >= self.MAX_ARCHIVOS_WARNING:
                    self.logger.warning(
                        f"Se detectaron más de {self.MAX_ARCHIVOS_WARNING} videos. "
                        "Considera filtrar o dividir el escaneo."
                    )
        
        # Ordenar alfabéticamente por nombre
        videos.sort(key=lambda v: v.nombre.lower())
        
        self.logger.info(f"Escaneo completado: {len(videos)} videos válidos encontrados")
        self._log_statistics()
        
        return videos
    
    def _validar_video(
        self, 
        ruta: str, 
        nombre: str, 
        subcarpeta: str
    ) -> Optional[VideoInfo]:
        """
        Validar que el archivo sea un video MP4 real y extraer metadatos
        
        Returns:
            VideoInfo si es válido, None si hay error crítico
        """
        try:
            # Verificar existencia y tamaño
            if not os.path.exists(ruta):
                return None
            
            tamano_bytes = os.path.getsize(ruta)
            tamano_mb = tamano_bytes / (1024 * 1024)
            
            # Filtro de tamaño
            if tamano_mb < self.TAMANO_MIN_MB or tamano_mb > self.TAMANO_MAX_MB:
                return VideoInfo(
                    ruta=ruta,
                    nombre=nombre,
                    subcarpeta=subcarpeta,
                    tamano_mb=tamano_mb,
                    duracion_segundos=0,
                    resolucion="N/A",
                    codec="N/A",
                    fps=0,
                    bitrate_kbps=0,
                    fecha_modificacion="",
                    es_valido=False,
                    error=f"Tamaño fuera de rango ({tamano_mb:.1f} MB)"
                )
            
            # Extraer metadatos con ffmpeg
            try:
                probe = ffmpeg.probe(ruta)
                video_stream = next(
                    (s for s in probe['streams'] if s['codec_type'] == 'video'),
                    None
                )
                
                if not video_stream:
                    raise ValueError("No se encontró stream de video")
                
                # Extraer información
                duracion = float(probe['format'].get('duration', 0))
                ancho = int(video_stream.get('width', 0))
                alto = int(video_stream.get('height', 0))
                codec = video_stream.get('codec_name', 'unknown')
                fps = eval(video_stream.get('r_frame_rate', '0/1'))
                bitrate = float(probe['format'].get('bit_rate', 0)) / 1000  # kbps
                
                fecha_mod = datetime.fromtimestamp(
                    os.path.getmtime(ruta)
                ).strftime('%Y-%m-%d %H:%M:%S')
                
                return VideoInfo(
                    ruta=ruta,
                    nombre=nombre,
                    subcarpeta=subcarpeta,
                    tamano_mb=tamano_mb,
                    duracion_segundos=duracion,
                    resolucion=f"{ancho}x{alto}",
                    codec=codec,
                    fps=fps,
                    bitrate_kbps=bitrate,
                    fecha_modificacion=fecha_mod,
                    es_valido=True
                )
                
            except Exception as e:
                # Video corrupto o no válido
                return VideoInfo(
                    ruta=ruta,
                    nombre=nombre,
                    subcarpeta=subcarpeta,
                    tamano_mb=tamano_mb,
                    duracion_segundos=0,
                    resolucion="N/A",
                    codec="N/A",
                    fps=0,
                    bitrate_kbps=0,
                    fecha_modificacion="",
                    es_valido=False,
                    error=f"Error al leer video: {str(e)}"
                )
        
        except Exception as e:
            self.logger.error(f"Error procesando {nombre}: {str(e)}")
            self.stats['errores'] += 1
            return None
    
    def _log_statistics(self):
        """Registrar estadísticas finales"""
        duracion_total = str(timedelta(seconds=int(self.stats['duracion_total_segundos'])))
        
        self.logger.info("=" * 60)
        self.logger.info("ESTADÍSTICAS DEL ESCANEO")
        self.logger.info("=" * 60)
        self.logger.info(f"Carpetas escaneadas: {self.stats['carpetas_escaneadas']}")
        self.logger.info(f"Archivos procesados: {self.stats['archivos_procesados']}")
        self.logger.info(f"Videos válidos: {self.stats['videos_validos']}")
        self.logger.info(f"Videos inválidos: {self.stats['videos_invalidos']}")
        self.logger.info(f"Errores: {self.stats['errores']}")
        self.logger.info(f"Tamaño total: {self.stats['tamano_total_mb']:.2f} MB "
                        f"({self.stats['tamano_total_mb']/1024:.2f} GB)")
        self.logger.info(f"Duración total: {duracion_total}")
        self.logger.info("=" * 60)
    
    def guardar_resultados(self, videos: List[VideoInfo], output_path: str, carpeta_raiz: str = None):
        """Guardar lista de videos en JSON"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            data = {
                'fecha_escaneo': datetime.now().isoformat(),
                'carpeta_raiz': carpeta_raiz,
                'estadisticas': self.stats,
                'videos': [asdict(v) for v in videos]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Resultados guardados en: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando resultados: {str(e)}")
            return False
    
    def cargar_resultados(self, input_path: str) -> Tuple[List[VideoInfo], dict, Optional[str]]:
        """Cargar lista de videos desde JSON"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            videos = [VideoInfo(**v) for v in data['videos']]
            stats = data.get('estadisticas', {})
            carpeta_raiz = data.get('carpeta_raiz')
            
            self.logger.info(f"Cargados {len(videos)} videos desde: {input_path}")
            return videos, stats, carpeta_raiz
            
        except Exception as e:
            self.logger.error(f"Error cargando resultados: {str(e)}")
            return [], {}, None
            
        except Exception as e:
            self.logger.error(f"Error cargando resultados: {str(e)}")
            return [], {}
    
    def pause(self):
        """Pausar el escaneo"""
        self.paused = True
        self.logger.info("Escaneo pausado")
    
    def resume(self):
        """Reanudar el escaneo"""
        self.paused = False
        self.logger.info("Escaneo reanudado")
    
    def cancel(self):
        """Cancelar el escaneo"""
        self.cancelled = True
        self.logger.warning("Escaneo cancelado")


def formatear_duracion(segundos: float) -> str:
    """Convertir segundos a formato HH:MM:SS"""
    return str(timedelta(seconds=int(segundos)))


def formatear_tamano(mb: float) -> str:
    """Formatear tamaño en unidades legibles"""
    if mb < 1024:
        return f"{mb:.1f} MB"
    else:
        return f"{mb/1024:.2f} GB"
