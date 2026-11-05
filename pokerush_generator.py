from random import Random

from errors import InvalidArgumentError
from pokeball import Pokeball


class PokerushGenerator:
    """Erzeugt zufällige Pokebälle für 'pokerush'."""

    MIN_COUNT = 10
    MAX_COUNT = 100
    MIN_RADIUS = 10

    def __init__(self, seed=None):
        """Erzeugt den Zufallsgenerator (seed ist nur für Tests)."""
        self.__random = Random(seed)

    def generate(self, bitmap):
        """Gibt eine Liste zufälliger Pokebälle zurück. Ist die Bitmap zu klein, gibt es einen InvalidArgumentError."""

        if self.__max_radius(bitmap) < PokerushGenerator.MIN_RADIUS:
            raise InvalidArgumentError(
                "Die Bitmap ist für 'pokerush' zu klein: Die kleinere Kante muss "
                "mindestens " + str(2 * PokerushGenerator.MIN_RADIUS) + " Pixel lang sein.")

        pokeballs = []
        for _ in range(self.__random_count()):
            x, y = self.__random_center(bitmap)
            radius = self.__random_radius(bitmap)
            pokeballs.append(Pokeball(x, y, radius))
        return pokeballs

    def __random_count(self):
        """Wählt die Anzahl der Pokebälle (10 bis 100)."""
        return self.__random.randint(PokerushGenerator.MIN_COUNT,
                                     PokerushGenerator.MAX_COUNT)

    def __max_radius(self, bitmap):
        """Gibt die Hälfte der kleineren Kante zurück."""
        return min(bitmap.get_width(), bitmap.get_height()) // 2

    def __random_radius(self, bitmap):
        """Wählt einen Radius zwischen 10 und dem größten erlaubten."""
        return self.__random.randint(PokerushGenerator.MIN_RADIUS,
                                     self.__max_radius(bitmap))

    def __random_center(self, bitmap):
        """Wählt einen Mittelpunkt im Bild."""
        x = self.__random.randint(0, bitmap.get_width() - 1)
        y = self.__random.randint(0, bitmap.get_height() - 1)
        return x, y


