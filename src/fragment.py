class Fragment:
    """
    Repräsentiert ein einzelnes DNA-Fragment.

    Attribute:
        _id (int oder str): Eine eindeutige Kennung für das Fragment.
        _sequence (str): Die DNA-Sequenz des Fragments.
    """

    def __init__(self, id: int | str, sequence: str):
        if not isinstance(sequence, str) or not sequence:
            raise ValueError("Die Sequenz muss ein nicht-leerer String sein.")
        if not all(base in "ATGCatgc" for base in sequence):
            raise ValueError(f"Die Sequenz enthält möglicherweise ungültige Basen: {sequence}")

        self._id = id
        self._sequence = sequence.upper()

    @property
    def sequence(self) -> str:
        """Zugriff auf die DNA-Sequenz (öffentlich lesbar, aber geschützt gespeichert)."""
        return self._sequence

    @property
    def id(self) -> int | str:
        """Zugriff auf die ID (öffentlich lesbar, aber geschützt gespeichert)."""
        return self._id

    def reverse_complement(self) -> "Fragment":
        """
        Erzeugt das Reverse Complement der Sequenz und gibt ein neues Fragment zurück.
        """
        complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
        rc_seq = "".join(complement[base] for base in reversed(self._sequence))
        return Fragment(f"{self._id}_cf", rc_seq)
    
    def __str__(self) -> str:
        """
        String-Repräsentation des Fragments.
        """
        return f"Fragment {self._id}: {self._sequence}"
