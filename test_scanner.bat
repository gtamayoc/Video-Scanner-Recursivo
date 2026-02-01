@echo off
REM ===================================================
REM Script de Prueba - Test Rápido sin UI
REM ===================================================

echo.
echo ========================================
echo   TEST: Escaner de Videos (consola)
echo ========================================
echo.

REM Verificar si existe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en PATH
    pause
    exit /b 1
)

REM Activar entorno virtual si existe
IF EXIST "env\\Scripts\\activate.bat" (
    echo [INFO] Activando entorno virtual...
    call env\\Scripts\\activate.bat
) ELSE (
    echo [ADVERTENCIA] Entorno virtual no encontrado
    echo [INFO] Ejecuta run_video_scanner.bat primero
    echo.
)

REM Ejecutar script de prueba
python test_scanner.py

pause
