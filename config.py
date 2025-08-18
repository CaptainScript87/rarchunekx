#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plik konfiguracyjny aplikacji System Rachunków
"""

from version import __version__, APP_FULL_NAME, get_full_version_string

# Ustawienia aplikacji
APP_TITLE = APP_FULL_NAME
APP_VERSION = __version__
APP_GEOMETRY = "1100x800"
APP_FULL_TITLE = get_full_version_string()

# Ustawienia bazy danych
DATABASE_PATH = "rachunki.db"

# Ustawienia PDF
DEFAULT_PDF_FOLDER = ""  # Pozostaw puste dla folderu aplikacji
PDF_EXTENSION = ".pdf"  # Zmień na ".txt" jeśli chcesz zawsze tekstowe

# Ustawienia formatowania dat
DATE_FORMAT_DISPLAY = "%d.%m.%Y"  # Format wyświetlania dat
DATE_FORMAT_DB = "%Y-%m-%d"       # Format w bazie danych

# Domyślne dane sprzedawcy (wypełnij jeśli chcesz)
DEFAULT_SPRZEDAWCA = {
    "imie": "",
    "nazwisko": "", 
    "ulica": "",
    "nr_domu": "",
    "kod_pocztowy": "",
    "miasto": ""
}

# Ustawienia walidacji
VALIDATE_POSTAL_CODE = True  # Czy sprawdzać format kodu pocztowego XX-XXX
MIN_SERVICE_NAME_LENGTH = 3  # Minimalna długość nazwy usługi
MAX_SERVICE_NAME_LENGTH = 500  # Maksymalna długość nazwy usługi
MAX_AMOUNT = 999999.99  # Maksymalna kwota rachunku

# Limity miesięczne zgodne z prawem polskim
MONTHLY_REVENUE_LIMIT_2025 = 3499.50  # Limit przychodów miesięcznych w 2025 roku
VALIDATE_MONTHLY_LIMIT = True  # Czy sprawdzać limit miesięczny

# Ustawienia eksportu CSV
CSV_DELIMITER = ","
CSV_ENCODING = "utf-8"

# Komunikaty
MESSAGES = {
    "no_reportlab": "UWAGA: Biblioteka reportlab nie jest dostępna. Rachunki będą generowane jako pliki tekstowe (.txt)",
    "success_invoice": "Rachunek został wygenerowany!",
    "success_seller_saved": "Dane sprzedawcy zostały zapisane",
    "error_no_seller": "Brak danych sprzedawcy. Uzupełnij dane w zakładce Ustawienia.",
    "error_validation": "Błąd walidacji",
    "error_monthly_limit": "UWAGA: Przekroczony limit miesięczny przychodów!",
    "warning_monthly_limit": "Ostrzeżenie: Zbliżasz się do limitu miesięcznego przychodów.",
    "info_monthly_remaining": "Pozostały limit w tym miesiącu: {amount:.2f} PLN"
}

# Ustawienia debugowania
DEBUG_MODE = False
VERBOSE_LOGGING = False