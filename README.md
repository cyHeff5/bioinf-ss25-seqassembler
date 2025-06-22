# DNA-Sequenz-Assembler mit Greedy-Algorithmus

Dieses Tool rekonstruiert eine ursprüngliche DNA-Sequenz aus überlappenden Fragmenten. Dabei wird ein **Greedy-Ansatz** verwendet, der durch unterschiedliche Strategien zur Orientierung und Auswahl von Fragmenten ergänzt wird. Das Programm lässt sich sowohl mit echten Daten als auch mit synthetisch generierten Testdaten nutzen.

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