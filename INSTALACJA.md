# System Rachunków - Instrukcja Instalacji

## 🚀 Szybka instalacja

### Opcja 1: Automatyczny instalator (Windows)

1. **Uruchom instalator**:
   - Kliknij prawym na `install.bat` → "Uruchom jako administrator"
   - LUB otwórz PowerShell jako admin i wpisz: `.\install.ps1`

2. **Aplikacja uruchomi się automatycznie**

---

### Opcja 2: Instalacja ręczna

1. **Sprawdź Python**:
   ```cmd
   python --version
   ```
   Jeśli nie masz Pythona: https://www.python.org/downloads/

2. **Zainstaluj biblioteki** (opcjonalnie dla PDF):
   ```cmd
   pip install reportlab num2words
   ```
   Jeśli pip nie działa, spróbuj:
   ```cmd
   python -m pip install reportlab num2words
   ```

3. **Uruchom aplikację**:
   ```cmd
   python run.py
   ```

---

## 📱 Jak używać

### Pierwszy start:
1. Uruchomi się **wersja testowa** 
2. Kliknij "Uruchom pełną aplikację"
3. Przejdź do zakładki **"Ustawienia"**
4. Wypełnij swoje dane jako sprzedawcy
5. Kliknij **"Zapisz dane sprzedawcy"**

### Tworzenie rachunku:
1. Zakładka **"Nowy Rachunek"**
2. Wypełnij dane nabywcy
3. Podaj nazwę usługi i cenę  
4. Kliknij **"Generuj Rachunek"**
5. Wybierz folder do zapisania

### Przeglądanie:
1. Zakładka **"Lista Rachunków"**
2. Podwójne kliknięcie otwiera rachunek
3. Wyszukiwanie po numerze/nazwisku
4. Eksport do CSV

---

## ⚠️ Rozwiązywanie problemów

### "Fatal error in launcher" / pip nie działa
```cmd
# Spróbuj tych komend po kolei:
python -m pip install reportlab num2words
py -m pip install reportlab num2words
python -m ensurepip --upgrade
```

### "SyntaxError" w rachunek_gui.py
- Użyj `python run.py` zamiast `python main.py`
- Plik `run.py` to bezpieczna wersja testowa

### Brak PDF, tylko pliki .txt
- To normalne bez biblioteki `reportlab`
- Pliki `.txt` zawierają wszystkie wymagane dane
- Do drukowania skopiuj treść do Word/LibreOffice

### Aplikacja się nie uruchamia
1. Sprawdź czy masz Python 3.7+: `python --version`
2. Sprawdź czy wszystkie pliki są w folderze
3. Uruchom `python run.py` dla diagnostyki

---

## 📁 Pliki w folderze

```
rachunek2025/
├── main.py              # Główna aplikacja (pełna)
├── run.py               # Wersja testowa/diagnostyczna  
├── install.bat          # Instalator Windows (CMD)
├── install.ps1          # Instalator Windows (PowerShell)
├── rachunek_gui.py      # Interfejs graficzny
├── rachunek_manager.py  # Logika biznesowa
├── database.py          # Baza danych
├── pdf_generator.py     # Generator PDF (wymaga reportlab)
├── simple_pdf_generator.py  # Generator tekstowy (fallback)
├── walidacja.py         # Walidacja danych
├── requirements.txt     # Lista bibliotek
├── README.md           # Dokumentacja główna
├── INSTALACJA.md       # Ten plik
└── rachunki.db         # Baza danych (tworzy się automatycznie)
```

---

## 💡 Wskazówki

- **Pierwsze uruchomienie**: Użyj `python run.py` żeby sprawdzić czy wszystko działa
- **Kopie zapasowe**: Regularnie kopiuj plik `rachunki.db` 
- **PDF vs TXT**: Bez reportlab rachunki są w formacie .txt (nadal zgodne z prawem)
- **Problemy**: Sprawdź dokumentację w `README.md`

---

## ✅ Status instalacji

Po uruchomieniu `install.bat` powinieneś zobaczyć:
```
✓ Python zainstalowany
✓ Biblioteki zainstalowane (lub komunikat o trybie tekstowym)
✓ Baza danych działa
✓ Aplikacja uruchomiona
```

**Powodzenia z używaniem aplikacji! 📊**