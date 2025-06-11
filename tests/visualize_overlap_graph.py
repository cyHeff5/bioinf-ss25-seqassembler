# tests/visualize_overlap_graph.py

import os
import sys

# Pfad zur src/ hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import matplotlib.pyplot as plt
import networkx as nx

from file_parser import FileParser
from overlap_graph import OverlapGraph

def visualize_overlap_graph(graph: OverlapGraph):
    """
    Zeichnet den Overlap-Graphen mit networkx und matplotlib.
    """
    G = nx.DiGraph()

    # Knoten hinzufügen
    for fragment in graph.fragments:
        G.add_node(fragment.get_id())

    # Kanten mit Overlap-Länge hinzufügen
    for edge in graph.get_edges():
        G.add_edge(
            edge.source.get_id(),
            edge.target.get_id(),
            weight=edge.length,
            label=str(edge.length)
        )

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Visualisierung des Overlap-Graphen")
    plt.tight_layout()
    plt.show()

def main():
    filepath = os.path.join("data", "fragmentsEinzelstrang_short.txt")

    try:
        fragments = FileParser.parse_fragments(filepath)
        graph = OverlapGraph(fragments)

        print(f"✅ {len(fragments)} Fragmente geladen.")
        print(f"🔗 {len(graph.get_edges())} Overlap-Kanten gefunden. Starte Visualisierung...\n")
        visualize_overlap_graph(graph)

    except Exception as e:
        print(f"❌ Fehler bei der Visualisierung: {e}")

if __name__ == "__main__":
    main()
