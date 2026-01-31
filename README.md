<div align="center">
  # 🎥 Video Scanner Recursivo
  
  ![Repo Card](https://via.placeholder.com/1200x300/1e3a8a/ffffff?text=Video+Scanner+Recursivo+-+Escaneo+TOTAL+de+Carpetas)
</div>

# 🎥 Video Scanner Recursivo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/Windows-Optimized-blue.svg)](https://github.com/)
[![FFmpeg](https://img.shields.io/badge/Powered%20by-FFmpeg-orange.svg)](https://ffmpeg.org/)

**Escanea recursivamente TODAS las subcarpetas para encontrar videos MP4 válidos con metadatos completos. 100% Local.**

## ✨ Características Principales

| ✅ **Escaneo Total** | 🔍 **Validación Inteligente** | 📊 **Metadatos Completos** |
|---------------------|------------------------------|---------------------------|
| Recorre **sin límite** de profundidad | Verifica MP4 **reales** (FFmpeg) | Duración, resolución, FPS, codec |
| Progreso **en tiempo real** | Ignora corrupto/archivos falsos | Tamaño, bitrate, fecha mod. |
| Pausar/Reanudar/Cancelar | Filtros de tamaño configurables | Exporta JSON + CSV (Excel) |

## 🚀 Instalación en 3 Clics

```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/video-scanner-recursivo.git
cd video-scanner-recursivo

# 2. Doble click:
run_video_scanner.bat
```

**¡Automático!** ✅ Crea entorno virtual + instala dependencias + abre UI

## 📱 Demo de Uso

```
PASO 1: Seleccionar Carpeta Raíz
📁 C:\Videos\YouTube\2025

PASO 2: Analizar Completamente
🔍 Escaneando... 847/1.247 carpetas (73%)

PASO 3: Resultados
📁 Carpetas: 1,247
🎥 Videos MP4: 1,847 válidos
⏱️ Duración: 45:23:14
💾 Tamaño: 128.4 GB
```

## 📊 Ejemplo de Resultados

**Resumen Visual:**
```
📁 Carpeta escaneada: "C:\MisVideos\2025"
🔍 Árbol recorrido: 1.247 carpetas
🎥 Videos MP4 encontrados: 1.847 archivos
⏱️ Duración total: 45:23:14
💾 Tamaño total: 128.4 GB

**Vista previa (15 primeros):**
📄 video001.mp4 (Temporada1/Episodio1)
📄 highlight_game.mp4 (Gaming/2025_01)
📄 clip_reunion.mp4 (Trabajo/2025/Enero)
...
```

**Exporta automáticamente:**
- `config/videos_escaneados.json`
- `config/videos_escaneados.csv` (Excel)

## 🛠️ Requisitos Mínimos

| Requisito | Acción |
|-----------|--------|
| **Python 3.8+** | [Descargar](https://python.org/downloads/) |
| **FFmpeg** | [Descargar](https://ffmpeg.org/download.html) + PATH |

**Verificar FFmpeg:**
```bash
ffmpeg -version
```

## 📁 Estructura del Proyecto

```
📁 video-scanner-recursivo/
├── run_video_scanner.bat          ⭐ PRINCIPAL
├── test_scanner.bat              Test consola
├── requirements.txt              Dependencias
├── README.md                     ⭐ Este archivo
├── GUIA-RAPIDA.md                Guía rápida
│
├── 📁 scripts/
│   ├── video_scanner.py          Motor core
│   └── video_scanner_app.py      UI NiceGUI
│
├── 📁 config/                    ⭐ RESULTADOS
│   ├── videos_escaneados.json
│   └── videos_escaneados.csv
├── 📁 logs/                      Logs detallados
└── 📁 env/                       Auto-generado
```

## 🎯 Uso Paso a Paso

```
1. run_video_scanner.bat
2. "Seleccionar Carpeta Raíz de Videos"
3. Configurar filtros (opcional)
4. "Analizar Completamente"
5. ✅ Ver resultados + exportar
```

## 📈 Rendimiento Esperado

| Videos | SSD | HDD |
|--------|-----|-----|
| **100** | 10s | 30s |
| **1,000** | 1-2min | 3-5min |
| **10,000** | 10-15min | 30-40min |
| **100,000** | 1-2h | 3-5h |

## 💾 Formato JSON de Salida

```json
{
  "fecha_escaneo": "2026-01-31T15:00:00",
  "estadisticas": {
    "carpetas_escaneadas": 1247,
    "videos_validos": 1847,
    "duracion_total_segundos": 163394
  },
  "videos": [
    {
      "ruta": "C:\\Videos\\Gaming\\clip1.mp4",
      "nombre": "clip1.mp4",
      "subcarpeta": "Gaming/2025_01",
      "tamano_mb": 245.8,
      "duracion_segundos": 3600,
      "resolucion": "1920x1080",
      "codec": "h264",
      "fps": 30.0,
      "es_valido": true
    }
  ]
}
```

## 🎛️ Configuración Avanzada

**En la UI:**
```
⚙️ Tamaño mínimo: 1 MB (thumbnails)
⚙️ Tamaño máximo: 50 GB (gigantes)
```

**En código** (`scripts/video_scanner.py`):
```python
EXTENSIONES_VALIDAS = ['.mp4']           # + '.avi', '.mkv'
TAMANO_MIN_MB = 1.0                     # Filtro mínimo
TAMANO_MAX_MB = 50 * 1024               # Filtro máximo
```

## 🐛 Problemas Comunes + Soluciones

| Error | Solución |
|-------|----------|
| `nicegui==1.4.32` | Usa `requirements.txt` actualizado |
| `pywebview` faltante | `pip install pywebview` |
| `FFmpeg no encontrado` | Descargar + agregar a PATH |
| UI no abre | Cambiar puerto: `port=8081` |

## 📚 Documentación Completa

- [🆕 **Guía Rápida** (3 pasos)](GUIA-RAPIDA.md)
- [📁 **Estructura del Proyecto**](ESTRUCTURA.md)

## 🤝 Cómo Contribuir

1. Fork el repositorio
2. Crear branch (`git checkout -b feature`)
3. Commit (`git commit -m 'Add feature'`)
4. Push (`git push origin feature`)
5. Abrir Pull Request

## 📄 Licencia

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Usa libremente en proyectos personales y comerciales.

## 🙏 Agradecimientos

<div align="center">

[![NiceGUI](https://nicegui.io/badge.svg)](https://nicegui.io/) 
[![FFmpeg](https://img.shields.io/badge/Powered%20by-FFmpeg-orange.svg)](https://ffmpeg.org/)
[![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://python.org/)

</div>

---

<div align="center">
  
**⭐ Star si te sirvió** | **🍴 Fork para modificar** | **🚀 ¡Escanea miles de videos!**

</div>

---
```

## 📋 **Archivos Adicionales para GitHub**

### **requirements.txt** (Actualizado)
```txt
# Dependencias estables Enero 2026
nicegui>=1.4.33,<3.0.0
pywebview>=5.0
opencv-python>=4.9.0
Pillow>=10.2.0
moviepy>=1.0.3
mutagen>=1.47.0
ffmpeg-python>=0.2.0
```

### **LICENSE** (MIT)
```
MIT License

Copyright (c) 2026 gtamayoc

Permission is hereby granted, free of charge, to any person obtaining a copy...
```
