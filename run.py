#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prosty plik uruchomieniowy aplikacji do rachunków
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime

# Sprawdź importy
try:
    from rachunek_manager import RachunekManager
    print("[OK] Manager rachunków załadowany")
except Exception as e:
    print(f"[BLAD] Blad importu managera: {e}")
    exit(1)

class SimpleRachunekApp:
    """Uproszczona wersja aplikacji"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("System Rachunków")
        self.root.geometry("600x400")
        
        try:
            self.manager = RachunekManager()
            print("[OK] Manager zainicjalizowany")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można zainicjalizować managera: {e}")
            return
        
        self.create_ui()
    
    def create_ui(self):
        """Tworzy podstawowy interfejs"""
        # Główna ramka
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Tytuł
        ttk.Label(main_frame, text="System Rachunków", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # Status
        status_text = "Aplikacja działa poprawnie!"
        if not hasattr(self.manager, 'manager'):
            try:
                # Test bazy danych
                self.manager.pobierz_liste_rachunkow()
                status_text += "\n[OK] Baza danych polaczona"
            except Exception as e:
                status_text += f"\n[BLAD] Problem z baza: {e}"
        
        ttk.Label(main_frame, text=status_text).pack(pady=10)
        
        # Przyciski testowe
        ttk.Button(main_frame, text="Test - Pokaż rachunki", 
                  command=self.pokaz_rachunki).pack(pady=5)
        
        ttk.Button(main_frame, text="Uruchom pełną aplikację", 
                  command=self.uruchom_pelna_app).pack(pady=5)
        
        ttk.Button(main_frame, text="Zakończ", 
                  command=self.root.quit).pack(pady=5)
    
    def pokaz_rachunki(self):
        """Pokazuje listę rachunków"""
        try:
            rachunki = self.manager.pobierz_liste_rachunkow()
            if rachunki:
                msg = f"Znaleziono {len(rachunki)} rachunków:\n\n"
                for r in rachunki[:5]:  # Pokaż pierwszych 5
                    msg += f"• {r['numer_rachunku']} - {r['nabywca']} - {r['kwota']:.2f} PLN\n"
            else:
                msg = "Brak rachunków w bazie danych"
            
            messagebox.showinfo("Lista rachunków", msg)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można pobrać rachunków: {e}")
    
    def uruchom_pelna_app(self):
        """Próbuje uruchomić pełną aplikację"""
        try:
            self.root.destroy()
            from rachunek_gui import RachunekApp
            
            new_root = tk.Tk()
            app = RachunekApp(new_root)
            new_root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Błąd", 
                f"Nie można uruchomić pełnej aplikacji:\n{str(e)}\n\nSprawdź plik rachunek_gui.py")

def main():
    print("Uruchamiam aplikacje rachunkow...")
    print("Python dziala poprawnie [OK]")
    
    root = tk.Tk()
    app = SimpleRachunekApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()