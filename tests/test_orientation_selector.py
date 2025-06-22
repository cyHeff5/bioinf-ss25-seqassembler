import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fragment import Fragment
from orientation_selector import OrientationSelector

def test_orientation_selector():
    # Testfragmente – bewusst so gewählt, dass eine klare Orientierung sinnvoll ist
    f1 = Fragment("F1", "AGTTGACGAG")
    f2 = Fragment("F2", "ATAGGACT")
    f3 = Fragment("F3", "ATGCCTGTTA")

    fragments = [f1, f2, f3]

    selector = OrientationSelector(fragments)
    oriented = selector.select_orientation()

    print("Ausgewählte Orientierungen:")
    for frag in oriented:
        print(f"{frag.id}: {frag.sequence}")

if __name__ == "__main__":
    test_orientation_selector()
