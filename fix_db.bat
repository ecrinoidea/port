@echo off
REM Script untuk menjalankan fix database dengan Python

setlocal enabledelayedexpansion

REM Cari Python di PATH
for /f "tokens=*" %%i in ('where python.exe 2^>nul') do set PYTHON_PATH=%%i

if not defined PYTHON_PATH (
    echo Python tidak ditemukan di PATH
    echo Mencoba menemukan Python dari Microsoft Store...
    
    REM Cek di AppData
    if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
        set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python314\python.exe
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
        set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    )
)

if not defined PYTHON_PATH (
    echo Python tidak dapat ditemukan
    pause
    exit /b 1
)

echo Menggunakan Python: !PYTHON_PATH!

REM Install dependencies
echo.
echo Installing dependencies...
"!PYTHON_PATH!" -m pip install --break-system-packages Flask python-dotenv PyMySQL cloudinary resend cryptography > nul 2>&1

REM Run fix_database.py
echo.
echo Memperbaiki database...
"!PYTHON_PATH!" fix_database.py

echo.
echo Selesai!
pause
