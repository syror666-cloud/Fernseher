import doctest
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dosis  # noqa: E402
import dosisrechner  # noqa: E402


def ergebnisse(text, kg):
    return [s["ergebnis"] for s in dosis.berechne(text, kg) if "dosis_pro_kg" in s]


class TestBerechnung(unittest.TestCase):
    def test_einzelwert(self):
        self.assertEqual(ergebnisse("10 mg/kg täglich, über 7 Tage", 12.5), ["125 mg"])

    def test_bereich(self):
        self.assertEqual(ergebnisse("3 × täglich 12 - 15 mg/kg alle 8 Stunden", 10), ["120 - 150 mg"])

    def test_mehrere_werte(self):
        self.assertEqual(ergebnisse("initial: 15 mg/kg, folgend: 12 mg/kg alle 8 Stunden", 4),
                         ["60 mg", "48 mg"])

    def test_nicht_pro_kg_wird_ignoriert(self):
        segs = dosis.berechne("Plasmakonzentration von 20 µg/ml: 2 - 3 × täglich 10 mg/kg", 2)
        self.assertEqual([s["text"] for s in segs if "dosis_pro_kg" in s], ["10 mg/kg"])

    def test_maus_kleine_dosis(self):
        self.assertEqual(ergebnisse("4 - 7 mg/kg", 0.025), ["0,1 - 0,175 mg (= 100 - 175 µg)"])

    def test_grosse_dosis(self):
        self.assertEqual(ergebnisse("25 mg/kg einmalig", 600), ["15000 mg (= 15 g)"])

    def test_dezimalkomma(self):
        self.assertEqual(ergebnisse("0,5 mg/kg", 3), ["1,5 mg"])

    def test_ohne_gewicht(self):
        self.assertEqual(ergebnisse("10 mg/kg", None), [None])

    def test_doctest(self):
        self.assertEqual(doctest.testmod(dosis).failed, 0)


class TestDatenbank(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sqlite3
        cls.con = sqlite3.connect(":memory:")
        cls.con.row_factory = sqlite3.Row
        cls.con.executescript(dosisrechner.SCHEMA)
        import json
        for w in json.loads(dosisrechner.STARTDATEN.read_text(encoding="utf-8")):
            dosisrechner.speichere_wirkstoff(cls.con, w)

    def test_suche(self):
        self.assertEqual([t["name"] for t in dosisrechner.suche(self.con, "ibu")], ["Ibuprofen"])
        self.assertEqual([t["name"] for t in dosisrechner.suche(self.con, "PROFEN")], ["Ibuprofen"])
        self.assertEqual(dosisrechner.suche(self.con, "xyz"), [])

    def test_alle_dosierungen_der_seite(self):
        d = dosisrechner.wirkstoff_details(self.con, 1, 10)
        self.assertEqual(sum(len(g["dosierungen"]) for g in d["gruppen"]), 13)
        self.assertEqual(d["tierarten"], ["Pferd, Pony", "Hund", "Rind", "Kaninchen & Hase", "Maus",
                                          "Huhn, Trute, Fasan & Wachtel"])

    def test_hund_warnung(self):
        d = dosisrechner.wirkstoff_details(self.con, 1, 20, "Hund")
        self.assertEqual(len(d["gruppen"]), 1)
        h = d["gruppen"][0]["hinweise"]
        self.assertEqual(len(h), 1)
        self.assertTrue(h[0]["warnung"])

    def test_kaninchen(self):
        d = dosisrechner.wirkstoff_details(self.con, 1, 2, "Kaninchen & Hase")
        texte = [s["ergebnis"] for x in d["gruppen"][0]["dosierungen"] for s in x["segmente"]
                 if s.get("ergebnis")]
        self.assertEqual(texte, ["560 mg", "140 mg", "20 - 40 mg"])

    def test_web_export(self):
        html = dosisrechner.web_seite(self.con)
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn('"name": "Ibuprofen"', html)
        self.assertNotIn("__DATEN__", html)
        ohne = dosisrechner.web_seite(self.con, eigenstaendig=False)
        self.assertNotIn("<!doctype", ohne)


if __name__ == "__main__":
    unittest.main()
