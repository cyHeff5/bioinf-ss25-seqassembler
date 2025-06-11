import matplotlib.pyplot as plt
import networkx as nx

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from file_parser import FileParser
from overlap_graph import OverlapGraph
from greedy_assembler import GreedyAssembler
import time

def draw_graph(graph, step: int):
    """
    Visualisiert den aktuellen Zustand des Overlap-Graphen.
    """
    G = nx.DiGraph()

    for frag in graph.fragments:
        G.add_node(frag.get_id())

    for edge in graph.edges:
        G.add_edge(edge.source.get_id(), edge.target.get_id(), label=str(edge.length))

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title(f"Overlap-Graph – Schritt {step}")
    plt.tight_layout()
    plt.show()


class VisualGreedyAssembler(GreedyAssembler):
    def assemble_with_visualization(self):
        """
        Wie assemble(), aber mit Visualisierung nach jedem Merge.
        """
        step = 1
        while len(self.graph.fragments) > 1:
            print(f"\n🔁 Schritt {step}: {len(self.graph.fragments)} Fragmente im Graph")
            draw_graph(self.graph, step)
            best_edge = self._find_best_overlap()

            if best_edge is None:
                raise ValueError("Keine weiteren Overlaps – Sequenz nicht vollständig.")

            print(f"➡️ Merge: {best_edge.source.get_id()} + {best_edge.target.get_id()} (Overlap {best_edge.length})")
            self.graph.merge_and_replace(best_edge.source, best_edge.target, best_edge.length)
            step += 1

        draw_graph(self.graph, step)
        return self.graph.fragments[0]

def main():
    filepath = os.path.join("data", "fragmentsEinzelstrang_short.txt")
    fragments = FileParser.parse_fragments(filepath)
    graph = OverlapGraph(fragments)

    assembler = VisualGreedyAssembler(graph)
    result = assembler.assemble_with_visualization()

    print("\n✅ Finale Sequenz:")
    print(result.get_sequence())

if __name__ == "__main__":
    main()
