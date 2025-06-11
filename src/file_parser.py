# src/file_parser.py

from typing import List
from fragment import Fragment # Importieren der Fragment-Klasse aus der entsprechenden Datei

class FileParser:
    """
    Eine Klasse zum Parsen von Dateien, die DNA-Fragmente enthalten.
    """

    @staticmethod
    def parse_fragments(filepath: str) -> List[Fragment]:
        """
        Liest eine Datei mit DNA-Fragmenten ein und erstellt eine Liste von Fragment-Objekten.
        Jede Zeile in der Datei wird als ein einzelnes DNA-Fragment interpretiert.

        Args:
            filepath (str): Der Pfad zur Eingabedatei mit den Fragmenten.

        Returns:
            List[Fragment]: Eine Liste von Fragment-Objekten, die die eingelesenen Sequenzen darstellen.

        Raises:
            FileNotFoundError: Wenn die angegebene Datei nicht gefunden wird.
            IOError: Bei anderen Fehlern während des Dateizugriffs.
        """
        fragments: List[Fragment] = []
        try:
            with open(filepath, 'r') as f:
                fragment_id_counter = 0 # Zum Generieren eindeutiger IDs
                for line in f:
                    sequence = line.strip() # Entfernt Leerzeichen und Zeilenumbrüche
                    if sequence: # Stellt sicher, dass die Zeile nicht leer ist
                        # Erstellt ein Fragment-Objekt für jede gültige Sequenz
                        fragments.append(Fragment(id=f"Frag_{fragment_id_counter}", sequence=sequence))
                        fragment_id_counter += 1
            return fragments
        except FileNotFoundError:
            raise FileNotFoundError(f"Die Datei '{filepath}' wurde nicht gefunden.")
        except Exception as e:
            raise IOError(f"Fehler beim Lesen der Datei '{filepath}': {e}")
        