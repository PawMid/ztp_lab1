## 1. Temat Zadania
___

### W oparciu o mikroframework Flask oraz wzorzec REST zaimplementuj aplikacje do obsługi wypożyczania książek w bibliotece.
___

Aplikacja powinna realizować następujące zadania:
  1. dodawanie nowego użytkownika do systemu,
  2. usuwanie istniejącego użytkownika z systemu,
  3. wyświetlenie listy użytkowników w systemie,
  4. wyświetlenie konta użytkownika wraz z informacją o wypożyczonych pozycjach,
  5. wyświetlenie listy wszystkich tytułów książek znajdujących się bibliotece,
  6. wyświetlanie listy wypożyczonych egzemplarzy danego tytułu wraz z informacją kto i kiedy wypożyczył dany egzemplarz książki,
  7. obsługę wypożyczania/zwrotu danego egzemplarza książki przez użytkownika.

**Wymagania dotyczące aplikacji:**
1. zasoby i funkcjonalność powinny być udostępniane  poprzez REST API,
2. dostęp do aplikacji poprzez adres: http://localhost:5000,
3. treść żądań powinna być w formacie JSON,
4. treść odpowiedzi powinna być w formacie JSON.

Szczegóły żądań HTTP zostały zdefiniowane w pliku [rest-biblioteka-swagger.yaml](doc/rest-biblioteka-swagger.yaml) w katalogu `doc`. Plik został utworzony zgodnie ze standardem OpenApi. Do przeglądania zawartości pliku  użyj aplikacji Swagger Editor która jest dostępna [tutaj](https://editor.swagger.io/). 

## 2. Ocena rozwiązania
* poprawnie zaimplementowanie wymaganych endpoint'ów, 
* poprawnie zaimplementowanie obsługa parametrów przesyłanych w zapytaniach,
* zaimplementowanie zwracanych kodów błędów oraz danych zgodnie ze specyfikacją,
* foramtowanie kodu zgodne z pep8,
* opinia prowadzącego na temat zaimplementowanego kodu.

## 3. Ustawienie środowiska pracy
### 3.1. Klonowanie repozytoria z GitHub
- Lokalnie utwórz katalog roboczy dla repozytoriów z którymi bedziesz pracował w ramach zajęć. Np. katalog o nazwie _ztp_2021_. 
- sklonuj repozytorium dla bieżących zajęć z GitHub'a do katalogu roboczego.
  
    > `git clone <repository_url>`


### 3.2. Wirtualne środowisko 
- Przejdź do katalogu zawierające sklonowane repozytorium (dalej nazywany *katalog projektu*)
- Utwórz wirtualne środowisko pythona

    > `python3 -m venv .venv`

- Aktywuj wirtualne środowisko
  - Windows:
    > `.venv\Scripts\activate`

  - Unix lub MacOS:
    > `source .venv/bin/activate`

- Zainstaluj moduły `flask`

    > `pip install flask`
___
Więcej informacji n/t pracy z wirtualnym środowiskiem python możesz znaleźść w dokumentacji ["Virtual Environments and Packages"](https://docs.python.org/3.8/tutorial/venv.html)
___

## 4. Implementacja.
### 4.1. Inicjalizacja aplikacji Flask.
* Utwórz główny plik aplikacji `app.py`
* W pliku aplikacji zaimportuj moduły `Flask` oraz zainicalizuj instacje aplikacji Flask.

```python
# app.py
from flask import Flask
  
app = app = Flask(__name__)


if __name__ == "__main__":
    app.run()
```

### 4.2. Definiowanie endpoint'ów przy pomocy dekoratora Flask `@route` - przykad


```python
# app.py
from flask import request

@app.route('/users', methods=['GET', 'POST'])
def users():
  if request.method == 'GET':
    pass

  if request.method == 'POST':
    pass


@app.route('/books/rent/<int: id>', methods=['PATCH'])
def rent_book(id):
    pass
```

### 4.3. Odczytywanie danych z zapytania.

```python
from flask import request
...

@app.route('/books/rent/<int: id>', methods=['PATCH'])
def rent_book(id):
  '''
  Parametr przesyłany w nagłówku zapytania:
  curl -X PATCH http://localhost:5000/books/return/3 \
    -H 'accept: application/json' \
    -H 'user: 20' \
    -H 'Content-Type: application/json' \
    -d '{ 'username": "Jan Nowak" }'
  '''
    # Odczytanie wartości parametru 'user' z nagłówka zapytania:
    user = request.headers['user']

    # Odczytanie struktury JSON z parametrem 'username':
    json_data = request.get_json()
    pass


@app.route('/books', methods=['GET'])
def books():
  '''
  Dla parametru przekazanego w postaci querery:
  curl -X PATCH http://localhost:5000/books?author=Grzegorczyk \
    -H 'accept: application/json'
  '''

  author = request.args.get('author')
  pass

```

### 4.4. Zwracanie dany w formacie JSON oraz statusu.

```python
from flask import json

@app.route('/books', methods=['GET'])
def books():
  .
  .
  .
  return app.response_class(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')

```
## 5. Baza danych SQLite3
* Baza danych w pamięci RAM:
```python
# app.py
import sqlite3
# Podłączenie do bazy
db_con = sqlite3.connect(:memory:)
db_con.row_factory = sqlite3.Row

# Inicjalizacja przykładowej bazy danych


with open('doc/create_library_db.sql','r') as f:
  db_con.executescript(f.read())
  db_con.commit()
  
# Wywołanie kwerendy SQL

cur = db_con.cursor()
row = cur.execute("SELECT * FROM tbl_books;").fetchall()

# konwersja do JSON'a
data = json.dumps(row)
```
## 6. Walidacja kodu zgodnie ze standardem pep8.
Do sprawdzenia formatowania kodu zgodnie ze standartem `pep8` użyj modułu `flake8`.

* Instalacja `flake8`:
  
  > `pip install flake8`

* Sprawdzenie czy plik `app.py` jest zgodny z `pep8`:

> `python -m flake8 app.py`





