import os

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivyn3.icons import icon_font_name, icon_glyph
from kivyn3.rendering import M3Surface
from kivyn3.theme import ROLE_NAMES, TYPOGRAPHY, get_theme


class ThemedMixin:
    def _connect_theme(self):
        get_theme().bind(on_scheme=self._on_scheme)
        self.apply_theme(get_theme())

    def _on_scheme(self, theme, *args):
        self.apply_theme(theme)

    def apply_theme(self, theme):
        pass


class M3Label(Label, ThemedMixin):
    role = OptionProperty("body-medium", options=tuple(TYPOGRAPHY))
    color_role = OptionProperty("on_surface", options=ROLE_NAMES)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._apply_role()
        self._connect_theme()

    def on_role(self, *args):
        self._apply_role()

    def on_color_role(self, *args):
        self.apply_theme(get_theme())

    def _apply_role(self):
        size, bold = TYPOGRAPHY[self.role]
        self.font_size = sp(size)
        self.bold = bold

    def apply_theme(self, theme):
        self.color = theme.colors[self.color_role]


class M3Button(ButtonBehavior, M3Surface, ThemedMixin):
    text = StringProperty("")
    icon = StringProperty("")
    variant = OptionProperty(
        "filled",
        options=("filled", "tonal", "elevated", "outlined", "text", "fab", "navigation"),
    )
    active = BooleanProperty(False)
    icon_font_size = NumericProperty(18)

    def __init__(self, text="", icon="", variant="filled", **kwargs):
        has_size = "size" in kwargs
        has_width = "width" in kwargs
        has_height = "height" in kwargs
        self._auto_width = not (has_size or has_width)
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.shape = "full"
        self.interactive = True
        self._icon_label = Label(size_hint=(None, None))
        self._text_label = M3Label(role="label-large", size_hint=(None, None))
        self._icon_label.bind(texture_size=self._icon_label.setter("size"))
        self._text_label.bind(texture_size=self._text_label.setter("size"))
        self._content = BoxLayout(orientation="horizontal", size_hint=(None, None))
        self._content.bind(
            minimum_size=self._content.setter("size"),
            size=self._fit_width,
        )
        self._content.add_widget(self._icon_label)
        self._content.add_widget(self._text_label)
        self.add_widget(self._content)
        self.bind(pos=self._place_content, size=self._place_content)
        if not has_size and not has_height:
            self.height = dp(40)
        if self._auto_width and not text:
            self.width = dp(40)
        self.text = text
        self.icon = icon
        self.variant = variant
        self._sync_content()
        self._connect_theme()

    def _sync_content(self, *args):
        if not hasattr(self, "_content"):
            return
        self._icon_label.text = icon_glyph(self.icon)
        font_name = icon_font_name()
        if font_name:
            self._icon_label.font_name = font_name
        self._icon_label.font_size = sp(self.icon_font_size)
        self._text_label.text = self.text
        self._content.spacing = dp(8) if (self.icon and self.text) else 0
        self._fit_width()

    def _fit_width(self, *args):
        if self._auto_width and hasattr(self, "_content"):
            self.width = max(dp(40), self._content.width + dp(48))

    def _place_content(self, *args):
        self._content.center = self.center

    def on_text(self, *args):
        self._sync_content()

    def on_icon(self, *args):
        self._sync_content()

    def on_icon_font_size(self, *args):
        self._sync_content()

    def on_variant(self, *args):
        self.apply_theme(get_theme())

    def on_active(self, *args):
        self.apply_theme(get_theme())

    def apply_theme(self, theme):
        if not hasattr(self, "_text_label"):
            return
        colors = theme.colors
        transparent = [*colors["surface"][:3], 0]
        foreground = colors["primary"]
        self.elevation = 0
        self.outline_width = 0
        self.outline_color = transparent
        if self.variant == "filled":
            self.surface_color = colors["primary"]
            foreground = colors["on_primary"]
        elif self.variant == "tonal":
            self.surface_color = colors["secondary_container"]
            foreground = colors["on_secondary_container"]
        elif self.variant == "elevated":
            self.surface_color = colors["surface_container_low"]
            self.elevation = 1
        elif self.variant == "outlined":
            self.surface_color = transparent
            self.outline_color = colors["outline"]
            self.outline_width = dp(1)
        elif self.variant == "fab":
            self.surface_color = colors["primary_container"]
            foreground = colors["on_primary_container"]
            self.elevation = 3
        elif self.variant == "navigation":
            if self.active:
                self.surface_color = colors["secondary_container"]
                foreground = colors["on_secondary_container"]
            else:
                self.surface_color = transparent
                foreground = colors["on_surface_variant"]
        else:
            self.surface_color = transparent
        self.state_color = foreground
        self._text_label.color = foreground
        self._icon_label.color = foreground


class M3IconButton(M3Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("variant", "text")
        super().__init__(**kwargs)


class M3FAB(M3Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("size", (dp(56), dp(56)))
        kwargs["variant"] = "fab"
        super().__init__(**kwargs)
        self.shape = "lg"
        self.icon_font_size = 24


class M3Card(BoxLayout, M3Surface, ThemedMixin):
    variant = OptionProperty("elevated", options=("elevated", "filled", "outlined"))
    __events__ = ("on_release",)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape = "lg"
        self._connect_theme()

    def on_variant(self, *args):
        self.apply_theme(get_theme())

    def on_release(self, *args):
        pass

    def apply_theme(self, theme):
        colors = theme.colors
        self.state_color = colors["on_surface"]
        self.outline_width = 0
        self.outline_color = [0, 0, 0, 0]
        self.elevation = 0
        if self.variant == "filled":
            self.surface_color = colors["surface_container_highest"]
        elif self.variant == "outlined":
            self.surface_color = colors["surface"]
            self.outline_color = colors["outline_variant"]
            self.outline_width = dp(1)
        else:
            self.surface_color = colors["surface_container_low"]
            self.elevation = 1

    def on_touch_down(self, touch):
        if self.interactive and self.collide_point(*touch.pos):
            touch.ud[self.uid] = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        handled = super().on_touch_up(touch)
        if touch.ud.pop(self.uid, False) and self.interactive and not handled:
            self.dispatch("on_release")
        return handled


class M3TopAppBar(BoxLayout, M3Surface, ThemedMixin):
    title = StringProperty("")
    leading_icon = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(64)
        self.shape = "none"
        self._leading = M3IconButton(icon=self.leading_icon)
        self._title = M3Label(role="title-large", halign="left", size_hint_x=1)
        self._title.bind(size=self._title.setter("text_size"))
        self._actions = BoxLayout(orientation="horizontal", size_hint=(None, None))
        self._actions.bind(minimum_size=self._actions.setter("size"))
        self.add_widget(self._leading)
        self.add_widget(self._title)
        self.add_widget(self._actions)
        self._sync()
        self.bind(title=self._sync, leading_icon=self._sync)
        self._connect_theme()

    def _sync(self, *args):
        self._leading.icon = self.leading_icon
        self._title.text = self.title

    def add_action(self, icon, on_release=None):
        button = M3IconButton(icon=icon)
        if on_release is not None:
            button.bind(on_release=on_release)
        self._actions.add_widget(button)
        return button

    def apply_theme(self, theme):
        self.surface_color = theme.colors["surface"]
        self.state_color = theme.colors["on_surface"]
        self.elevation = 0


class M3SearchBar(BoxLayout, M3Surface, ThemedMixin):
    __events__ = ("on_search",)
    placeholder = StringProperty("Pesquisar")
    leading_icon = StringProperty("magnify")
    trailing_icon = StringProperty("")
    text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(56)
        self.shape = "full"
        self._leading = M3IconButton(variant="text", size=(dp(40), dp(40)))
        self._input = TextInput(
            text=self.text,
            hint_text=self.placeholder,
            multiline=False,
            write_tab=False,
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            foreground_color=(0.12, 0.12, 0.12, 1),
            hint_text_color=(0.4, 0.4, 0.4, 1),
            cursor_color=(0.2, 0.2, 0.2, 1),
            padding=(0, dp(17)),
            size_hint_x=1,
        )
        self._input.bind(text=self._on_input_text, on_text_validate=self._submit)
        self._trailing = M3IconButton(variant="text", size=(dp(40), dp(40)))
        self._trailing.bind(on_release=self._submit)
        self.add_widget(self._leading)
        self.add_widget(self._input)
        self.add_widget(self._trailing)
        self._sync()
        self.bind(
            placeholder=self._sync,
            leading_icon=self._sync,
            trailing_icon=self._sync,
            text=self._sync_text,
        )
        self._connect_theme()

    def _sync(self, *args):
        self._leading.icon = self.leading_icon
        self._input.hint_text = self.placeholder
        self._trailing.icon = self.trailing_icon
        self._trailing.opacity = 1 if self.trailing_icon else 0
        self._trailing.disabled = not bool(self.trailing_icon)
        self._trailing.width = dp(40) if self.trailing_icon else 0

    def _on_input_text(self, instance, value):
        if self.text != value:
            self.text = value

    def _sync_text(self, *args):
        if self._input.text != self.text:
            self._input.text = self.text

    def _submit(self, *args):
        self.dispatch("on_search", self.text)

    def focus_search(self):
        self._input.focus = True

    def clear(self):
        self.text = ""
        self._input.text = ""

    def on_search(self, text):
        pass

    def apply_theme(self, theme):
        colors = theme.colors
        self.surface_color = colors["surface_container_high"]
        self.state_color = colors["on_surface"]
        self._input.foreground_color = colors["on_surface"]
        self._input.hint_text_color = colors["on_surface_variant"]
        self._input.cursor_color = colors["primary"]
        self.elevation = 0


class M3NavigationBar(BoxLayout, M3Surface, ThemedMixin):
    __events__ = ("on_select",)
    items = ListProperty()
    current = NumericProperty(0)
    rail = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._buttons = []
        self.shape = "none"
        self._rebuild()
        self.bind(current=self._refresh_active)
        self._connect_theme()

    def on_items(self, *args):
        if hasattr(self, "_buttons"):
            self._rebuild()

    def on_rail(self, *args):
        if hasattr(self, "_buttons"):
            self._rebuild()

    def on_select(self, index):
        pass

    def select(self, index):
        if not self.items:
            return
        index = max(0, min(int(index), len(self.items) - 1))
        self.current = index
        self.dispatch("on_select", index)

    def apply_theme(self, theme):
        self.surface_color = theme.colors["surface_container"]
        self.state_color = theme.colors["on_surface"]
        self.elevation = 0

    def _rebuild(self):
        self.clear_widgets()
        self._buttons = []
        if self.rail:
            self.orientation = "vertical"
            self.size_hint = (None, 1)
            self.width = dp(80)
        else:
            self.orientation = "horizontal"
            self.size_hint = (1, None)
            self.height = dp(80)
        for index, (icon, label) in enumerate(self.items):
            self.add_widget(self._make_slot(index, icon, label))
        self._refresh_active()
        self.apply_theme(get_theme())

    def _make_slot(self, index, icon, label):
        slot = BoxLayout(orientation="vertical", spacing=dp(4))
        anchor = AnchorLayout(size_hint_y=None, height=dp(32))
        button = M3IconButton(icon=icon, variant="navigation", size=(dp(64), dp(32)))
        button.bind(on_release=lambda *args, i=index: self.select(i))
        anchor.add_widget(button)
        caption = M3Label(
            text=label,
            role="label-medium",
            halign="center",
            size_hint_y=None,
            height=dp(16),
        )
        caption.bind(size=caption.setter("text_size"))
        slot.add_widget(anchor)
        slot.add_widget(caption)
        if self.rail:
            slot.size_hint_y = None
            slot.height = dp(56)
        else:
            slot.padding = [0, dp(12), 0, 0]
        self._buttons.append(button)
        return slot

    def _refresh_active(self, *args):
        buttons = getattr(self, "_buttons", ())
        if buttons and (self.current < 0 or self.current >= len(buttons)):
            self.current = max(0, min(int(self.current), len(buttons) - 1))
            return
        for index, button in enumerate(buttons):
            button.active = index == self.current


class M3NavigationRail(M3NavigationBar):
    def __init__(self, **kwargs):
        kwargs["rail"] = True
        super().__init__(**kwargs)


for _name in (
    "M3Label",
    "M3Button",
    "M3IconButton",
    "M3FAB",
    "M3Card",
    "M3TopAppBar",
    "M3SearchBar",
    "M3NavigationBar",
    "M3NavigationRail",
):
    Factory.register(_name, module=__name__)

Builder.load_file(os.path.join(os.path.dirname(__file__), "kv", "kivyn3.kv"))
