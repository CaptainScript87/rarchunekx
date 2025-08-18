# System Rachunków - Uproszczone Rachunki

Aplikacja do wystawiania i ewidencjonowania uproszczonych rachunków zgodnych z polskim prawem, napisana w języku Python.

## Funkcjonalności

- ✅ **Wystawianie rachunków** - wprowadzanie danych i generowanie rachunków PDF
- ✅ **Automatyczna numeracja** - unikalny numer w formacie "nr/miesiąc/rok" (np. "1/08/2025")
- ✅ **Ewidencja rachunków** - zapisywanie wszystkich rachunków w bazie danych SQLite
- ✅ **Wyszukiwanie** - znajdowanie rachunków po numerze, dacie lub nazwisku nabywcy
- ✅ **Eksport do CSV** - możliwość wyeksportowania listy rachunków
- ✅ **Domyślne dane sprzedawcy** - zapisywanie i edycja danych sprzedawcy
- ✅ **Walidacja danych** - sprawdzanie poprawności wprowadzonych danych
- ✅ **Interfejs graficzny** - przejrzysty GUI oparty na tkinter

## Wymagania systemowe

- Python 3.7 lub nowszy
- System operacyjny: Windows, macOS, Linux

## Instalacja

1. **Pobierz aplikację**
   ```bash
   # Jeśli korzystasz z git
   git clone <url-repozytorium>
   cd rachunek2025
   
   # Lub rozpakuj pobrane pliki do folderu
   ```

2. **Zainstaluj wymagane biblioteki**
   ```bash
   pip install -r requirements.txt
   ```

3. **Uruchom aplikację**
   ```bash
   python main.py
   ```

## Instrukcja użytkowania

### Pierwsze uruchomienie

1. Po uruchomieniu aplikacji przejdź do zakładki **"Ustawienia"**
2. Uzupełnij swoje dane jako sprzedawcy (imię, nazwisko, adres)
3. Kliknij **"Zapisz dane sprzedawcy"**

### Wystawianie nowego rachunku

1. Przejdź do zakładki **"Nowy Rachunek"**
2. Wypełnij dane nabywcy:
   - Imię i nazwisko (lub nazwa firmy)
   - Pełny adres (ulica, numer domu, kod pocztowy, miasto)
3. Wprowadź szczegóły usługi:
   - Data wykonania usługi (domyślnie dzisiejsza data)
   - Nazwa/opis usługi
   - Cenę w PLN (np. 100.50)
4. Kliknij **"Generuj Rachunek"**
5. Wybierz folder, gdzie ma zostać zapisany plik PDF
6. Rachunek zostanie wygenerowany i zapisany w ewidencji

### Przeglądanie i wyszukiwanie rachunków

1. Przejdź do zakładki **"Lista Rachunków"**
2. Wszystkie rachunki są wyświetlane w tabeli
3. Możesz wyszukiwać rachunki wpisując:
   - Numer rachunku
   - Datę wystawienia
   - Nazwisko nabywcy
4. **Podwójne kliknięcie** na rachunku otwiera plik PDF
5. **Prawy przycisk myszy** pokazuje menu kontekstowe z opcjami:
   - Otwórz PDF
   - Regeneruj PDF (jeśli plik został usunięty)
   - Pokaż szczegóły

### Eksport danych

1. W zakładce **"Lista Rachunków"** kliknij **"Eksportuj do CSV"**
2. Wybierz lokalizację dla pliku CSV
3. Plik będzie zawierał: numer rachunku, datę, nabywcę i kwotę

## Elementy rachunku

Każdy wygenerowany rachunek zawiera wszystkie wymagane elementy:

- 📋 Napis "RACHUNEK" i unikalny numer
- 📅 Data wystawienia i data wykonania usługi
- 👤 Dane sprzedawcy (imię, nazwisko, adres)
- 🏢 Dane nabywcy (imię, nazwisko/firma, adres)
- 🔧 Nazwa wykonywanej usługi
- 💰 Cenę jednostkową
- 💵 Kwotę do zapłaty (cyfrowo i słownie)
- ✍️ Miejsce na podpis sprzedawcy

## Struktura plików

```\nrachunek2025/\n├── main.py              # Główny plik uruchamiający aplikację\n├── rachunek_gui.py      # Interfejs graficzny (tkinter)\n├── rachunek_manager.py  # Logika biznesowa\n├── database.py          # Obsługa bazy danych SQLite\n├── pdf_generator.py     # Generowanie plików PDF\n├── walidacja.py         # Walidacja danych wejściowych\n├── requirements.txt     # Lista wymaganych bibliotek\n├── README.md           # Ta dokumentacja\n└── rachunki.db         # Baza danych (tworzona automatycznie)\n```\n\n## Formaty danych\n\n### Daty\nMożesz wprowadzać daty w formatach:\n- `DD.MM.YYYY` (np. 15.08.2025)\n- `DD/MM/YYYY` (np. 15/08/2025)\n- `YYYY-MM-DD` (np. 2025-08-15)\n\n### Kwoty\nKwoty wprowadzaj w formacie:\n- `100.50` lub `100,50`\n- Bez symbolu waluty\n- Maksymalnie 2 miejsca po przecinku\n\n### Kod pocztowy\nFormat: `XX-XXX` (np. `00-001`)\n\n## Rozwiązywanie problemów\n\n### Aplikacja nie uruchamia się\n1. Sprawdź czy masz zainstalowany Python 3.7+\n2. Zainstaluj wymagane biblioteki: `pip install -r requirements.txt`\n3. Sprawdź czy wszystkie pliki są w tym samym folderze\n\n### Błąd przy generowaniu PDF\n1. Sprawdź czy wybrany folder istnieje i masz uprawnienia do zapisu\n2. Upewnij się, że żaden plik PDF o tej nazwie nie jest otwarty\n\n### Błąd \"Brak danych sprzedawcy\"\n1. Przejdź do zakładki \"Ustawienia\"\n2. Wypełnij wszystkie pola danych sprzedawcy\n3. Kliknij \"Zapisz dane sprzedawcy\"\n\n### Problem z polskimi znakami\nAplikacja automatycznie obsługuje polskie znaki. Jeśli wystąpią problemy, upewnij się że używasz Python 3.7+.\n\n## Bezpieczeństwo danych\n\n- Wszystkie dane są przechowywane lokalnie w bazie SQLite\n- Baza danych znajduje się w pliku `rachunki.db` w folderze aplikacji\n- **Ważne**: Regularnie rób kopie zapasowe pliku `rachunki.db`\n- Pliki PDF są zapisywane w wybranych przez Ciebie lokalizacjach\n\n## Zgodność prawna\n\nAplikacja generuje uproszczone rachunki zgodnie z polskim prawem, zawierające wszystkie wymagane elementy. Jednak zawsze skonsultuj się z księgowym lub prawnikiem w sprawie specyficznych wymagań dla Twojej działalności.\n\n## Wsparcie\n\nJeśli napotkasz problemy lub masz pytania:\n1. Sprawdź sekcję \"Rozwiązywanie problemów\" powyżej\n2. Upewnij się, że używasz najnowszej wersji aplikacji\n3. Sprawdź czy wszystkie wymagane biblioteki są zainstalowane\n\n## Licencja\n\nAplikacja została stworzona w celach edukacyjnych i może być swobodnie używana i modyfikowana.\n\n---\n\n**Wersja:** 1.0  \n**Data:** Sierpień 2025  \n**Autor:** System generowania rachunków Python"