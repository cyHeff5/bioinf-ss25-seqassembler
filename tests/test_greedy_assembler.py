import random

import sys
import os

# Erlaube Imports aus dem src/ Verzeichnis
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fragment import Fragment
from overlap_graph import OverlapGraph
from greedy_assembler import GreedyAssembler

def generate_random_dna(length: int) -> str:
    return ''.join(random.choices("ATGC", k=length))

def fragment_sequence(sequence: str, min_overlap: int = 5, avg_length: int = 20) -> list[Fragment]:
    """
    Zerlegt die DNA-Sequenz in überlappende Fragmente.
    Jeder neue Startpunkt überlappt mit mindestens `min_overlap` Zeichen.
    """
    fragments = []
    start = 0
    idx = 0
    while start < len(sequence) - min_overlap:
        frag_len = random.randint(avg_length - 5, avg_length + 5)
        end = min(start + frag_len, len(sequence))
        frag_seq = sequence[start:end]
        fragments.append(Fragment(id=f"f{idx}", sequence=frag_seq))
        start += frag_len - min_overlap  # sorgt für den gewünschten Overlap
        idx += 1
    random.shuffle(fragments)
    return fragments

def test_greedy_assembler():
    print("🔬 Starte Test für Einzelstrang-Greedy-Assembler...")

    # Schritt 1: Generiere DNA-Sequenz
    original_seq = generate_random_dna(10000)
    print(f"Original DNA (100 bp):\n{original_seq}\n")

    input("Drücke Enter um fortzufahren")

    # Schritt 2: Zerlege in Fragmente mit Overlap
    fragments = fragment_sequence(original_seq, min_overlap=20, avg_length=100)
    print(f"Erzeugte {len(fragments)} Fragmente:")
    for frag in fragments:
        print(f"  - {frag.id}: {frag.sequence}")

    input("Drücke Enter um fortzufahren")

    # Schritt 3: Assemblieren mit GreedyAssembler
    graph = OverlapGraph(fragments)
    assembler = GreedyAssembler(graph)
    assembled_seq = assembler.assemble()

    input("Drücke Enter um fortzufahren")


    # Schritt 4: Ergebnis prüfen
    print("\n🧬 Assemblierte Sequenz:")
    print(assembled_seq)
    print(f"\n✅ Übereinstimmung mit Original: {assembled_seq.sequence == original_seq}")

if __name__ == "__main__":
    test_greedy_assembler()
