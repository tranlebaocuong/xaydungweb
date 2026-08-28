Set-Location -Path $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Dang mo demo tai lieu tu hoc..."
Write-Host "Thu muc: $(Get-Location)"
Write-Host "URL mac dinh: http://127.0.0.1:8000/index.html"
Write-Host "Server: main.py"
Write-Host "Giao dien: index.html"
Write-Host "Neu vua cap nhat code, bam Ctrl+F5 hoac mo tab moi de tai ban moi."
Write-Host ""

if (Test-Path $venvPython) {
    & $venvPython main.py --port 8000 --no-browser
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python main.py --port 8000 --no-browser
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py main.py --port 8000 --no-browser
} else {
    Write-Host "Khong tim thay Python hoac .venv."
    Write-Host "Hay cai dat Python hoac chay lenh: python main.py --port 8000 --no-browser"
    Read-Host "Nhan Enter de thoat"
    exit 1
}

Write-Host ""
Write-Host "Demo da chay. Mo dia chi tren trong trinh duyet."
Write-Host "Nhan Ctrl+C de dung server."
Read-Host "Nhan Enter de dong cua so"
