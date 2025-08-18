# Historia Zmian - System Rachunków

Wszystkie istotne zmiany w tym projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
a projekt stosuje [Semantic Versioning](https://semver.org/lang/pl/).

---

## [2.0.0] - 2025-01-18

### ✅ Dodane
- **System limitów miesięcznych**: Automatyczne pilnowanie limitu 3499,50 PLN dla 2025 roku
- **Podsumowanie miesięczne**: Wizualna reprezentacja przychodów z paskiem postępu
- **Nowoczesny interfejs graficzny**: Nowy design z ikonami i lepszą typografią
- **Kolorowe statusy**: Wizualne ostrzeżenia (zielony/żółty/pomarańczowy/czerwony)
- **Automatyczne dopasowanie okna**: Inteligentne dopasowywanie rozmiaru do zawartości
- **Skróty klawiszowe**: 
  - Ctrl+R / F11 - dopasowanie rozmiaru okna
  - Escape - czyszczenie formularza
- **System wersjonowania**: Pełne śledzenie wersji z historią zmian
- **Okno "O aplikacji"**: Szczegółowe informacje o wersji i historii

### 🔄 Zmienione
- **Walidacja danych**: Rozszerzona o kontrolę limitów miesięcznych
- **Baza danych**: Nowe zapytania do śledzenia miesięcznych przychodów
- **Interfejs użytkownika**: Całkowicie przeprojektowany z nowoczesnymi elementami
- **Zarządzanie oknami**: Inteligentne wyśrodkowywanie i skalowanie
- **Rozmiar okna**: Zwiększony do 1100x800px z automatycznym dopasowaniem

### 🐛 Naprawione
- Problemy z importami modułów
- Błędy inicjalizacji zmiennych w GUI
- Problemy z kodowaniem polskich znaków

### 📦 Techniczne
- Dodany moduł `version.py` do zarządzania wersjami
- Rozszerzona konfiguracja w `config.py`
- Nowe metody w `database.py` do obsługi limitów miesięcznych
- Ulepszona klasa walidatora w `walidacja.py`

---

## [1.0.0] - 2024-12-01

### ✅ Dodane
- **Podstawowa funkcjonalność**: Tworzenie rachunków z automatyczną numeracją
- **Generator PDF**: Tworzenie plików PDF z polskimi znakami
- **Baza danych SQLite**: Pełna ewidencja rachunków
- **Interface graficzny**: GUI oparty na tkinter
- **Wyszukiwanie**: Filtrowanie rachunków po numerze, dacie, nazwisku
- **Eksport CSV**: Możliwość eksportu danych do pliku CSV
- **Walidacja danych**: Sprawdzanie poprawności wprowadzanych informacji
- **Obsługa dat**: Różne formaty dat (DD.MM.YYYY, DD/MM/YYYY, YYYY-MM-DD)
- **Kwoty słownie**: Automatyczne konwersje kwot na słowa
- **Fallback tekstowy**: Możliwość pracy bez biblioteki reportlab

### 📦 Pierwsze wydanie
- Struktura modułowa aplikacji
- Dokumentacja użytkownika (README.md)
- Instrukcje instalacji
- Testy podstawowej funkcjonalności

---

## Typy zmian
- **Dodane** - nowe funkcjonalności
- **Zmienione** - zmiany w istniejących funkcjonalnościach
- **Przestarzałe** - funkcjonalności, które będą usunięte w przyszłych wersjach
- **Usunięte** - funkcjonalności usunięte w tej wersji
- **Naprawione** - poprawki błędów
- **Bezpieczeństwo** - w przypadku luk w zabezpieczeniach

---

## Planowane funkcjonalności (Roadmap)

### v2.1.0 (Planowane)
- [ ] Kopia zapasowa bazy danych
- [ ] Motywy kolorystyczne (jasny/ciemny)
- [ ] Eksport do różnych formatów (Word, Excel)
- [ ] Więcej opcji personalizacji PDF

### v2.2.0 (Planowane)
- [ ] Raportowanie miesięczne/roczne
- [ ] Integracja z e-mail
- [ ] Automatyczne przypomnienia
- [ ] Zaawansowane filtry wyszukiwania

### v3.0.0 (Długoterminowe)
- [ ] Obsługa faktur VAT
- [ ] API dla integracji
- [ ] Aplikacja mobilna
- [ ] Synchronizacja w chmurze

---

**Legenda formatów dat:**
- [2.0.0] - wydana wersja
- [Unreleased] - zmiany w trakcie rozwoju

**Autor:** System Rachunków Development Team  
**Kontakt:** Sprawdź README.md w celu uzyskania informacji o wsparciu