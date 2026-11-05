from argparse import ArgumentParser

from errors import InvalidArgumentError
from program_config import ProgramConfig


class _RaisingArgumentParser(ArgumentParser):
    """ArgumentParser, der Fehler als InvalidArgumentError meldet.
    Der normale ArgumentParser beendet bei Fehlern das Programm.
    """

    def error(self, message):
        """Löst eine InvalidArgumentError mit dem Fehlertext aus."""
        raise InvalidArgumentError(message)


class PokeballArgumentParser:
    """Wertet die Kommandozeile aus und prüft die Eingaben."""

    def __init__(self):
        """Erzeugt den Parser und legt alle Parameter fest."""
        self.__parser = self.__build_parser()

    def parse(self, args):
        """Wertet die Argumente aus und gibt eine ProgramConfig zurück."""
        namespace = self.__parser.parse_intermixed_args(args)
        config = ProgramConfig(namespace.path, namespace.width, namespace.height,
                               namespace.x, namespace.y, namespace.radius,
                               namespace.mode == "pokerush")
        self.__validate(config)
        return config

    def __build_parser(self):
        """Legt die erlaubten Parameter fest und gibt der vorbereitete ArgumentParser zurück. """

        parser = _RaisingArgumentParser(
            prog = "pokeball", add_help = False,  # add_help=False, damit "-h" für die Höhe benutzt werden kann
            description = "Rendert Pokébälle in einfache Windows-Bitmaps.")
        parser.add_argument("path", help = "Pfad der Bitmap-Datei")
        parser.add_argument("mode", nargs = "?", choices = ["pokerush"],
                            help = "'pokerush' erzeugt zufällige Pokébälle")
        parser.add_argument("-w", dest = "width", type = int,
                            help = "Breite der neuen Bitmap")
        parser.add_argument("-h", dest = "height", type = int,
                            help = "Höhe der neuen Bitmap")
        parser.add_argument("-x", dest = "x", type = int,
                            help = "x-Koordinate des Mittelpunkts")
        parser.add_argument("-y", dest = "y", type = int,
                            help = "y-Koordinate des Mittelpunkts")
        parser.add_argument("-r", dest = "radius", type = int,
                            help = "Radius des Pokéballs")
        return parser

    def __validate(self, config):
        """Prüft die Eingaben auf Widersprüche und falsche Werte."""
        if (config.width is None) != (config.height is None):
            raise InvalidArgumentError(
                "Breite (-w) und Höhe (-h) müssen zusammen angegeben werden.")
        self.__check_positive("-w", config.width)
        self.__check_positive("-h", config.height)
        self.__check_positive("-r", config.radius)

        given = [config.x, config.y, config.radius]
        if config.pokerush and any(value is not None for value in given):
            raise InvalidArgumentError(
                "Bei 'pokerush' dürfen -x, -y und -r nicht angegeben werden.")
        if not config.pokerush and any(value is not None for value in given) \
                and not config.has_pokeball():
            raise InvalidArgumentError(
                "Für einen einzelnen Pokeball müssen -x, -y und -r zusammen angegeben werden.")

    def __check_positive(self, name, value):
        """Prüft, dass ein angegebener Wert größer als 0 ist."""
        if value is not None and value <= 0:
            raise InvalidArgumentError(
                "Der Parameter " + name + " muss größer als 0 sein (angegeben: "
                + str(value) + ").")


