#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prosty generator rachunków jako pliki tekstowe (fallback gdy brak reportlab)
"""

import os
from typing import Dict
from datetime import datetime

class SimplePDFGenerator:
    """Klasa generująca rachunki jako pliki tekstowe"""
    
    def generuj_rachunek_pdf(self, dane_rachunku: Dict, sciezka_pliku: str) -> str:
        """
        Generuje rachunek jako plik tekstowy (.txt zamiast .pdf)
        
        Args:
            dane_rachunku: Słownik z danymi rachunku
            sciezka_pliku: Ścieżka gdzie ma zostać zapisany plik
            
        Returns:
            Ścieżka do wygenerowanego pliku
        """
        # Zamień .pdf na .txt
        if sciezka_pliku.endswith('.pdf'):
            sciezka_pliku = sciezka_pliku[:-4] + '.txt'
        
        rachunek_tekst = self._utworz_tekst_rachunku(dane_rachunku)
        
        with open(sciezka_pliku, 'w', encoding='utf-8') as f:
            f.write(rachunek_tekst)
        
        return sciezka_pliku
    
    def _utworz_tekst_rachunku(self, dane: Dict) -> str:
        """Tworzy tekst rachunku"""
        
        tekst = f"""
════════════════════════════════════════════════════════════════
                           R A C H U N E K
                        nr {dane['numer_rachunku']}
════════════════════════════════════════════════════════════════

Data wystawienia: {dane['data_wystawienia']}
Data wykonania usługi: {dane['data_wykonania_uslugi']}

────────────────────────────────────────────────────────────────

SPRZEDAWCA:
{dane['sprzedawca']['imie']} {dane['sprzedawca']['nazwisko']}
{dane['sprzedawca']['ulica']} {dane['sprzedawca']['nr_domu']}
{dane['sprzedawca']['kod_pocztowy']} {dane['sprzedawca']['miasto']}

NABYWCA:
{dane['nabywca']['imie']} {dane['nabywca']['nazwisko']}
{dane['nabywca']['ulica']} {dane['nabywca']['nr_domu']}
{dane['nabywca']['kod_pocztowy']} {dane['nabywca']['miasto']}

────────────────────────────────────────────────────────────────

WYKONANA USŁUGA:
{dane['nazwa_uslugi']}

Cena jednostkowa: {dane['cena_jednostkowa']:.2f} PLN

════════════════════════════════════════════════════════════════

DO ZAPŁATY: {dane['kwota_do_zaplaty']:.2f} PLN

Słownie: {dane['kwota_slownie']}

════════════════════════════════════════════════════════════════

Miejsce i data: ........................., dnia {datetime.now().strftime('%d.%m.%Y')}


                                        ________________________
                                         Podpis sprzedawcy


════════════════════════════════════════════════════════════════
           Ten rachunek został wygenerowany automatycznie
            przez System Rachunków - Uproszczone Rachunki
════════════════════════════════════════════════════════════════
"""
        return tekst

def kwota_slownie(kwota: float) -> str:
    """
    Prosta konwersja kwoty na słowa (bez biblioteki num2words)
    
    Args:
        kwota: Kwota do konwersji
        
    Returns:
        Kwota zapisana słownie
    """
    
    # Prosta implementacja dla podstawowych kwot
    zlote = int(kwota)
    grosze = int(round((kwota - zlote) * 100))
    
    # Słownik cyfr
    cyfry = {
        0: 'zero', 1: 'jeden', 2: 'dwa', 3: 'trzy', 4: 'cztery',
        5: 'pięć', 6: 'sześć', 7: 'siedem', 8: 'osiem', 9: 'dziewięć',
        10: 'dziesięć', 11: 'jedenaście', 12: 'dwanaście', 13: 'trzynaście',
        14: 'czternaście', 15: 'piętnaście', 16: 'szesnaście', 17: 'siedemnaście',
        18: 'osiemnaście', 19: 'dziewiętnaście', 20: 'dwadzieścia',
        30: 'trzydzieści', 40: 'czterdzieści', 50: 'pięćdziesiąt',
        60: 'sześćdziesiąt', 70: 'siedemdziesiąt', 80: 'osiemdziesiąt', 90: 'dziewięćdziesiąt',
        100: 'sto', 200: 'dwieście', 300: 'trzysta', 400: 'czterysta',
        500: 'pięćset', 600: 'sześćset', 700: 'siedemset', 800: 'osiemset', 900: 'dziewięćset'
    }
    
    def liczba_na_slowa(n):
        if n == 0:
            return 'zero'
        if n < 21:
            return cyfry.get(n, str(n))
        elif n < 100:
            dziesiątki = (n // 10) * 10
            jednostki = n % 10
            if jednostki == 0:
                return cyfry[dziesiątki]
            else:
                return cyfry[dziesiątki] + ' ' + cyfry[jednostki]
        elif n < 1000:
            setki = (n // 100) * 100
            reszta = n % 100
            if reszta == 0:
                return cyfry[setki]
            else:
                return cyfry[setki] + ' ' + liczba_na_slowa(reszta)
        else:
            # Dla większych kwot zwróć liczbę
            return str(n)
    
    try:
        zlote_slownie = liczba_na_slowa(zlote)
        
        # Odmiana słowa "złoty"
        if zlote == 1:
            zlote_word = "złoty"
        elif zlote in [2, 3, 4] or (zlote % 10 in [2, 3, 4] and zlote % 100 not in [12, 13, 14]):
            zlote_word = "złote"
        else:
            zlote_word = "złotych"
        
        if grosze == 0:
            return f"{zlote_slownie} {zlote_word} 00/100"
        else:
            return f"{zlote_slownie} {zlote_word} {grosze:02d}/100"
            
    except:
        # Fallback
        return f"{kwota:.2f} PLN"