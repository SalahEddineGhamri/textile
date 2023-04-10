# representation layer --------------------------------
from textual.app import App, ComposeResult
from textual.widgets import TextLog
from textual.widgets import Button
from textual.containers import Container
from bindings import bindings
from text import generate_rich_text, \
                 colorize_text, \
                 ANALYZED_TEXT, \
                 generate_rich_analysis, \
                 generate_rich_analysis_verb

# PROGRESS IN TUI------------------------------------
# TODO: manager arguments in the TUI script >> input is selected
# ---------------------------------------------------
"""
# TODO: use it to redraw text
press = Button.Pressed(TextileApp.nouns_button)
TextileApp.nouns_button.on_button_pressed(press)
"""

TEXT_WIDTH = 80


# routines definiton when button is presed
def call_nouns():
    TextileApp.set_text(generate_rich_text(colorize_text(ANALYZED_TEXT, "NOUN"), width=TEXT_WIDTH))
    TextileApp.set_message(generate_rich_analysis(ANALYZED_TEXT))


def call_verbs():
    TextileApp.set_text(generate_rich_text(colorize_text(ANALYZED_TEXT, "VERB"), width=TEXT_WIDTH))
    TextileApp.set_message(generate_rich_analysis_verb(ANALYZED_TEXT))


def call_adjectives():
    TextileApp.set_text(generate_rich_text(colorize_text(ANALYZED_TEXT, "ADJ"), width=TEXT_WIDTH))
    TextileApp.set_message(generate_rich_analysis(ANALYZED_TEXT, group='ADJ'))

def call_adverbs():
    TextileApp.set_text(generate_rich_text(colorize_text(ANALYZED_TEXT, "ADV"), width=TEXT_WIDTH))
    TextileApp.set_message(generate_rich_analysis(ANALYZED_TEXT, group='ADV'))

# dict of all button actions
button_action = {'Nouns': call_nouns,
                 'Verbs': call_verbs,
                 'Adjectives': call_adjectives,
                 'Adverbs': call_adverbs,
                 'Conjunctions': lambda: None,
                 'Prepositions': lambda: None}


class Butt(Button):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        TextileApp.set_message(f"{self.label} pressed")
        button_action[str(self.label)]()


class TextileApp(App):
    """A Textual app as inteface to textile."""

    CSS_PATH = "TextileApp.css"
    BINDINGS = bindings

    #TODO: add redraw func
    message = None
    text = generate_rich_text(ANALYZED_TEXT, width=TEXT_WIDTH)

    # buttons
    nouns_button = Butt("Nouns")
    verbs_button = Butt("Verbs")
    adjectives_button = Butt("Adjectives")
    adverbs_button = Butt("Adverbs")
    prepositions_button = Butt("Prepositions")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(Container(TextLog(highlight=True,
                                          markup=True,
                                          id="text"),
                                  Container(self.nouns_button,
                                            self.verbs_button,
                                            self.adjectives_button,
                                            self.adverbs_button,
                                            self.prepositions_button,
                                            id="buttons"),
                                  id="text_buttons_container"),
                        TextLog(highlight=True,
                                markup=True,
                                id="analysis"),
                        id="main")

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""
        self.text_log = self.query_one("#text")
        self.analysis_log = self.query_one("#analysis")
        # write a colorful text
        self.text_log.write(self.text)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.text_log.clear()
        self.analysis_log.clear()
        self.text_log.write(TextileApp.text)

        if isinstance(TextileApp.message, list):
            for element in TextileApp.message:
                self.analysis_log.write(element)
        else:
            self.analysis_log.write(f"Heeerre {TextileApp.message}")

    @staticmethod
    def set_message(message):
        TextileApp.message = message

    @staticmethod
    def set_text(text: str) -> None:
        TextileApp.text = text


if __name__ == "__main__":
    app = TextileApp()
    app.run()
