Set-Location -Path $PSScriptRoot

Write-Host "Dang mo demo tai lieu tu hoc..."
Write-Host "Thu muc: $(Get-Location)"
Write-Host "URL mac dinh: http://127.0.0.1:8000/index.html"
Write-Host "Server: main.py"
Write-Host "Giao dien: index.html"
Write-Host "Neu xem tren dien thoai, hay mo dung dia chi do cua so demo hien ra."
Write-Host "Neu vua cap nhat code, bam Ctrl+F5 hoac dong tab mo lai de tai ban moi."
Write-Host ""

$python = Get-Command python -ErrorAction SilentlyContinue
$py = Get-Command py -ErrorAction SilentlyContinue

if ($python) {
    python main.py --port 8000 --no-browser
} elseif ($py) {
    py main.py --port 8000 --no-browser
} else {
    Write-Host "Khong tim thay Python."
    Write-Host "Hay cai Python hoac chay lenh: python main.py --port 8000 --no-browser"
}

Write-Host ""
Write-Host "Demo da chay. Mo vao dia chi tren trong trinh duyet."
Write-Host "Nhan Ctrl+C de dung server."
Read-Host "Nhan Enter de dong cua so"
