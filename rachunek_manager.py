#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Główna logika biznesowa aplikacji do rachunków
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from database import DatabaseManager
from walidacja import WalidatorDanych

# Spróbuj zaimportować reportlab, jeśli nie ma to użyj prostej wersji
try:
    from pdf_generator import PDFGenerator, kwota_slownie
    PDF_AVAILABLE = True
except ImportError:
    from simple_pdf_generator import SimplePDFGenerator as PDFGenerator, kwota_slownie
    PDF_AVAILABLE = False
    print("UWAGA: Biblioteka reportlab nie jest dostępna. Rachunki będą generowane jako pliki tekstowe (.txt)")

class RachunekManager:
    """Klasa zarządzająca logiką biznesową rachunków"""
    
    def __init__(self, db_path: str = "rachunki.db"):
        """
        Inicjalizacja managera rachunków
        
        Args:
            db_path: Ścieżka do bazy danych
        """
        self.db = DatabaseManager(db_path)
        self.pdf_generator = PDFGenerator()
        self.walidator = WalidatorDanych()
    
    def pobierz_domyslnego_sprzedawce(self) -> Optional[Dict]:
        """Pobiera dane domyślnego sprzedawcy"""
        return self.db.get_domyslny_sprzedawca()
    
    def zapisz_domyslnego_sprzedawce(self, dane_sprzedawcy: Dict) -> List[str]:
        """
        Zapisuje dane domyślnego sprzedawcy
        
        Args:
            dane_sprzedawcy: Słownik z danymi sprzedawcy
            
        Returns:
            Lista błędów walidacji (pusta jeśli sukces)
        """
        # Walidacja danych
        bledy = self.walidator.waliduj_dane_osoby(dane_sprzedawcy, "sprzedawcy")
        
        if not bledy:
            self.db.zapisz_domyslnego_sprzedawce(dane_sprzedawcy)
        
        return bledy
    
    def stworz_rachunek(self, dane_rachunku: Dict, folder_docelowy: str = None) -> Dict:
        """
        Tworzy nowy rachunek
        
        Args:
            dane_rachunku: Słownik z danymi rachunku
            folder_docelowy: Folder gdzie zapisać PDF (opcjonalnie)
            
        Returns:
            Słownik z wynikiem operacji: {'success': bool, 'errors': List[str], 'rachunek_id': int, 'pdf_path': str}
        """
        wynik = {
            'success': False,
            'errors': [],
            'rachunek_id': None,
            'pdf_path': None
        }
        
        # Walidacja danych
        bledy = self.walidator.waliduj_caly_rachunek(dane_rachunku)
        
        if bledy:
            wynik['errors'] = bledy
            return wynik
        
        try:
            # Normalizacja danych
            dane_znormalizowane = self._normalizuj_dane_rachunku(dane_rachunku)
            
            # Walidacja limitu miesięcznego
            kwota_nowego_rachunku = dane_znormalizowane['cena_jednostkowa']
            data_rachunku = dane_znormalizowane.get('data_wykonania_uslugi')
            
            # Pobierz obecne przychody w miesiącu rachunku
            if data_rachunku:
                try:
                    dt = datetime.strptime(data_rachunku, '%Y-%m-%d')
                    obecne_przychody = self.db.pobierz_przychody_miesiac(dt.month, dt.year)
                except ValueError:
                    obecne_przychody = self.db.pobierz_przychody_biezacy_miesiac()
            else:
                obecne_przychody = self.db.pobierz_przychody_biezacy_miesiac()
            
            bledy_limit = self.walidator.waliduj_limit_miesięczny(
                kwota_nowego_rachunku, 
                obecne_przychody, 
                data_rachunku
            )
            
            if bledy_limit:
                # Rozróżnij błędy od ostrzeżeń
                bledy_krytyczne = [b for b in bledy_limit if b.startswith("Przekroczony")]
                ostrzezenia = [b for b in bledy_limit if b.startswith("OSTRZEŻENIE")]
                
                if bledy_krytyczne:
                    wynik['errors'] = bledy_krytyczne
                    return wynik
                elif ostrzezenia:
                    # Ostrzeżenia nie blokują, ale informują użytkownika
                    wynik['warnings'] = ostrzezenia
            
            # Generowanie numeru rachunku
            numer_rachunku = self.db.generuj_numer_rachunku()
            dane_znormalizowane['numer_rachunku'] = numer_rachunku
            
            # Ustawienie daty wystawienia
            dane_znormalizowane['data_wystawienia'] = datetime.now().strftime('%Y-%m-%d')
            
            # Wyliczenie kwoty słownie
            kwota = dane_znormalizowane['cena_jednostkowa']
            dane_znormalizowane['kwota_do_zaplaty'] = kwota
            dane_znormalizowane['kwota_slownie'] = kwota_slownie(kwota)
            
            # Tworzenie nazwy pliku PDF
            if folder_docelowy is None:
                folder_docelowy = os.getcwd()
            
            safe_numer = numer_rachunku.replace('/', '_')
            nazwa_pliku = f"rachunek_{safe_numer}.pdf"
            sciezka_pdf = os.path.join(folder_docelowy, nazwa_pliku)
            
            # Generowanie PDF
            self.pdf_generator.generuj_rachunek_pdf(dane_znormalizowane, sciezka_pdf)
            dane_znormalizowane['plik_pdf'] = sciezka_pdf
            
            # Zapisanie do bazy danych
            rachunek_id = self.db.zapisz_rachunek(dane_znormalizowane)
            
            wynik['success'] = True
            wynik['rachunek_id'] = rachunek_id
            wynik['pdf_path'] = sciezka_pdf
            
        except Exception as e:
            wynik['errors'].append(f"Błąd podczas tworzenia rachunku: {str(e)}")
        
        return wynik
    
    def pobierz_liste_rachunkow(self) -> List[Dict]:
        """Pobiera listę wszystkich rachunków"""
        return self.db.pobierz_wszystkie_rachunki()
    
    def wyszukaj_rachunki(self, query: str) -> List[Dict]:
        """
        Wyszukuje rachunki
        
        Args:
            query: Fraza do wyszukania
            
        Returns:
            Lista znalezionych rachunków
        """
        if not query.strip():
            return self.pobierz_liste_rachunkow()
        
        return self.db.szukaj_rachunki(query.strip())
    
    def pobierz_szczegoly_rachunku(self, rachunek_id: int) -> Optional[Dict]:
        """
        Pobiera szczegółowe dane rachunku
        
        Args:
            rachunek_id: ID rachunku
            
        Returns:
            Słownik z danymi rachunku lub None
        """
        return self.db.pobierz_rachunek_szczegoly(rachunek_id)
    
    def eksportuj_rachunki_csv(self, sciezka_pliku: str) -> Dict:
        """
        Eksportuje rachunki do pliku CSV
        
        Args:
            sciezka_pliku: Ścieżka do pliku CSV
            
        Returns:
            Słownik z wynikiem operacji
        """
        wynik = {'success': False, 'error': None}
        
        try:
            self.db.eksportuj_do_csv(sciezka_pliku)
            wynik['success'] = True
        except Exception as e:
            wynik['error'] = f"Błąd podczas eksportu: {str(e)}"
        
        return wynik
    
    def otworz_plik_pdf(self, sciezka_pliku: str) -> bool:
        """
        Otwiera plik PDF w domyślnej aplikacji
        
        Args:
            sciezka_pliku: Ścieżka do pliku PDF
            
        Returns:
            True jeśli udało się otworzyć, False w przeciwnym razie
        """
        try:
            if os.path.exists(sciezka_pliku):
                os.startfile(sciezka_pliku)  # Windows
                return True
            else:
                return False
        except Exception:
            try:
                # Próba dla innych systemów operacyjnych
                import subprocess
                subprocess.run(['xdg-open', sciezka_pliku], check=True)  # Linux
                return True
            except Exception:
                try:
                    subprocess.run(['open', sciezka_pliku], check=True)  # macOS
                    return True
                except Exception:
                    return False
    
    def _normalizuj_dane_rachunku(self, dane: Dict) -> Dict:
        """
        Normalizuje dane rachunku do odpowiednich formatów
        
        Args:
            dane: Surowe dane rachunku
            
        Returns:
            Znormalizowane dane rachunku
        """
        dane_znormalizowane = dane.copy()
        
        # Normalizacja daty wykonania usługi
        if 'data_wykonania_uslugi' in dane:
            dane_znormalizowane['data_wykonania_uslugi'] = self.walidator.normalizuj_date(
                dane['data_wykonania_uslugi']
            )
        
        # Normalizacja kwoty
        if 'cena_jednostkowa' in dane and isinstance(dane['cena_jednostkowa'], str):
            dane_znormalizowane['cena_jednostkowa'] = self.walidator.normalizuj_kwote(
                dane['cena_jednostkowa']
            )
        
        # Czyszczenie białych znaków w tekstach
        for osoba in ['sprzedawca', 'nabywca']:
            if osoba in dane_znormalizowane:
                for pole in dane_znormalizowane[osoba]:
                    if isinstance(dane_znormalizowane[osoba][pole], str):
                        dane_znormalizowane[osoba][pole] = dane_znormalizowane[osoba][pole].strip()
        
        if 'nazwa_uslugi' in dane_znormalizowane:
            dane_znormalizowane['nazwa_uslugi'] = dane_znormalizowane['nazwa_uslugi'].strip()
        
        return dane_znormalizowane
    
    def sprawdz_czy_plik_pdf_istnieje(self, rachunek_id: int) -> Optional[str]:
        """
        Sprawdza czy plik PDF dla rachunku istnieje
        
        Args:
            rachunek_id: ID rachunku
            
        Returns:
            Ścieżka do pliku PDF jeśli istnieje, None w przeciwnym razie
        """
        szczegoly = self.pobierz_szczegoly_rachunku(rachunek_id)
        
        if szczegoly and szczegoly.get('plik_pdf'):
            sciezka = szczegoly['plik_pdf']
            if os.path.exists(sciezka):
                return sciezka
        
        return None
    
    def regeneruj_pdf_rachunku(self, rachunek_id: int, folder_docelowy: str = None) -> Dict:
        """
        Regeneruje plik PDF dla istniejącego rachunku
        
        Args:
            rachunek_id: ID rachunku
            folder_docelowy: Folder gdzie zapisać nowy PDF
            
        Returns:
            Słownik z wynikiem operacji
        """
        wynik = {'success': False, 'error': None, 'pdf_path': None}
        
        try:
            # Pobierz dane rachunku
            szczegoly = self.pobierz_szczegoly_rachunku(rachunek_id)
            
            if not szczegoly:
                wynik['error'] = "Rachunek o podanym ID nie istnieje"
                return wynik
            
            # Przygotuj dane do regeneracji PDF
            dane_rachunku = {
                'numer_rachunku': szczegoly['numer_rachunku'],
                'data_wystawienia': szczegoly['data_wystawienia'],
                'data_wykonania_uslugi': szczegoly['data_wykonania_uslugi'],
                'sprzedawca': {
                    'imie': szczegoly['sprzedawca_imie'],
                    'nazwisko': szczegoly['sprzedawca_nazwisko'],
                    'ulica': szczegoly['sprzedawca_ulica'],
                    'nr_domu': szczegoly['sprzedawca_nr_domu'],
                    'kod_pocztowy': szczegoly['sprzedawca_kod_pocztowy'],
                    'miasto': szczegoly['sprzedawca_miasto']
                },
                'nabywca': {
                    'imie': szczegoly['nabywca_imie'],
                    'nazwisko': szczegoly['nabywca_nazwisko'],
                    'ulica': szczegoly['nabywca_ulica'],
                    'nr_domu': szczegoly['nabywca_nr_domu'],
                    'kod_pocztowy': szczegoly['nabywca_kod_pocztowy'],
                    'miasto': szczegoly['nabywca_miasto']
                },
                'nazwa_uslugi': szczegoly['nazwa_uslugi'],
                'cena_jednostkowa': szczegoly['cena_jednostkowa'],
                'kwota_do_zaplaty': szczegoly['kwota_do_zaplaty'],
                'kwota_slownie': szczegoly['kwota_slownie']
            }
            
            # Ustaw folder docelowy
            if folder_docelowy is None:
                folder_docelowy = os.path.dirname(szczegoly.get('plik_pdf', os.getcwd()))
            
            # Wygeneruj nowy PDF
            safe_numer = szczegoly['numer_rachunku'].replace('/', '_')
            nazwa_pliku = f"rachunek_{safe_numer}.pdf"
            sciezka_pdf = os.path.join(folder_docelowy, nazwa_pliku)
            
            self.pdf_generator.generuj_rachunek_pdf(dane_rachunku, sciezka_pdf)
            
            wynik['success'] = True
            wynik['pdf_path'] = sciezka_pdf
            
        except Exception as e:
            wynik['error'] = f"Błąd podczas regeneracji PDF: {str(e)}"
        
        return wynik
    
    def pobierz_podsumowanie_miesięczne(self, miesiac: int = None, rok: int = None) -> Dict:
        """
        Pobiera podsumowanie przychodów miesięcznych
        
        Args:
            miesiac: Miesiąc (domyślnie bieżący)
            rok: Rok (domyślnie bieżący)
            
        Returns:
            Słownik z informacjami o przychodach miesięcznych
        """
        if miesiac is None or rok is None:
            teraz = datetime.now()
            miesiac = miesiac or teraz.month
            rok = rok or teraz.year
        
        przychody = self.db.pobierz_przychody_miesiac(miesiac, rok)
        rachunki = self.db.pobierz_rachunki_miesiac(miesiac, rok)
        
        # Określ limit na podstawie roku
        limit_miesięczny = 3499.50  # Domyślny limit
        if rok == 2025:
            import config
            limit_miesięczny = config.MONTHLY_REVENUE_LIMIT_2025
        
        pozostaly_limit = max(0, limit_miesięczny - przychody)
        procent_wykorzystania = (przychody / limit_miesięczny) * 100 if limit_miesięczny > 0 else 0
        
        # Określ status
        if przychody > limit_miesięczny:
            status = "PRZEKROCZONY"
            status_kolor = "red"
        elif przychody > limit_miesięczny * 0.8:
            status = "OSTRZEŻENIE"
            status_kolor = "orange"
        elif przychody > limit_miesięczny * 0.5:
            status = "NORMALNY"
            status_kolor = "yellow"
        else:
            status = "BEZPIECZNY"
            status_kolor = "green"
        
        return {
            'miesiac': miesiac,
            'rok': rok,
            'nazwa_miesiaca': [
                "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
                "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
            ][miesiac - 1],
            'przychody_suma': przychody,
            'limit_miesięczny': limit_miesięczny,
            'pozostaly_limit': pozostaly_limit,
            'procent_wykorzystania': round(procent_wykorzystania, 1),
            'liczba_rachunkow': len(rachunki),
            'rachunki': rachunki,
            'status': status,
            'status_kolor': status_kolor
        }