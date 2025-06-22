import random
from fragment import Fragment

class FragmentGenerator:
    """
    Hilfsklasse zur Generierung synthetischer DNA-Fragmente für Testszenarien.

    Ermöglicht:
    - Erstellung eines zufälligen DNA-Strangs.
    - Fragmentierung mit gegebenem Overlap.
    - Optionales Shuffeln der Fragmente.
    - Optionales Reverse-Komplementieren eines Anteils der Fragmente.
    """

    def __init__(self, total_length: int, avg_fragment_length: int, min_overlap: int,
                 shuffle: bool = True, reverse_ratio: float = 0.4):
        if total_length <= 0:
            raise ValueError("Die Gesamtlänge des DNA-Strangs muss positiv sein.")
        if avg_fragment_length < min_overlap + 1:
            raise ValueError("Die Fragmentlänge muss größer als die minimale Overlap-Länge sein.")
        if not (0 <= reverse_ratio <= 1):
            raise ValueError("Der Reverse-Ratio muss zwischen 0 und 1 liegen.")

        self.total_length = total_length
        self.avg_fragment_length = avg_fragment_length
        self.min_overlap = min_overlap
        self.shuffle = shuffle
        self.reverse_ratio = reverse_ratio
        self.dna = None  # Original-DNA-Sequenz (wird bei Generierung gesetzt)

    @staticmethod
    def generate_random_dna(length: int) -> str:
        """Erstellt eine zufällige DNA-Sequenz mit gegebener Länge."""
        return ''.join(random.choices("ATGC", k=length))

    @staticmethod
    def fragment_sequence(sequence: str, min_overlap: int = 5, avg_length: int = 20) -> list[Fragment]:
        """
        Zerteilt eine DNA-Sequenz in sich überlappende Fragmente.

        Parameter:
            sequence (str): Die zu fragmentierende DNA-Sequenz.
            min_overlap (int): Mindestüberlappung zwischen zwei Fragmenten.
            avg_length (int): Durchschnittliche Länge der Fragmente.

        Rückgabe:
            list[Fragment]: Liste der generierten Fragmente (ungeordnet).
        """
        fragments = []
        start = 0
        idx = 0
        while start < len(sequence) - min_overlap:
            frag_len = random.randint(avg_length - 5, avg_length + 5)
            end = min(start + frag_len, len(sequence))
            frag_seq = sequence[start:end]
            fragments.append(Fragment(id=f"f{idx}", sequence=frag_seq))
            start += frag_len - min_overlap
            idx += 1
        return fragments

    @staticmethod
    def randomly_reverse_some_fragments(fragments: list[Fragment], ratio: float = 0.4) -> list[Fragment]:
        """
        Erzeugt bei einem gegebenen Anteil Reverse Complements der Fragmente.

        Parameter:
            fragments (list[Fragment]): Ursprüngliche Fragmentliste.
            ratio (float): Anteil der Fragmente, die als Reverse Complement vorliegen sollen.

        Rückgabe:
            list[Fragment]: Neue Liste mit ggf. umorientierten Fragmenten.
        """
        return [
            f.reverse_complement() if random.random() < ratio else f
            for f in fragments
        ]

    def generate_fragments(self) -> list[Fragment]:
        """
        Gesamtfunktion zum Erzeugen zufälliger DNA-Fragmente mit optionalem Shuffling und Reverse Complement.

        Rückgabe:
            list[Fragment]: Veränderte Fragmentliste.
        """
        # 1. Generiere Original-DNA
        self.dna = FragmentGenerator.generate_random_dna(self.total_length)

        # 2. Erzeuge Fragmente mit Overlap
        fragments = FragmentGenerator.fragment_sequence(
            sequence=self.dna,
            min_overlap=self.min_overlap,
            avg_length=self.avg_fragment_length
        )

        # 3. Optional: Shuffle
        if self.shuffle:
            random.shuffle(fragments)

        # 4. Optional: Reverse Complements einfügen
        if self.reverse_ratio > 0:
            fragments = FragmentGenerator.randomly_reverse_some_fragments(fragments, self.reverse_ratio)

        return fragments
