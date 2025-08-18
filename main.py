#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplikacja do wystawiania i ewidencjonowania uproszczonych rachunków
System Rachunków v2.0.0 (2025-01-18)
"""

import tkinter as tk
import sys
from rachunek_gui import RachunekApp
from version import print_version_info, __version__

def main():
    """Główna funkcja uruchamiająca aplikację"""
    # Sprawdź czy użytkownik chce wyświetlić informacje o wersji
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--version', '-v', '--info']:
            print_version_info()
            return
        elif sys.argv[1] in ['--help', '-h']:
            print_help()
            return
    
    # Uruchom aplikację GUI
    root = tk.Tk()
    app = RachunekApp(root)
    root.mainloop()

def print_help():
    """Wyświetla pomoc dla aplikacji"""
    print(f"""
System Rachunków v{__version__} - Aplikacja do wystawiania uproszczonych rachunków

Użycie:
    python main.py              - Uruchamia aplikację GUI
    python main.py --version    - Wyświetla informacje o wersji
    python main.py --help       - Wyświetla tę pomoc

Dostępne pliki:
    python run.py              - Uruchamia tryb diagnostyczny
    python test_pdf.py         - Testuje generator PDF
    python version.py          - Wyświetla szczegółowe info o wersji

Więcej informacji znajdziesz w pliku README.md
""")

if __name__ == "__main__":
    main()