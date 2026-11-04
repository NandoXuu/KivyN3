import os

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty

from kivyn3 import KivyN3App, M3Card

HERE = os.path.dirname(os.path.abspath(__file__))


class MailCard(M3Card):
    sender = StringProperty("")
    time_text = StringProperty("")
    subject = StringProperty("")
    preview = StringProperty("")
    selected = BooleanProperty(False)

    def on_selected(self, *args):
        self.variant = "filled" if self.selected else "outlined"


Factory.register("MailCard", cls=MailCard)

KV = """
#:import dp kivy.metrics.dp

<MailCard>:
    size_hint_y: None
    height: dp(160)
    shape: "xl"
    interactive: True
    BoxLayout:
        size_hint_y: None
        height: dp(42)
        spacing: dp(8)
        M3IconButton:
            icon: "account-circle"
        BoxLayout:
            orientation: "vertical"
            M3Label:
                text: root.sender
                role: "title-small"
            M3Label:
                text: root.time_text
                role: "label-small"
                color_role: "on_surface_variant"
        M3IconButton:
            icon: "star-outline"
    M3Label:
        text: root.subject
        role: "title-medium"
        size_hint_y: None
        height: self.texture_size[1]
    M3Label:
        text: root.preview
        role: "body-medium"
        color_role: "on_surface_variant"
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        halign: "left"

FloatLayout:
    BoxLayout:
        padding: dp(8)
        spacing: dp(8)

        M3NavigationRail:
            items: [("pencil", "Escrever"), ("inbox", "Entrada"), ("file-document-outline", "Rascunhos"), ("comment-outline", "Chat")]
            current: 1

        BoxLayout:
            orientation: "vertical"
            spacing: dp(8)

            M3TopAppBar:
                title: "Entrada"
                leading_icon: "menu"

            M3SearchBar:
                placeholder: "Pesquisar e-mails"
                trailing_icon: "account-circle"

            BoxLayout:
                spacing: dp(12)

                ScrollView:
                    size_hint_x: 0.45
                    do_scroll_x: False

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(12)
                        padding: dp(4)

                        MailCard:
                            sender: "Google"
                            time_text: "20 min atrás"
                            subject: "Pacote enviado!"
                            preview: "Sua máscara facial de pepino já saiu para entrega..."

                        MailCard:
                            sender: "Ali"
                            time_text: "40 min atrás"
                            subject: "Brunch no fim de semana?"
                            preview: "Vou estar no seu bairro resolvendo algumas coisas e queria te encontrar..."

                        MailCard:
                            sender: "Allison"
                            time_text: "1 hora atrás"
                            subject: "Olá de Paris"
                            preview: "Aqui estão algumas fotos incríveis da minha viagem..."

                        MailCard:
                            sender: "Kim"
                            time_text: "2 horas atrás"
                            subject: "Reunião do ensino médio?"
                            preview: "Oi, pessoal..."
                            selected: True

                M3Card:
                    variant: "outlined"
                    shape: "xl"
                    size_hint_x: 0.55
                    padding: dp(24)
                    spacing: dp(12)

                    M3Label:
                        text: "Reunião do ensino médio?"
                        role: "headline-small"
                        size_hint_y: None
                        height: self.texture_size[1]

                    M3Label:
                        text: "De Kim · 2 horas atrás"
                        role: "body-medium"
                        color_role: "on_surface_variant"
                        size_hint_y: None
                        height: self.texture_size[1]

                    M3Label:
                        text: "Oi, pessoal! Estava pensando se não seria legal a gente se reunir de novo. Alguém topa? Podemos escolher um lugar novo para jantar esta semana."
                        role: "body-large"
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_size: self.width, None
                        halign: "left"

                    Widget:

                    BoxLayout:
                        size_hint_y: None
                        height: dp(40)
                        spacing: dp(8)

                        M3Button:
                            text: "Responder"
                            variant: "tonal"

                        M3Button:
                            text: "Responder a todos"
                            variant: "outlined"

                        Widget:

        M3FAB:
            icon: "pencil"
            pos_hint: {"right": 0.98, "y": 0.04}
"""


class MailApp(KivyN3App):
    seed_color = "#6750A4"
    icon_font = os.path.join(HERE, "fonts", "materialdesignicons-webfont.ttf")
    icon_css = os.path.join(HERE, "fonts", "materialdesignicons-webfont.css")

    def build_root(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    MailApp().run()
