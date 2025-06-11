# src/overlap_graph.py

from typing import List
from fragment import Fragment
from overlap import Overlap

class OverlapGraph:
    """
    Baut und verwaltet einen gerichteten Overlap-Graph aus Fragmenten.
    Jeder Knoten ist ein Fragment, jede Kante zeigt einen möglichen Übergang mit Overlap.
    """

    _merge_counter = 0  # Für eindeutige IDs bei Merges

    def __init__(self, fragments: List[Fragment]):
        self.fragments = fragments
        self.edges: List[Overlap] = []
        self._build_graph()

    def _build_graph(self):
        """
        Baut den vollständigen gerichteten Overlap-Graph basierend auf den Fragmenten.
        """
        for a in self.fragments:
            for b in self.fragments:
                if a != b:
                    overlap_len = self._compute_overlap(a.get_sequence(), b.get_sequence())
                    if overlap_len > 0:
                        self.edges.append(Overlap(a, b, overlap_len))

    @staticmethod
    def _compute_overlap(seq_a: str, seq_b: str) -> int:
        """
        Berechnet die Länge des längsten Suffixes von seq_a, der ein Präfix von seq_b ist.
        """
        max_len = min(len(seq_a), len(seq_b)) - 1
        for l in range(max_len, 0, -1):
            if seq_a[-l:] == seq_b[:l]:
                return l
        return 0

    def get_edges(self) -> List[Overlap]:
        """
        Gibt alle aktuell gespeicherten Overlap-Kanten zurück.
        """
        return self.edges

    def remove_fragment(self, fragment: Fragment):
        """
        Entfernt ein Fragment sowie alle zugehörigen Kanten aus dem Graphen.
        """
        self.fragments = [f for f in self.fragments if f != fragment]
        self.edges = [e for e in self.edges if e.source != fragment and e.target != fragment]

    def add_fragment(self, new_fragment: Fragment):
        """
        Fügt ein neues Fragment hinzu und berechnet alle Overlap-Kanten zu bestehenden Fragmenten.
        """
        for other in self.fragments:
            if other != new_fragment:
                # new → other
                len1 = self._compute_overlap(new_fragment.get_sequence(), other.get_sequence())
                if len1 > 0:
                    self.edges.append(Overlap(new_fragment, other, len1))

                # other → new
                len2 = self._compute_overlap(other.get_sequence(), new_fragment.get_sequence())
                if len2 > 0:
                    self.edges.append(Overlap(other, new_fragment, len2))

        self.fragments.append(new_fragment)

    def merge_and_replace(self, source: Fragment, target: Fragment, overlap_len: int) -> Fragment:
        """
        Merged zwei Fragmente zu einem neuen Fragment und ersetzt sie im OverlapGraph.

        Returns:
            Fragment: Das neu erzeugte Fragment
        """
        if overlap_len <= 0:
            raise ValueError("Overlap-Länge muss positiv sein.")

        merged_seq = source.get_sequence() + target.get_sequence()[overlap_len:]
        new_id = f"MERGED_{OverlapGraph._merge_counter}"
        OverlapGraph._merge_counter += 1

        new_fragment = Fragment(id=new_id, sequence=merged_seq)

        self.remove_fragment(source)
        self.remove_fragment(target)
        self.add_fragment(new_fragment)

        return new_fragment
