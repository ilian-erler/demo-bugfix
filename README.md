# demo-bugfix

Demo-Repository für die Live-Präsentation im Rahmen der Studienarbeit **AI-native Development Platforms**.

Dieses Projekt zeigt den SWE-bench-Anwendungsfall aus Kapitel 2.5.2 der Arbeit live: Ein KI-Agent (OpenHands) erhält ein reales GitHub Issue, klont das Repository, reproduziert den Bug, schreibt den Fix, lässt Tests laufen und öffnet einen Pull Request — vollständig autonom.

---

## Projektstruktur

```
demo-bugfix/
├── calculator.py       # Kernlogik — enthält die Bugs
├── calculator_ui.py    # Tkinter-GUI — visueller Taschenrechner
├── test_calculator.py  # Unit-Tests
└── README.md
```

---

## Wie dieses Projekt erstellt wurde

### Schritt 1 — Repository anlegen

Neues öffentliches Repository auf github.com erstellt:

- Name: `demo-bugfix`
- Sichtbarkeit: Public
- README: aktiviert

Lokal geklont:

```bash
git clone https://github.com/DEIN_USERNAME/demo-bugfix
cd demo-bugfix
```

### Schritt 2 — Projektdateien anlegen

**`calculator.py`** enthält drei Funktionen mit absichtlichen Bugs:

```python
def divide(a, b):
    return a / b  # Bug: ZeroDivisionError bei b=0

def average(numbers):
    return sum(numbers) / len(numbers)  # Bug: ZeroDivisionError bei leerem List

def first_element(lst):
    return lst[0]  # Bug: IndexError bei leerem List
```

**`test_calculator.py`** enthält grundlegende Tests (ohne Edge-Case-Abdeckung):

```python
from calculator import divide, average, first_element

def test_divide():
    assert divide(10, 2) == 5

def test_average():
    assert average([1, 2, 3]) == 2.0

def test_first_element():
    assert first_element([1, 2, 3]) == 1
```

**`calculator_ui.py`** ist ein visueller Taschenrechner mit tkinter. Die UI ruft `divide()` direkt auf — ohne Fehlerbehandlung. Bei Division durch 0 crashed die App mit einem `ZeroDivisionError`.

Alle Dateien committen und pushen:

```bash
git add .
git commit -m "Add calculator module with UI"
git push
```

### Schritt 3 — GitHub Issue anlegen

Auf github.com im Repository unter **Issues → New Issue**:

**Titel:**
```
Bug: Functions crash with empty input
```

**Beschreibung:**
```
The following functions crash with an unhandled exception when
called with empty or zero input:

- divide(10, 0) raises ZeroDivisionError
- average([]) raises ZeroDivisionError
- first_element([]) raises IndexError

Expected behavior: functions should handle edge cases gracefully
and raise a descriptive ValueError instead.

Steps to reproduce:

    from calculator import divide, average, first_element
    divide(10, 0)      # ZeroDivisionError
    average([])        # ZeroDivisionError
    first_element([])  # IndexError
```

### Schritt 4 — GitHub Personal Access Token erstellen

Wird benötigt damit OpenHands den Pull Request öffnen kann.

github.com → Profilbild → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

Berechtigungen:
- `repo` (vollständig)
- `workflow`

Token kopieren — er wird nur einmal angezeigt.

---

## Bug reproduzieren

### App starten

```bash
python3 calculator_ui.py
```

### Bug auslösen

Im Taschenrechner eingeben:

```
1 0 ÷ 0 =
```

Die App beendet sich mit folgendem Traceback im Terminal:

```
ZeroDivisionError: float division by zero
```

---

## OpenHands Demo

OpenHands löst das Issue vollständig autonom.

### Option A — Cloud (empfohlen, kein lokales Setup)

1. app.all-hands.dev aufrufen
2. Mit GitHub einloggen
3. Repository verbinden
4. Folgenden Prompt eingeben:

```
Please fix this GitHub issue:
https://github.com/DEIN_USERNAME/demo-bugfix/issues/1

Steps:
1. Clone the repository
2. Reproduce the bugs by running the tests
3. Fix all three functions to handle empty/zero input gracefully
4. Make sure all tests pass
5. Add new tests for the edge cases
6. Open a pull request with your changes
```

### Option B — Lokal via Docker

```bash
docker run -it --rm \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.38-nikolaik \
  -e LOG_ALL_EVENTS=true \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openhands-state:/.openhands-state \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  --name openhands-app \
  docker.all-hands.dev/all-hands-ai/openhands:0.38
```

Browser öffnen: `http://localhost:3000`

LLM Provider: Anthropic  
Model: claude-sonnet-4-6  
API Key: Anthropic API Key einfügen  
GitHub Token: Token aus Schritt 4 einfügen

### Was OpenHands live tut

```
▸ Cloning repository...
▸ Running tests... 3 passed, 0 failed
▸ Reproducing bug: divide(10, 0) → ZeroDivisionError ✓
▸ Fixing calculator.py...
▸ Running tests... 6 passed, 0 failed ✓
▸ Opening Pull Request...
✓ PR opened: https://github.com/DEIN_USERNAME/demo-bugfix/pull/2
```

---

## Erwartetes Ergebnis nach dem Fix

`calculator.py` nach dem OpenHands-Fix:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)

def first_element(lst):
    if not lst:
        raise ValueError("Cannot get first element of empty list")
    return lst[0]
```

Tests nach dem Fix: 6 bestanden, 0 fehlgeschlagen.

---

## Verbindung zur Studienarbeit

Dieses Demo illustriert direkt die empirischen Befunde aus der Arbeit:

- **Kapitel 2.1** — Der Agent nutzt Repository-Kontext, Tool-Use (pytest) und Human-in-the-Loop (PR-Review)
- **Kapitel 2.3** — OpenHands als Open-Source-Plattform (Issue → PR vollständig automatisiert)
- **Kapitel 2.5.2** — SWE-bench-Prinzip live: reales GitHub Issue, eigenständig gelöst, PR mit grünen Tests

---

## Voraussetzungen

```bash
# Python 3.10+
python3 --version

# Abhängigkeiten
pip3 install pytest

# Tests ausführen
pytest test_calculator.py -v
```