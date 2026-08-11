@echo off
title Demo Tai lieu tu hoc
cd /d "%~dp0"

echo Dang mo demo tai lieu tu hoc...
echo Thu muc: %cd%
echo URL mac dinh: http://127.0.0.1:8000/index.html
echo Server: main.py
echo Giao dien: index.html
echo Neu xem tren dien thoai, hay mo dung dia chi do cua so demo hien ra.
echo Neu vua cap nhat code, bam Ctrl+F5 hoac dong tab mo lai de tai ban moi.
echo.

where python >nul 2>nul
if %errorlevel%==0 (
    python main.py --port 8000 --no-browser
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        py main.py --port 8000 --no-browser
    ) else (
        echo Khong tim thay Python.
        echo Hay cai Python hoac chay lenh: python main.py --port 8000 --no-browser
    )
)

echo.
echo Demo da chay. Mo vao dia chi tren trong trinh duyet.
echo Neu muon dung, bam Ctrl+C trong cua so terminal.
pause
