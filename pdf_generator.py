#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moduł odpowiedzialny za generowanie rachunków w formacie PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.fonts import addMapping
import os
from typing import Dict
from datetime import datetime

class PDFGenerator:
    """Klasa odpowiedzialna za generowanie rachunków PDF"""
    
    def __init__(self):
        """Inicjalizacja generatora PDF"""
        self.page_width, self.page_height = A4
        self._setup_fonts()
    
    def _setup_fonts(self):
        """Konfiguruje fonty z obsługą polskich znaków"""
        try:
            # Próba użycia fontów systemowych Windows z polskimi znakami
            import platform
            if platform.system() == "Windows":
                # Windows - spróbuj użyć Arial Unicode MS lub innych fontów z polskimi znakami
                try:
                    # Rejestrujemy standardowe fonty z lepszą obsługą Unicode
                    from reportlab.pdfbase import pdfmetrics
                    from reportlab.pdfbase.ttfonts import TTFont
                    
                    # Spróbuj znaleźć font Arial na Windows
                    windows_fonts = [
                        "C:/Windows/Fonts/arial.ttf",
                        "C:/Windows/Fonts/calibri.ttf", 
                        "C:/Windows/Fonts/times.ttf"
                    ]
                    
                    for font_path in windows_fonts:
                        if os.path.exists(font_path):
                            font_name = os.path.basename(font_path).replace('.ttf', '').title()
                            pdfmetrics.registerFont(TTFont(font_name, font_path))
                            self.font_family = font_name
                            break
                    else:
                        # Fallback - użyj standardowych fontów ReportLab
                        self.font_family = "Helvetica"
                        
                except Exception:
                    self.font_family = "Helvetica"
            else:
                self.font_family = "Helvetica"
                
        except Exception:
            # Fallback - standardowe fonty
            self.font_family = "Helvetica"
        
        # Mapowanie wariantów fontów
        self.fonts = {
            'regular': self.font_family,
            'bold': f"{self.font_family}-Bold" if self.font_family == "Helvetica" else self.font_family,
            'italic': f"{self.font_family}-Oblique" if self.font_family == "Helvetica" else self.font_family
        }
        
    def generuj_rachunek_pdf(self, dane_rachunku: Dict, sciezka_pliku: str) -> str:
        """
        Generuje rachunek w formacie PDF
        
        Args:
            dane_rachunku: Słownik z danymi rachunku
            sciezka_pliku: Ścieżka gdzie ma zostać zapisany plik PDF
            
        Returns:
            Ścieżka do wygenerowanego pliku
        """
        c = canvas.Canvas(sciezka_pliku, pagesize=A4)
        
        # Ustawienie enkodowania dla polskich znaków
        c.setTitle(f"Rachunek {dane_rachunku['numer_rachunku']}")
        
        # Nagłówek rachunku
        self._rysuj_naglowek(c, dane_rachunku)
        
        # Dane sprzedawcy i nabywcy
        self._rysuj_dane_stron(c, dane_rachunku)
        
        # Szczegóły usługi
        self._rysuj_szczegoly_uslugi(c, dane_rachunku)
        
        # Kwota do zapłaty
        self._rysuj_kwote_do_zaplaty(c, dane_rachunku)
        
        # Pole na podpis
        self._rysuj_pole_podpisu(c)
        
        c.save()
        return sciezka_pliku
    
    def _rysuj_naglowek(self, c: canvas.Canvas, dane: Dict) -> None:
        """Rysuje nagłówek rachunku"""
        # Tytuł "RACHUNEK"
        c.setFont(self.fonts['bold'], 24)
        title = "RACHUNEK"
        title_width = c.stringWidth(title, self.fonts['bold'], 24)
        c.drawString((self.page_width - title_width) / 2, self.page_height - 3*cm, title)
        
        # Numer rachunku
        c.setFont(self.fonts['bold'], 16)
        number_text = f"nr {dane['numer_rachunku']}"
        number_width = c.stringWidth(number_text, self.fonts['bold'], 16)
        c.drawString((self.page_width - number_width) / 2, self.page_height - 4*cm, number_text)
        
        # Daty
        c.setFont(self.fonts['regular'], 12)
        y_pos = self.page_height - 5.5*cm
        
        c.drawString(3*cm, y_pos, f"Data wystawienia: {dane['data_wystawienia']}")
        c.drawString(12*cm, y_pos, f"Data wykonania usługi: {dane['data_wykonania_uslugi']}")
    
    def _rysuj_dane_stron(self, c: canvas.Canvas, dane: Dict) -> None:
        """Rysuje dane sprzedawcy i nabywcy"""
        y_start = self.page_height - 7*cm
        
        # Sprzedawca
        c.setFont(self.fonts['bold'], 12)
        c.drawString(3*cm, y_start, "SPRZEDAWCA:")
        
        c.setFont(self.fonts['regular'], 10)
        sprzedawca = dane['sprzedawca']
        c.drawString(3*cm, y_start - 0.5*cm, f"{sprzedawca['imie']} {sprzedawca['nazwisko']}")
        c.drawString(3*cm, y_start - 1*cm, f"{sprzedawca['ulica']} {sprzedawca['nr_domu']}")
        c.drawString(3*cm, y_start - 1.5*cm, f"{sprzedawca['kod_pocztowy']} {sprzedawca['miasto']}")
        
        # Nabywca
        c.setFont(self.fonts['bold'], 12)
        c.drawString(11*cm, y_start, "NABYWCA:")
        
        c.setFont(self.fonts['regular'], 10)
        nabywca = dane['nabywca']
        c.drawString(11*cm, y_start - 0.5*cm, f"{nabywca['imie']} {nabywca['nazwisko']}")
        c.drawString(11*cm, y_start - 1*cm, f"{nabywca['ulica']} {nabywca['nr_domu']}")
        c.drawString(11*cm, y_start - 1.5*cm, f"{nabywca['kod_pocztowy']} {nabywca['miasto']}")
    
    def _rysuj_szczegoly_uslugi(self, c: canvas.Canvas, dane: Dict) -> None:
        """Rysuje szczegóły wykonywanej usługi"""
        y_start = self.page_height - 11*cm
        
        # Nagłówek tabeli
        c.setFont(self.fonts['bold'], 12)
        c.drawString(3*cm, y_start, "WYKONANA USŁUGA:")
        
        # Rysowanie tabeli
        y_table = y_start - 1*cm
        
        # Nagłówki kolumn
        c.setFont(self.fonts['bold'], 10)
        c.drawString(3*cm, y_table, "Nazwa usługi")
        c.drawString(13*cm, y_table, "Cena")
        
        # Linia pod nagłówkami
        c.line(3*cm, y_table - 0.2*cm, 17*cm, y_table - 0.2*cm)
        
        # Dane usługi
        c.setFont(self.fonts['regular'], 10)
        y_table -= 0.7*cm
        
        # Nazwa usługi (może być długa, więc dzielimy na wiersze jeśli potrzeba)
        nazwa_uslugi = dane['nazwa_uslugi']
        max_width = 9*cm
        
        # Prosta implementacja łamania tekstu
        if len(nazwa_uslugi) > 60:
            words = nazwa_uslugi.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + word) < 60:
                    current_line += word + " "
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            for i, line in enumerate(lines):
                c.drawString(3*cm, y_table - i*0.4*cm, line)
        else:
            c.drawString(3*cm, y_table, nazwa_uslugi)
        
        # Cena
        c.drawString(13*cm, y_table, f"{dane['cena_jednostkowa']:.2f} PLN")
        
        # Linia pod danymi
        c.line(3*cm, y_table - 0.7*cm, 17*cm, y_table - 0.7*cm)
    
    def _rysuj_kwote_do_zaplaty(self, c: canvas.Canvas, dane: Dict) -> None:
        """Rysuje kwotę do zapłaty"""
        y_pos = self.page_height - 15*cm
        
        c.setFont(self.fonts['bold'], 14)
        c.drawString(3*cm, y_pos, "DO ZAPŁATY:")
        
        # Kwota cyfrowo
        c.setFont(self.fonts['bold'], 16)
        c.drawString(8*cm, y_pos, f"{dane['kwota_do_zaplaty']:.2f} PLN")
        
        # Kwota słownie
        c.setFont(self.fonts['regular'], 12)
        c.drawString(3*cm, y_pos - 1*cm, f"Słownie: {dane['kwota_slownie']}")
    
    def _rysuj_pole_podpisu(self, c: canvas.Canvas) -> None:
        """Rysuje pole na podpis sprzedawcy"""
        y_pos = self.page_height - 20*cm
        
        # Linia na podpis
        c.line(11*cm, y_pos, 17*cm, y_pos)
        
        # Opis
        c.setFont(self.fonts['regular'], 10)
        signature_text = "Podpis sprzedawcy"
        signature_width = c.stringWidth(signature_text, self.fonts['regular'], 10)
        c.drawString(14*cm - signature_width/2, y_pos - 0.5*cm, signature_text)
        
        # Data miejsca wystawienia
        c.drawString(3*cm, y_pos, f"Miejsce i data: ........................., dnia {datetime.now().strftime('%d.%m.%Y')}")

def kwota_slownie(kwota: float) -> str:
    """
    Konwertuje kwotę liczbową na słowną reprezentację w języku polskim
    
    Args:
        kwota: Kwota do konwersji
        
    Returns:
        Kwota zapisana słownie
    """
    try:
        from num2words import num2words
        
        # Rozdzielenie na złote i grosze
        zlote = int(kwota)
        grosze = int(round((kwota - zlote) * 100))
        
        # Konwersja złotych
        zlote_slownie = num2words(zlote, lang='pl')
        
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
            
    except ImportError:
        # Fallback jeśli num2words nie jest dostępne
        return f"{kwota:.2f} PLN"