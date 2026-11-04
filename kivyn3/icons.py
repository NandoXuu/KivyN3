import os
import re

from kivy.core.text import LabelBase

ICON_FONT_NAME = "KivyN3Icons"
CSS_PATTERN = re.compile(
    r'\.mdi-([a-z0-9-]+):before\s*\{\s*content:\s*"\\([0-9a-fA-F]+)"',
    re.IGNORECASE,
)

_glyphs = {}
_loaded = False


def load_icons(font_path, css_path):
    global _loaded
    if not os.path.isfile(font_path):
        raise FileNotFoundError(font_path)
    if not os.path.isfile(css_path):
        raise FileNotFoundError(css_path)
    with open(css_path, encoding="utf-8") as stylesheet:
        content = stylesheet.read()
    glyphs = {
        name: chr(int(codepoint, 16))
        for name, codepoint in CSS_PATTERN.findall(content)
    }
    if not glyphs:
        raise ValueError("No Material Design Icon glyphs were found in the CSS file")
    LabelBase.register(name=ICON_FONT_NAME, fn_regular=font_path)
    _glyphs.clear()
    _glyphs.update(glyphs)
    _loaded = True
    return len(_glyphs)


def icon_glyph(name):
    return _glyphs.get(str(name).strip().lower(), "")


def icon_font_name():
    return ICON_FONT_NAME if _loaded else None
