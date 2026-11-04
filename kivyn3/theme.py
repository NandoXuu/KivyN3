import colorsys

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, OptionProperty, StringProperty

SHAPES = {
    "none": 0,
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 28,
    "full": 9999,
}

ELEVATIONS = {
    0: (),
    1: ((1, 2, 0.14), (1, 1, 0.12)),
    2: ((2, 4, 0.16), (1, 2, 0.12)),
    3: ((4, 8, 0.18), (2, 3, 0.12)),
    4: ((6, 10, 0.20), (3, 4, 0.12)),
    5: ((8, 14, 0.22), (4, 5, 0.14)),
}

TYPOGRAPHY = {
    "display-large": (57, True),
    "display-medium": (45, True),
    "display-small": (36, True),
    "headline-large": (32, False),
    "headline-medium": (28, False),
    "headline-small": (24, False),
    "title-large": (22, False),
    "title-medium": (16, True),
    "title-small": (14, True),
    "label-large": (14, True),
    "label-medium": (12, True),
    "label-small": (11, True),
    "body-large": (16, False),
    "body-medium": (14, False),
    "body-small": (12, False),
}

STATE_LAYER = {
    "hover": 0.08,
    "focus": 0.12,
    "pressed": 0.12,
    "dragged": 0.16,
}

MOTION = {
    "short": 0.15,
    "medium": 0.25,
    "long": 0.45,
    "standard": "out_cubic",
    "emphasized": "out_quint",
}


def hex_to_rgba(value, alpha=1.0):
    if not isinstance(value, str):
        raise TypeError("seed color must be a hexadecimal string")
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if len(value) != 6:
        raise ValueError("seed color must use #RGB or #RRGGBB format")
    try:
        channels = [int(value[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    except ValueError as exc:
        raise ValueError("seed color contains invalid hexadecimal characters") from exc
    alpha = min(1.0, max(0.0, float(alpha)))
    return [*channels, alpha]


def _hsl(hue, saturation, lightness, alpha=1.0):
    red, green, blue = colorsys.hls_to_rgb(hue % 1.0, lightness, saturation)
    return [red, green, blue, alpha]


def build_scheme(seed="#6750A4", mode="light"):
    if mode not in ("light", "dark"):
        raise ValueError("mode must be 'light' or 'dark'")
    red, green, blue, _ = hex_to_rgba(seed)
    hue, _, saturation = colorsys.rgb_to_hls(red, green, blue)
    hp = hue
    ht = (hue + 1 / 6) % 1.0
    he = 0.0
    ps = min(max(saturation, 0.45), 0.9)

    if mode == "dark":
        palette = {
            "primary": (hp, ps * 0.7, 0.80),
            "on_primary": (hp, ps, 0.20),
            "primary_container": (hp, ps * 0.6, 0.30),
            "on_primary_container": (hp, ps * 0.7, 0.90),
            "secondary": (hp, 0.18, 0.80),
            "on_secondary": (hp, 0.25, 0.20),
            "secondary_container": (hp, 0.20, 0.30),
            "on_secondary_container": (hp, 0.25, 0.90),
            "tertiary": (ht, 0.45, 0.80),
            "on_tertiary": (ht, 0.50, 0.20),
            "tertiary_container": (ht, 0.40, 0.30),
            "on_tertiary_container": (ht, 0.50, 0.90),
            "error": (he, 0.75, 0.80),
            "on_error": (he, 0.80, 0.20),
            "error_container": (he, 0.70, 0.30),
            "on_error_container": (he, 0.80, 0.90),
            "background": (hp, 0.06, 0.08),
            "on_background": (hp, 0.06, 0.90),
            "surface": (hp, 0.06, 0.08),
            "on_surface": (hp, 0.06, 0.90),
            "surface_variant": (hp, 0.10, 0.30),
            "on_surface_variant": (hp, 0.10, 0.80),
            "outline": (hp, 0.08, 0.55),
            "outline_variant": (hp, 0.10, 0.30),
            "surface_container_lowest": (hp, 0.06, 0.05),
            "surface_container_low": (hp, 0.06, 0.10),
            "surface_container": (hp, 0.07, 0.12),
            "surface_container_high": (hp, 0.07, 0.17),
            "surface_container_highest": (hp, 0.08, 0.22),
            "inverse_surface": (hp, 0.06, 0.90),
            "inverse_on_surface": (hp, 0.06, 0.20),
            "inverse_primary": (hp, ps, 0.40),
            "scrim": (0.0, 0.0, 0.0),
            "shadow": (0.0, 0.0, 0.0),
        }
    else:
        palette = {
            "primary": (hp, ps, 0.40),
            "on_primary": (hp, 0.0, 1.0),
            "primary_container": (hp, ps * 0.7, 0.90),
            "on_primary_container": (hp, ps, 0.12),
            "secondary": (hp, 0.18, 0.42),
            "on_secondary": (hp, 0.0, 1.0),
            "secondary_container": (hp, 0.25, 0.90),
            "on_secondary_container": (hp, 0.25, 0.12),
            "tertiary": (ht, 0.45, 0.42),
            "on_tertiary": (ht, 0.0, 1.0),
            "tertiary_container": (ht, 0.45, 0.90),
            "on_tertiary_container": (ht, 0.50, 0.12),
            "error": (he, 0.75, 0.42),
            "on_error": (he, 0.0, 1.0),
            "error_container": (he, 0.80, 0.92),
            "on_error_container": (he, 0.80, 0.15),
            "background": (hp, 0.08, 0.98),
            "on_background": (hp, 0.08, 0.10),
            "surface": (hp, 0.08, 0.98),
            "on_surface": (hp, 0.08, 0.10),
            "surface_variant": (hp, 0.12, 0.90),
            "on_surface_variant": (hp, 0.10, 0.30),
            "outline": (hp, 0.08, 0.50),
            "outline_variant": (hp, 0.10, 0.80),
            "surface_container_lowest": (hp, 0.06, 1.00),
            "surface_container_low": (hp, 0.07, 0.96),
            "surface_container": (hp, 0.08, 0.94),
            "surface_container_high": (hp, 0.09, 0.92),
            "surface_container_highest": (hp, 0.10, 0.90),
            "inverse_surface": (hp, 0.06, 0.20),
            "inverse_on_surface": (hp, 0.05, 0.95),
            "inverse_primary": (hp, ps, 0.80),
            "scrim": (0.0, 0.0, 0.0),
            "shadow": (0.0, 0.0, 0.0),
        }

    return {role: _hsl(*value) for role, value in palette.items()}


ROLE_NAMES = tuple(build_scheme())


class ThemeManager(EventDispatcher):
    __events__ = ("on_scheme",)
    seed = StringProperty("#6750A4")
    mode = OptionProperty("light", options=("light", "dark"))
    colors = DictProperty()

    def __init__(self, seed="#6750A4", mode="light", **kwargs):
        super().__init__(**kwargs)
        self.seed = seed
        self.mode = mode
        self.bind(seed=self._rebuild, mode=self._rebuild)
        self._rebuild()

    def _rebuild(self, *args):
        self.colors = build_scheme(self.seed, self.mode)
        self.dispatch("on_scheme", self)

    def on_scheme(self, *args):
        pass

    def toggle_mode(self):
        self.mode = "dark" if self.mode == "light" else "light"


_theme = None


def get_theme():
    global _theme
    if _theme is None:
        _theme = ThemeManager()
    return _theme
