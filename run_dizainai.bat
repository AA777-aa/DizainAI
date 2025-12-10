@echo off
chcp 65001 >nul
title DizainAI - Запуск

echo ========================================
echo    DizainAI - Программа дизайна интерьера
echo ========================================
echo.

cd /d "%~dp0"

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python 3.9+ с python.org
    pause
    exit /b 1
)

REM Проверяем виртуальное окружение
if not exist "venv" (
    echo [INFO] Создание виртуального окружения...
    python -m venv venv
)

REM Активируем виртуальное окружение
call venv\Scripts\activate.bat

REM Устанавливаем зависимости если нужно
if not exist "venv\Lib\site-packages\PyQt5" (
    echo [INFO] Установка зависимостей...
    pip install -r requirements.txt
)

echo [INFO] Запуск DizainAI...
python main.py

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Программа завершилась с ошибкой
    pause
)