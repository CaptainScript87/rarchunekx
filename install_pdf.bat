@echo off
echo ===============================================
echo    INSTALATOR PDF dla Systemu Rachunkow
echo ===============================================
echo.

echo Sprawdzam Python...
python --version
if errorlevel 1 (
    echo BLAD: Python nie jest zainstalowany!
    echo Pobierz z: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo === INSTALUJE BIBLIOTEKI PDF ===
echo.

echo 1. Aktualizuje pip...
python -m pip install --upgrade pip
echo.

echo 2. Instaluje reportlab...
python -m pip install reportlab
if errorlevel 1 (
    echo Probuje alternatywna metode...
    pip install reportlab
    if errorlevel 1 (
        echo Probuje z --user...
        python -m pip install --user reportlab
    )
)

echo.
echo 3. Instaluje num2words...
python -m pip install num2words
if errorlevel 1 (
    echo Probuje alternatywna metode...
    pip install num2words
    if errorlevel 1 (
        echo Probuje z --user...
        python -m pip install --user num2words
    )
)

echo.
echo === TESTUJE INSTALACJE ===
echo.

python -c "import reportlab; print('reportlab:', reportlab.__version__)"
if errorlevel 1 (
    echo BLAD: reportlab nie zostal zainstalowany!
    goto :error
)

python -c "import num2words; print('num2words: OK')"
if errorlevel 1 (
    echo BLAD: num2words nie zostal zainstalowany!
    goto :error
)

echo.
echo ===============================================
echo    SUKCES! Biblioteki PDF zainstalowane!
echo ===============================================
echo.

echo Uruchamiam aplikacje z PDF...
python main.py

goto :end

:error
echo.
echo ===============================================
echo    BLAD INSTALACJI
echo ===============================================
echo.
echo Proby rozwiazania:
echo.
echo 1. Uruchom jako Administrator:
echo    - Klik prawym na install_pdf.bat
echo    - Wybierz "Uruchom jako administrator"
echo.
echo 2. Lub sprobuj recznej instalacji:
echo    python -m pip install --upgrade pip
echo    python -m pip install reportlab num2words
echo.
echo 3. Sprawdz internet i firewall
echo.
echo 4. Jesli dalej nie dziala, mozesz uzyc wersji tekstowej:
echo    python main.py
echo    (rachunki beda jako .txt zamiast .pdf)
echo.

:end
pause