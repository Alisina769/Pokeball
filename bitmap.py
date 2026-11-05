from color import Color
from errors import BitmapFormatError
class Bitmap:
    """Ein Bild aus Pixeln. Die Koordinate (0, 0) ist oben links, x wächst nach rechts, y nach unten."""

    def __init__(self, width, height, pixels):
        """Speichert Breite, Höhe und die Pixel."""
        self.__width = width
        self.__height = height
        self.__pixels = pixels

    @staticmethod
    def create(width, height, color):
        """Erzeugt eine neue Bitmap, deren Pixel alle dieselbe Farbe haben und wird die neue Bitmap zurück gegeben.
        hier wird parameter width für Breite in Pixeln, height für Höhe in Pixeln und color für Füllfarbe als color-Objekt gegeben. """
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(color)
            pixels.append(row)
        return Bitmap(width, height, pixels)

    def get_width(self):
        """Gibt die Breite der Bitmap in Pixeln zurück. """
        return self.__width

    def get_height(self):
        """Gibt die Höhe der Bitmap in Pixeln zurück."""
        return self.__height

    def contains(self, x, y):
        """True, wenn der Punkt im Bild liegt."""
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return True
        else:
            return False

    def set_pixel(self, x, y, color):
        """Setzt die Farbe eines Pixels. Liegt die Koordinate außerhalb der Bitmap, wird nichts geändert."""
        if self.contains(x, y):
            self.__pixels[y][x] = color

    @staticmethod
    def read(path):
        """Liest eine Bitmap aus einer Datei. Bei falschem Format gibt es einen BitmapFormatError."""
        with open(path, "rb") as file:
            data = file.read()

        width, height, offset = Bitmap.__parse_headers(data)
        pixels = Bitmap.__parse_pixel_data(data, width, height, offset)
        return Bitmap(width, height, pixels)

    @staticmethod
    def __parse_headers(data):
        """Liest Breite, Höhe und Start der Pixeldaten aus den Köpfen."""
        if len(data) < 54 or data[0:2] != b"BM":
            raise BitmapFormatError(
                "Keine gültige Bitmap-Datei (Signatur 'BM' fehlt oder Datei ist zu kurz).")

        offset = int.from_bytes(data[10:14], "little")
        width = int.from_bytes(data[18:22], "little")
        height = int.from_bytes(data[22:26], "little")
        bits = int.from_bytes(data[28:30], "little")
        compression = int.from_bytes(data[30:34], "little")

        if bits != 24 or compression != 0:
            raise BitmapFormatError(
                "Es wird nur unkomprimierte Bitmaps mit 24 Bit pro Pixel unterstützt.")
        if width <= 0 or height <= 0:
            raise BitmapFormatError(
                "Ungültige Bildgröße: Breite und Höhe müssen positiv sein.")

        return width, height, offset

    @staticmethod
    def __parse_pixel_data(data, width, height, offset):
        """Wandelt die Pixeldaten der Datei in eine Liste von Pixelzeilen um.

        Die Datei speichert die Zeilen von unten nach oben, die zurückgegebene
        Liste beginnt mit der obersten Zeile.

        parameter data: der gesamte Dateiinhalt als bytes
        parameter width: Breite in Pixeln
        parameter height: Höhe in Pixeln
        parameter offset: Position, an der die Pixeldaten beginnen
        return: Liste von Zeilen, jede Zeile eine Liste von Color-Objekten
        raises BitmapFormatError: wenn die Datei zu kurz ist
        """
        row_size = width * 3 + Bitmap.__row_padding(width)
        if len(data) < offset + row_size * height:
            raise BitmapFormatError("Die Bitmap-Datei ist unvollständig (zu wenig Pixeldaten).")

        pixels = []
        for r in range(height):
            row = []
            start = offset + r * row_size
            for x in range(width):
                p = start + x * 3
                row.append(Color.from_bgr_bytes(data[p:p + 3]))
            pixels.insert(0, row)
        return pixels

    def write(self, path):
        """Schreibt die Bitmap in eine Datei."""
        with open(path, "wb") as file:
            file.write(self.__build_file_header())
            file.write(self.__build_info_header())
            file.write(self.__build_pixel_data())
    @staticmethod
    def __row_padding(width):
        """Berechnet, wie viele Füllbytes eine Pixelzeile braucht. Es wird Anzahl der Füllbytes (0 bis 3) zurück gegeben.
        Jede Zeile einer Bitmap-Datei muss ein Vielfaches von 4 Byte lang sein. """
        bytes_row = width * 3
        rest = bytes_row % 4
        if rest == 0:
            return 0
        return 4 - rest

    def __build_pixel_data(self):
        """Wandelt alle Pixel in die Bytefolge für die Bitmap-Datei um. Es wird die Pixeldaten als bytes zurück gegeben.
        Die Zeilen werden von unten nach oben gespeichert, jede Zeile wird
        mit Füllbytes auf ein Vielfaches von 4 Byte aufgefüllt.
        """
        data = bytearray()
        padding = self.__row_padding(self.__width)

        for y in range(self.__height - 1, -1, -1):
            for x in range(self.__width):
                pixel = self.__pixels[y][x]
                data.extend(pixel.to_bgr_bytes())
            data.extend(b"\x00" * padding)

        return bytes(data)

    def __build_file_header(self):
        """Erzeugt den 14 Byte langen Dateikopf der Bitmap. Es gibt der Dateikopf als bytes zurück."""

        pixel_size = len(self.__build_pixel_data())
        header = bytearray()
        header.extend(b"BM")     # Signatur
        header.extend((54 + pixel_size).to_bytes(4, "little"))  # Dateigröße
        header.extend((0).to_bytes(4, "little"))       # reserviert
        header.extend((54).to_bytes(4, "little"))        # Start der Pixeldaten
        return bytes(header)

    def __build_info_header(self):
        """Erzeugt den 40 Byte langen Infokopf der Bitmap und es gibt der Infokopf als bytes zurück. """
        pixel_size = len(self.__build_pixel_data())
        header = bytearray()
        header.extend((40).to_bytes(4, "little"))      # Größe dieses Kopfes
        header.extend(self.__width.to_bytes(4, "little"))     # Breite
        header.extend(self.__height.to_bytes(4, "little"))      # Höhe
        header.extend((1).to_bytes(2, "little"))     # Ebenen
        header.extend((24).to_bytes(2, "little"))          # Bits pro Pixel
        header.extend((0).to_bytes(4, "little"))      # Kompression
        header.extend(pixel_size.to_bytes(4, "little"))      # Größe der Pixeldaten
        header.extend((0).to_bytes(4, "little"))   # Auflösung horizontal
        header.extend((0).to_bytes(4, "little"))      # Auflösung vertikal
        header.extend((0).to_bytes(4, "little"))      # Farben in der Palette
        header.extend((0).to_bytes(4, "little"))   # wichtige Farben
        return bytes(header)

