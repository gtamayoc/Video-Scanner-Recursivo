# 🚀 Guía Rápida de Inicio

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Primera Vez - Instalación
```bash
# Doble click en:
run_video_scanner.bat
```
✅ Crea entorno virtual automáticamente
✅ Instala todas las dependencias
✅ Abre la interfaz visual

### 2️⃣ Seleccionar Carpeta
En la interfaz que se abre:
1. Click en **"Seleccionar Carpeta"**
2. Navegar a tu carpeta de videos (ejemplo: `C:\Videos\YouTube`)
3. Click **"Select Folder"**

### 3️⃣ Escanear
1. Click en **"Analizar Completamente"**
2. Esperar a que termine (ver barra de progreso)
3. ✅ ¡Listo! Ver resultados y exportar

---

## 📋 Ejemplo Práctico

### Escenario: Tienes 1000+ videos en subcarpetas

```
C:\MisVideos\
├── 2023\
│   ├── Enero\
│   │   ├── video001.mp4
│   │   └── video002.mp4
│   ├── Febrero\
│   └── Diciembre\
├── 2024\
│   ├── Gaming\
│   ├── Tutoriales\
│   └── Vlogs\
└── 2025\
    └── ...
```

**Acción**: Seleccionar `C:\MisVideos\`

**Resultado**: El sistema encuentra **TODOS** los MP4 en **TODAS** las subcarpetas

**Exportación**: 
- `config/videos_escaneados.json` → Datos completos
- `config/videos_escaneados.csv` → Abrir en Excel

---

## 🎯 ¿Qué Hace el Escáner?

### ✅ SÍ Hace
- ✅ Recorre **TODAS** las subcarpetas (sin límite)
- ✅ Encuentra **TODOS** los `.mp4`
- ✅ Valida que sean videos reales (no archivos corruptos)
- ✅ Extrae duración, resolución, tamaño, FPS, codec
- ✅ Guarda todo en JSON y CSV
- ✅ Muestra progreso en tiempo real
- ✅ Permite pausar/reanudar/cancelar

### ❌ NO Hace
- ❌ No modifica archivos
- ❌ No mueve ni copia videos
- ❌ No sube nada a internet
- ❌ No convierte formatos

---

## 🔧 Configuración Opcional

### Filtrar por Tamaño

**En la interfaz → "Configuración Avanzada":**

| Parámetro | Default | Uso |
|-----------|---------|-----|
| **Tamaño mínimo** | 1 MB | Ignorar thumbnails y clips muy cortos |
| **Tamaño máximo** | 50 GB | Ignorar archivos sospechosamente grandes |

**Ejemplo**: Si solo quieres videos entre 10 MB y 5 GB:
- Tamaño mínimo: `10`
- Tamaño máximo: `5` (en GB)

---

## 📊 Interpretando Resultados

### Pantalla de Resumen

```
📁 Carpetas Escaneadas: 1,247
🎥 Videos Encontrados: 1,847
⏱️ Duración Total: 45:23:14
💾 Tamaño Total: 128.4 GB
```

**Significado**:
- **1,247 carpetas** → Recorrió TODO el árbol de directorios
- **1,847 videos** → Encontró y validó todos los MP4
- **45:23:14** → Suma de duración de todos los videos
- **128.4 GB** → Espacio total ocupado

### Tabla de Vista Previa

Muestra los **primeros 50 videos** con:
- Nombre del archivo
- Subcarpeta relativa
- Duración (HH:MM:SS)
- Resolución (1920x1080, etc.)
- Tamaño (MB/GB)

---

## 💾 Usando los Archivos Exportados

### JSON (`videos_escaneados.json`)

**Usar para**:
- Scripts de automatización
- Integración con APIs (YouTube, etc.)
- Procesamiento por lotes

**Ejemplo Python**:
```python
import json

with open('config/videos_escaneados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

videos = data['videos']
for video in videos:
    print(f"{video['nombre']} - {video['duracion_segundos']}s")
```

### CSV (`videos_escaneados.csv`)

**Usar para**:
- Abrir en Excel / Google Sheets
- Análisis con tablas dinámicas
- Reportes visuales

**Columnas**:
- Nombre
- Subcarpeta
- Ruta Completa
- Duración
- Tamaño (MB)
- Resolución
- FPS
- Codec
- Fecha Modificación

---

## 🐛 Problemas Comunes

### ❌ "FFmpeg no encontrado"

**Causa**: FFmpeg no está instalado o no está en PATH

**Solución**:
1. Descargar FFmpeg: https://ffmpeg.org/download.html
2. Extraer a `C:\ffmpeg`
3. Agregar `C:\ffmpeg\bin` a PATH del sistema
4. Reiniciar terminal

**Verificar instalación**:
```bash
ffmpeg -version
```

### ❌ UI no se abre

**Causa**: Puerto 8080 ocupado

**Solución temporal**:
Editar `scripts/video_scanner_app.py` (última línea):
```python
ui.run(port=8081, native=True)  # Cambiar puerto
```

### ⚠️ Escaneo muy lento

**Causas posibles**:
- Disco duro lento (HDD)
- Carpeta con millones de archivos
- Antivirus escaneando cada archivo

**Soluciones**:
1. Excluir carpeta del antivirus temporalmente
2. Dividir escaneo en subcarpetas más pequeñas
3. Aumentar tamaño mínimo en configuración (filtrar más)

### ⚠️ "Se detectaron más de 10,000 videos"

**No es error**, solo advertencia.

**Opciones**:
- ✅ Continuar normalmente (funciona igual)
- ✅ Filtrar por fecha/tamaño para reducir
- ✅ Dividir en múltiples escaneos

---

## 📁 Estructura de Carpetas Creadas

```
video-scanner/
├── config/                    # ← RESULTADOS AQUÍ
│   ├── videos_escaneados.json # Archivo principal
│   └── videos_escaneados.csv  # Para Excel
│
├── logs/                      # ← LOGS DETALLADOS
│   └── scanner.log            # Registro completo
│
├── temp/                      # Archivos temporales
└── env/                       # Entorno Python (ignorar)
```

---

## 🎓 Tips Avanzados

### 1. Escanear solo una subcarpeta específica

No selecciones la raíz completa, selecciona directamente:
```
C:\Videos\2025\Gaming\  # Solo Gaming de 2025
```

### 2. Comparar dos escaneos

Ejecuta el escáner dos veces:
1. Primera vez → `videos_escaneados.json`
2. Renombrar a `escaneo_enero.json`
3. Segunda vez → nuevo `videos_escaneados.json`
4. Comparar ambos JSON para ver diferencias

### 3. Integrar con script de subida

```python
# Cargar resultados del escáner
import json

with open('config/videos_escaneados.json', 'r') as f:
    data = json.load(f)

# Subir cada video a YouTube
for video in data['videos']:
    upload_to_youtube(
        file_path=video['ruta'],
        title=video['nombre'],
        duration=video['duracion_segundos']
    )
```

---

## ⏱️ Tiempos Estimados

| Cantidad de Videos | SSD | HDD |
|-------------------|-----|-----|
| 100 videos | 10 seg | 30 seg |
| 1,000 videos | 1-2 min | 3-5 min |
| 10,000 videos | 10-15 min | 30-40 min |
| 100,000 videos | 1-2 horas | 3-5 horas |

*Tiempos aproximados, varían según hardware*

---

## 🆘 Ayuda Rápida

### Ver logs en tiempo real
```bash
# Windows
notepad logs\scanner.log

# O usar editor de texto favorito
```

### Limpiar y reiniciar
```bash
# Borrar resultados anteriores
del config\*.json
del config\*.csv
del logs\*.log

# Ejecutar de nuevo
run_video_scanner.bat
```

### Desinstalar
```bash
# Borrar entorno virtual
rmdir /s env

# Borrar resultados
rmdir /s config
rmdir /s logs
```

---

## 📞 Soporte

1. **Revisar logs**: `logs/scanner.log`
2. **Verificar FFmpeg**: `ffmpeg -version`
3. **Probar carpeta pequeña primero**: Test con 10-20 videos
4. **Usar modo test**: `test_scanner.bat` (modo consola)

---

**¡Listo para escanear miles de videos! 🚀**
