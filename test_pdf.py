#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test generatora PDF
"""

from datetime import datetime
from pdf_generator import PDFGenerator, kwota_slownie

def test_pdf():
    """Test generowania PDF"""
    print("=== TEST GENERATORA PDF ===")
    
    # Przykładowe dane rachunku
    dane_rachunku = {
        'numer_rachunku': '1/08/2025',
        'data_wystawienia': '2025-08-18',
        'data_wykonania_uslugi': '2025-08-18',
        'sprzedawca': {
            'imie': 'Jan',
            'nazwisko': 'Kowalski', 
            'ulica': 'Testowa',
            'nr_domu': '123',
            'kod_pocztowy': '00-001',
            'miasto': 'Warszawa'
        },
        'nabywca': {
            'imie': 'Anna',
            'nazwisko': 'Nowak',
            'ulica': 'Przykładowa', 
            'nr_domu': '456',
            'kod_pocztowy': '01-234',
            'miasto': 'Kraków'
        },
        'nazwa_uslugi': 'Test - programowanie aplikacji rachunków',
        'cena_jednostkowa': 100.50,
        'kwota_do_zaplaty': 100.50,
        'kwota_slownie': kwota_slownie(100.50)
    }
    
    try:
        # Test kwoty słownie
        print("1. Test kwoty słownie...")
        kwota_test = kwota_slownie(123.45)
        print(f"   123.45 PLN = {kwota_test}")
        
        # Test generatora PDF
        print("2. Test generatora PDF...")
        generator = PDFGenerator()
        
        # Generuj PDF
        sciezka_pdf = "test_rachunek.pdf"
        wynik = generator.generuj_rachunek_pdf(dane_rachunku, sciezka_pdf)
        
        print(f"3. PDF wygenerowany: {wynik}")
        
        # Sprawdź czy plik istnieje
        import os
        if os.path.exists(sciezka_pdf):
            size = os.path.getsize(sciezka_pdf)
            print(f"4. Plik PDF istnieje, rozmiar: {size} bajtów")
            
            if size > 1000:  # PDF powinien mieć co najmniej 1KB
                print("[OK] SUKCES! PDF zostal wygenerowany poprawnie!")
                print(f"[OK] Plik: {os.path.abspath(sciezka_pdf)}")
                return True
            else:
                print("[BLAD] Plik PDF jest za maly")
        else:
            print("[BLAD] Plik PDF nie zostal utworzony")
            
    except Exception as e:
        print(f"[BLAD] podczas testu: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False

if __name__ == "__main__":
    if test_pdf():
        print("\n🎉 Test zakończony sukcesem!")
        print("Generator PDF działa poprawnie.")
        print("Możesz uruchomić aplikację: python main.py")
    else:
        print("\n❌ Test nie powiódł się.")
        print("Sprawdź błędy powyżej lub użyj wersji tekstowej.")
    
    input("\nNaciśnij Enter aby zakończyć...")