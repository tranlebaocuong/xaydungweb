Set-Location -Path $PSScriptRoot

Write-Host "Dang mo demo tai lieu tu hoc..."
Write-Host "Thu muc: $(Get-Location)"
Write-Host "URL mac dinh: http://127.0.0.1:8000/index.html"
Write-Host "Style hien tai: styles.css?v=14"
Write-Host "Script hien tai: script.js?v=18"
Write-Host "Neu vua cap nhat code, bam Ctrl+F5 trong trinh duyet de tai script moi."
Write-Host ""

$python = Get-Command python -ErrorAction SilentlyContinue
$py = Get-Command py -ErrorAction SilentlyContinue

if ($python) {
    python music.py --demo --port 8000
} elseif ($py) {
    py music.py --demo --port 8000
} else {
    Write-Host "Khong tim thay Python. Hay cai Python hoac chay lenh: python music.py --demo --port 8000"
}

Write-Host ""
Write-Host "Demo da dung hoac co loi. Xem thong bao ben tren neu khong mo duoc."
Read-Host "Nhan Enter de dong cua so"
