# System Rachunków - Instalator PowerShell
Write-Host "===============================================" -ForegroundColor Green
Write-Host "    Instalator Systemu Rachunków" -ForegroundColor Green  
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Sprawdź Python
Write-Host "Sprawdzam instalację Pythona..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python nie jest zainstalowany lub nie jest w PATH" -ForegroundColor Red
    Write-Host "Pobierz Python z: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Naciśnij Enter aby zakończyć"
    exit 1
}

Write-Host ""
Write-Host "Próbuję zainstalować wymagane biblioteki..." -ForegroundColor Yellow

# Funkcja do instalacji pakietów
function Install-Packages {
    param($command)
    
    Write-Host "Próbuję: $command" -ForegroundColor Cyan
    try {
        Invoke-Expression "$command reportlab num2words" 2>&1 | Out-Host
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Sukces! Biblioteki zainstalowane." -ForegroundColor Green
            return $true
        } else {
            Write-Host "✗ Niepowodzenie (kod: $LASTEXITCODE)" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "✗ Błąd: $_" -ForegroundColor Red
        return $false
    }
}

# Próby instalacji
$installed = $false

if (Install-Packages "pip install") {
    $installed = $true
} elseif (Install-Packages "python -m pip install") {
    $installed = $true
} elseif (Install-Packages "py -m pip install") {
    $installed = $true
}

if (-not $installed) {
    Write-Host ""
    Write-Host "UWAGA: Nie udało się zainstalować bibliotek PDF." -ForegroundColor Yellow
    Write-Host "Aplikacja będzie działać w trybie tekstowym (.txt zamiast .pdf)." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "Testuję aplikację..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Uruchom test
try {
    Write-Host "Uruchamiam prosty test..." -ForegroundColor Yellow
    python run.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Test zakończony pomyślnie!" -ForegroundColor Green
    } else {
        Write-Host "✗ Test nie powiódł się (kod: $LASTEXITCODE)" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Błąd podczas testu: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "Instalacja zakończona!" -ForegroundColor Green
Write-Host ""
Write-Host "Aby uruchomić aplikację:" -ForegroundColor Yellow
Write-Host "  python run.py      - wersja testowa" -ForegroundColor White
Write-Host "  python main.py     - pełna aplikacja" -ForegroundColor White
Write-Host "===============================================" -ForegroundColor Green

Read-Host "Naciśnij Enter aby zakończyć"