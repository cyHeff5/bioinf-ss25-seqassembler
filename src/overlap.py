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
        self._source = source
        self._target = target
        self._length = length

    @property
    def source(self) -> Fragment:
        return self._source
    
    @property
    def target(self) -> Fragment:
        return self._target
    
    @property
    def length(self) -> int:
        return self._length