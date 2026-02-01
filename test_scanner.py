"""
Script de Prueba - Escaneo Recursivo sin UI
Para testing rápido del motor de escaneo
"""

import sys
import os
from pathlib import Path

# Agregar ruta de scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from video_scanner import VideoScanner, formatear_duracion, formatear_tamano


def callback_progreso(total, actual, carpeta):
    """Mostrar progreso en consola"""
    porcentaje = (actual / total * 100) if total > 0 else 0
    carpeta_corta = os.path.basename(carpeta)
    print(f"\r🔍 Progreso: {actual}/{total} ({porcentaje:.1f}%) - {carpeta_corta[:50]:<50}", end='')


def main():
    print("=" * 80)
    print("🎥 ESCÁNER RECURSIVO DE VIDEOS - TEST")
    print("=" * 80)
    print()
    
    # Solicitar carpeta
    carpeta = input("📁 Ingresa la ruta de la carpeta a escanear: ").strip()
    
    if not os.path.exists(carpeta):
        print(f"❌ Error: La carpeta '{carpeta}' no existe")
        return
    
    print()
    print(f"✅ Carpeta válida: {carpeta}")
    print()
    
    # Confirmar
    confirmar = input("¿Iniciar escaneo recursivo? (s/n): ").strip().lower()
    if confirmar != 's':
        print("❌ Escaneo cancelado")
        return
    
    print()
    print("🚀 Iniciando escaneo recursivo...")
    print()
    
    # Crear escáner
    scanner = VideoScanner(log_file='logs/test_scanner.log')
    
    # Ejecutar escaneo
    try:
        videos = scanner.escanear_recursivo(
            carpeta,
            callback_progreso=callback_progreso
        )
        
        print()  # Nueva línea después de progreso
        print()
        print("=" * 80)
        print("📊 RESULTADOS DEL ESCANEO")
        print("=" * 80)
        print()
        
        # Estadísticas
        stats = scanner.stats
        print(f"📁 Carpetas escaneadas: {stats['carpetas_escaneadas']:,}")
        print(f"📄 Archivos procesados: {stats['archivos_procesados']:,}")
        print(f"🎥 Videos válidos: {stats['videos_validos']:,}")
        print(f"⚠️  Videos inválidos: {stats['videos_invalidos']:,}")
        print(f"❌ Errores: {stats['errores']:,}")
        print()
        print(f"⏱️  Duración total: {formatear_duracion(stats['duracion_total_segundos'])}")
        print(f"💾 Tamaño total: {formatear_tamano(stats['tamano_total_mb'])}")
        print()
        
        # Vista previa de primeros 15 videos
        if videos:
            print("=" * 80)
            print("📋 VISTA PREVIA (primeros 15 videos)")
            print("=" * 80)
            print()
            
            for i, video in enumerate(videos[:15], 1):
                print(f"{i:2d}. 📄 {video.nombre}")
                print(f"    └─ Subcarpeta: {video.subcarpeta}")
                print(f"    └─ Duración: {formatear_duracion(video.duracion_segundos)} | "
                      f"Tamaño: {formatear_tamano(video.tamano_mb)} | "
                      f"Resolución: {video.resolucion}")
                print()
            
            if len(videos) > 15:
                print(f"... y {len(videos) - 15} videos más")
                print()
        
        # Guardar resultados
        output_json = 'config/videos_escaneados_test.json'
        output_csv = 'config/videos_escaneados_test.csv'
        
        print("=" * 80)
        print("💾 GUARDANDO RESULTADOS")
        print("=" * 80)
        print()
        
        if scanner.guardar_resultados(videos, output_json):
            print(f"✅ JSON guardado: {output_json}")
        
        # Guardar CSV
        import csv
        try:
            with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Nombre', 'Subcarpeta', 'Ruta Completa', 'Duración',
                    'Tamaño (MB)', 'Resolución', 'FPS', 'Codec', 'Fecha Modificación'
                ])
                
                for v in videos:
                    writer.writerow([
                        v.nombre,
                        v.subcarpeta,
                        v.ruta,
                        formatear_duracion(v.duracion_segundos),
                        f"{v.tamano_mb:.2f}",
                        v.resolucion,
                        f"{v.fps:.2f}",
                        v.codec,
                        v.fecha_modificacion
                    ])
            
            print(f"✅ CSV guardado: {output_csv}")
        except Exception as e:
            print(f"❌ Error guardando CSV: {str(e)}")
        
        print()
        print("=" * 80)
        print("✅ ESCANEO COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print()
        print()
        print("⚠️  Escaneo interrumpido por usuario")
    
    except Exception as e:
        print()
        print()
        print(f"❌ Error durante el escaneo: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    input("Presiona Enter para salir...")


if __name__ == "__main__":
    main()
