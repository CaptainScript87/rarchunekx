#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatyczny reset licznika rachunków do 1
"""

import sqlite3
import os

def reset_auto():
    """Automatycznie resetuje licznik do 1"""
    db_path = "rachunki.db"
    
    print("=== AUTOMATYCZNY RESET LICZNIKA ===")
    
    if not os.path.exists(db_path):
        print("Baza danych nie istnieje - zostanie utworzona z licznikiem od 1")
        return
    
    # Pokaż obecny stan
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Sprawdź liczniki
        cursor.execute("SELECT miesiac, rok, ostatni_numer FROM numeracja")
        numeracja = cursor.fetchall()
        
        if numeracja:
            print("Obecne liczniki:")
            for m, r, n in numeracja:
                print(f"  {m:02d}/{r}: ostatni numer {n}")
        else:
            print("Liczniki już są puste")
            return
        
        # Sprawdź rachunki
        cursor.execute("SELECT COUNT(*) FROM rachunki")
        ile_rachunkow = cursor.fetchone()[0]
        print(f"Rachunków w bazie: {ile_rachunkow}")
    
    # Reset liczników
    print("\nResetuje liczniki...")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM numeracja")
        conn.commit()
        
    print("[OK] Liczniki zresetowane!")
    print("[OK] Nastepny rachunek bedzie mial numer 1/MM/YYYY") 
    print(f"[OK] Istniejace rachunki ({ile_rachunkow}) pozostaja w bazie")

if __name__ == "__main__":
    try:
        reset_auto()
        print("\nReset zakończony pomyślnie!")
    except Exception as e:
        print(f"Błąd podczas resetu: {e}")