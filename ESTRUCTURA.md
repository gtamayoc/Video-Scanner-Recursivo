# Estructura del Proyecto - Video Scanner

## 📁 Organización de Archivos

```
video-scanner/
│
├── 📄 run_video_scanner.bat      # ⭐ EJECUTAR ESTO (principal con UI)
├── 📄 test_scanner.bat            # Test rápido por consola
├── 📄 requirements.txt            # Dependencias Python
├── 📄 README.md                   # Documentación completa
├── 📄 GUIA-RAPIDA.md             # Guía de inicio rápido
├── 📄 ESTRUCTURA.md              # Este archivo
│
├── 📁 scripts/                    # Código fuente
│   ├── video_scanner.py          # Motor de escaneo (core engine)
│   └── video_scanner_app.py      # Interfaz visual NiceGUI
│
├── 📁 config/                     # ⭐ RESULTADOS AQUÍ
│   ├── videos_escaneados.json    # Exportación JSON completa
│   └── videos_escaneados.csv     # Exportación CSV para Excel
│
├── 📁 logs/                       # Logs del sistema
│   ├── scanner.log               # Log principal
│   └── test_scanner.log          # Log de pruebas
│
├── 📁 temp/                       # Archivos temporales
│   └── (cache temporal)
│
└── 📁 env/                        # Entorno virtual Python (auto-generado)
    ├── Scripts/
    │   └── activate.bat
    └── Lib/
```

---

## 🚀 Archivos Importantes

### ⭐ Para Ejecutar

| Archivo | Propósito | Cuándo Usar |
|---------|-----------|-------------|
| `run_video_scanner.bat` | Interfaz visual completa | **Uso normal** - Siempre |
| `test_scanner.bat` | Test por consola | Pruebas rápidas o debugging |

### 📖 Para Leer

| Archivo | Contenido |
|---------|-----------|
| `README.md` | Documentación completa y detallada |
| `GUIA-RAPIDA.md` | Inicio rápido en 3 pasos |
| `ESTRUCTURA.md` | Este archivo (organización) |

### 📊 Resultados

| Archivo | Formato | Uso |
|---------|---------|-----|
| `config/videos_escaneados.json` | JSON | Scripts, APIs, automatización |
| `config/videos_escaneados.csv` | CSV | Excel, Google Sheets, análisis |

### 📝 Logs

| Archivo | Contenido |
|---------|-----------|
| `logs/scanner.log` | Log detallado del escaneo principal |
| `logs/test_scanner.log` | Log de pruebas por consola |

---

## 🔧 Código Fuente

### `scripts/video_scanner.py` - Motor Principal

**Responsabilidades**:
- ✅ Escaneo recursivo de carpetas (método `escanear_recursivo`)
- ✅ Validación de videos con FFmpeg
- ✅ Extracción de metadatos completos
- ✅ Sistema de logging
- ✅ Exportación a JSON/CSV
- ✅ Control de pausa/reanudar/cancelar

**Clases principales**:
```python
@dataclass
class VideoInfo:
    # Información completa de cada video
    ruta: str
    nombre: str
    duracion_segundos: float
    resolucion: str
    # ... más campos

class VideoScanner:
    # Motor de escaneo
    def escanear_recursivo(carpeta_raiz, callback_progreso)
    def guardar_resultados(videos, output_path)
    # ... más métodos
```

### `scripts/video_scanner_app.py` - Interfaz Visual

**Responsabilidades**:
- ✅ Interfaz NiceGUI interactiva
- ✅ Diálogo de selección de carpetas
- ✅ Barra de progreso en tiempo real
- ✅ Tarjetas de resumen estadístico
- ✅ Tabla de vista previa
- ✅ Botones de exportación
- ✅ Integración con motor de escaneo

**Componentes UI**:
```python
class VideoScannerApp:
    def create_ui()              # Construir interfaz
    def seleccionar_carpeta()    # Diálogo de carpetas
    def iniciar_escaneo()        # Ejecutar escaneo
    def mostrar_resumen()        # Tarjeta de estadísticas
    def mostrar_tabla_videos()   # Tabla interactiva
    # ... más métodos UI
```

---

## 🔄 Flujo de Ejecución

### 1. Usuario ejecuta `run_video_scanner.bat`

```
run_video_scanner.bat
    ↓
1. Verifica Python instalado
2. Crea env/ si no existe
3. Instala dependencias (requirements.txt)
4. Crea carpetas (config/, logs/, temp/)
5. Ejecuta: python scripts/video_scanner_app.py
    ↓
video_scanner_app.py inicia UI
```

### 2. Usuario interactúa con UI

```
UI Abierta
    ↓
Usuario selecciona carpeta
    ↓
Usuario click "Analizar"
    ↓
VideoScannerApp.iniciar_escaneo()
    ↓
VideoScanner.escanear_recursivo()
    ├─ Callback de progreso → Actualiza UI
    ├─ Valida cada video con FFmpeg
    └─ Retorna lista de VideoInfo
    ↓
Mostrar resumen + tabla
    ↓
Guardar JSON + CSV automático
```

### 3. Resultados disponibles

```
config/
├── videos_escaneados.json  # Listo para usar
└── videos_escaneados.csv   # Listo para Excel

logs/
└── scanner.log             # Auditoría completa
```

---

## 📦 Dependencias (requirements.txt)

| Paquete | Versión | Uso |
|---------|---------|-----|
| `nicegui` | 1.4.32 | Interfaz visual moderna |
| `opencv-python` | 4.9.0.80 | Procesamiento de video |
| `Pillow` | 10.2.0 | Manipulación de imágenes |
| `moviepy` | 1.0.3 | Edición de video |
| `mutagen` | 1.47.0 | Metadatos de archivos |
| `ffmpeg-python` | 0.2.0 | Wrapper de FFmpeg |

**Requisito externo**: FFmpeg instalado en el sistema

---

## 🗂️ Carpetas Auto-Generadas

### `env/` - Entorno Virtual

**Creado por**: `run_video_scanner.bat` (primera ejecución)

**Contiene**:
- Python aislado del sistema
- Todas las dependencias instaladas
- Scripts de activación

**No tocar**: Se gestiona automáticamente

---

### `config/` - Resultados de Escaneo

**Creado por**: Script BAT

**Archivos generados**:
```
config/
├── videos_escaneados.json      # Cada escaneo completo
├── videos_escaneados.csv       # Versión Excel
├── videos_escaneados_test.json # De test_scanner.bat
└── videos_escaneados_test.csv  # De test_scanner.bat
```

**Formato JSON**:
```json
{
  "fecha_escaneo": "2025-01-31T14:30:00",
  "estadisticas": {
    "carpetas_escaneadas": 1247,
    "videos_validos": 1847,
    "duracion_total_segundos": 163394
  },
  "videos": [
    {
      "ruta": "C:\\Videos\\video1.mp4",
      "nombre": "video1.mp4",
      "subcarpeta": "2025\\Enero",
      "duracion_segundos": 3600,
      "resolucion": "1920x1080",
      "codec": "h264",
      "fps": 30.0,
      "tamano_mb": 245.8
    }
  ]
}
```

---

### `logs/` - Registros del Sistema

**Creado por**: Script BAT

**Archivos generados**:
```
logs/
├── scanner.log        # UI principal (run_video_scanner.bat)
└── test_scanner.log   # Modo test (test_scanner.bat)
```

**Formato de log**:
```
2025-01-31 14:30:15 - INFO - Iniciando escaneo recursivo en: C:\Videos
2025-01-31 14:30:16 - INFO - Árbol a recorrer: 1247 carpetas
2025-01-31 14:32:45 - INFO - Escaneo completado: 1847 videos válidos
2025-01-31 14:32:45 - INFO - ========================================
2025-01-31 14:32:45 - INFO - ESTADÍSTICAS DEL ESCANEO
2025-01-31 14:32:45 - INFO - Carpetas escaneadas: 1247
```

---

### `temp/` - Archivos Temporales

**Creado por**: Script BAT

**Uso**: Cache temporal durante procesamiento

**Se puede borrar**: Sí (se regenera automáticamente)

---

## 🎯 Personalización

### Modificar Filtros de Tamaño

**Archivo**: `scripts/video_scanner.py`

```python
class VideoScanner:
    TAMANO_MIN_MB = 1.0          # Cambiar mínimo aquí
    TAMANO_MAX_MB = 50 * 1024    # Cambiar máximo aquí (en MB)
```

**Alternativa**: Usar configuración avanzada en la UI (no requiere editar código)

---

### Agregar Extensiones

**Archivo**: `scripts/video_scanner.py`

```python
class VideoScanner:
    EXTENSIONES_VALIDAS = ['.mp4']  # Agregar: '.avi', '.mkv', etc.
```

---

### Cambiar Puerto de UI

**Archivo**: `scripts/video_scanner_app.py` (última línea)

```python
ui.run(
    title='Escáner de Videos',
    native=True,
    window_size=(1400, 900),
    port=8080,  # Cambiar puerto aquí
    reload=False
)
```

---

## 🧹 Limpieza

### Borrar Resultados Antiguos
```bash
del config\*.json
del config\*.csv
```

### Borrar Logs
```bash
del logs\*.log
```

### Resetear Completamente
```bash
rmdir /s env
rmdir /s config
rmdir /s logs
rmdir /s temp
```

Luego ejecutar `run_video_scanner.bat` para reinstalar todo.

---

## 📋 Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] FFmpeg instalado y en PATH
- [ ] Todos los archivos del proyecto descargados
- [ ] Ejecutado `run_video_scanner.bat` por primera vez
- [ ] Entorno virtual creado en `env/`
- [ ] Dependencias instaladas correctamente
- [ ] UI se abre sin errores
- [ ] Carpetas `config/`, `logs/`, `temp/` creadas

---

**¡Sistema listo para escanear miles de videos! 🚀**
