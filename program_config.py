class ProgramConfig:
    """Speichert die Eingaben des Anwenders."""

    def __init__(self, path, width, height, x, y, radius, pokerush):
        """hier erzeugt die Konfiguration.
        parameter path: Pfad der Bitmap-Datei
        parameter width: Breite der neuen Bitmap oder None
        parameter height: Höhe der neuen Bitmap oder None
        parameter x: x-Koordinate des Mittelpunkts oder None
        parameter y: y-Koordinate des Mittelpunkts oder None
        parameter radius: Radius des Pokeballs oder None
        parameter pokerush: True, wenn zufällige Pokeballs erzeugt werden sollen
        """
        self.path = path
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.radius = radius
        self.pokerush = pokerush

    def has_size(self):
        """Prüft, ob Breite und Höhe angegeben wurden und gibt True zurück, wenn beide Werte vorhanden sind, sonst False. """
        return self.width is not None and self.height is not None

    def has_pokeball(self):
        """Prüft, ob Mittelpunkt und Radius vollständig angegeben wurden und gibt True zurück, wenn x, y und radius vorhanden sind, sonst False. """
        return self.x is not None and self.y is not None and self.radius is not None