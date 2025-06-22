# src/greedy_assembler.py

from overlap_graph import OverlapGraph
from overlap import Overlap
from fragment import Fragment

class GreedyAssembler:
    """
    Führt einen Greedy-Algorithmus aus, um aus Fragmenten eine DNA-Sequenz zu rekonstruieren.
    """

    def __init__(self, graph: OverlapGraph):
        self.graph = graph

    def assemble(self) -> Fragment:
        """
        Führt den Greedy-Assembly durch.

        Returns:
            Fragment: Das finale zusammengefügte Fragment.
        """
        while len(self.graph.fragments) > 1:
            best_edge = self._find_best_overlap()

            if best_edge is None:
                raise ValueError(f"Keine weiteren Overlaps vorhanden – Sequenz kann nicht vollständig rekonstruiert werden.\n" \
                "Verbleibende Fragmente:" \
                f"{self.graph.fragments}")

            # Merge source → target
            merged = self.graph.merge_and_replace(
                best_edge.source, best_edge.target, best_edge.length
            )

        return self.graph.fragments[0]  # Das letzte übrig gebliebene Fragment

    def _find_best_overlap(self) -> Overlap | None:
        """
        Findet die beste Overlap-Kante mit dem größten Overlap-Wert.

        Returns:
            Overlap | None: Die beste Kante oder None, falls keine vorhanden ist.
        """
        if not self.graph.edges:
            return None

        return max(self.graph.edges, key=lambda e: e.length, default=None)
