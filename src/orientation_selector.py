from fragment import Fragment

class OrientationSelector:
    """
    Diese Klasse implementiert zwei Varianten zur Wahl der Orientierung (Original oder Reverse Complement)
    für eine Liste von DNA-Fragmenten, basierend auf der Stärke ihrer Overlaps.
    """

    def __init__(self, fragments: list[Fragment]):
        # Ursprüngliche Liste der ungeordneten und nicht-orientierten Fragmente
        self.initial_fragments = fragments

    def _get_overlap(self, a: Fragment, b: Fragment, min_length: int = 1) -> int:
        """
        Berechnet die maximale Overlap-Länge zwischen dem Suffix von a und dem Präfix von b.
        Gibt 0 zurück, wenn kein Overlap vorhanden ist.
        """
        max_len = min(len(a.sequence), len(b.sequence))
        for i in range(max_len, min_length - 1, -1):
            if a.sequence[-i:] == b.sequence[:i]:
                return i
        return 0

    def _total_overlap_score(self, fragment: Fragment, reference_list: list[Fragment]) -> int:
        """
        Berechnet die gesamte Overlap-Summe eines Fragments zu allen Fragmenten in der Referenzliste.
        Dabei wird sowohl der Overlap von fragment - ref als auch ref - fragment berücksichtigt.
        """
        return sum(
            self._get_overlap(fragment, ref) + self._get_overlap(ref, fragment)
            for ref in reference_list
        )

    def select_orientation_local(self) -> list[Fragment]:
        """
        Lokaler Greedy-Ansatz:
        Iteriert durch die ursprüngliche Reihenfolge der Fragmente und entscheidet für jedes Fragment
        lokal, ob Original oder Reverse Complement besser zu den bereits orientierten Fragmenten passt.
        """
        print("[OrientationSelector] Starte lokale Orientierungswahl...")
        oriented = []

        for idx, fragment in enumerate(self.initial_fragments):
            rc = fragment.reverse_complement()
            score_f = self._total_overlap_score(fragment, oriented)
            score_rc = self._total_overlap_score(rc, oriented)

            print(f"\n[{idx}] Fragment {fragment.id}")
            print(f"    Original: {fragment.sequence[:20]}... - Score: {score_f}")
            print(f"    Rev. Complement: {rc.sequence[:20]}... - Score: {score_rc}")

            # Wähle die Orientierung mit dem besseren Score
            if score_rc > score_f:
                print(f"    Entscheidung: Reverse Complement wird gewählt.")
                oriented.append(rc)
            else:
                print(f"    Entscheidung: Originalfragment wird gewählt.")
                oriented.append(fragment)
        print("[OrientationSelector] Lokale Orientierungsauswahl abgeschlossen.")
        return oriented

    def select_orientation_global(self) -> list[Fragment]:
        """
        Globaler Greedy-Ansatz:
        Wählt zuerst global das beste Startfragment (mit höchstem Overlap zu allen anderen).
        Fügt danach iterativ das beste nächste Fragment hinzu, das den höchsten Overlap zu allen
        bereits orientierten Fragmenten besitzt (inkl. Richtungswahl).
        """
        print("[OrientationSelector] Starte globale Orientierungswahl... \n")
        fragments = self.initial_fragments[:]
        oriented = []

        best_fragment = None
        best_score = -1

        # Suche Startfragment mit höchstem Gesamtscore zu allen anderen Fragmenten
        print("[OrientationSelector] Suche bestes Startfragment")
        for fragment in fragments:
            rc = fragment.reverse_complement()
            score_f = self._total_overlap_score(fragment, fragments)
            score_rc = self._total_overlap_score(rc, fragments)

            if score_f > best_score:
                best_score = score_f
                best_fragment = fragment
            if score_rc > best_score:
                best_score = score_rc
                best_fragment = rc

        print(f"    Startfragment gewählt: {best_fragment.id} (Score: {best_score})")
        oriented.append(best_fragment)

        # Entferne Original (egal ob f oder cf) aus Liste der verbleibenden
        fragments = [f for f in fragments if f.id != best_fragment.id.replace("_cf", "")]

        step = 2
        while fragments:
            best_next = None
            best_score = -1
            best_id = None
            print(f"[OrientationSelector] [{step}] Auswahl nächstes bestes Fragment:")

            for fragment in fragments:
                rc = fragment.reverse_complement()
                score_f = self._total_overlap_score(fragment, oriented)
                score_rc = self._total_overlap_score(rc, oriented)

                if score_f > best_score:
                    best_next = fragment
                    best_score = score_f
                    best_id = fragment.id
                if score_rc > best_score:
                    best_next = rc
                    best_score = score_rc
                    best_id = fragment.id

            print(f"    Hinzugefügt: {best_next.id} (Score: {best_score})")
            oriented.append(best_next)
            fragments = [f for f in fragments if f.id != best_id]
            step += 1

        print("[OrientationSelector] Globale Orientierungsauswahl abgeschlossen.")
        return oriented
