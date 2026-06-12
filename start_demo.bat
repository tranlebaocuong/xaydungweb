@echo off
title Demo Tai lieu tu hoc
cd /d "%~dp0"

echo Dang mo demo tai lieu tu hoc...
echo Thu muc: %cd%
echo URL mac dinh: http://127.0.0.1:8000/index.html
echo Style hien tai: styles.css?v=14
echo Script hien tai: script.js?v=18
echo Neu vua cap nhat code, bam Ctrl+F5 trong trinh duyet de tai script moi.
echo.

where python >nul 2>nul
if %errorlevel%==0 (
    python music.py --demo --port 8000
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        py music.py --demo --port 8000
    ) else (
        echo Khong tim thay Python. Hay cai Python hoac chay lenh: python music.py --demo --port 8000
    )
)

echo.
echo Demo da dung hoac co loi. Xem thong bao ben tren neu khong mo duoc.
pause
