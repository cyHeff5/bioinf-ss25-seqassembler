from typing import List
from fragment import Fragment
from overlap import Overlap

class OverlapGraph:
    """
    Repräsentiert einen gerichteten Overlap-Graph, der aus DNA-Fragmenten besteht.

    Jeder Knoten im Graph ist ein Fragment. 
    Eine gerichtete Kante (Overlap) existiert, wenn das Suffix eines Fragments mit dem Präfix eines anderen überlappt.
    """
    _merge_counter = 0 # Zähler für die Vergabe eindeutiger IDs bei Merges

    def __init__(self, fragments: List[Fragment]):
        """
        Initialisiert den OverlapGraph mit einer Liste von Fragmenten.
        Baut beim Erzeugen automatisch den vollständigen Overlap-Graph auf.
        """
        self._fragments = fragments
        self._edges: List[Overlap] = []
        self._build_graph()

    def _build_graph(self):
        """
        Baut alle möglichen gerichteten Kanten (Overlaps) zwischen Fragmenten auf.
        """
        print("[OverlapGraph] Baue Overlap-Graph aus Fragmenten aus...")
        edge_count = 0
        for a in self.fragments:
            for b in self.fragments:
                if a != b:
                    overlap_len = self._compute_overlap(a.sequence, b.sequence)
                    if overlap_len > 0:
                        self._edges.append(Overlap(a, b, overlap_len))
                        edge_count += 1
        print(f"[OverlapGraph] {edge_count} Kanten wurden erzeugt.")

    @staticmethod
    def _compute_overlap(seq_a: str, seq_b: str) -> int:
        """
        Berechnet die Länge des längsten Suffixes von seq_a,
        der mit dem Präfix von seq_b übereinstimmt.
        """
        max_len = min(len(seq_a), len(seq_b)) - 1
        for l in range(max_len, 0, -1):
            if seq_a[-l:] == seq_b[:l]:
                return l
        return 0

    def remove_fragment(self, fragment: Fragment):
        """
        Entfernt ein Fragment sowie alle zugehörigen Overlap-Kanten aus dem Graph.
        """
        self._fragments = [f for f in self._fragments if f != fragment]
        self._edges = [e for e in self._edges if e.source != fragment and e.target != fragment]
        print(f"[-] Fragment wurde entfernt: {fragment.id}")

    def add_fragment(self, new_fragment: Fragment):
        """
        Fügt ein neues Fragment dem Graph hinzu und berechnet Overlaps zu allen vorhandenen Fragmenten.
        """
        for other in self._fragments:
            if other != new_fragment:
                # new - other
                len1 = self._compute_overlap(new_fragment.sequence, other.sequence)
                if len1 > 0:
                    self._edges.append(Overlap(new_fragment, other, len1))

                # other - new
                len2 = self._compute_overlap(other.sequence, new_fragment.sequence)
                if len2 > 0:
                    self._edges.append(Overlap(other, new_fragment, len2))
        self.fragments.append(new_fragment)
        print(f"[+] Neues Fragment wurde hinzugefügt: {new_fragment.id}")

    def merge_and_replace(self, source: Fragment, target: Fragment, overlap_len: int) -> Fragment:
        """
        Führt zwei Fragmente mit gegebenem Overlap zusammen zu einem neuen Fragment.
        Entfernt die Ursprungsfragmente und ersetzt sie durch das neue.
        
        Rückgabe:
            Das neu entstandene, zusammengeführte Fragment
        """
        if overlap_len <= 0:
            raise ValueError("Overlap-Länge muss positiv sein.")

        # Erzeuge zusammengeführte Sequenz
        merged_seq = source.sequence + target.sequence[overlap_len:]
        new_id = f"MERGED_{OverlapGraph._merge_counter}"
        OverlapGraph._merge_counter += 1

        new_fragment = Fragment(id=new_id, sequence=merged_seq)

        # Aktualisiere den Graphen
        self.remove_fragment(source)
        self.remove_fragment(target)
        self.add_fragment(new_fragment)

        return new_fragment

    @property
    def edges(self) -> List[Overlap]:
        return self._edges

    @property
    def fragments(self) -> List[Fragment]:
        return self._fragments