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
        self._fragments = fragments
        self._edges: List[Overlap] = []
        self._build_graph()

    def _build_graph(self):
        print("\n[⚙️  OverlapGraph] Baue Overlap-Graph auf...")
        count = 0
        for a in self.fragments:
            for b in self.fragments:
                if a != b:
                    overlap_len = self._compute_overlap(a.sequence, b.sequence)
                    if overlap_len > 0:
                        self._edges.append(Overlap(a, b, overlap_len))
                        print(f"  ➤ Kante: {a.id} → {b.id} (Overlap: {overlap_len})")
                        count += 1
        print(f"[✅ OverlapGraph] Aufbau abgeschlossen. {count} Kanten erzeugt.\n")

    @staticmethod
    def _compute_overlap(seq_a: str, seq_b: str) -> int:
        max_len = min(len(seq_a), len(seq_b)) - 1
        for l in range(max_len, 0, -1):
            if seq_a[-l:] == seq_b[:l]:
                return l
        return 0

    def remove_fragment(self, fragment: Fragment):
        print(f"[–] Entferne Fragment: {fragment.id}")
        self._fragments = [f for f in self._fragments if f != fragment]
        self._edges = [e for e in self._edges if e.source != fragment and e.target != fragment]

    def add_fragment(self, new_fragment: Fragment):
        print(f"[+] Füge neues Fragment hinzu: {new_fragment.id}")
        for other in self._fragments:
            if other != new_fragment:
                len1 = self._compute_overlap(new_fragment.sequence, other.sequence)
                if len1 > 0:
                    self._edges.append(Overlap(new_fragment, other, len1))
                    print(f"  ➤ Neue Kante: {new_fragment.id} → {other.id} (Overlap: {len1})")

                len2 = self._compute_overlap(other.sequence, new_fragment.sequence)
                if len2 > 0:
                    self._edges.append(Overlap(other, new_fragment, len2))
                    print(f"  ➤ Neue Kante: {other.id} → {new_fragment.id} (Overlap: {len2})")

        self.fragments.append(new_fragment)

    def merge_and_replace(self, source: Fragment, target: Fragment, overlap_len: int) -> Fragment:
        if overlap_len <= 0:
            raise ValueError("Overlap-Länge muss positiv sein.")

        merged_seq = source.sequence + target.sequence[overlap_len:]
        new_id = f"MERGED_{OverlapGraph._merge_counter}"
        OverlapGraph._merge_counter += 1

        new_fragment = Fragment(id=new_id, sequence=merged_seq)

        print(f"\n[🔁 Merge] {source.id} + {target.id} (Overlap: {overlap_len}) → {new_id}")
        print(f"         Neue Sequenz: {merged_seq[:30]}... (Länge: {len(merged_seq)})")

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