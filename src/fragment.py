class Fragment:
    """
    Repräsentiert ein einzelnes DNA-Fragment.

    Attribute:
        _id (int oder str): Eine eindeutige Kennung für das Fragment.
        _sequence (str): Die DNA-Sequenz des Fragments.
    """

    def __init__(self, id: int | str, sequence: str):
        """
        Initialisiert ein neues Fragment-Objekt.

        Args:
            id (int | str): Eine eindeutige Kennung für das Fragment.
            sequence (str): Die DNA-Sequenz des Fragments.
        """
        if not isinstance(sequence, str) or not sequence:
            raise ValueError("Die Sequenz muss ein nicht-leerer String sein.")
        if not all(base in "ATGCatgc" for base in sequence):
            # Prüft, ob die Sequenz nur gültige DNA-Basen enthält.
            # Erlaubt Groß- und Kleinbuchstaben, normalisiert aber nicht
            print(f"Warnung: Fragment {id} enthält möglicherweise ungültige Basen: {sequence}")
        
        self._id = id
        self._sequence = sequence.upper() # Normalisiert zu Großbuchstaben

    def get_sequence(self) -> str:
        """
        Gibt die DNA-Sequenz des Fragments zurück.

        Returns:
            str: Die DNA-Sequenz.
        """
        return self._sequence

    def get_id(self) -> int | str:
        """
        Gibt die eindeutige Kennung des Fragments zurück.

        Returns:
            int | str: Die ID des Fragments.
        """
        return self._id

    def __len__(self) -> int:
        """
        Gibt die Länge der DNA-Sequenz des Fragments zurück.
        Ermöglicht die Verwendung von len(fragment_obj).

        Returns:
            int: Die Länge der Sequenz.
        """
        return len(self._sequence)

    def __str__(self) -> str:
        """
        Gibt eine lesbare String-Repräsentation des Fragments zurück.

        Returns:
            str: Eine String-Repräsentation.
        """
        return f"Fragment(ID: {self._id}, Seq: '{self._sequence[:20]}...')" # Zeigt nur die ersten 20 Basen

    def __repr__(self) -> str:
        """
        Gibt eine offizielle String-Repräsentation des Fragments zurück,
        die zur Rekonstruktion des Objekts verwendet werden könnte.

        Returns:
            str: Eine String-Repräsentation.
        """
        return f"Fragment(id='{self._id}', sequence='{self._sequence}')"

    def __hash__(self) -> int:
        """
        Ermöglicht es, Fragment-Objekte als Schlüssel in Dictionaries oder
        Elemente in Sets zu verwenden. Wichtig für die OverlapGraph-Implementierung.
        """
        return hash((self._id, self._sequence))

    def __eq__(self, other: object) -> bool:
        """
        Definiert, wann zwei Fragment-Objekte als gleich betrachtet werden.
        Wichtig für Vergleiche und Dictionary-Lookups.
        """
        if not isinstance(other, Fragment):
            return NotImplemented
        return self._id == other.get_id() and self._sequence == other.get_sequence()