import os

from kivy.app import App
from kivy.core.window import Window

from kivyn3.icons import load_icons
from kivyn3.theme import get_theme
from kivyn3.widgets import M3Label


class KivyN3App(App):
    seed_color = "#6750A4"
    color_mode = "light"
    icon_font = None
    icon_css = None

    def build(self):
        if self.icon_font and self.icon_css and os.path.exists(self.icon_font) and os.path.exists(self.icon_css):
            load_icons(self.icon_font, self.icon_css)
        self.theme = get_theme()
        self.theme.seed = self.seed_color
        self.theme.mode = self.color_mode
        self.theme.bind(on_scheme=self._sync_window)
        self._sync_window()
        return self.build_root()

    def build_root(self):
        return M3Label(text="KivyN3", role="headline-medium")

    def toggle_mode(self):
        self.theme.toggle_mode()

    def _sync_window(self, *args):
        Window.clearcolor = self.theme.colors["background"]
