import os
import sys

from argument_parser import PokeballArgumentParser
from bitmap import Bitmap
from color import Color
from errors import BitmapFormatError, InvalidArgumentError
from pokeball import Pokeball
from pokerush_generator import PokerushGenerator


class Main:
    """Steuert den Programmablauf: Eingaben auswerten, Bitmap laden oder
    erzeugen, Pokebälle rendern und die Datei speichern."""

    def __init__(self):
        """Erzeugt den Parser."""
        self.__parser = PokeballArgumentParser()

    def run(self, args=None):
        """Führt das Programm aus und gibt 0 (Erfolg) oder 1 (Fehler) zurück."""
        if args is None:
            args = sys.argv[1:]
        try:
            config = self.__parser.parse(args)
            bitmap = self.__load_or_create_bitmap(config)
            self.__render_pokeballs(config, bitmap)
            bitmap.write(config.path)
        except (InvalidArgumentError, BitmapFormatError) as error:
            self.__print_error(str(error))
            return 1
        except OSError as error:
            self.__print_error("Dateifehler: " + str(error))
            return 1
        print("Fertig: " + config.path)
        return 0

    def __load_or_create_bitmap(self, config):
        """Liest die vorhandene Bitmap oder erzeugt eine neue graue."""
        if os.path.isdir(config.path):
            raise InvalidArgumentError(
                "Der Pfad '" + config.path + "' ist ein Ordner, keine Datei.")

        if os.path.exists(config.path):
            if config.has_size():
                print("Hinweis: -w und -h werden ignoriert, "
                      "die vorhandene Bitmap behält ihre Größe.")
            return Bitmap.read(config.path)

        if not config.has_size():
            raise InvalidArgumentError(
                "Die Datei '" + config.path + "' existiert nicht. Zum Erzeugen "
                "einer neuen Bitmap müssen -w und -h angegeben werden.")
        return Bitmap.create(config.width, config.height, Color.GRAY)

    def __render_pokeballs(self, config, bitmap):
        """Zeichnet einen oder mehrere Pokebälle in die Bitmap."""
        if config.pokerush:
            pokeballs = PokerushGenerator().generate(bitmap)
        elif config.has_pokeball():
            pokeballs = [Pokeball(config.x, config.y, config.radius)]
        else:
            width = bitmap.get_width()
            height = bitmap.get_height()
            pokeballs = [Pokeball(width // 2, height // 2, min(width, height) // 2)]

        for pokeball in pokeballs:
            pokeball.render(bitmap)

    def __print_error(self, message):
        """Gibt eine Fehlermeldung aus."""
        print("Fehler: " + message, file=sys.stderr)


if __name__ == "__main__":
    sys.exit(Main().run())