@echo off
title System Rachunkow

echo ===============================================
echo           SYSTEM RACHUNKOW
echo ===============================================
echo.

echo Uruchamiam aplikacje...
echo.

REM Probuj uruchomic rozne wersje
if exist "run.py" (
    echo Uruchamiam wersje testowa...
    python run.py
    if errorlevel 1 (
        echo.
        echo Blad w wersji testowej. Probuje pelna aplikacje...
        python main.py
    )
) else if exist "main.py" (
    echo Uruchamiam pelna aplikacje...
    python main.py
) else (
    echo BLAD: Nie znaleziono plikow aplikacji!
    pause
    exit /b 1
)

echo.
echo Aplikacja zostala zamknieta.
pause