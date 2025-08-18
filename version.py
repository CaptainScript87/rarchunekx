#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Informacje o wersji aplikacji System Rachunków
"""

from datetime import datetime

# Wersja główna aplikacji
__version__ = "2.0.0"

# Informacje szczegółowe
VERSION_INFO = {
    'major': 2,
    'minor': 0,
    'patch': 0,
    'build': '20250118'  # Format: RRRRMMDD
}

# Nazwa aplikacji
APP_NAME = "System Rachunków"
APP_FULL_NAME = "System Rachunków - Uproszczone Rachunki"

# Informacje o wydaniu
RELEASE_DATE = "2025-01-18"
RELEASE_NOTES = [
    "Dodano system limitów miesięcznych (3499,50 PLN dla 2025)",
    "Nowoczesny interfejs graficzny z ikonami",
    "Automatyczne dopasowanie rozmiaru okna", 
    "Podsumowanie miesięczne z paskiem postępu",
    "Kolorowe statusy i ostrzeżenia",
    "Skróty klawiszowe (Ctrl+R, F11, Escape)",
    "Ulepszona walidacja danych",
    "Lepsze zarządzanie bazą danych"
]

# Historia wersji
VERSION_HISTORY = [
    {
        'version': '2.0.0',
        'date': '2025-01-18',
        'description': 'Główna aktualizacja - limity miesięczne i nowy interfejs',
        'changes': RELEASE_NOTES
    },
    {
        'version': '1.0.0',
        'date': '2024-12-01',
        'description': 'Pierwsze wydanie aplikacji',
        'changes': [
            "Podstawowa funkcjonalność tworzenia rachunków",
            "Generowanie plików PDF",
            "Baza danych SQLite",
            "Interfejs graficzny tkinter",
            "Eksport do CSV"
        ]
    }
]

def get_version():
    """Zwraca aktualną wersję jako string"""
    return __version__

def get_version_info():
    """Zwraca szczegółowe informacje o wersji"""
    return VERSION_INFO

def get_full_version_string():
    """Zwraca pełny string z wersją i datą"""
    return f"{APP_FULL_NAME} v{__version__} ({RELEASE_DATE})"

def get_build_info():
    """Zwraca informacje o buildzie"""
    build_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        'version': __version__,
        'build': VERSION_INFO['build'],
        'build_date': build_date,
        'release_date': RELEASE_DATE
    }

def print_version_info():
    """Wyświetla informacje o wersji w konsoli"""
    print(f"{'='*50}")
    print(f"{APP_FULL_NAME}")
    print(f"{'='*50}")
    print(f"Wersja: {__version__}")
    print(f"Data wydania: {RELEASE_DATE}")
    print(f"Build: {VERSION_INFO['build']}")
    print(f"{'='*50}")
    print("Nowości w tej wersji:")
    for note in RELEASE_NOTES:
        print(f"• {note}")
    print(f"{'='*50}")

if __name__ == "__main__":
    print_version_info()