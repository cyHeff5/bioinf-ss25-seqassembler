import sys
import os

# Erlaube Imports aus dem src/ Verzeichnis
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from file_parser import FileParser


def main():
    # Pfad zur Datei
    filepath = os.path.join("data", "fragmentsEinzelstrang_short.txt")

    # Datei einlesen
    try:
        fragments = FileParser.parse_fragments(filepath)
        print(f"✅ {len(fragments)} Fragmente erfolgreich eingelesen.\n")

        for i, fragment in enumerate(fragments):
            print(f"{i+1}: {fragment.get_id()} - {fragment.get_sequence()}")

    except FileNotFoundError:
        print(f"❌ Datei nicht gefunden: {filepath}")
    except Exception as e:
        print(f"❌ Fehler beim Parsen: {e}")

if __name__ == "__main__":
    main()
