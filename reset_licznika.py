#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt do resetowania licznika rachunków
"""

import sqlite3
import os
from database import DatabaseManager

def reset_licznika():
    """Resetuje licznik rachunków do 0"""
    db_path = "rachunki.db"
    
    print("=== RESET LICZNIKA RACHUNKÓW ===")
    
    # Sprawdź czy baza istnieje
    if not os.path.exists(db_path):
        print("Baza danych nie istnieje. Tworzę nową...")
        db = DatabaseManager(db_path)
        print("✓ Nowa baza utworzona z licznikiem od 1")
        return
    
    # Pokaż obecny stan
    db = DatabaseManager(db_path)
    
    print("\nObecny stan bazy danych:")
    rachunki = db.pobierz_wszystkie_rachunki()
    print(f"Liczba rachunków: {len(rachunki)}")
    
    if rachunki:
        print("Ostatnie rachunki:")
        for r in rachunki[:5]:
            print(f"  - {r['numer_rachunku']} | {r['nabywca']} | {r['kwota']:.2f} PLN")
    
    # Sprawdź numerację
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT miesiac, rok, ostatni_numer FROM numeracja ORDER BY rok DESC, miesiac DESC")
        numeracja = cursor.fetchall()
        
        if numeracja:
            print(f"\nObecna numeracja:")
            for m, r, n in numeracja:
                print(f"  {m:02d}/{r}: ostatni numer {n}")
    
    # Zapytaj o reset
    print("\nOPCJE:")
    print("1. Wyczyść całą bazę danych (usuń wszystkie rachunki)")
    print("2. Resetuj tylko liczniki (zachowaj rachunki)")
    print("3. Anuluj")
    
    wybor = input("\nWybierz opcję (1/2/3): ").strip()
    
    if wybor == "1":
        # Usuń wszystko
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM rachunki")
            cursor.execute("DELETE FROM numeracja") 
            cursor.execute("DELETE FROM sprzedawca")
            conn.commit()
            
        print("✓ Cała baza danych została wyczyszczona")
        print("✓ Następny rachunek będzie miał numer 1/MM/YYYY")
        
    elif wybor == "2":
        # Resetuj tylko liczniki
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM numeracja")
            conn.commit()
            
        print("✓ Liczniki zostały zresetowane")
        print("✓ Następny rachunek będzie miał numer 1/MM/YYYY")
        print("✓ Istniejące rachunki pozostają nietknięte")
        
    elif wybor == "3":
        print("Anulowano reset")
        
    else:
        print("Nieprawidłowy wybór")

def sprawdz_stan():
    """Sprawdza obecny stan licznika"""
    db_path = "rachunki.db"
    
    if not os.path.exists(db_path):
        print("Baza danych nie istnieje")
        return
        
    print("=== STAN LICZNIKA ===")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Pokaż numerację
        cursor.execute("SELECT miesiac, rok, ostatni_numer FROM numeracja ORDER BY rok DESC, miesiac DESC")
        numeracja = cursor.fetchall()
        
        if numeracja:
            print("Obecne liczniki:")
            for m, r, n in numeracja:
                print(f"  {m:02d}/{r}: ostatni numer {n}")
        else:
            print("Brak liczników - następny rachunek będzie 1/MM/YYYY")
        
        # Pokaż ostatnie rachunki
        cursor.execute("SELECT numer_rachunku FROM rachunki ORDER BY data_utworzenia DESC LIMIT 3")
        ostatnie = cursor.fetchall()
        
        if ostatnie:
            print("\nOstatnie rachunki:")
            for (numer,) in ostatnie:
                print(f"  - {numer}")

if __name__ == "__main__":
    try:
        # Najpierw pokaż stan
        sprawdz_stan()
        print()
        
        # Zapytaj czy zresetować
        if input("Czy chcesz zresetować licznik? (t/n): ").lower() == 't':
            reset_licznika()
        else:
            print("Anulowano")
            
    except Exception as e:
        print(f"Błąd: {e}")
    
    input("\nNaciśnij Enter aby zakończyć...")