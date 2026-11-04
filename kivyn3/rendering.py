from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import (
    Color,
    Ellipse,
    Line,
    RoundedRectangle,
    StencilPop,
    StencilPush,
    StencilUnUse,
    StencilUse,
)
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    BoundedNumericProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
)
from kivy.uix.widget import Widget

from kivyn3.theme import ELEVATIONS, MOTION, SHAPES, STATE_LAYER


class M3Surface(Widget):
    shape = OptionProperty("md", options=tuple(SHAPES))
    elevation = BoundedNumericProperty(0, min=0, max=5)
    surface_color = ListProperty([1, 1, 1, 1])
    outline_color = ListProperty([0, 0, 0, 0])
    outline_width = NumericProperty(0)
    shadow_color = ListProperty([0, 0, 0, 1])
    state_color = ListProperty([0, 0, 0, 1])
    state_opacity = NumericProperty(0)
    ripple_progress = NumericProperty(0)
    ripple_alpha = NumericProperty(0)
    ripple_center = ListProperty([0, 0])
    interactive = BooleanProperty(False)
    disabled = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._hovered = False
        self._touch_key = "_kivyn3_surface_touch_" + str(self.uid)
        self._build_canvas()
        self.bind(
            pos=self._build_canvas,
            size=self._build_canvas,
            shape=self._build_canvas,
            elevation=self._build_canvas,
            surface_color=self._build_canvas,
            outline_color=self._build_canvas,
            outline_width=self._build_canvas,
            shadow_color=self._build_canvas,
        )
        self.bind(
            state_color=self._update_dynamic,
            state_opacity=self._update_dynamic,
            ripple_progress=self._update_dynamic,
            ripple_alpha=self._update_dynamic,
            ripple_center=self._update_dynamic,
        )

    def on_parent(self, _, parent):
        Window.unbind(mouse_pos=self._on_mouse_pos)
        self._hovered = False
        if parent is not None and self.interactive:
            Window.bind(mouse_pos=self._on_mouse_pos)

    def on_interactive(self, _, value):
        Window.unbind(mouse_pos=self._on_mouse_pos)
        if value and self.parent is not None:
            Window.bind(mouse_pos=self._on_mouse_pos)
        if not value:
            self._hovered = False
            if hasattr(self, "_hovered"):
                self._animate_state(0)

    def _radius(self):
        return max(0, min(dp(SHAPES[self.shape]), max(0, min(self.width, self.height)) / 2))

    def _build_canvas(self, *args):
        self.canvas.before.clear()
        x, y = self.pos
        w, h = self.size
        radius = self._radius()
        with self.canvas.before:
            for dy, spread, alpha in ELEVATIONS.get(int(self.elevation), ()):
                Color(*self.shadow_color[:3], alpha)
                RoundedRectangle(
                    pos=(x - dp(spread), y - dp(spread) - dp(dy)),
                    size=(w + 2 * dp(spread), h + 2 * dp(spread)),
                    radius=[radius + dp(spread)] * 4,
                )

            Color(*self.surface_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[radius] * 4)

            StencilPush()
            RoundedRectangle(pos=self.pos, size=self.size, radius=[radius] * 4)
            StencilUse()
            self._state_instr = Color(0, 0, 0, 0)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[radius] * 4)
            self._ripple_instr = Color(0, 0, 0, 0)
            self._ripple_shape = Ellipse(pos=(0, 0), size=(0, 0))
            StencilUnUse()
            RoundedRectangle(pos=self.pos, size=self.size, radius=[radius] * 4)
            StencilPop()

            if self.outline_width > 0:
                Color(*self.outline_color)
                half = self.outline_width / 2
                Line(
                    rounded_rectangle=(x + half, y + half, w - 2 * half, h - 2 * half, radius),
                    width=self.outline_width,
                )
        self._update_dynamic()

    def _update_dynamic(self, *args):
        if not hasattr(self, "_state_instr"):
            return
        red, green, blue = self.state_color[:3]
        self._state_instr.rgba = [red, green, blue, self.state_opacity]
        self._ripple_instr.rgba = [red, green, blue, self.ripple_alpha]
        radius = max(self.width, self.height) * self.ripple_progress
        cx, cy = self.ripple_center
        self._ripple_shape.pos = (cx - radius, cy - radius)
        self._ripple_shape.size = (radius * 2, radius * 2)

    def _animate_state(self, opacity):
        Animation.cancel_all(self, "state_opacity")
        Animation(
            state_opacity=opacity,
            duration=MOTION["short"],
            t=MOTION["standard"],
        ).start(self)

    def _start_ripple(self, pos):
        self.ripple_center = [pos[0], pos[1]]
        Animation.cancel_all(self, "ripple_progress", "ripple_alpha")
        self.ripple_progress = 0
        self.ripple_alpha = STATE_LAYER["pressed"]
        Animation(
            ripple_progress=1,
            duration=MOTION["long"],
            t=MOTION["emphasized"],
        ).start(self)

    def _fade_ripple(self):
        Animation.cancel_all(self, "ripple_alpha")
        Animation(
            ripple_alpha=0,
            duration=MOTION["medium"],
            t=MOTION["standard"],
        ).start(self)

    def _on_mouse_pos(self, _, pos):
        if not self.interactive or self.disabled or self.parent is None:
            return
        hovered = self.collide_point(*pos)
        if hovered != self._hovered:
            self._hovered = hovered
            self._animate_state(STATE_LAYER["hover"] if hovered else 0)

    def on_touch_down(self, touch):
        if (
            self.interactive
            and not self.disabled
            and not touch.is_mouse_scrolling
            and self.collide_point(*touch.pos)
        ):
            touch.ud[self._touch_key] = True
            self._start_ripple(touch.pos)
            self._animate_state(STATE_LAYER["pressed"])
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.ud.pop(self._touch_key, False):
            self._animate_state(STATE_LAYER["hover"] if self._hovered else 0)
            self._fade_ripple()
        return super().on_touch_up(touch)
