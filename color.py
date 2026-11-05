class Color:
    """Stellt eine Farbe aus Rot, Grün und Blau."""

    RED = None
    WHITE = None
    BLACK = None
    GRAY = None

    def __init__(self, red, green, blue):
        """Speichert die drei Farbwerte (0 bis 255)."""
        self.__red = red
        self.__green = green
        self.__blue = blue

    def to_bgr_bytes(self):
        """Gibt die Farbe als 3 Bytes in der Reihenfolge Blau, Grün, Rot zurück."""
        return bytes([self.__blue, self.__green, self.__red])

    @staticmethod
    def from_bgr_bytes(data):
        """Erzeugt eine Farbe aus 3 Bytes in der Reihenfolge Blau, Grün, Rot und gibt die neue Farbe zurück."""
        return Color(data[2], data[1], data[0])


Color.RED = Color(255, 0, 0)
Color.WHITE = Color(255, 255, 255)
Color.BLACK = Color(0, 0, 0)
Color.GRAY = Color(200, 200, 200)

