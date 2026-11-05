"""Einfache Tests für den Pokéball-Renderer (Start: python3 test.py)."""
import os
import subprocess
import sys
import tempfile
import unittest

from bitmap import Bitmap
from color import Color

MAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
FARBEN = {(255, 0, 0): "rot", (255, 255, 255): "weiß", (0, 0, 0): "schwarz"}


def groesse(pfad):
    """Gibt (Breite, Höhe, Dateigröße) einer Bitmap-Datei zurück."""
    with open(pfad, "rb") as datei:
        daten = datei.read()
    breite = int.from_bytes(daten[18:22], "little")
    hoehe = int.from_bytes(daten[22:26], "little")
    return breite, hoehe, len(daten)


def pixel(pfad, x, y):
    """Gibt die Farbe von Pixel (x, y) zurück: rot, weiß, schwarz oder 'andere'."""
    with open(pfad, "rb") as datei:
        daten = datei.read()
    breite = int.from_bytes(daten[18:22], "little")
    hoehe = int.from_bytes(daten[22:26], "little")
    zeilenlaenge = (breite * 3 + 3) // 4 * 4
    pos = 54 + (hoehe - 1 - y) * zeilenlaenge + x * 3
    rgb = (daten[pos + 2], daten[pos + 1], daten[pos])
    return FARBEN.get(rgb, "andere")


class Tests(unittest.TestCase):
    """Ruft main.py auf wie im Terminal und prüft das Ergebnis."""

    def setUp(self):
        """Legt einen temporären Ordner für die Testdateien an."""
        self.ordner = tempfile.TemporaryDirectory()
        self.addCleanup(self.ordner.cleanup)

    def datei(self, name):
        """Gibt den Pfad einer Testdatei im temporären Ordner zurück."""
        return os.path.join(self.ordner.name, name)

    def starte(self, *argumente):
        """Startet main.py mit den Argumenten und gibt das Ergebnis zurück."""
        return subprocess.run([sys.executable, MAIN, *argumente],
                              capture_output=True, text=True, cwd=self.ordner.name)

    def fehler(self, ergebnis):
        """Prüft: Exit-Code 1, eine Fehlermeldung und kein Traceback."""
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("Fehler", ergebnis.stderr)
        self.assertNotIn("Traceback", ergebnis.stderr)

    def test_1_neue_bitmap(self):
        """Neue Bitmap mit Ball: Größe, Dateigröße und Pixel stimmen."""
        e = self.starte("neu.bmp", "-w", "200", "-h", "100", "-x", "100", "-y", "50", "-r", "40")
        self.assertEqual(e.returncode, 0)
        self.assertEqual(groesse(self.datei("neu.bmp")), (200, 100, 60054))
        self.assertEqual(pixel(self.datei("neu.bmp"), 100, 25), "rot")
        self.assertEqual(pixel(self.datei("neu.bmp"), 100, 75), "weiß")
        self.assertEqual(pixel(self.datei("neu.bmp"), 60, 50), "schwarz")

    def test_2_ball_ohne_angaben(self):
        """Ohne -x, -y, -r liegt der Ball in der Mitte."""
        self.starte("std.bmp", "-w", "100", "-h", "100")
        self.assertEqual(pixel(self.datei("std.bmp"), 50, 10), "rot")
        self.assertEqual(pixel(self.datei("std.bmp"), 50, 50), "weiß")

    def test_3_padding(self):
        """3 x 2 Pixel ergibt 78 Byte (Füllbytes pro Zeile)."""
        self.starte("klein.bmp", "-w", "3", "-h", "2")
        self.assertEqual(groesse(self.datei("klein.bmp")), (3, 2, 78))

    def test_4_mittelpunkt_und_radius(self):
        """-x, -y und -r bestimmen Lage und Größe des Balls."""
        self.starte("a.bmp", "-w", "100", "-h", "100", "-x", "30", "-y", "30", "-r", "20")
        self.assertEqual(pixel(self.datei("a.bmp"), 30, 15), "rot")
        self.assertNotIn(pixel(self.datei("a.bmp"), 80, 80), ("rot", "schwarz"))
        self.starte("b.bmp", "-w", "100", "-h", "100", "-x", "50", "-y", "50", "-r", "10")
        self.starte("c.bmp", "-w", "100", "-h", "100", "-x", "50", "-y", "50", "-r", "30")
        self.assertNotEqual(pixel(self.datei("b.bmp"), 50, 35), "rot")
        self.assertEqual(pixel(self.datei("c.bmp"), 50, 35), "rot")

    def test_5_vorhandene_bitmap(self):
        """Zweiter Ball kommt in dieselbe Datei, die Größe bleibt gleich."""
        self.starte("neu.bmp", "-w", "200", "-h", "100", "-x", "100", "-y", "50", "-r", "40")
        self.assertNotEqual(pixel(self.datei("neu.bmp"), 30, 15), "rot")
        e = self.starte("neu.bmp", "-x", "30", "-y", "30", "-r", "20")
        self.assertEqual(e.returncode, 0)
        self.assertEqual(groesse(self.datei("neu.bmp")), (200, 100, 60054))
        self.assertEqual(pixel(self.datei("neu.bmp"), 30, 15), "rot")
        self.assertEqual(pixel(self.datei("neu.bmp"), 100, 25), "rot")

    def test_6_pokerush(self):
        """pokerush erzeugt ein Bild mit Bällen."""
        e = self.starte("rush.bmp", "pokerush", "-w", "400", "-h", "300")
        self.assertEqual(e.returncode, 0)
        self.assertEqual(groesse(self.datei("rush.bmp")), (400, 300, 360054))

    def test_7_pokerush_zu_klein(self):
        """Bei 19 Pixeln Kantenlänge gibt es einen Fehler und keine Datei."""
        self.fehler(self.starte("z.bmp", "pokerush", "-w", "19", "-h", "100"))
        self.assertFalse(os.path.exists(self.datei("z.bmp")))

    def test_8_fehlende_oder_falsche_eingaben(self):
        """Fehlerhafte Eingaben ergeben eine Fehlermeldung ohne Absturz."""
        self.fehler(self.starte())
        self.fehler(self.starte("nix.bmp"))
        self.fehler(self.starte("nix.bmp", "-w", "100"))
        self.fehler(self.starte("nix.bmp", "-w", "0", "-h", "100"))
        self.fehler(self.starte("nix.bmp", "-w", "abc", "-h", "100"))
        self.assertFalse(os.path.exists(self.datei("nix.bmp")))

    def test_9_datei_ist_keine_bitmap(self):
        """Eine Textdatei wird nicht überschrieben."""
        with open(self.datei("text.txt"), "w") as datei:
            datei.write("kein bild")
        self.fehler(self.starte("text.txt", "-x", "1", "-y", "1", "-r", "5"))
        with open(self.datei("text.txt")) as datei:
            self.assertEqual(datei.read(), "kein bild")

    def test_10_bitmap_schreiben_und_lesen(self):
        """Eine geschriebene Bitmap wird beim Lesen identisch zurückgegeben."""
        bild = Bitmap.create(5, 3, Color.WHITE)
        bild.set_pixel(0, 0, Color.RED)
        bild.write(self.datei("eins.bmp"))
        Bitmap.read(self.datei("eins.bmp")).write(self.datei("zwei.bmp"))
        with open(self.datei("eins.bmp"), "rb") as a, open(self.datei("zwei.bmp"), "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_11_farben_als_bytes(self):
        """Farben werden als Blau, Grün, Rot gespeichert."""
        self.assertEqual(Color.RED.to_bgr_bytes(), b"\x00\x00\xff")
        self.assertEqual(Color.WHITE.to_bgr_bytes(), b"\xff\xff\xff")


if __name__ == "__main__":
    unittest.main(verbosity=2)
