from fragment import Fragment

class OrientationSelector:
    """
    Wählt für jedes Fragment die bessere Orientierung (Original oder Reverse Complement),
    basierend auf den Overlaps mit bereits orientierten Fragmenten.
    """

    def __init__(self, fragments: list[Fragment]):
        self.original_fragments = fragments
        self.oriented_fragments = []

    def _get_overlap(self, a: Fragment, b: Fragment, min_length: int = 1) -> int:
        max_len = min(len(a.sequence), len(b.sequence))
        for i in range(max_len, min_length - 1, -1):
            if a.sequence[-i:] == b.sequence[:i]:
                return i
        return 0

    def _total_overlap_score(self, fragment: Fragment) -> int:
        score = 0
        for f in self.oriented_fragments:
            score += self._get_overlap(f, fragment)
            score += self._get_overlap(fragment, f)
        return score

    def select_orientation(self) -> list[Fragment]:
        if not self.original_fragments:
            return []

        print("Starte Orientierungswahl...\n")

        # Erstes Fragment einfach übernehmen
        first = self.original_fragments[0]
        self.oriented_fragments.append(first)
        print(f"[1] Fragment {first.id} wird ohne Vergleich übernommen (Startpunkt)")

        for idx, fragment in enumerate(self.original_fragments[1:], start=2):
            rc = fragment.reverse_complement()

            score_orig = self._total_overlap_score(fragment)
            score_rc   = self._total_overlap_score(rc)

            print(f"\n[{idx}] Vergleich für Fragment {fragment.id}")
            print(f"   ➤ Original:       {fragment.sequence[:20]}... → Score: {score_orig}")
            print(f"   ➤ ReverseComp.:   {rc.sequence[:20]}... → Score: {score_rc}")

            if score_rc > score_orig:
                print("   → Auswahl: Reverse Complement wird hinzugefügt.")
                self.oriented_fragments.append(rc)
            else:
                print("   → Auswahl: Originalfragment wird hinzugefügt.")
                self.oriented_fragments.append(fragment)

        print("\nOrientierungswahl abgeschlossen.")
        return self.oriented_fragments
