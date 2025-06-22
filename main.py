import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from file_parser import FileParser
from fragment_generator import FragmentGenerator
from orientation_selector import OrientationSelector
from greedy_assembler import GreedyAssembler
from overlap_graph import OverlapGraph

def ask_choice(prompt: str, choices: list[str]) -> str:
    """Fragt den Nutzer nach einer Eingabe aus einer Liste erlaubter Optionen."""
    choices_str = "/".join(choices)
    while True:
        value = input(f"{prompt} ({choices_str}): ").strip().lower()
        if value in choices:
            return value
        print("[ERROR] Ungültige Eingabe, bitte erneut versuchen.")

def ask_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Fragt eine Ganzzahl ab, optional mit Bereich."""
    while True:
        try:
            value = int(input(f"{prompt}: ").strip())
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print("[ERROR] Zahl außerhalb des gültigen Bereichs.")
                continue
            return value
        except ValueError:
            print("[ERROR] Bitte eine gültige Ganzzahl eingeben.")

def ask_float(prompt: str, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Fragt eine Kommazahl ab, z. B. für Reverse-Ratio."""
    while True:
        try:
            value = float(input(f"{prompt}: ").strip())
            if value < min_val or value > max_val:
                print(f"[ERROR] Wert muss zwischen {min_val} und {max_val} liegen.")
                continue
            return value
        except ValueError:
            print("[ERROR] Bitte eine gültige Kommazahl eingeben.")

def ask_yes_no(prompt: str) -> bool:
    """Fragt eine Ja/Nein-Frage ab (y/n)."""
    while True:
        value = input(f"{prompt} (y/n): ").strip().lower()
        if value in ("y", "yes"):
            return True
        elif value in ("n", "no"):
            return False
        print("[ERROR] Bitte 'y' oder 'n' eingeben.")

def pause(msg="\nDrücke Enter, um fortzufahren...\n"):
    input(msg)


def main():
    print("Willkommen beim DNA-Sequenzierungstool!")

    mode = ask_choice("Möchten Sie eine Datei einlesen, oder zuällige Fragmente generieren?", ["file", "generate"])
    strand = ask_choice("Möchten Sie einen Einzel- oder Doppelstrang einlesen?", ["single", "double"])

    if mode == "file":
        filename = input("Dateiname eingeben (aus dem 'data/' Ordner) ").strip()
        filepath = f"data/{filename}"
        fragments = FileParser.parse_fragments(filepath)
        print(f"{len(fragments)} Fragmente geladen.")

    else:
        length = ask_int("Länge der DNA-Sequenz eingeben", 10)
        frag_len = ask_int("Durchschnittliche Fragmentlänge eingeben", 5)
        overlap = ask_int("Mindestüberlappung eingeben", 1)
        shuffle = ask_yes_no("Fragmente shuffeln?")
        reverse_ratio = ask_float("Anteil an Reverse Complements eingeben (z. B. 0.4)", 0.0, 1.0) if strand == "double" else 0.0

        generator = FragmentGenerator(length, frag_len, overlap, shuffle, reverse_ratio)
        fragments = generator.generate_fragments()
        print(f"{len(fragments)} Fragmente generiert.")
        for frag in fragments:
            print(frag)

        print("Originalsequenz:", generator.dna)

    if strand == "double":
        method = ask_choice("\nOrientierungsmethode wählen", ["local", "global"])
        selector = OrientationSelector(fragments)
        fragments = selector.select_orientation_local() if method == "local" else selector.select_orientation_global()

    pause()

    print("Starte Greedy-Assembly...")
    graph = OverlapGraph(fragments)
    assembler = GreedyAssembler(graph)
    result = assembler.assemble()

    pause()

    print("\nRekonstruierte Sequenz:")
    print(result.sequence)
    result_reverse = result.reverse_complement()

    if mode == "generate":
        correct = result.sequence == generator.dna or result_reverse.sequence == generator.dna
        print("Sequenzierung erfolgreich:", "JA" if correct else "NEIN")
        if correct:
            print("Die rekonstruierte Sequenz und das Original sind identisch!")
        else:
            print("Die rekonstruierte Sequenz unterscheidet sich vom Original.")

if __name__ == "__main__":
    main()
