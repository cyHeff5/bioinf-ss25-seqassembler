from typing import List
from fragment import Fragment

class FileParser:
    """
    Eine Hilfsklasse zum Einlesen von DNA-Fragmenten aus einer Textdatei.

    Jede Zeile der Datei wird als ein Fragment interpretiert.
    Die Fragmente werden als Fragment-Objekte mit eindeutiger ID zurückgegeben.
    """

    @staticmethod
    def parse_fragments(filepath: str) -> List[Fragment]:
        """
        Liest eine Datei zeilenweise ein und wandelt jede nicht-leere Zeile
        in ein Fragment-Objekt um.
        """
        fragments: List[Fragment] = []
        try:
            with open(filepath, 'r') as f:
                fragment_id_counter = 0 # Zähler zur Vergabe eindeutiger IDs

                for line in f:
                    sequence = line.strip() # Entfernt \n und Leerzeichen
                    if sequence:
                        # Erzeuge ein Fragment-Objekt mit eindeutiger ID
                        fragments.append(Fragment(id=f"Frag_{fragment_id_counter}", sequence=sequence))
                        fragment_id_counter += 1
            return fragments
        except FileNotFoundError:
            # Falls Datei nicht existiert
            raise FileNotFoundError(f"Die Datei '{filepath}' wurde nicht gefunden.")
        except Exception as e:
            # Allgemeiner Fehler beim Einlesen
            raise IOError(f"Fehler beim Lesen der Datei '{filepath}': {e}")
        