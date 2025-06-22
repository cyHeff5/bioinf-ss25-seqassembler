from overlap_graph import OverlapGraph
from overlap import Overlap
from fragment import Fragment

class GreedyAssembler:
    """
    Führt eine Greedy-Assembly durch, indem jeweils das Fragmentpaar mit dem größten Overlap 
    zusammengeführt wird. Verwendet dafür den OverlapGraph.
    """

    def __init__(self, graph: OverlapGraph):
        """
        Initialisiert den Assembler mit einem OverlapGraph.
        """
        self.graph = graph

    def assemble(self) -> Fragment:
        """
        Führt die Greedy-Assembly durch, bis nur noch ein Fragment übrig ist.
        In jedem Schritt wird das Fragmentpaar mit dem größten Overlap gemerged.
        
        Rückgabe:
            Fragment: Das final zusammengesetzte Fragment
        """
        while len(self.graph.fragments) > 1:
            best_edge = self._find_best_overlap()

            # Falls keine Kanten mehr vorhanden sind, aber noch mehrere Fragmente existieren
            if best_edge is None:
                raise ValueError(f"Keine weiteren Overlaps vorhanden – Sequenz kann nicht vollständig rekonstruiert werden.\n" \
                "Verbleibende Fragmente:" \
                f"{self.graph.fragments}")

            # Führe das beste Fragmentpaar (mit größtem Overlap) zusammen
            merged = self.graph.merge_and_replace(
                best_edge.source, best_edge.target, best_edge.length
            )
        return self.graph.fragments[0]  # Das letzte übrig gebliebene Fragment

    def _find_best_overlap(self) -> Overlap | None:
        """
        Sucht die Kante mit dem größten Overlap im Graphen.
        
        Rückgabe:
            Overlap: Die beste (längste) Overlap-Kante, oder None wenn keine vorhanden ist
        """
        if not self.graph.edges:
            return None
        # Wähle die Kante mit der größten Overlap-Länge
        return max(self.graph.edges, key=lambda e: e.length, default=None)
