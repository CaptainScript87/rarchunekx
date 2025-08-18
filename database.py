#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moduł odpowiedzialny za zarządzanie bazą danych rachunków
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """Klasa zarządzająca bazą danych rachunków"""
    
    def __init__(self, db_path: str = "rachunki.db"):
        """
        Inicjalizacja połączenia z bazą danych
        
        Args:
            db_path: Ścieżka do pliku bazy danych
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Tworzenie tabel w bazie danych jeśli nie istnieją"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela z danymi sprzedawcy (ustawienia domyślne)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sprzedawca (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    imie TEXT NOT NULL,
                    nazwisko TEXT NOT NULL,
                    ulica TEXT NOT NULL,
                    nr_domu TEXT NOT NULL,
                    kod_pocztowy TEXT NOT NULL,
                    miasto TEXT NOT NULL,
                    data_utworzenia TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela z rachunkami
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rachunki (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numer_rachunku TEXT UNIQUE NOT NULL,
                    data_wystawienia DATE NOT NULL,
                    data_wykonania_uslugi DATE NOT NULL,
                    
                    sprzedawca_imie TEXT NOT NULL,
                    sprzedawca_nazwisko TEXT NOT NULL,
                    sprzedawca_ulica TEXT NOT NULL,
                    sprzedawca_nr_domu TEXT NOT NULL,
                    sprzedawca_kod_pocztowy TEXT NOT NULL,
                    sprzedawca_miasto TEXT NOT NULL,
                    
                    nabywca_imie TEXT NOT NULL,
                    nabywca_nazwisko TEXT NOT NULL,
                    nabywca_ulica TEXT NOT NULL,
                    nabywca_nr_domu TEXT NOT NULL,
                    nabywca_kod_pocztowy TEXT NOT NULL,
                    nabywca_miasto TEXT NOT NULL,
                    
                    nazwa_uslugi TEXT NOT NULL,
                    cena_jednostkowa REAL NOT NULL,
                    kwota_do_zaplaty REAL NOT NULL,
                    kwota_slownie TEXT NOT NULL,
                    
                    plik_pdf TEXT,
                    data_utworzenia TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela z numeracją rachunków (do śledzenia kolejnych numerów w miesiącach)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS numeracja (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    miesiac INTEGER NOT NULL,
                    rok INTEGER NOT NULL,
                    ostatni_numer INTEGER NOT NULL,
                    UNIQUE(miesiac, rok)
                )
            ''')
            
            conn.commit()
    
    def get_domyslny_sprzedawca(self) -> Optional[Dict]:
        """Pobiera dane domyślnego sprzedawcy"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT imie, nazwisko, ulica, nr_domu, kod_pocztowy, miasto
                FROM sprzedawca 
                ORDER BY data_utworzenia DESC 
                LIMIT 1
            ''')
            
            result = cursor.fetchone()
            if result:
                return {
                    'imie': result[0],
                    'nazwisko': result[1],
                    'ulica': result[2],
                    'nr_domu': result[3],
                    'kod_pocztowy': result[4],
                    'miasto': result[5]
                }
            return None
    
    def zapisz_domyslnego_sprzedawce(self, dane_sprzedawcy: Dict) -> None:
        """Zapisuje lub aktualizuje dane domyślnego sprzedawcy"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sprzedawca (imie, nazwisko, ulica, nr_domu, kod_pocztowy, miasto)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                dane_sprzedawcy['imie'],
                dane_sprzedawcy['nazwisko'],
                dane_sprzedawcy['ulica'],
                dane_sprzedawcy['nr_domu'],
                dane_sprzedawcy['kod_pocztowy'],
                dane_sprzedawcy['miasto']
            ))
            conn.commit()
    
    def generuj_numer_rachunku(self) -> str:
        """
        Generuje unikalny numer rachunku w formacie nr/miesiąc/rok
        
        Returns:
            Numer rachunku jako string
        """
        teraz = datetime.now()
        miesiac = teraz.month
        rok = teraz.year
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Sprawdź ostatni numer dla tego miesiąca i roku
            cursor.execute('''
                SELECT ostatni_numer FROM numeracja 
                WHERE miesiac = ? AND rok = ?
            ''', (miesiac, rok))
            
            result = cursor.fetchone()
            
            if result:
                nowy_numer = result[0] + 1
                cursor.execute('''
                    UPDATE numeracja 
                    SET ostatni_numer = ? 
                    WHERE miesiac = ? AND rok = ?
                ''', (nowy_numer, miesiac, rok))
            else:
                nowy_numer = 1
                cursor.execute('''
                    INSERT INTO numeracja (miesiac, rok, ostatni_numer)
                    VALUES (?, ?, ?)
                ''', (miesiac, rok, nowy_numer))
            
            conn.commit()
            
        return f"{nowy_numer}/{miesiac:02d}/{rok}"
    
    def zapisz_rachunek(self, dane_rachunku: Dict) -> int:
        """
        Zapisuje rachunek do bazy danych
        
        Args:
            dane_rachunku: Słownik z danymi rachunku
            
        Returns:
            ID zapisanego rachunku
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO rachunki (
                    numer_rachunku, data_wystawienia, data_wykonania_uslugi,
                    sprzedawca_imie, sprzedawca_nazwisko, sprzedawca_ulica, 
                    sprzedawca_nr_domu, sprzedawca_kod_pocztowy, sprzedawca_miasto,
                    nabywca_imie, nabywca_nazwisko, nabywca_ulica, 
                    nabywca_nr_domu, nabywca_kod_pocztowy, nabywca_miasto,
                    nazwa_uslugi, cena_jednostkowa, kwota_do_zaplaty, kwota_slownie, plik_pdf
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dane_rachunku['numer_rachunku'],
                dane_rachunku['data_wystawienia'],
                dane_rachunku['data_wykonania_uslugi'],
                dane_rachunku['sprzedawca']['imie'],
                dane_rachunku['sprzedawca']['nazwisko'],
                dane_rachunku['sprzedawca']['ulica'],
                dane_rachunku['sprzedawca']['nr_domu'],
                dane_rachunku['sprzedawca']['kod_pocztowy'],
                dane_rachunku['sprzedawca']['miasto'],
                dane_rachunku['nabywca']['imie'],
                dane_rachunku['nabywca']['nazwisko'],
                dane_rachunku['nabywca']['ulica'],
                dane_rachunku['nabywca']['nr_domu'],
                dane_rachunku['nabywca']['kod_pocztowy'],
                dane_rachunku['nabywca']['miasto'],
                dane_rachunku['nazwa_uslugi'],
                dane_rachunku['cena_jednostkowa'],
                dane_rachunku['kwota_do_zaplaty'],
                dane_rachunku['kwota_slownie'],
                dane_rachunku.get('plik_pdf', '')
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def pobierz_wszystkie_rachunki(self) -> List[Dict]:
        """Pobiera wszystkie rachunki z bazy danych"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, numer_rachunku, data_wystawienia, 
                       nabywca_imie, nabywca_nazwisko, kwota_do_zaplaty, plik_pdf
                FROM rachunki 
                ORDER BY data_wystawienia DESC
            ''')
            
            rachunki = []
            for row in cursor.fetchall():
                rachunki.append({
                    'id': row[0],
                    'numer_rachunku': row[1],
                    'data_wystawienia': row[2],
                    'nabywca': f"{row[3]} {row[4]}",
                    'kwota': row[5],
                    'plik_pdf': row[6]
                })
            
            return rachunki
    
    def szukaj_rachunki(self, query: str) -> List[Dict]:
        """
        Wyszukuje rachunki po numerze, dacie lub nazwisku nabywcy
        
        Args:
            query: Fraza do wyszukania
            
        Returns:
            Lista znalezionych rachunków
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Wyszukiwanie w numerze rachunku, nazwisku nabywcy i dacie
            cursor.execute('''
                SELECT id, numer_rachunku, data_wystawienia, 
                       nabywca_imie, nabywca_nazwisko, kwota_do_zaplaty, plik_pdf
                FROM rachunki 
                WHERE numer_rachunku LIKE ? 
                   OR nabywca_imie LIKE ? 
                   OR nabywca_nazwisko LIKE ?
                   OR data_wystawienia LIKE ?
                ORDER BY data_wystawienia DESC
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
            
            rachunki = []
            for row in cursor.fetchall():
                rachunki.append({
                    'id': row[0],
                    'numer_rachunku': row[1],
                    'data_wystawienia': row[2],
                    'nabywca': f"{row[3]} {row[4]}",
                    'kwota': row[5],
                    'plik_pdf': row[6]
                })
            
            return rachunki
    
    def pobierz_rachunek_szczegoly(self, rachunek_id: int) -> Optional[Dict]:
        """Pobiera szczegółowe dane rachunku"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rachunki WHERE id = ?', (rachunek_id,))
            
            result = cursor.fetchone()
            if not result:
                return None
            
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
    
    def eksportuj_do_csv(self, sciezka_pliku: str) -> None:
        """Eksportuje wszystkie rachunki do pliku CSV"""
        import csv
        
        rachunki = self.pobierz_wszystkie_rachunki()
        
        with open(sciezka_pliku, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Numer rachunku', 'Data wystawienia', 'Nabywca', 'Kwota (PLN)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for rachunek in rachunki:
                writer.writerow({
                    'Numer rachunku': rachunek['numer_rachunku'],
                    'Data wystawienia': rachunek['data_wystawienia'],
                    'Nabywca': rachunek['nabywca'],
                    'Kwota (PLN)': f"{rachunek['kwota']:.2f}"
                })
    
    def pobierz_przychody_miesiac(self, miesiac: int, rok: int) -> float:
        """
        Pobiera sumę przychodów dla danego miesiąca i roku
        
        Args:
            miesiac: Miesiąc (1-12)
            rok: Rok
            
        Returns:
            Suma przychodów w PLN
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COALESCE(SUM(kwota_do_zaplaty), 0) 
                FROM rachunki 
                WHERE strftime('%m', data_wystawienia) = ? 
                AND strftime('%Y', data_wystawienia) = ?
            ''', (f"{miesiac:02d}", str(rok)))
            
            result = cursor.fetchone()
            return result[0] if result else 0.0
    
    def pobierz_przychody_biezacy_miesiac(self) -> float:
        """
        Pobiera sumę przychodów dla bieżącego miesiąca
        
        Returns:
            Suma przychodów w PLN
        """
        teraz = datetime.now()
        return self.pobierz_przychody_miesiac(teraz.month, teraz.year)
    
    def pobierz_rachunki_miesiac(self, miesiac: int, rok: int) -> List[Dict]:
        """
        Pobiera wszystkie rachunki dla danego miesiąca i roku
        
        Args:
            miesiac: Miesiąc (1-12)
            rok: Rok
            
        Returns:
            Lista rachunków
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, numer_rachunku, data_wystawienia, 
                       nabywca_imie, nabywca_nazwisko, kwota_do_zaplaty, plik_pdf
                FROM rachunki 
                WHERE strftime('%m', data_wystawienia) = ? 
                AND strftime('%Y', data_wystawienia) = ?
                ORDER BY data_wystawienia DESC
            ''', (f"{miesiac:02d}", str(rok)))
            
            rachunki = []
            for row in cursor.fetchall():
                rachunki.append({
                    'id': row[0],
                    'numer_rachunku': row[1],
                    'data_wystawienia': row[2],
                    'nabywca': f"{row[3]} {row[4]}",
                    'kwota': row[5],
                    'plik_pdf': row[6]
                })
            
            return rachunki
    
    def pobierz_raport_miesięczny(self, rok: int = None) -> List[Dict]:
        """
        Pobiera raport miesięczny dla danego roku
        
        Args:
            rok: Rok do analizy (domyślnie bieżący)
            
        Returns:
            Lista z podsumowaniem dla każdego miesiąca
        """
        if rok is None:
            rok = datetime.now().year
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    strftime('%m', data_wystawienia) as miesiac,
                    COUNT(*) as liczba_rachunkow,
                    SUM(kwota_do_zaplaty) as suma_kwot,
                    AVG(kwota_do_zaplaty) as srednia_kwota,
                    MIN(kwota_do_zaplaty) as min_kwota,
                    MAX(kwota_do_zaplaty) as max_kwota
                FROM rachunki 
                WHERE strftime('%Y', data_wystawienia) = ?
                GROUP BY strftime('%m', data_wystawienia)
                ORDER BY miesiac
            ''', (str(rok),))
            
            miesiace = []
            nazwa_miesiecy = [
                "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
                "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
            ]
            
            for row in cursor.fetchall():
                miesiac_nr = int(row[0])
                miesiace.append({
                    'miesiac_nr': miesiac_nr,
                    'miesiac_nazwa': nazwa_miesiecy[miesiac_nr - 1],
                    'rok': rok,
                    'liczba_rachunkow': row[1],
                    'suma_kwot': round(row[2], 2),
                    'srednia_kwota': round(row[3], 2),
                    'min_kwota': round(row[4], 2),
                    'max_kwota': round(row[5], 2)
                })
            
            return miesiace
    
    def pobierz_raport_roczny(self) -> List[Dict]:
        """
        Pobiera raport roczny dla wszystkich lat
        
        Returns:
            Lista z podsumowaniem dla każdego roku
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    strftime('%Y', data_wystawienia) as rok,
                    COUNT(*) as liczba_rachunkow,
                    SUM(kwota_do_zaplaty) as suma_kwot,
                    AVG(kwota_do_zaplaty) as srednia_kwota,
                    MIN(kwota_do_zaplaty) as min_kwota,
                    MAX(kwota_do_zaplaty) as max_kwota
                FROM rachunki 
                GROUP BY strftime('%Y', data_wystawienia)
                ORDER BY rok DESC
            ''')
            
            lata = []
            for row in cursor.fetchall():
                lata.append({
                    'rok': int(row[0]),
                    'liczba_rachunkow': row[1],
                    'suma_kwot': round(row[2], 2),
                    'srednia_kwota': round(row[3], 2),
                    'min_kwota': round(row[4], 2),
                    'max_kwota': round(row[5], 2)
                })
            
            return lata
    
    def pobierz_top_klientow(self, limit: int = 10) -> List[Dict]:
        """
        Pobiera top klientów według liczby rachunków i kwot
        
        Args:
            limit: Maksymalna liczba klientów do zwrócenia
            
        Returns:
            Lista z top klientami
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    nabywca_imie || ' ' || nabywca_nazwisko as klient,
                    COUNT(*) as liczba_rachunkow,
                    SUM(kwota_do_zaplaty) as suma_kwot,
                    AVG(kwota_do_zaplaty) as srednia_kwota,
                    MAX(data_wystawienia) as ostatni_rachunek
                FROM rachunki 
                GROUP BY nabywca_imie, nabywca_nazwisko
                ORDER BY suma_kwot DESC
                LIMIT ?
            ''', (limit,))
            
            klienci = []
            for row in cursor.fetchall():
                klienci.append({
                    'klient': row[0],
                    'liczba_rachunkow': row[1],
                    'suma_kwot': round(row[2], 2),
                    'srednia_kwota': round(row[3], 2),
                    'ostatni_rachunek': row[4]
                })
            
            return klienci
    
    def pobierz_statystyki_ogolne(self) -> Dict:
        """
        Pobiera ogólne statystyki aplikacji
        
        Returns:
            Słownik z ogólnymi statystykami
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Podstawowe statystyki
            cursor.execute('SELECT COUNT(*) FROM rachunki')
            total_rachunki = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(kwota_do_zaplaty) FROM rachunki')
            total_kwota = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT AVG(kwota_do_zaplaty) FROM rachunki')
            avg_kwota = cursor.fetchone()[0] or 0
            
            # Pierwszy i ostatni rachunek
            cursor.execute('SELECT MIN(data_wystawienia) FROM rachunki')
            pierwszy_rachunek = cursor.fetchone()[0]
            
            cursor.execute('SELECT MAX(data_wystawienia) FROM rachunki')
            ostatni_rachunek = cursor.fetchone()[0]
            
            # Liczba unikalnych klientów
            cursor.execute('SELECT COUNT(DISTINCT nabywca_imie || nabywca_nazwisko) FROM rachunki')
            unikalni_klienci = cursor.fetchone()[0]
            
            return {
                'total_rachunki': total_rachunki,
                'total_kwota': round(total_kwota, 2),
                'srednia_kwota': round(avg_kwota, 2),
                'pierwszy_rachunek': pierwszy_rachunek,
                'ostatni_rachunek': ostatni_rachunek,
                'unikalni_klienci': unikalni_klienci
            }