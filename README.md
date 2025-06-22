# DNA-Sequenz-Assembler mit Greedy-Algorithmus

Mithilfe dieses Tools kann eine ursprüngliche DNA-Sequenz aus überlappenden Fragmenten rekonstruiert werden. Dabei kommt ein Greedy-Ansatz zum Einsatz, der durch unterschiedliche Strategien zur Orientierung und Auswahl von Fragmenten ergänzt wird. Das Programm kann sowohl mit echten Daten als auch mit synthetisch generierten Testdaten genutzt werden.

## Voraussetzungen
- Python 3.10 oder neuer
- Keine externen Bibliotheken erforderlich

## Ausführen der Programms
```bash
python main.py
```

## Bedingung über die Kommandozeile
Das Programm wird vollständig über **interaktive Eingaben** in der Kommandozeile bedient.

---

### 1. Modus wählen

Wähle, ob Fragmente aus einer Datei eingelesen oder zufällig generiert werden sollen:

- `file` → Fragmente aus einer Datei im `data/`-Ordner lesen
- `generate` → DNA-Sequenz zufällig erzeugen und automatisch fragmentieren

---
### 2. Strang-Typ wählen

Wähle, ob mit einem Einzelstrang oder Doppelstrang gearbeitet werden soll:

- `single` → Alle Fragmente stammen vom ursprünglichen Strang
- `double` → Fragmente können zufällig als Reverse Complements vorliegen

---
### 3. Datei einlesen (`file`)

Wenn `file` gewählt wurde:

- Gib den Dateinamen ein, z. B. `fragmentsEinzelstrang_short.txt`
- Die Datei muss im Verzeichnis `data/` liegen

---
### 4. Fragmente generieren (`generate`)

Wenn `generate` gewählt wurde, wird nach folgenden Parametern gefragt:

| Eingabe                 | Beschreibung                                           | Beispiel      |
|------------------------|--------------------------------------------------------|---------------|
| Länge der DNA          | Gesamtlänge der zu generierenden DNA-Sequenz          | `100`         |
| Fragmentlänge          | Durchschnittliche Länge eines Fragments               | `20`          |
| Mindestüberlappung     | Minimale Überlappung zwischen zwei Fragmenten         | `5`           |
| Shuffle                | Fragmente zufällig durchmischen? (`y/n`)              | `y`           |
| Reverse Ratio (optional) | Anteil an Reverse Complements (nur bei `double`)     | `0.4`         |

---
### 5. Orientierung (nur bei `double`)

Wenn `double` gewählt wurde, gib an, wie die Orientierung der Fragmente gewählt werden soll:

- `local` → Jedes Fragment wird nacheinaner bewertet und orientiert
- `global` → In jedem Schritt wird das Fragment mit dem besten Gesamtscore gewählt

---
### 6. Start des Assemblierungsprozesses

Nach dem Einlesen oder Generieren der Fragmente beginnt der **Greedy-Assembly**, und das Tool versucht, die ursprüngliche DNA-Sequenz zu rekonstruieren.

**Hinweis:**
Sollte während der Assembly der folgende Fehler auftreten:
```bash
ValueError: Keine weiteren Overlaps vorhanden – Sequenz kann nicht vollständig rekonstruiert werden.
```
bedeutet das, dass beim Assembly **Fragmente übrig geblieben sind**, die **keine Overlaps zu anderen Fragmenten** haben. Die Sequenzierung war also nicht Erfolgreich.

---
### 7. Ausgabe und Erfolgskontrolle

- Die rekonstruierte Sequenz wird angezeigt.
- Falls `generate` gewählt wurde, wird geprüft, ob die Originalsequenz korrekt rekonstruiert wurde.
- Das Ergebnis wird deutlich angezeigt: „Sequenzierung erfolgreich“ oder „fehlgeschlagen“.