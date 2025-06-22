import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


from file_parser import FileParser
from fragment import Fragment
from orientation_selector import OrientationSelector
from overlap_graph import OverlapGraph
from greedy_assembler import GreedyAssembler 

def main():
    print("Willkommen zum DNA-Assembler.")
    print("Bitte wähle den Sequenztyp:")
    print("1 – Einzelstrang")
    print("2 – Doppelstrang")

    auswahl = input("Deine Wahl: ").strip()

    if auswahl == "1":
        dateiname = "fragmentsEinzelstrang_short.txt"
    elif auswahl == "2":
        dateiname = "fragmentsDoppelstrang_short.txt"
    else:
        print("Ungültige Eingabe. Bitte wähle 1 oder 2.")
        return

    dateipfad = os.path.join("data", dateiname)

    try:
        parser = FileParser()
        fragmente = parser.parse_fragments(dateipfad)

        print(f"\n{len(fragmente)} Fragmente erfolgreich geladen.")

        # Optional anzeigen
        # for f in fragmente:
        #     print(f"- {f.id}: {f.sequence[:30]}...")

        # Nur für Doppelstrang: Orientierung wählen
        if auswahl == "2":
            selector = OrientationSelector(fragmente)
            fragmente = selector.select_orientation()
            print("Orientierungen wurden mit Greedy-Heuristik ausgewählt.")

        # OverlapGraph erstellen
        graph = OverlapGraph(fragmente)
        print(f"OverlapGraph mit {len(graph.edges)} Kanten erstellt.")

        # GreedyAssembler ausführen
        assembler = GreedyAssembler(graph)
        assembled_sequence = assembler.assemble()

        print("\nErgebnis der Assemblierung:")
        print(assembled_sequence)

    except FileNotFoundError:
        print(f"Fehler: Datei '{dateipfad}' nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
