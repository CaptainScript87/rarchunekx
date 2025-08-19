#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfejs graficzny aplikacji do rachunków
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime
from typing import Dict, List
from rachunek_manager import RachunekManager
import config
from version import get_full_version_string, get_build_info, VERSION_HISTORY, __version__

class RachunekApp:
    """Główna klasa aplikacji GUI"""
    
    def __init__(self, root):
        """Inicjalizacja aplikacji"""
        self.root = root
        self.root.title(f"💼 {config.APP_FULL_TITLE}")
        
        # Wyśrodkuj okno na ekranie
        self.center_window(1100, 800)
        
        # Ustaw minimalny rozmiar
        self.root.minsize(900, 650)
        self.root.resizable(True, True)
        
        # Ustaw nowoczesny motyw
        self.setup_modern_theme()
        
        # Manager rachunków
        self.manager = RachunekManager()
        
        # Zmienne dla podsumowania miesięcznego
        self.monthly_summary_vars = {}
        
        # Tworzenie głównego interfejsu
        self.create_notebook()
        self.create_nowy_rachunek_tab()
        self.create_lista_rachunkow_tab()
        self.create_ustawienia_tab()
        
        # Załaduj domyślne dane sprzedawcy
        self.load_default_sprzedawca_data()
        
        # Dostosuj rozmiar okna po załadowaniu interfejsu
        self.root.after(100, self.adjust_window_size)
        
        # Dodaj skróty klawiszowe
        self.setup_keyboard_shortcuts()
    
    def center_window(self, width, height):
        """Wyśrodkowuje okno na ekranie"""
        # Pobierz rozmiary ekranu
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Oblicz pozycję okna
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Ustaw geometrię okna
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def adjust_window_size(self):
        """Dostosowuje rozmiar okna do zawartości"""
        # Aktualizuj wszystkie elementy
        self.root.update_idletasks()
        
        # Pobierz wymagany rozmiar dla notebook
        self.notebook.update_idletasks()
        req_width = self.notebook.winfo_reqwidth() + 40  # Dodaj margines
        req_height = self.notebook.winfo_reqheight() + 80  # Dodaj margines na tytuł okna
        
        # Upewnij się, że okno nie będzie za małe
        min_width = 900
        min_height = 800  # Zwiększ minimalną wysokość dla nowych sekcji
        
        # Upewnij się, że okno nie będzie za duże (max 90% ekranu)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        max_width = int(screen_width * 0.9)
        max_height = int(screen_height * 0.9)
        
        # Oblicz optymalny rozmiar
        optimal_width = max(min_width, min(req_width, max_width))
        optimal_height = max(min_height, min(req_height, max_height))
        
        # Wyśrodkuj okno z nowym rozmiarem
        self.center_window(optimal_width, optimal_height)
        
        # Ustaw nowy minimalny rozmiar
        self.root.minsize(min_width, min_height)
        
        # Aktualizuj informację o rozmiarze
        self.update_size_info()
    
    def update_size_info(self):
        """Aktualizuje informację o aktualnym rozmiarze okna"""
        try:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            if hasattr(self, 'size_info_var'):
                self.size_info_var.set(f"{width} × {height} pikseli")
        except:
            if hasattr(self, 'size_info_var'):
                self.size_info_var.set("Niedostępne")
    
    def weryfikuj_administratora(self) -> bool:
        """
        Weryfikuje hasło administratora
        
        Returns:
            True jeśli weryfikacja przebiegła pomyślnie
        """
        haslo_window = tk.Toplevel(self.root)
        haslo_window.title("🔐 Uwierzytelnienie Administratora")
        haslo_window.geometry("400x200")
        haslo_window.resizable(False, False)
        haslo_window.transient(self.root)
        haslo_window.grab_set()
        
        # Wyśrodkuj okno
        haslo_window.update_idletasks()
        x = (haslo_window.winfo_screenwidth() - 400) // 2
        y = (haslo_window.winfo_screenheight() - 200) // 2
        haslo_window.geometry(f"400x200+{x}+{y}")
        
        wynik = {'authenticated': False}
        
        # Ramka główna
        main_frame = ttk.Frame(haslo_window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Etykieta informacyjna
        ttk.Label(main_frame, text="🔐 Wprowadź hasło administratora:", 
                 font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(main_frame, text="Domyślne hasło: admin123", 
                 foreground="gray").pack(pady=(0, 15))
        
        # Pole hasła
        haslo_var = tk.StringVar()
        haslo_entry = ttk.Entry(main_frame, textvariable=haslo_var, show="*", width=30, font=('Segoe UI', 10))
        haslo_entry.pack(pady=(0, 20))
        haslo_entry.focus()
        
        # Ramka przycisków
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        def sprawdz_haslo():
            if self.manager.sprawdz_haslo_administratora(haslo_var.get()):
                wynik['authenticated'] = True
                haslo_window.destroy()
            else:
                messagebox.showerror("Błąd", "Niepoprawne hasło administratora!", parent=haslo_window)
                haslo_entry.delete(0, tk.END)
                haslo_entry.focus()
        
        def anuluj():
            haslo_window.destroy()
        
        # Przyciski
        ttk.Button(buttons_frame, text="✅ OK", command=sprawdz_haslo, 
                  style="Success.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="❌ Anuluj", command=anuluj).pack(side="left")
        
        # Obsługa Enter
        haslo_entry.bind('<Return>', lambda e: sprawdz_haslo())
        
        # Czekaj na zamknięcie okna
        self.root.wait_window(haslo_window)
        
        return wynik['authenticated']
    
    def otworz_usuwanie_rachunku(self):
        """Otwiera okno usuwania rachunku"""
        if not self.weryfikuj_administratora():
            return
        
        # Okno usuwania
        usun_window = tk.Toplevel(self.root)
        usun_window.title("❌ Usuń Rachunek")
        usun_window.geometry("600x500")
        usun_window.transient(self.root)
        usun_window.grab_set()
        
        # Wyśrodkuj okno
        usun_window.update_idletasks()
        x = (usun_window.winfo_screenwidth() - 600) // 2
        y = (usun_window.winfo_screenheight() - 500) // 2
        usun_window.geometry(f"600x500+{x}+{y}")
        
        main_frame = ttk.Frame(usun_window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Ostrzeżenie
        warning_frame = ttk.Frame(main_frame)
        warning_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(warning_frame, text="⚠️ OSTRZEŻENIE", 
                 font=('Segoe UI', 12, 'bold'), foreground="red").pack()
        ttk.Label(warning_frame, 
                 text="Usunięte rachunki mogą być przywrócone z sekcji 'Zarządzaj usuniętymi rachunkami'.", 
                 foreground="orange").pack()
        
        # Wybór rachunku
        ttk.Label(main_frame, text="Wybierz rachunek do usunięcia:", 
                 font=('Segoe UI', 10, 'bold')).pack(anchor="w", pady=(0, 5))
        
        # Ramka dla tabeli
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Lista rachunków
        columns = ("ID", "Numer", "Data", "Nabywca", "Kwota")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80 if col == "ID" else 100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pakowanie tree i scrollbar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Załaduj rachunki
        rachunki = self.manager.pobierz_liste_rachunkow()
        print(f"DEBUG: Ładuję {len(rachunki)} rachunków do tabeli usuwania")  # Debug
        for rachunek in rachunki:
            tree.insert("", "end", values=(
                rachunek['id'],
                rachunek['numer_rachunku'],
                rachunek['data_wystawienia'],
                rachunek['nabywca'],
                f"{rachunek['kwota']:.2f} PLN"
            ))
        print("DEBUG: Rachunki załadowane do tabeli")  # Debug
        
        # Powód usunięcia
        ttk.Label(main_frame, text="Powód usunięcia (opcjonalnie):").pack(anchor="w", pady=(5, 0))
        powod_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=powod_var, width=50).pack(fill="x", pady=(5, 15))
        
        # Przyciski
        def usun_wybrany():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Uwaga", "Wybierz rachunek do usunięcia.", parent=usun_window)
                return
            
            item = tree.item(selection[0])
            rachunek_id = item['values'][0]
            numer = item['values'][1]
            
            if messagebox.askyesno("Potwierdzenie", 
                                 f"Czy na pewno usunąć rachunek {numer}?", 
                                 parent=usun_window):
                wynik = self.manager.usun_rachunek_z_potwierdzeniem(rachunek_id, powod_var.get())
                
                if wynik['success']:
                    messagebox.showinfo("Sukces", 
                                      f"Rachunek {wynik['numer_rachunku']} został usunięty.", 
                                      parent=usun_window)
                    usun_window.destroy()
                    # Odśwież listę rachunków w głównym oknie
                    self.load_rachunki_data()
                else:
                    messagebox.showerror("Błąd", wynik['error'], parent=usun_window)
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        print("DEBUG: Tworzę przyciski w oknie usuwania")  # Debug
        ttk.Button(buttons_frame, text="❌ Usuń wybrany", command=usun_wybrany,
                  style="Warning.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="🚫 Anuluj", 
                  command=usun_window.destroy).pack(side="left")
        
        # Wymusza aktualizację okna
        usun_window.update_idletasks()
    
    def otworz_zarzadzanie_usuniete(self):
        """Otwiera okno zarządzania usuniętymi rachunkami"""
        if not self.weryfikuj_administratora():
            return
        
        # Okno zarządzania
        manage_window = tk.Toplevel(self.root)
        manage_window.title("🗑️ Zarządzanie usuniętymi rachunkami")
        manage_window.geometry("700x500")
        manage_window.transient(self.root)
        
        # Wyśrodkuj okno
        manage_window.update_idletasks()
        x = (manage_window.winfo_screenwidth() - 700) // 2
        y = (manage_window.winfo_screenheight() - 500) // 2
        manage_window.geometry(f"700x500+{x}+{y}")
        
        main_frame = ttk.Frame(manage_window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Nagłówek
        ttk.Label(main_frame, text="🗑️ Usunięte rachunki", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 15))
        
        # Lista usuniętych rachunków
        columns = ("ID", "Numer", "Data wystawienia", "Nabywca", "Kwota", "Data usunięcia", "Powód")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # Konfiguracja kolumn
        widths = [50, 100, 100, 120, 80, 120, 150]
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=widths[i])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pakowanie
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def odswież_liste():
            # Wyczyść listę
            for item in tree.get_children():
                tree.delete(item)
            
            # Załaduj usunięte rachunki
            usunięte = self.manager.pobierz_usunięte_rachunki()
            for rachunek in usunięte:
                tree.insert("", "end", values=(
                    rachunek['id'],
                    rachunek['numer_rachunku'],
                    rachunek['data_wystawienia'],
                    rachunek['nabywca'],
                    f"{rachunek['kwota']:.2f} PLN",
                    rachunek['data_usuniecia'][:19] if rachunek['data_usuniecia'] else "Nieznana",  # Obetnij mikrosekundy
                    rachunek['powod_usuniecia']
                ))
        
        # Załaduj dane
        odswież_liste()
        
        # Przyciski
        def przywroc_wybrany():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Uwaga", "Wybierz rachunek do przywrócenia.", parent=manage_window)
                return
            
            item = tree.item(selection[0])
            deleted_id = item['values'][0]
            numer = item['values'][1]
            
            if messagebox.askyesno("Potwierdzenie", 
                                 f"Czy na pewno przywrócić rachunek {numer}?", 
                                 parent=manage_window):
                wynik = self.manager.przywroc_rachunek(deleted_id)
                
                if wynik['success']:
                    messagebox.showinfo("Sukces", 
                                      f"Rachunek {numer} został przywrócony.", 
                                      parent=manage_window)
                    odswież_liste()
                    # Odśwież listę rachunków w głównym oknie
                    self.load_rachunki_data()
                else:
                    messagebox.showerror("Błąd", wynik['error'], parent=manage_window)
        
        def trwale_usun_wybrany():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Uwaga", "Wybierz rachunek do trwałego usunięcia.", parent=manage_window)
                return
            
            item = tree.item(selection[0])
            deleted_id = item['values'][0]
            numer = item['values'][1]
            
            if messagebox.askyesno("Ostrzeżenie", 
                                 f"⚠️ UWAGA: Trwałe usunięcie rachunku {numer} nie może być cofnięte!\n\nCzy na pewno kontynuować?", 
                                 parent=manage_window):
                wynik = self.manager.trwale_usun_rachunek(deleted_id)
                
                if wynik['success']:
                    messagebox.showinfo("Sukces", 
                                      f"Rachunek {numer} został trwale usunięty.", 
                                      parent=manage_window)
                    odswież_liste()
                else:
                    messagebox.showerror("Błąd", wynik['error'], parent=manage_window)
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(buttons_frame, text="↩️ Przywróć wybrany", command=przywroc_wybrany,
                  style="Success.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="🗑️ Usuń trwale", command=trwale_usun_wybrany,
                  style="Warning.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="🔄 Odśwież", command=odswież_liste).pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="🚫 Zamknij", command=manage_window.destroy).pack(side="right")
    
    def otworz_zmiana_hasla(self):
        """Otwiera okno zmiany hasła administratora"""
        if not self.weryfikuj_administratora():
            return
        
        # Okno zmiany hasła
        haslo_window = tk.Toplevel(self.root)
        haslo_window.title("🔑 Zmień hasło administratora")
        haslo_window.geometry("400x300")
        haslo_window.resizable(False, False)
        haslo_window.transient(self.root)
        haslo_window.grab_set()
        
        # Wyśrodkuj okno
        haslo_window.update_idletasks()
        x = (haslo_window.winfo_screenwidth() - 400) // 2
        y = (haslo_window.winfo_screenheight() - 300) // 2
        haslo_window.geometry(f"400x300+{x}+{y}")
        
        main_frame = ttk.Frame(haslo_window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Nagłówek
        ttk.Label(main_frame, text="🔑 Zmień hasło administratora", 
                 font=('Segoe UI', 12, 'bold')).pack(pady=(0, 20))
        
        # Stare hasło
        ttk.Label(main_frame, text="Obecne hasło:").pack(anchor="w", pady=(0, 5))
        stare_haslo_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=stare_haslo_var, show="*", width=40).pack(pady=(0, 15))
        
        # Nowe hasło
        ttk.Label(main_frame, text="Nowe hasło (min. 6 znaków):").pack(anchor="w", pady=(0, 5))
        nowe_haslo_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=nowe_haslo_var, show="*", width=40).pack(pady=(0, 15))
        
        # Potwierdzenie nowego hasła
        ttk.Label(main_frame, text="Potwierdź nowe hasło:").pack(anchor="w", pady=(0, 5))
        potwierdz_haslo_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=potwierdz_haslo_var, show="*", width=40).pack(pady=(0, 20))
        
        def zmien_haslo():
            stare = stare_haslo_var.get()
            nowe = nowe_haslo_var.get()
            potwierdz = potwierdz_haslo_var.get()
            
            if not stare or not nowe or not potwierdz:
                messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.", parent=haslo_window)
                return
            
            if nowe != potwierdz:
                messagebox.showerror("Błąd", "Nowe hasło i jego potwierdzenie muszą być identyczne.", parent=haslo_window)
                return
            
            wynik = self.manager.zmien_haslo_administratora(stare, nowe)
            
            if wynik['success']:
                messagebox.showinfo("Sukces", "Hasło administratora zostało zmienione.", parent=haslo_window)
                haslo_window.destroy()
            else:
                messagebox.showerror("Błąd", wynik['error'], parent=haslo_window)
        
        # Przyciski
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        ttk.Button(buttons_frame, text="✅ Zmień hasło", command=zmien_haslo,
                  style="Success.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="❌ Anuluj", command=haslo_window.destroy).pack(side="left")
        
        # Zaplanuj następną aktualizację za 2 sekundy
        self.root.after(2000, self.update_size_info)
    
    def usun_rachunek_z_menu(self):
        """Usuwa rachunek wybrany z menu kontekstowego"""
        if not self.weryfikuj_administratora():
            return
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uwaga", "Wybierz rachunek do usunięcia.")
            return
        
        item = self.tree.item(selection[0])
        rachunek_id = item['values'][0]
        numer = item['values'][1]
        
        # Okno z powodem usunięcia
        powod_window = tk.Toplevel(self.root)
        powod_window.title("❌ Usuń rachunek")
        powod_window.geometry("400x200")
        powod_window.resizable(False, False)
        powod_window.transient(self.root)
        powod_window.grab_set()
        
        # Wyśrodkuj okno
        powod_window.update_idletasks()
        x = (powod_window.winfo_screenwidth() - 400) // 2
        y = (powod_window.winfo_screenheight() - 200) // 2
        powod_window.geometry(f"400x200+{x}+{y}")
        
        main_frame = ttk.Frame(powod_window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Informacja o rachunku
        ttk.Label(main_frame, text=f"Rachunek do usunięcia: {numer}", 
                 font=('Segoe UI', 10, 'bold')).pack(pady=(0, 10))
        
        # Powód
        ttk.Label(main_frame, text="Powód usunięcia (opcjonalnie):").pack(anchor="w", pady=(0, 5))
        powod_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=powod_var, width=40).pack(pady=(0, 15))
        
        # Przyciski
        def potwierdz_usuniecie():
            wynik = self.manager.usun_rachunek_z_potwierdzeniem(rachunek_id, powod_var.get())
            
            if wynik['success']:
                messagebox.showinfo("Sukces", 
                                  f"Rachunek {wynik['numer_rachunku']} został usunięty.", 
                                  parent=powod_window)
                powod_window.destroy()
                # Odśwież listę rachunków
                self.load_rachunki_data()
            else:
                messagebox.showerror("Błąd", wynik['error'], parent=powod_window)
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        ttk.Button(buttons_frame, text="❌ Usuń", command=potwierdz_usuniecie,
                  style="Warning.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="🚫 Anuluj", 
                  command=powod_window.destroy).pack(side="left")
    
    def setup_keyboard_shortcuts(self):
        """Konfiguruje skróty klawiszowe"""
        # Ctrl+R - Dopasuj rozmiar okna
        self.root.bind('<Control-r>', lambda e: self.adjust_window_size())
        
        # F11 - Dopasuj rozmiar okna
        self.root.bind('<F11>', lambda e: self.adjust_window_size())
        
        # Escape - Wyczyść formularz (tylko w zakładce nowy rachunek)
        self.root.bind('<Escape>', self.handle_escape_key)
    
    def handle_escape_key(self, event):
        """Obsługuje klawisz Escape"""
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        if "Nowy Rachunek" in current_tab:
            self.wyczysc_formularz()
    
    def setup_modern_theme(self):
        """Konfiguruje nowoczesny motyw aplikacji"""
        style = ttk.Style()
        
        # Ustaw motyw
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'clam' in available_themes:
            style.theme_use('clam')
        
        # Kolory aplikacji
        colors = {
            'primary': '#2E86AB',      # Niebieski
            'secondary': '#A23B72',    # Fioletowy
            'success': '#4CAF50',      # Zielony
            'warning': '#FF9800',      # Pomarańczowy
            'danger': '#F44336',       # Czerwony
            'light': '#F8F9FA',        # Jasny szary
            'dark': '#343A40',         # Ciemny szary
            'background': '#FFFFFF'    # Biały
        }
        
        # Konfiguracja stylów
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground=colors['primary'])
        
        style.configure('Heading.TLabel', 
                       font=('Segoe UI', 11, 'bold'),
                       foreground=colors['dark'])
        
        style.configure('Success.TLabel', 
                       foreground=colors['success'],
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Warning.TLabel', 
                       foreground=colors['warning'],
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Danger.TLabel', 
                       foreground=colors['danger'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Przyciski
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10))
        
        # Notebook (zakładki)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        
        # Tło głównego okna
        self.root.configure(bg='#F8F9FA')
        
        # Przechowuj kolory dla późniejszego użycia
        self.colors = colors
    
    def create_notebook(self):
        """Tworzy główny notebook z zakładkami"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Zakładki
        self.tab_nowy = ttk.Frame(self.notebook)
        self.tab_lista = ttk.Frame(self.notebook)
        self.tab_ustawienia = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_nowy, text="📝 Nowy Rachunek")
        self.notebook.add(self.tab_lista, text="📋 Lista Rachunków")
        self.notebook.add(self.tab_ustawienia, text="⚙️ Ustawienia")
    
    def create_nowy_rachunek_tab(self):
        """Tworzy zakładkę nowego rachunku"""
        # Główny frame z przewijaniem
        canvas = tk.Canvas(self.tab_nowy)
        scrollbar = ttk.Scrollbar(self.tab_nowy, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Dane nabywcy
        nabywca_frame = ttk.LabelFrame(scrollable_frame, text="👤 Dane Nabywcy", padding=15)
        nabywca_frame.pack(fill="x", padx=15, pady=10)
        
        self.nabywca_vars = {}
        
        nabywca_fields = [
            ("Imię:", "imie"),
            ("Nazwisko:", "nazwisko"),
            ("Ulica:", "ulica"),
            ("Nr domu:", "nr_domu"),
            ("Kod pocztowy:", "kod_pocztowy"),
            ("Miasto:", "miasto")
        ]
        
        for i, (label, key) in enumerate(nabywca_fields):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(nabywca_frame, text=label).grid(row=row, column=col, sticky="w", padx=(0, 5))
            var = tk.StringVar()
            self.nabywca_vars[key] = var
            entry = ttk.Entry(nabywca_frame, textvariable=var, width=25)
            entry.grid(row=row, column=col+1, sticky="ew", padx=(0, 20))
        
        # Szczegóły usługi
        usluga_frame = ttk.LabelFrame(scrollable_frame, text="🔧 Szczegóły Usługi", padding=15)
        usluga_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(usluga_frame, text="Data wykonania usługi:").grid(row=0, column=0, sticky="w")
        self.data_uslugi_var = tk.StringVar(value=datetime.now().strftime("%d.%m.%Y"))
        ttk.Entry(usluga_frame, textvariable=self.data_uslugi_var, width=15).grid(row=0, column=1, sticky="w", padx=(5, 0))
        ttk.Label(usluga_frame, text="(format: DD.MM.YYYY)").grid(row=0, column=2, sticky="w", padx=(5, 0))
        
        ttk.Label(usluga_frame, text="Nazwa usługi:").grid(row=1, column=0, sticky="nw", pady=(10, 0))
        self.nazwa_uslugi_var = tk.StringVar()
        text_usluga = tk.Text(usluga_frame, height=3, width=50, wrap=tk.WORD)
        text_usluga.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(5, 0), pady=(10, 0))
        self.text_usluga = text_usluga
        
        ttk.Label(usluga_frame, text="Cena (PLN):").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.cena_var = tk.StringVar()
        ttk.Entry(usluga_frame, textvariable=self.cena_var, width=15).grid(row=2, column=1, sticky="w", padx=(5, 0), pady=(10, 0))
        ttk.Label(usluga_frame, text="(np. 100.50)").grid(row=2, column=2, sticky="w", padx=(5, 0), pady=(10, 0))
        
        usluga_frame.columnconfigure(1, weight=1)
        
        # Podsumowanie miesięczne
        self.create_monthly_summary_frame(scrollable_frame)
        
        # Przyciski
        buttons_frame = ttk.Frame(scrollable_frame)
        buttons_frame.pack(fill="x", padx=15, pady=20)
        
        # Główny przycisk generowania
        generate_btn = ttk.Button(buttons_frame, text="✅ Generuj Rachunek", 
                                 command=self.generuj_rachunek, style="Primary.TButton")
        generate_btn.pack(side="left", padx=(0, 15))
        
        # Przycisk czyszczenia
        clear_btn = ttk.Button(buttons_frame, text="🧹 Wyczyść Formularz", 
                              command=self.wyczysc_formularz)
        clear_btn.pack(side="left")
        
        # Pakowanie canvas i scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_lista_rachunkow_tab(self):
        """Tworzy zakładkę z listą rachunków"""
        # Główny kontener - PanedWindow dla podziału na listę i raporty
        main_paned = ttk.PanedWindow(self.tab_lista, orient=tk.HORIZONTAL)
        main_paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Lewa strona - Lista rachunków
        lista_frame = ttk.Frame(main_paned)
        main_paned.add(lista_frame, weight=2)
        
        # Frame wyszukiwania
        search_frame = ttk.Frame(lista_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Wyszukaj:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=(5, 10))
        search_entry.bind('<KeyRelease>', self.on_search_change)
        
        ttk.Button(search_frame, text="🔍 Wyszukaj", 
                  command=self.wyszukaj_rachunki).pack(side="left", padx=(0, 10))
        ttk.Button(search_frame, text="📄 Pokaż wszystkie", 
                  command=self.pokaz_wszystkie_rachunki).pack(side="left", padx=(0, 10))
        ttk.Button(search_frame, text="💾 Eksportuj CSV", 
                  command=self.eksportuj_csv).pack(side="left")
        
        # Tabela rachunków
        columns = ("ID", "Numer", "Data", "Nabywca", "Kwota (PLN)")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=15)
        
        # Nagłówki kolumn
        self.tree.heading("ID", text="ID")
        self.tree.heading("Numer", text="Numer rachunku")
        self.tree.heading("Data", text="Data wystawienia")
        self.tree.heading("Nabywca", text="Nabywca")
        self.tree.heading("Kwota (PLN)", text="Kwota (PLN)")
        
        # Szerokość kolumn
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Numer", width=120, anchor="center")
        self.tree.column("Data", width=100, anchor="center")
        self.tree.column("Nabywca", width=150)
        self.tree.column("Kwota (PLN)", width=80, anchor="e")
        
        # Scrollbar dla tabeli
        tree_scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Pakowanie tabeli
        tree_container = ttk.Frame(lista_frame)
        tree_container.pack(fill="both", expand=True)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")
        
        # Podwójne kliknięcie otwiera PDF
        self.tree.bind('<Double-1>', self.otworz_pdf_rachunek)
        
        # Menu kontekstowe
        self.create_context_menu()
        
        # Prawa strona - Sekcja raportów
        raporty_frame = ttk.LabelFrame(main_paned, text="📊 Raporty i Statystyki", padding=15)
        main_paned.add(raporty_frame, weight=1)
        
        # Notebook dla różnych typów raportów
        self.raporty_notebook = ttk.Notebook(raporty_frame)
        self.raporty_notebook.pack(fill="both", expand=True)
        
        # Zakładka - Podsumowanie miesięczne
        self.miesiac_frame = ttk.Frame(self.raporty_notebook)
        self.raporty_notebook.add(self.miesiac_frame, text="📅 Miesięczne")
        
        # Zakładka - Podsumowanie roczne
        self.rok_frame = ttk.Frame(self.raporty_notebook)
        self.raporty_notebook.add(self.rok_frame, text="📈 Roczne")
        
        # Zakładka - Top klienci
        self.klienci_frame = ttk.Frame(self.raporty_notebook)
        self.raporty_notebook.add(self.klienci_frame, text="👥 Klienci")
        
        # Utwórz zawartość zakładek raportów
        self.create_miesiac_raport()
        self.create_rok_raport()
        self.create_klienci_raport()
        
        # Załaduj dane
        self.load_rachunki_data()
    
    def create_miesiac_raport(self):
        """Tworzy zawartość raportu miesięcznego"""
        # Wybór roku i miesiąca
        wybor_frame = ttk.Frame(self.miesiac_frame)
        wybor_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(wybor_frame, text="Rok:").pack(side="left")
        self.miesiac_rok_var = tk.StringVar(value=str(datetime.now().year))
        rok_combo = ttk.Combobox(wybor_frame, textvariable=self.miesiac_rok_var, 
                                width=8, state="readonly")
        rok_combo['values'] = [str(y) for y in range(2020, datetime.now().year + 2)]
        rok_combo.pack(side="left", padx=(5, 15))
        
        ttk.Button(wybor_frame, text="📊 Generuj", 
                  command=self.generuj_raport_miesięczny).pack(side="left")
        ttk.Button(wybor_frame, text="🔄 Odśwież", 
                  command=self.odswież_raport_miesięczny).pack(side="left", padx=(5, 0))
        
        # Wyniki raportu
        self.miesiac_text = tk.Text(self.miesiac_frame, height=15, wrap=tk.WORD, 
                                   state="disabled", font=('Segoe UI', 9))
        
        # Scrollbar dla tekstu
        miesiac_scroll = ttk.Scrollbar(self.miesiac_frame, orient="vertical", 
                                      command=self.miesiac_text.yview)
        self.miesiac_text.configure(yscrollcommand=miesiac_scroll.set)
        
        # Pakowanie
        text_frame = ttk.Frame(self.miesiac_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.miesiac_text.pack(side="left", fill="both", expand=True)
        miesiac_scroll.pack(side="right", fill="y")
        
        # Wczytaj domyślny raport
        self.generuj_raport_miesięczny()
    
    def create_rok_raport(self):
        """Tworzy zawartość raportu rocznego"""
        # Przycisk generowania
        button_frame = ttk.Frame(self.rok_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(button_frame, text="📈 Generuj Raport Roczny", 
                  command=self.generuj_raport_roczny).pack(side="left")
        ttk.Button(button_frame, text="🔄 Odśwież", 
                  command=self.odswież_raport_roczny).pack(side="left", padx=(10, 0))
        
        # Wyniki raportu
        self.rok_text = tk.Text(self.rok_frame, height=15, wrap=tk.WORD,
                               state="disabled", font=('Segoe UI', 9))
        
        # Scrollbar dla tekstu
        rok_scroll = ttk.Scrollbar(self.rok_frame, orient="vertical",
                                  command=self.rok_text.yview)
        self.rok_text.configure(yscrollcommand=rok_scroll.set)
        
        # Pakowanie
        text_frame = ttk.Frame(self.rok_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.rok_text.pack(side="left", fill="both", expand=True)
        rok_scroll.pack(side="right", fill="y")
        
        # Wczytaj domyślny raport
        self.generuj_raport_roczny()
    
    def create_klienci_raport(self):
        """Tworzy zawartość raportu klientów"""
        # Wybór liczby klientów
        wybor_frame = ttk.Frame(self.klienci_frame)
        wybor_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(wybor_frame, text="Top:").pack(side="left")
        self.top_limit_var = tk.StringVar(value="10")
        limit_combo = ttk.Combobox(wybor_frame, textvariable=self.top_limit_var,
                                  width=5, state="readonly")
        limit_combo['values'] = ['5', '10', '15', '20', '25']
        limit_combo.pack(side="left", padx=(5, 10))
        
        ttk.Label(wybor_frame, text="klientów").pack(side="left")
        
        ttk.Button(wybor_frame, text="👥 Generuj", 
                  command=self.generuj_raport_klientów).pack(side="left", padx=(15, 0))
        ttk.Button(wybor_frame, text="🔄 Odśwież", 
                  command=self.odswież_raport_klientów).pack(side="left", padx=(5, 0))
        
        # Wyniki raportu
        self.klienci_text = tk.Text(self.klienci_frame, height=15, wrap=tk.WORD,
                                   state="disabled", font=('Segoe UI', 9))
        
        # Scrollbar dla tekstu
        klienci_scroll = ttk.Scrollbar(self.klienci_frame, orient="vertical",
                                      command=self.klienci_text.yview)
        self.klienci_text.configure(yscrollcommand=klienci_scroll.set)
        
        # Pakowanie
        text_frame = ttk.Frame(self.klienci_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.klienci_text.pack(side="left", fill="both", expand=True)
        klienci_scroll.pack(side="right", fill="y")
        
        # Wczytaj domyślny raport
        self.generuj_raport_klientów()
    
    def create_context_menu(self):
        """Tworzy menu kontekstowe dla tabeli rachunków"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Otwórz PDF", command=self.otworz_pdf_rachunek)
        self.context_menu.add_command(label="Regeneruj PDF", command=self.regeneruj_pdf)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Pokaż szczegóły", command=self.pokaz_szczegoly)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="❌ Usuń rachunek (Administrator)", 
                                     command=self.usun_rachunek_z_menu, foreground="red")
        
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Pokazuje menu kontekstowe"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def create_ustawienia_tab(self):
        """Tworzy zakładkę ustawień"""
        # Utwórz canvas i scrollbar dla przewijania
        canvas = tk.Canvas(self.tab_ustawienia, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_ustawienia, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Konfiguruj scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Obsługa scroll kółkiem myszy
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Pakowanie canvas i scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Teraz używaj scrollable_frame zamiast self.tab_ustawienia
        # Dane sprzedawcy
        sprzedawca_frame = ttk.LabelFrame(scrollable_frame, text="🏢 Domyślne dane sprzedawcy", padding=15)
        sprzedawca_frame.pack(fill="x", padx=15, pady=15)
        
        self.sprzedawca_vars = {}
        sprzedawca_fields = [
            ("Imię:", "imie"),
            ("Nazwisko:", "nazwisko"),
            ("Ulica:", "ulica"),
            ("Nr domu:", "nr_domu"),
            ("Kod pocztowy:", "kod_pocztowy"),
            ("Miasto:", "miasto")
        ]
        
        for i, (label, key) in enumerate(sprzedawca_fields):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(sprzedawca_frame, text=label).grid(row=row, column=col, sticky="w", padx=(0, 5), pady=2)
            var = tk.StringVar()
            self.sprzedawca_vars[key] = var
            entry = ttk.Entry(sprzedawca_frame, textvariable=var, width=25)
            entry.grid(row=row, column=col+1, sticky="ew", padx=(0, 20), pady=2)
        
        sprzedawca_frame.columnconfigure(1, weight=1)
        sprzedawca_frame.columnconfigure(3, weight=1)
        
        # Przycisk zapisz
        save_btn = ttk.Button(sprzedawca_frame, text="💾 Zapisz dane sprzedawcy", 
                             command=self.zapisz_dane_sprzedawcy, style="Success.TButton")
        save_btn.grid(row=3, column=0, columnspan=4, pady=15)
        
        # Informacje o aplikacji
        info_frame = ttk.LabelFrame(scrollable_frame, text="ℹ️ Informacje o aplikacji", padding=15)
        info_frame.pack(fill="x", padx=15, pady=15)
        
        build_info = get_build_info()
        info_text = f"""System do wystawiania uproszczonych rachunków

✨ Funkcjonalności:
• Tworzenie rachunków z automatyczną numeracją
• Generowanie plików PDF z polskimi znakami
• Ewidencja wszystkich rachunków w bazie danych
• System limitów miesięcznych (3499,50 PLN dla 2025)
• Wyszukiwanie i filtrowanie rachunków
• Eksport do pliku CSV
• Podsumowanie miesięczne z wizualizacją
• Nowoczesny interfejs graficzny

📦 Informacje techniczne:
• Wersja: {build_info['version']}
• Data wydania: {build_info['release_date']}
• Build: {build_info['build']}"""
        
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Przycisk "O aplikacji"
        about_btn = ttk.Button(info_frame, text="📋 Pokaż pełne informacje o wersji", 
                              command=self.show_about_dialog)
        about_btn.pack(pady=10)
        
        # Ustawienia okna
        window_frame = ttk.LabelFrame(scrollable_frame, text="🪟 Ustawienia okna", padding=15)
        window_frame.pack(fill="x", padx=15, pady=15)
        
        # Przycisk dopasowania rozmiaru
        adjust_btn = ttk.Button(window_frame, text="📏 Dopasuj rozmiar okna do zawartości", 
                               command=self.adjust_window_size)
        adjust_btn.pack(pady=10)
        
        # Informacja o aktualnym rozmiarze
        self.size_info_var = tk.StringVar(value="Aktualizowanie...")
        ttk.Label(window_frame, text="Aktualny rozmiar okna:").pack(anchor="w")
        ttk.Label(window_frame, textvariable=self.size_info_var, 
                 font=('Segoe UI', 9)).pack(anchor="w", padx=(20, 0))
        
        # Aktualizuj informację o rozmiarze
        self.update_size_info()
        
        # Skróty klawiszowe
        shortcuts_frame = ttk.LabelFrame(scrollable_frame, text="⌨️ Skróty klawiszowe", padding=15)
        shortcuts_frame.pack(fill="x", padx=15, pady=15)
        
        shortcuts_text = """• Ctrl+R lub F11 - Dopasuj rozmiar okna do zawartości
• Escape - Wyczyść formularz (w zakładce Nowy Rachunek)"""
        
        ttk.Label(shortcuts_frame, text=shortcuts_text, justify="left").pack(anchor="w")
        
        # Zarządzanie rachunkami (sekcja administratora)
        admin_frame = ttk.LabelFrame(scrollable_frame, text="🔐 Zarządzanie rachunkami (Administrator)", padding=15)
        admin_frame.pack(fill="x", padx=15, pady=15)
        
        admin_info = ttk.Label(admin_frame, 
                              text="⚠️ Ta sekcja wymaga uwierzytelnienia administratora.\nFunkcje usuwania i przywracania rachunków.", 
                              justify="left", foreground="orange")
        admin_info.pack(anchor="w", pady=(0, 10))
        
        admin_buttons_frame = ttk.Frame(admin_frame)
        admin_buttons_frame.pack(fill="x")
        
        # Przycisk zarządzania usuniętymi rachunkami
        ttk.Button(admin_buttons_frame, text="🗑️ Zarządzaj usuniętymi rachunkami", 
                  command=self.otworz_zarzadzanie_usuniete).pack(side="left", padx=(0, 10))
        
        # Przycisk usuwania rachunku
        ttk.Button(admin_buttons_frame, text="❌ Usuń rachunek", 
                  command=self.otworz_usuwanie_rachunku, style="Warning.TButton").pack(side="left", padx=(0, 10))
        
        # Przycisk zmiany hasła
        ttk.Button(admin_buttons_frame, text="🔑 Zmień hasło administratora", 
                  command=self.otworz_zmiana_hasla).pack(side="left")
    
    def load_default_sprzedawca_data(self):
        """Ładuje domyślne dane sprzedawcy"""
        dane = self.manager.pobierz_domyslnego_sprzedawce()
        if dane:
            for key, var in self.sprzedawca_vars.items():
                var.set(dane.get(key, ""))
    
    def zapisz_dane_sprzedawcy(self):
        """Zapisuje dane sprzedawcy"""
        dane = {key: var.get() for key, var in self.sprzedawca_vars.items()}
        
        bledy = self.manager.zapisz_domyslnego_sprzedawce(dane)
        
        if bledy:
            messagebox.showerror("Błąd walidacji", "\n".join(bledy))
        else:
            messagebox.showinfo("Sukces", "Dane sprzedawcy zostały zapisane")
    
    def generuj_rachunek(self):
        """Generuje nowy rachunek"""
        try:
            # Pobierz dane nabywcy
            nabywca_data = {key: var.get() for key, var in self.nabywca_vars.items()}
            
            # Pobierz dane sprzedawcy
            sprzedawca_data = self.manager.pobierz_domyslnego_sprzedawce()
            if not sprzedawca_data:
                messagebox.showerror("Błąd", "Brak danych sprzedawcy. Uzupełnij dane w zakładce Ustawienia.")
                return
            
            # Pobierz szczegóły usługi
            nazwa_uslugi = self.text_usluga.get("1.0", "end-1c").strip()
            
            dane_rachunku = {
                'sprzedawca': sprzedawca_data,
                'nabywca': nabywca_data,
                'data_wykonania_uslugi': self.data_uslugi_var.get(),
                'nazwa_uslugi': nazwa_uslugi,
                'cena_jednostkowa': self.cena_var.get()
            }
            
            # Wybierz folder docelowy
            folder = filedialog.askdirectory(title="Wybierz folder do zapisania PDF")
            if not folder:
                return
            
            # Generuj rachunek
            wynik = self.manager.stworz_rachunek(dane_rachunku, folder)
            
            if wynik['success']:
                success_msg = f"Rachunek został wygenerowany!\nPlik PDF: {wynik['pdf_path']}"
                
                # Dodaj ostrzeżenia jeśli są
                if 'warnings' in wynik and wynik['warnings']:
                    success_msg += "\n\nOSTRZEŻENIA:\n" + "\n".join(wynik['warnings'])
                
                messagebox.showinfo("Sukces", success_msg)
                
                # Wyczyść formularz
                self.wyczysc_formularz()
                
                # Odśwież listę rachunków
                self.load_rachunki_data()
                
                # Odśwież podsumowanie miesięczne
                self.update_monthly_summary()
                
                # Zapytaj czy otworzyć PDF
                if messagebox.askyesno("Otwórz plik", "Czy chcesz otworzyć wygenerowany plik PDF?"):
                    self.manager.otworz_plik_pdf(wynik['pdf_path'])
                    
            else:
                messagebox.showerror("Błąd", "\n".join(wynik['errors']))
                
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {str(e)}")
    
    def wyczysc_formularz(self):
        """Czyści formularz nowego rachunku"""
        for var in self.nabywca_vars.values():
            var.set("")
        
        self.data_uslugi_var.set(datetime.now().strftime("%d.%m.%Y"))
        self.text_usluga.delete("1.0", "end")
        self.cena_var.set("")
        
        # Odśwież podsumowanie miesięczne
        self.update_monthly_summary()
    
    def load_rachunki_data(self):
        """Ładuje dane rachunków do tabeli"""
        # Wyczyść tabelę
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Pobierz rachunki
        rachunki = self.manager.pobierz_liste_rachunkow()
        
        # Dodaj do tabeli
        for rachunek in rachunki:
            self.tree.insert("", "end", values=(
                rachunek['id'],
                rachunek['numer_rachunku'],
                rachunek['data_wystawienia'],
                rachunek['nabywca'],
                f"{rachunek['kwota']:.2f}"
            ))
    
    def wyszukaj_rachunki(self):
        """Wyszukuje rachunki według zapytania"""
        query = self.search_var.get().strip()
        
        # Wyczyść tabelę
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Wyszukaj
        rachunki = self.manager.wyszukaj_rachunki(query)
        
        # Dodaj do tabeli
        for rachunek in rachunki:
            self.tree.insert("", "end", values=(
                rachunek['id'],
                rachunek['numer_rachunku'],
                rachunek['data_wystawienia'],
                rachunek['nabywca'],
                f"{rachunek['kwota']:.2f}"
            ))
    
    def on_search_change(self, event):
        """Wywoływane przy zmianie tekstu wyszukiwania"""
        # Wyszukaj po 500ms od ostatniego naciśnięcia klawisza
        if hasattr(self, 'search_job'):
            self.root.after_cancel(self.search_job)
        self.search_job = self.root.after(500, self.wyszukaj_rachunki)
    
    def pokaz_wszystkie_rachunki(self):
        """Pokazuje wszystkie rachunki"""
        self.search_var.set("")
        self.load_rachunki_data()
    
    def otworz_pdf_rachunek(self, event=None):
        """Otwiera PDF rachunku"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        rachunek_id = item['values'][0]
        
        # Sprawdź czy plik istnieje
        sciezka_pdf = self.manager.sprawdz_czy_plik_pdf_istnieje(rachunek_id)
        
        if sciezka_pdf:
            if self.manager.otworz_plik_pdf(sciezka_pdf):
                pass  # Plik został otwarty
            else:
                messagebox.showerror("Błąd", "Nie można otworzyć pliku PDF")
        else:
            # Zaproponuj regenerację
            if messagebox.askyesno("Plik nie istnieje", 
                                 "Plik PDF nie istnieje. Czy chcesz go wygenerować ponownie?"):
                self.regeneruj_pdf()
    
    def regeneruj_pdf(self):
        """Regeneruje PDF dla wybranego rachunku"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Brak wyboru", "Wybierz rachunek z listy")
            return
        
        item = self.tree.item(selection[0])
        rachunek_id = item['values'][0]
        
        # Wybierz folder
        folder = filedialog.askdirectory(title="Wybierz folder do zapisania PDF")
        if not folder:
            return
        
        # Regeneruj PDF
        wynik = self.manager.regeneruj_pdf_rachunku(rachunek_id, folder)
        
        if wynik['success']:
            messagebox.showinfo("Sukces", f"PDF został wygenerowany: {wynik['pdf_path']}")
            
            if messagebox.askyesno("Otwórz plik", "Czy chcesz otworzyć wygenerowany plik PDF?"):
                self.manager.otworz_plik_pdf(wynik['pdf_path'])
        else:
            messagebox.showerror("Błąd", wynik['error'])
    
    def pokaz_szczegoly(self):
        """Pokazuje szczegóły wybranego rachunku"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Brak wyboru", "Wybierz rachunek z listy")
            return
        
        item = self.tree.item(selection[0])
        rachunek_id = item['values'][0]
        
        szczegoly = self.manager.pobierz_szczegoly_rachunku(rachunek_id)
        
        if szczegoly:
            # Okno ze szczegółami
            szczegoly_window = tk.Toplevel(self.root)
            szczegoly_window.title(f"Szczegóły rachunku {szczegoly['numer_rachunku']}")
            szczegoly_window.geometry("600x500")
            
            # Tekst ze szczegółami
            text_widget = tk.Text(szczegoly_window, wrap=tk.WORD, padx=10, pady=10)
            
            szczegoly_text = f"""SZCZEGÓŁY RACHUNKU {szczegoly['numer_rachunku']}

Data wystawienia: {szczegoly['data_wystawienia']}
Data wykonania usługi: {szczegoly['data_wykonania_uslugi']}

SPRZEDAWCA:
{szczegoly['sprzedawca_imie']} {szczegoly['sprzedawca_nazwisko']}
{szczegoly['sprzedawca_ulica']} {szczegoly['sprzedawca_nr_domu']}
{szczegoly['sprzedawca_kod_pocztowy']} {szczegoly['sprzedawca_miasto']}

NABYWCA:
{szczegoly['nabywca_imie']} {szczegoly['nabywca_nazwisko']}
{szczegoly['nabywca_ulica']} {szczegoly['nabywca_nr_domu']}
{szczegoly['nabywca_kod_pocztowy']} {szczegoly['nabywca_miasto']}

USŁUGA:
{szczegoly['nazwa_uslugi']}

CENA: {szczegoly['cena_jednostkowa']:.2f} PLN
DO ZAPŁATY: {szczegoly['kwota_do_zaplaty']:.2f} PLN
SŁOWNIE: {szczegoly['kwota_slownie']}

Plik PDF: {szczegoly.get('plik_pdf', 'Brak')}"""
            
            text_widget.insert("1.0", szczegoly_text)
            text_widget.config(state="disabled")
            text_widget.pack(fill="both", expand=True)
            
            # Przycisk zamknij
            ttk.Button(szczegoly_window, text="Zamknij", 
                      command=szczegoly_window.destroy).pack(pady=10)
    
    def eksportuj_csv(self):
        """Eksportuje rachunki do pliku CSV"""
        sciezka = filedialog.asksaveasfilename(
            title="Zapisz jako CSV",
            defaultextension=".csv",
            filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
        )
        
        if sciezka:
            wynik = self.manager.eksportuj_rachunki_csv(sciezka)
            
            if wynik['success']:
                messagebox.showinfo("Sukces", f"Rachunki zostały wyeksportowane do: {sciezka}")
            else:
                messagebox.showerror("Błąd", wynik['error'])
    
    def generuj_raport_miesięczny(self):
        """Generuje raport miesięczny"""
        try:
            rok = int(self.miesiac_rok_var.get())
            raport = self.manager.pobierz_raport_miesięczny(rok)
            
            # Formatuj raport
            tekst = f"🗓️ RAPORT MIESIĘCZNY - {rok}\n"
            tekst += "=" * 50 + "\n\n"
            
            if not raport['miesiace']:
                tekst += "❌ Brak danych dla tego roku.\n"
            else:
                for miesiac in raport['miesiace']:
                    status_emoji = {
                        'PRZEKROCZONY': '🔴',
                        'OSTRZEŻENIE': '🟠', 
                        'NORMALNY': '🟡',
                        'BEZPIECZNY': '🟢'
                    }.get(miesiac['status'], '⚪')
                    
                    tekst += f"{status_emoji} {miesiac['miesiac_nazwa']} {rok}\n"
                    tekst += f"   💰 Przychody: {miesiac['suma_kwot']:.2f} PLN\n"
                    tekst += f"   📊 Rachunków: {miesiac['liczba_rachunkow']}\n"
                    tekst += f"   📈 Średnia: {miesiac['srednia_kwota']:.2f} PLN\n"
                    tekst += f"   🎯 Limit: {miesiac['limit_miesięczny']:.2f} PLN\n"
                    tekst += f"   ⚡ Pozostało: {miesiac['pozostaly_limit']:.2f} PLN\n"
                    tekst += f"   📍 Status: {miesiac['status']} ({miesiac['procent_wykorzystania']:.1f}%)\n\n"
                
                # Podsumowanie roczne
                podsumowanie = raport['podsumowanie_roczne']
                tekst += "📈 PODSUMOWANIE ROCZNE\n"
                tekst += "-" * 30 + "\n"
                tekst += f"📊 Łączna liczba rachunków: {podsumowanie['total_rachunki']}\n"
                tekst += f"💰 Łączne przychody: {podsumowanie['total_kwoty']:.2f} PLN\n"
                tekst += f"📅 Aktywnych miesięcy: {podsumowanie['miesiace_aktywne']}/12\n"
                tekst += f"🔴 Miesięcy z przekroczonym limitem: {podsumowanie['miesiace_przekroczone']}\n"
                tekst += f"📊 Średnia miesięczna: {podsumowanie['srednia_miesieczna']:.2f} PLN\n"
                
                if podsumowanie['max_miesiac']:
                    tekst += f"🏆 Najlepszy miesiąc: {podsumowanie['max_miesiac']['miesiac_nazwa']} ({podsumowanie['max_miesiac']['suma_kwot']:.2f} PLN)\n"
                if podsumowanie['min_miesiac']:
                    tekst += f"📉 Najsłabszy miesiąc: {podsumowanie['min_miesiac']['miesiac_nazwa']} ({podsumowanie['min_miesiac']['suma_kwot']:.2f} PLN)\n"
            
            # Wyświetl w widget tekstowym
            self.miesiac_text.config(state="normal")
            self.miesiac_text.delete("1.0", tk.END)
            self.miesiac_text.insert("1.0", tekst)
            self.miesiac_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas generowania raportu: {str(e)}")
    
    def generuj_raport_roczny(self):
        """Generuje raport roczny"""
        try:
            raport = self.manager.pobierz_raport_roczny()
            
            # Formatuj raport
            tekst = "📅 RAPORT ROCZNY - WSZYSTKIE LATA\n"
            tekst += "=" * 50 + "\n\n"
            
            if not raport['lata']:
                tekst += "❌ Brak danych w bazie.\n"
            else:
                tekst += "📊 PRZYCHODY WG LAT\n"
                tekst += "-" * 25 + "\n"
                for rok in raport['lata']:
                    tekst += f"📅 Rok {rok['rok']}\n"
                    tekst += f"   💰 Przychody: {rok['suma_kwot']:.2f} PLN\n"
                    tekst += f"   📊 Rachunków: {rok['liczba_rachunkow']}\n"
                    tekst += f"   📈 Średnia: {rok['srednia_kwota']:.2f} PLN\n"
                    tekst += f"   📉 Min: {rok['min_kwota']:.2f} PLN | 📈 Max: {rok['max_kwota']:.2f} PLN\n\n"
                
                # Statystyki ogólne
                stats = raport['statystyki_ogolne']
                tekst += "📈 STATYSTYKI OGÓLNE\n"
                tekst += "-" * 20 + "\n"
                tekst += f"📊 Łączna liczba rachunków: {stats['total_rachunki']}\n"
                tekst += f"💰 Łączne przychody: {stats['total_kwota']:.2f} PLN\n"
                tekst += f"📊 Średnia wartość rachunku: {stats['srednia_kwota']:.2f} PLN\n"
                tekst += f"👥 Unikalnych klientów: {stats['unikalni_klienci']}\n"
                if stats['pierwszy_rachunek']:
                    tekst += f"📅 Pierwszy rachunek: {stats['pierwszy_rachunek']}\n"
                if stats['ostatni_rachunek']:
                    tekst += f"📅 Ostatni rachunek: {stats['ostatni_rachunek']}\n"
            
            # Wyświetl w widget tekstowym
            self.rok_text.config(state="normal")
            self.rok_text.delete("1.0", tk.END)
            self.rok_text.insert("1.0", tekst)
            self.rok_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas generowania raportu: {str(e)}")
    
    def generuj_raport_klientów(self):
        """Generuje raport top klientów"""
        try:
            limit = int(self.top_limit_var.get())
            klienci = self.manager.pobierz_raport_top_klientow(limit)
            
            # Formatuj raport
            tekst = f"👥 TOP {limit} KLIENTÓW\n"
            tekst += "=" * 40 + "\n\n"
            
            if not klienci:
                tekst += "❌ Brak danych o klientach.\n"
            else:
                for i, klient in enumerate(klienci, 1):
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
                    tekst += f"{medal} {klient['klient']}\n"
                    tekst += f"    💰 Łączne kwoty: {klient['suma_kwot']:.2f} PLN\n"
                    tekst += f"    📊 Rachunków: {klient['liczba_rachunkow']}\n"
                    tekst += f"    📈 Średnia: {klient['srednia_kwota']:.2f} PLN\n"
                    tekst += f"    📅 Ostatni rachunek: {klient['ostatni_rachunek']}\n\n"
            
            # Wyświetl w widget tekstowym
            self.klienci_text.config(state="normal")
            self.klienci_text.delete("1.0", tk.END)
            self.klienci_text.insert("1.0", tekst)
            self.klienci_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas generowania raportu: {str(e)}")
    
    def odswież_raport_miesięczny(self):
        """Odświeża raport miesięczny"""
        self.generuj_raport_miesięczny()
    
    def odswież_raport_roczny(self):
        """Odświeża raport roczny"""
        self.generuj_raport_roczny()
    
    def odswież_raport_klientów(self):
        """Odświeża raport klientów"""
        self.generuj_raport_klientów()
    
    def create_monthly_summary_frame(self, parent):
        """Tworzy ramkę z podsumowaniem miesięcznym"""
        summary_frame = ttk.LabelFrame(parent, text="📊 Podsumowanie Miesięczne", padding=15)
        summary_frame.pack(fill="x", padx=15, pady=10)
        
        # Przychody w bieżącym miesiącu
        self.monthly_summary_vars['przychody'] = tk.StringVar(value="Ładowanie...")
        ttk.Label(summary_frame, text="💰 Przychody w tym miesiącu:", 
                 style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(summary_frame, textvariable=self.monthly_summary_vars['przychody'],
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, sticky="w", padx=(15, 0), pady=5)
        
        # Limit miesięczny
        self.monthly_summary_vars['limit'] = tk.StringVar(value="3499.50 PLN")
        ttk.Label(summary_frame, text="🎯 Limit miesięczny:", 
                 style="Heading.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(summary_frame, textvariable=self.monthly_summary_vars['limit'],
                 font=('Segoe UI', 10, 'bold')).grid(row=1, column=1, sticky="w", padx=(15, 0), pady=5)
        
        # Pozostały limit
        self.monthly_summary_vars['pozostaly'] = tk.StringVar(value="Ładowanie...")
        ttk.Label(summary_frame, text="⚡ Pozostały limit:", 
                 style="Heading.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.pozostaly_label = ttk.Label(summary_frame, textvariable=self.monthly_summary_vars['pozostaly'],
                                        font=('Segoe UI', 10, 'bold'))
        self.pozostaly_label.grid(row=2, column=1, sticky="w", padx=(15, 0), pady=5)
        
        # Status
        self.monthly_summary_vars['status'] = tk.StringVar(value="Ładowanie...")
        ttk.Label(summary_frame, text="📈 Status:", 
                 style="Heading.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.status_label = ttk.Label(summary_frame, textvariable=self.monthly_summary_vars['status'],
                                     font=('Segoe UI', 10, 'bold'))
        self.status_label.grid(row=3, column=1, sticky="w", padx=(15, 0), pady=5)
        
        # Pasek postępu
        ttk.Label(summary_frame, text="📊 Wykorzystanie limitu:", 
                 style="Heading.TLabel").grid(row=4, column=0, sticky="w", pady=(10, 5))
        
        progress_frame = ttk.Frame(summary_frame)
        progress_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400, mode='determinate')
        self.progress_bar.pack(fill="x")
        
        summary_frame.columnconfigure(1, weight=1)
        
        # Załaduj dane
        self.update_monthly_summary()
    
    def update_monthly_summary(self):
        """Aktualizuje podsumowanie miesięczne"""
        try:
            podsumowanie = self.manager.pobierz_podsumowanie_miesięczne()
            
            # Zaktualizuj etykiety
            self.monthly_summary_vars['przychody'].set(f"{podsumowanie['przychody_suma']:.2f} PLN")
            self.monthly_summary_vars['limit'].set(f"{podsumowanie['limit_miesięczny']:.2f} PLN")
            self.monthly_summary_vars['pozostaly'].set(f"{podsumowanie['pozostaly_limit']:.2f} PLN")
            self.monthly_summary_vars['status'].set(f"{podsumowanie['status']} ({podsumowanie['procent_wykorzystania']:.1f}%)")
            
            # Ustaw kolor statusu
            if podsumowanie['status_kolor'] == 'red':
                self.status_label.config(foreground='red')
                self.pozostaly_label.config(foreground='red')
            elif podsumowanie['status_kolor'] == 'orange':
                self.status_label.config(foreground='orange')
                self.pozostaly_label.config(foreground='orange')
            elif podsumowanie['status_kolor'] == 'yellow':
                self.status_label.config(foreground='#DAA520')  # Ciemny złoty
                self.pozostaly_label.config(foreground='black')
            else:
                self.status_label.config(foreground='green')
                self.pozostaly_label.config(foreground='green')
            
            # Ustaw pasek postępu
            self.progress_var.set(podsumowanie['procent_wykorzystania'])
            
            # Ustaw kolor paska postępu
            style = ttk.Style()
            if podsumowanie['status_kolor'] == 'red':
                style.configure("TProgressbar", background='red')
            elif podsumowanie['status_kolor'] == 'orange':
                style.configure("TProgressbar", background='orange')
            elif podsumowanie['status_kolor'] == 'yellow':
                style.configure("TProgressbar", background='#DAA520')
            else:
                style.configure("TProgressbar", background='green')
                
        except Exception as e:
            self.monthly_summary_vars['przychody'].set("Błąd ładowania")
            self.monthly_summary_vars['pozostaly'].set("Błąd ładowania")
            self.monthly_summary_vars['status'].set("Błąd ładowania")
            print(f"Błąd aktualizacji podsumowania: {e}")
    
    def show_about_dialog(self):
        """Pokazuje okno dialogowe z pełnymi informacjami o wersji"""
        about_window = tk.Toplevel(self.root)
        about_window.title(f"O aplikacji - {config.APP_TITLE}")
        about_window.geometry("600x700")
        about_window.resizable(False, False)
        
        # Wyśrodkuj okno
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Główna ramka z przewijaniem
        canvas = tk.Canvas(about_window)
        scrollbar = ttk.Scrollbar(about_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Treść okna
        main_frame = ttk.Frame(scrollable_frame, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Tytuł
        title_label = ttk.Label(main_frame, text=f"💼 {config.APP_TITLE}", 
                               style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        # Aktualna wersja
        build_info = get_build_info()
        version_text = f"""🔖 Wersja: {build_info['version']}
📅 Data wydania: {build_info['release_date']}
🔧 Build: {build_info['build']}
⏰ Utworzono: {build_info['build_date']}"""
        
        version_frame = ttk.LabelFrame(main_frame, text="Aktualna wersja", padding=10)
        version_frame.pack(fill="x", pady=10)
        ttk.Label(version_frame, text=version_text, justify="left").pack(anchor="w")
        
        # Historia wersji
        history_frame = ttk.LabelFrame(main_frame, text="Historia wersji", padding=10)
        history_frame.pack(fill="x", pady=10)
        
        for version_info in VERSION_HISTORY:
            version_label = ttk.Label(history_frame, 
                                    text=f"📌 Wersja {version_info['version']} ({version_info['date']})",
                                    font=('Segoe UI', 10, 'bold'))
            version_label.pack(anchor="w", pady=(10, 5))
            
            desc_label = ttk.Label(history_frame, 
                                 text=version_info['description'],
                                 font=('Segoe UI', 9, 'italic'))
            desc_label.pack(anchor="w", padx=(20, 0))
            
            changes_text = ""
            for change in version_info['changes']:
                changes_text += f"• {change}\n"
            
            changes_label = ttk.Label(history_frame, text=changes_text.strip(), 
                                    justify="left")
            changes_label.pack(anchor="w", padx=(20, 0), pady=(5, 0))
        
        # Przycisk zamknij
        close_btn = ttk.Button(main_frame, text="Zamknij", 
                              command=about_window.destroy)
        close_btn.pack(pady=20)
        
        # Pakowanie canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Wyśrodkuj okno względem głównego okna
        about_window.update_idletasks()
        x = (self.root.winfo_x() + (self.root.winfo_width() // 2)) - (about_window.winfo_width() // 2)
        y = (self.root.winfo_y() + (self.root.winfo_height() // 2)) - (about_window.winfo_height() // 2)
        about_window.geometry(f"+{x}+{y}")