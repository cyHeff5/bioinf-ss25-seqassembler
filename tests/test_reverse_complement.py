import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fragment import Fragment

def test_reverse_complement():
    original = Fragment("F1", "AGTCCTAT")
    reverse = original.reverse_complement()

    print(f"Original ID:   {original.id}")
    print(f"Original Seq:  {original.sequence}")
    print(f"Reverse ID:    {reverse.id}")
    print(f"Reverse Seq:   {reverse.sequence}")

    # Optionaler einfacher Check
    expected = "TCGACT"
    assert reverse.sequence == expected, f"Expected {expected}, got {reverse.sequence}"

if __name__ == "__main__":
    test_reverse_complement()
