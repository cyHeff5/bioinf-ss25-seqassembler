import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from file_parser import FileParser
from overlap_graph import OverlapGraph
from greedy_assembler import GreedyAssembler

def choose_file() -> str:
    """
    Bietet eine Auswahl an Fragmentdateien im data/-Ordner.
    """
    options = {
        "1": "fragmenteEinzelstrang.txt",
        "2": "fragmentsEinzelstrang_short.txt"
    }

    print("🧬 Wähle die Fragment-Datei aus:\n")
    for key, filename in options.items():
        print(f"{key}) {filename}")

    choice = ""
    while choice not in options:
        choice = input("\nEingabe (1/2): ").strip()

    selected_path = os.path.join("data", options[choice])
    print(f"\n📂 Gewählte Datei: {selected_path}")
    return selected_path

def main():
    filepath = choose_file()

    try:
        fragments = FileParser.parse_fragments(filepath)
        print(f"\n📄 {len(fragments)} Fragmente geladen.")

        graph = OverlapGraph(fragments)
        assembler = GreedyAssembler(graph)
        result_fragment = assembler.assemble()

        print("\n✅ Rekonstruierte Sequenz:")
        print(result_fragment.get_sequence())

    except Exception as e:
        print(f"❌ Fehler beim Verarbeiten: {e}")

if __name__ == "__main__":
    main()
