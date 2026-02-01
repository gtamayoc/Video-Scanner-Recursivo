@echo off
REM ===================================================
REM Script de ejecución - Escáner Recursivo de Videos
REM ===================================================

echo.
echo ========================================
echo   Escaner Recursivo de Videos YouTube
echo ========================================
echo.

REM Verificar si existe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en PATH
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
IF NOT EXIST "env\\Scripts\\activate.bat" (
    echo [INFO] Creando entorno virtual...
    python -m venv env
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call env\\Scripts\\activate.bat

REM Actualizar pip
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install -r requirements.txt --quiet

REM Crear carpetas necesarias
IF NOT EXIST "config" mkdir config
IF NOT EXIST "temp" mkdir temp
IF NOT EXIST "logs" mkdir logs

REM Ejecutar aplicación principal
echo.
echo [INFO] Iniciando escaner de videos...
echo [INFO] Presiona Ctrl+C para detener
echo.

python scripts/video_scanner_app.py

pause
