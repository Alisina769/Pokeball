from color import Color


class Pokeball:
    """Stellt einen Pokeball dar, der in eine Bitmap gerendert werden kann.
    Der Pokeball besteht aus einer roten oberen und einer weißen unteren
    Hälfte, einem schwarzen Band, einem schwarzen Ring und einem weißen
    Kreis in der Mitte.
    """

    def __init__(self, center_x, center_y, radius):
        """Speichert Mittelpunkt und Radius und berechnet die Bandbreite."""
        self.__center_x = center_x
        self.__center_y = center_y
        self.__radius = radius
        self.__band_width = Pokeball.__calc_band_width(radius)

    @staticmethod
    def __calc_band_width(radius):
        """Berechnet die Dicke vom schwarzen Band (immer ungerade)."""
        half = max(1, radius // 10)
        return 2 * half + 1

    @staticmethod
    def __is_inside_circle(px, py, cx, cy, r):
        """True, wenn der Punkt im Kreis liegt."""
        a = px - cx
        b = py - cy
        if r * r >= a * a + b * b:
            return True
        return False

    def __render_circle(self, bitmap, cx, cy, r, color):
        """Zeichnet einen ausgefüllten Kreis."""
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if Pokeball.__is_inside_circle(x, y, cx, cy, r):
                    bitmap.set_pixel(x, y, color)

    def __render_upper_half(self, bitmap):
        """Zeichnet die obere Hälfte in Rot."""
        cx, cy, r = self.__center_x, self.__center_y, self.__radius
        for y in range(cy - r, cy):
            for x in range(cx - r, cx + r + 1):
                if Pokeball.__is_inside_circle(x, y, cx, cy, r):
                    bitmap.set_pixel(x, y, Color.RED)

    def __render_lower_half(self, bitmap):
        """Zeichnet die untere Hälfte in Weiß."""
        cx, cy, r = self.__center_x, self.__center_y, self.__radius
        for y in range(cy, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if Pokeball.__is_inside_circle(x, y, cx, cy, r):
                    bitmap.set_pixel(x, y, Color.WHITE)

    def __render_band(self, bitmap):
        """Zeichnet das schwarze Band durch die Mitte."""
        cx, cy, r = self.__center_x, self.__center_y, self.__radius
        half = (self.__band_width - 1) // 2
        for y in range(cy - half, cy + half + 1):
            for x in range(cx - r, cx + r + 1):
                if Pokeball.__is_inside_circle(x, y, cx, cy, r):
                    bitmap.set_pixel(x, y, Color.BLACK)

    def __render_ring(self, bitmap):
        """Zeichnet den schwarzen Ring (dreifacher Durchmesser vom Band)."""

        ring_radius = (3 * self.__band_width - 1) // 2
        ring_radius = min(ring_radius, self.__radius)   # nie größer als der Ball
        self.__render_circle(bitmap, self.__center_x, self.__center_y,
                             ring_radius, Color.BLACK)

    def __render_button(self, bitmap):
        """Zeichnet den weißen Kreis in der Mitte (Durchmesser wie das Band)."""
        button_radius = (self.__band_width - 1) // 2
        self.__render_circle(bitmap, self.__center_x, self.__center_y,
                             button_radius, Color.WHITE)

    def render(self, bitmap):
        """Zeichnet den Pokeball. Die Reihenfolge ist wichtig, weil spätere Teile frühere übermalen."""
        self.__render_upper_half(bitmap)
        self.__render_lower_half(bitmap)
        self.__render_band(bitmap)
        self.__render_ring(bitmap)
        self.__render_button(bitmap)

