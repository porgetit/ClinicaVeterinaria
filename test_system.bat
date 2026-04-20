@echo off
title Sistema Veterinaria - Ejecutando Pruebas

echo ===================================================
echo   SUITE DE PRUEBAS - CLINICA VETERINARIA
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

echo [2/4] Activando entorno virtual...
call venv\Scripts\activate

:: Install dependencies
echo [3/4] Instalando dependencias...
pip install -r backend/requirements.txt -q

echo [4/4] Ejecutando pruebas con pytest...
echo.
set PYTHONPATH=.
pytest backend/tests/test_api.py -v

echo.
echo ===================================================
echo   PRUEBAS FINALIZADAS
echo ===================================================
pause >nul
