@echo off
setlocal
cd /d "%~dp0"

set "VENV_PY=%~dp0.venv\Scripts\python.exe"

echo Dang mo demo tai lieu tu hoc...
echo Thu muc: %cd%
echo URL mac dinh: http://127.0.0.1:8000/index.html
echo Server: main.py
echo Giao dien: index.html
echo Neu vua cap nhat code, bam Ctrl+F5 hoac mo tab moi de tai ban moi.
echo.

if exist "%VENV_PY%" (
    "%VENV_PY%" main.py --port 8000 --no-browser
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        python main.py --port 8000 --no-browser
    ) else (
        where py >nul 2>nul
        if %errorlevel%==0 (
            py main.py --port 8000 --no-browser
        ) else (
            echo Khong tim thay Python hoac .venv.
            echo Hay cai dat Python hoac chay lenh: python main.py --port 8000 --no-browser
            pause
            exit /b 1
        )
    )
)

echo.
echo Demo da chay. Mo dia chi tren trong trinh duyet.
echo Neu muon dung, bam Ctrl+C trong cua so terminal.
pause
