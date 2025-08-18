#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moduł odpowiedzialny za walidację danych wejściowych
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
import config

class WalidatorDanych:
    """Klasa odpowiedzialna za walidację danych rachunku"""
    
    @staticmethod
    def waliduj_dane_osoby(dane: Dict, nazwa_osoby: str = "osoba") -> List[str]:
        """
        Waliduje dane osoby (sprzedawca/nabywca)
        
        Args:
            dane: Słownik z danymi osoby
            nazwa_osoby: Nazwa osoby do komunikatów błędów
            
        Returns:
            Lista błędów walidacji
        """
        bledy = []
        
        # Sprawdzenie wymaganych pól
        wymagane_pola = ['imie', 'nazwisko', 'ulica', 'nr_domu', 'kod_pocztowy', 'miasto']
        
        for pole in wymagane_pola:
            if not dane.get(pole, '').strip():
                bledy.append(f"Pole '{pole}' jest wymagane dla {nazwa_osoby}")
        
        # Walidacja imienia i nazwiska
        if dane.get('imie', '').strip():
            if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s-]+$', dane['imie'].strip()):
                bledy.append(f"Imię {nazwa_osoby} zawiera nieprawidłowe znaki")
        
        if dane.get('nazwisko', '').strip():
            if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s-]+$', dane['nazwisko'].strip()):
                bledy.append(f"Nazwisko {nazwa_osoby} zawiera nieprawidłowe znaki")
        
        # Walidacja kodu pocztowego (format XX-XXX)
        if dane.get('kod_pocztowy', '').strip():
            kod = dane['kod_pocztowy'].strip()
            if not re.match(r'^\d{2}-\d{3}$', kod):
                bledy.append(f"Kod pocztowy {nazwa_osoby} musi być w formacie XX-XXX (np. 00-001)")
        
        # Walidacja miasta
        if dane.get('miasto', '').strip():
            if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s-]+$', dane['miasto'].strip()):
                bledy.append(f"Nazwa miasta {nazwa_osoby} zawiera nieprawidłowe znaki")
        
        # Walidacja ulicy i numeru domu
        if dane.get('ulica', '').strip():
            if len(dane['ulica'].strip()) < 2:
                bledy.append(f"Nazwa ulicy {nazwa_osoby} jest zbyt krótka")
        
        if dane.get('nr_domu', '').strip():
            nr = dane['nr_domu'].strip()
            if not re.match(r'^[0-9a-zA-Z/\s-]+$', nr):
                bledy.append(f"Numer domu {nazwa_osoby} zawiera nieprawidłowe znaki")
        
        return bledy
    
    @staticmethod
    def waliduj_date(data_str: str, nazwa_daty: str = "data") -> List[str]:
        """
        Waliduje format daty
        
        Args:
            data_str: Data w formacie string
            nazwa_daty: Nazwa daty do komunikatów błędów
            
        Returns:
            Lista błędów walidacji
        """
        bledy = []
        
        if not data_str.strip():
            bledy.append(f"Pole '{nazwa_daty}' jest wymagane")
            return bledy
        
        # Sprawdzenie formatu daty (YYYY-MM-DD lub DD.MM.YYYY lub DD/MM/YYYY)
        formaty = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}\.\d{2}\.\d{4}$',  # DD.MM.YYYY
            r'^\d{2}/\d{2}/\d{4}$'   # DD/MM/YYYY
        ]
        
        poprawny_format = False
        for format_regex in formaty:
            if re.match(format_regex, data_str.strip()):
                poprawny_format = True
                break
        
        if not poprawny_format:
            bledy.append(f"{nazwa_daty} musi być w formacie YYYY-MM-DD, DD.MM.YYYY lub DD/MM/YYYY")
            return bledy
        
        # Próba parsowania daty
        try:
            if '-' in data_str:
                datetime.strptime(data_str.strip(), '%Y-%m-%d')
            elif '.' in data_str:
                datetime.strptime(data_str.strip(), '%d.%m.%Y')
            elif '/' in data_str:
                datetime.strptime(data_str.strip(), '%d/%m/%Y')
        except ValueError:
            bledy.append(f"{nazwa_daty} jest nieprawidłowa")
        
        return bledy
    
    @staticmethod
    def waliduj_kwote(kwota_str: str) -> List[str]:
        """
        Waliduje kwotę pieniężną
        
        Args:
            kwota_str: Kwota w formacie string
            
        Returns:
            Lista błędów walidacji
        """
        bledy = []
        
        if not kwota_str.strip():
            bledy.append("Kwota jest wymagana")
            return bledy
        
        # Usunięcie spacji i zamianie przecinka na kropkę
        kwota_clean = kwota_str.strip().replace(',', '.').replace(' ', '')
        
        # Sprawdzenie czy to liczba
        try:
            kwota = float(kwota_clean)
            
            if kwota <= 0:
                bledy.append("Kwota musi być większa od zera")
            
            if kwota > 999999.99:
                bledy.append("Kwota jest zbyt duża (maksymalnie 999 999,99 PLN)")
            
            # Sprawdzenie czy ma maksymalnie 2 miejsca po przecinku
            if '.' in kwota_clean:
                czesc_dziesietna = kwota_clean.split('.')[1]
                if len(czesc_dziesietna) > 2:
                    bledy.append("Kwota może mieć maksymalnie 2 miejsca po przecinku")
                    
        except ValueError:
            bledy.append("Kwota musi być liczbą (np. 100.50)")
        
        return bledy
    
    @staticmethod
    def waliduj_nazwa_uslugi(nazwa: str) -> List[str]:
        """
        Waliduje nazwę usługi
        
        Args:
            nazwa: Nazwa usługi
            
        Returns:
            Lista błędów walidacji
        """
        bledy = []
        
        if not nazwa.strip():
            bledy.append("Nazwa usługi jest wymagana")
            return bledy
        
        if len(nazwa.strip()) < 3:
            bledy.append("Nazwa usługi musi mieć co najmniej 3 znaki")
        
        if len(nazwa.strip()) > 500:
            bledy.append("Nazwa usługi jest zbyt długa (maksymalnie 500 znaków)")
        
        return bledy
    
    @staticmethod
    def waliduj_caly_rachunek(dane_rachunku: Dict) -> List[str]:
        """
        Waliduje wszystkie dane rachunku
        
        Args:
            dane_rachunku: Słownik z danymi rachunku
            
        Returns:
            Lista wszystkich błędów walidacji
        """
        wszystkie_bledy = []
        
        # Walidacja danych sprzedawcy
        if 'sprzedawca' in dane_rachunku:
            bledy_sprzedawca = WalidatorDanych.waliduj_dane_osoby(
                dane_rachunku['sprzedawca'], 
                "sprzedawcy"
            )
            wszystkie_bledy.extend(bledy_sprzedawca)
        else:
            wszystkie_bledy.append("Dane sprzedawcy są wymagane")
        
        # Walidacja danych nabywcy
        if 'nabywca' in dane_rachunku:
            bledy_nabywca = WalidatorDanych.waliduj_dane_osoby(
                dane_rachunku['nabywca'], 
                "nabywcy"
            )
            wszystkie_bledy.extend(bledy_nabywca)
        else:
            wszystkie_bledy.append("Dane nabywcy są wymagane")
        
        # Walidacja dat
        if 'data_wykonania_uslugi' in dane_rachunku:
            bledy_data = WalidatorDanych.waliduj_date(
                dane_rachunku['data_wykonania_uslugi'], 
                "Data wykonania usługi"
            )
            wszystkie_bledy.extend(bledy_data)
        else:
            wszystkie_bledy.append("Data wykonania usługi jest wymagana")
        
        # Walidacja nazwy usługi
        if 'nazwa_uslugi' in dane_rachunku:
            bledy_usluga = WalidatorDanych.waliduj_nazwa_uslugi(
                dane_rachunku['nazwa_uslugi']
            )
            wszystkie_bledy.extend(bledy_usluga)
        else:
            wszystkie_bledy.append("Nazwa usługi jest wymagana")
        
        # Walidacja kwoty
        if 'cena_jednostkowa' in dane_rachunku:
            if isinstance(dane_rachunku['cena_jednostkowa'], str):
                bledy_kwota = WalidatorDanych.waliduj_kwote(
                    dane_rachunku['cena_jednostkowa']
                )
                wszystkie_bledy.extend(bledy_kwota)
        else:
            wszystkie_bledy.append("Cena jednostkowa jest wymagana")
        
        return wszystkie_bledy
    
    @staticmethod
    def normalizuj_date(data_str: str) -> str:
        """
        Normalizuje datę do formatu YYYY-MM-DD
        
        Args:
            data_str: Data w różnych formatach
            
        Returns:
            Data w formacie YYYY-MM-DD
        """
        data_str = data_str.strip()
        
        try:
            if '-' in data_str and len(data_str.split('-')[0]) == 4:
                # Format YYYY-MM-DD - już poprawny
                return data_str
            elif '.' in data_str:
                # Format DD.MM.YYYY
                dt = datetime.strptime(data_str, '%d.%m.%Y')
                return dt.strftime('%Y-%m-%d')
            elif '/' in data_str:
                # Format DD/MM/YYYY
                dt = datetime.strptime(data_str, '%d/%m/%Y')
                return dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
        
        return data_str
    
    @staticmethod
    def normalizuj_kwote(kwota_str: str) -> float:
        """
        Normalizuje kwotę do formatu float
        
        Args:
            kwota_str: Kwota w formacie string
            
        Returns:
            Kwota jako liczba float
        """
        kwota_clean = kwota_str.strip().replace(',', '.').replace(' ', '')
        return float(kwota_clean)
    
    @staticmethod
    def waliduj_limit_miesięczny(nowa_kwota: float, obecne_przychody: float, 
                                 data_rachunku: str = None) -> List[str]:
        """
        Waliduje czy dodanie nowej kwoty nie przekroczy limitu miesięcznego
        
        Args:
            nowa_kwota: Kwota nowego rachunku
            obecne_przychody: Obecne przychody w miesiącu
            data_rachunku: Data rachunku (do określenia roku)
            
        Returns:
            Lista błędów walidacji
        """
        bledy = []
        
        if not config.VALIDATE_MONTHLY_LIMIT:
            return bledy
        
        # Określ limit na podstawie roku
        rok_rachunku = datetime.now().year
        if data_rachunku:
            try:
                if '-' in data_rachunku:
                    rok_rachunku = datetime.strptime(data_rachunku, '%Y-%m-%d').year
                elif '.' in data_rachunku:
                    rok_rachunku = datetime.strptime(data_rachunku, '%d.%m.%Y').year
                elif '/' in data_rachunku:
                    rok_rachunku = datetime.strptime(data_rachunku, '%d/%m/%Y').year
            except ValueError:
                pass
        
        # Na razie tylko limit na 2025, można rozszerzyć dla innych lat
        limit_miesięczny = config.MONTHLY_REVENUE_LIMIT_2025 if rok_rachunku == 2025 else 3499.50
        
        suma_po_dodaniu = obecne_przychody + nowa_kwota
        
        if suma_po_dodaniu > limit_miesięczny:
            przekroczenie = suma_po_dodaniu - limit_miesięczny
            bledy.append(
                f"Przekroczony limit miesięczny przychodów! "
                f"Obecne przychody: {obecne_przychody:.2f} PLN, "
                f"Nowy rachunek: {nowa_kwota:.2f} PLN, "
                f"Suma: {suma_po_dodaniu:.2f} PLN. "
                f"Limit miesięczny: {limit_miesięczny:.2f} PLN. "
                f"Przekroczenie o: {przekroczenie:.2f} PLN."
            )
        elif suma_po_dodaniu > limit_miesięczny * 0.8:  # Ostrzeżenie przy 80% limitu
            pozostalo = limit_miesięczny - suma_po_dodaniu
            bledy.append(
                f"OSTRZEŻENIE: Zbliżasz się do limitu miesięcznego! "
                f"Po tym rachunku pozostanie: {pozostalo:.2f} PLN z limitu {limit_miesięczny:.2f} PLN."
            )
        
        return bledy