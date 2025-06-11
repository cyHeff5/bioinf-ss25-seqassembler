# tests/test_overlap_graph.py

import os
import sys

# Pfad zur src/ hinzufügen, damit Importe funktionieren
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from file_parser import FileParser
from overlap_graph import OverlapGraph

def main():
    filepath = os.path.join("data", "FragmenteEinzelstrang.txt")

    try:
        # Fragmente einlesen
        fragments = FileParser.parse_fragments(filepath)
        print(f"✅ {len(fragments)} Fragmente eingelesen.")

        # OverlapGraph erzeugen
        graph = OverlapGraph(fragments)
        edges = graph.get_edges()
        print(f"🔗 {len(edges)} Overlap-Kanten gefunden.\n")

        # Ausgabe aller Kanten
        # for edge in edges:
        #     print(f"{edge.source.get_id()} -> {edge.target.get_id()} (Overlap: {edge.length})")

    except Exception as e:
        print(f"❌ Fehler beim Testen des OverlapGraph: {e}")

if __name__ == "__main__":
    main()
