@echo off
title Sistema Veterinaria - Cargando...

echo ===================================================
echo   SISTEMA DE GESTION - CLINICA VETERINARIA
echo ===================================================

:: Check for python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    pause
    exit /b
)

:: Virtual Environment Management
if not exist "venv\" (
    echo [1/4] Creando entorno virtual ^(venv^)...
    python -m venv venv
) else (
    echo [1/4] Entorno virtual detectado.
)

echo [2/4] Activando entorno virtual e instalando dependencias...
call venv\Scripts\activate
pip install -r backend/requirements.txt -q

echo [3/4] Abriendo Interfaz de Usuario...
start "" "http://localhost:8080"

:: Start backend in the foreground
echo [4/4] Iniciando Servidor Backend (FastAPI)...
echo.
echo ===================================================
echo   PRESIONE CTRL+C PARA DETENER EL SISTEMA
echo   O CIERRE ESTA VENTANA PARA FINALIZAR
echo ===================================================
echo.
uvicorn backend.app.main:app --host 0.0.0.0 --port 8080

echo.
echo [OK] El sistema se ha detenido.
pause >nul
