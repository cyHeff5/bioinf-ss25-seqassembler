import random

import sys
import os

# Erlaube Imports aus dem src/ Verzeichnis
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fragment import Fragment
from overlap_graph import OverlapGraph
from greedy_assembler import GreedyAssembler
from orientation_selector import OrientationSelector

def generate_random_dna(length: int) -> str:
    return ''.join(random.choices("ATGC", k=length))

def fragment_sequence(sequence: str, min_overlap: int = 5, avg_length: int = 20) -> list[Fragment]:
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
    #random.shuffle(fragments)
    return fragments

def randomly_reverse_some_fragments(fragments: list[Fragment], ratio: float = 0.4) -> list[Fragment]:
    """
    Wählt zufällig einige Fragmente aus und ersetzt sie durch ihr Reverse Complement.
    """
    reversed_fragments = []
    for f in fragments:
        if random.random() < ratio:
            reversed_fragments.append(f.reverse_complement())
        else:
            reversed_fragments.append(f)
    return reversed_fragments

def pause(msg="🔸 Drücke Enter, um fortzufahren..."):
    input(msg)

def test_orientation_selector_and_greedy():
    print("🧬 Test: OrientationSelector + GreedyAssembler")

    # Schritt 1: DNA erzeugen
    original_seq = generate_random_dna(5000)
    print(f"Original DNA:\n{original_seq}\n")
    pause()

    # Schritt 2: Fragmentieren
    fragments = fragment_sequence(original_seq, min_overlap=40, avg_length=100)
    print(f"{len(fragments)} Fragmente erzeugt (unorientiert):")
    for frag in fragments:
        print(f" - {frag.id}: {frag.sequence}")
    pause()

    # Schritt 3: Einige Fragmente umdrehen
    scrambled_fragments = randomly_reverse_some_fragments(fragments)
    print("🔁 Zufällige Fragmente wurden gedreht:")
    for frag in scrambled_fragments:
        print(f" - {frag.id}: {frag.sequence}")
    pause()

    # Schritt 4: OrientationSelector anwenden
    selector = OrientationSelector(scrambled_fragments)
    oriented_fragments = selector.select_orientation()
    print("📐 Orientierung gewählt:")
    for frag in oriented_fragments:
        print(f" - {frag.id}: {frag.sequence}")
    pause()

    # Schritt 5: Assemblieren
    graph = OverlapGraph(oriented_fragments)
    assembler = GreedyAssembler(graph)
    assembled = assembler.assemble()
    print(f"🔧 Assemblierte Sequenz:\n{assembled}\n")
    pause()

    # Schritt 6: Vergleich
    if assembled.sequence == original_seq:
        print("✅ Erfolg: Die Sequenz wurde korrekt rekonstruiert!")
    else:
        print("❌ Fehler: Die rekonstruierte Sequenz stimmt nicht mit dem Original überein.")

if __name__ == "__main__":
    test_orientation_selector_and_greedy()
