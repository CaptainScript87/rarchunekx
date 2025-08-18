@echo off
echo ===============================================
echo    Instalator Systemu Rachunkow
echo ===============================================
echo.

echo Sprawdzam instalacje Pythona...
python --version
if errorlevel 1 (
    echo BLAD: Python nie jest zainstalowany lub nie jest w PATH
    echo Pobierz Python z: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Probuje zainstalowac wymagane biblioteki...

echo.
echo 1. Probuje pip install...
pip install reportlab num2words
if not errorlevel 1 (
    echo Sukces! Biblioteki zostaly zainstalowane przez pip.
    goto :run_app
)

echo.
echo 2. Probuje python -m pip install...
python -m pip install reportlab num2words
if not errorlevel 1 (
    echo Sukces! Biblioteki zostaly zainstalowane przez python -m pip.
    goto :run_app
)

echo.
echo 3. Probuje py -m pip install...
py -m pip install reportlab num2words
if not errorlevel 1 (
    echo Sukces! Biblioteki zostaly zainstalowane przez py -m pip.
    goto :run_app
)

echo.
echo UWAGA: Nie udalo sie zainstalowac bibliotek PDF.
echo Aplikacja bedzie dzialac w trybie tekstowym (pliki .txt zamiast .pdf).
echo.

:run_app
echo.
echo ===============================================
echo Uruchamiam aplikacje...
echo ===============================================
echo.

python main.py
if errorlevel 1 (
    echo.
    echo BLAD: Nie udalo sie uruchomic aplikacji.
    echo Sprawdz logi powyzej.
    pause
    exit /b 1
)

echo.
echo Aplikacja zostala zamknieta.
pause