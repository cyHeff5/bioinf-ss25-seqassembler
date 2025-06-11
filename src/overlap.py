# src/overlap.py

from fragment import Fragment

class Overlap:
    """
    Repräsentiert eine gerichtete Kante im Overlap-Graph:
    Fragment A hat am Ende eine Überlappung mit dem Anfang von Fragment B.

    Attribute:
        source (Fragment): Das Ausgangsfragment (Start der Kante)
        target (Fragment): Das Ziel-Fragment (Ende der Kante)
        length (int): Die Länge der Überlappung
    """

    def __init__(self, source: Fragment, target: Fragment, length: int):
        if length <= 0:
            raise ValueError("Overlap-Länge muss positiv sein.")
        self.source = source
        self.target = target
        self.length = length

    def __repr__(self) -> str:
        return f"Overlap({self.source.get_id()} → {self.target.get_id()}, len={self.length})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Overlap):
            return NotImplemented
        return (
            self.source == other.source
            and self.target == other.target
            and self.length == other.length
        )

    def __hash__(self) -> int:
        return hash((self.source, self.target, self.length))
