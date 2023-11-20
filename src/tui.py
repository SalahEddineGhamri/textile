# representation layer --------------------------------
from textual.app import App, ComposeResult
from textual.widgets import RichLog
from textual.widgets import Button
from textual.containers import Container
from config.bindings import bindings
from config.config import INPUT_PATH
from text import Blackboard, TextAnalyzer

"""
# TODO: use it to redraw text
press = Button.Pressed(TextileApp.nouns_button)
TextileApp.nouns_button.on_button_pressed(press)
"""

# create blackboard
blackboard = Blackboard(INPUT_PATH)

# analyze text
TextAnalyzer(blackboard.manager)


# routines definiton when button is presed
def call_nouns():
    TextileApp.set_text(blackboard.manager["nouns_rich_text"])
    TextileApp.set_message(blackboard.manager["nouns_rich_analysis"])


def call_verbs():
    TextileApp.set_text(blackboard.manager["verbs_rich_text"])
    TextileApp.set_message(blackboard.manager["verbs_rich_analysis"])


def call_adjectives():
    TextileApp.set_text(blackboard.manager["adjectives_rich_text"])
    TextileApp.set_message(blackboard.manager["adjectives_rich_analysis"])


def call_adverbs():
    TextileApp.set_text(blackboard.manager["adverbs_rich_text"])
    TextileApp.set_message(blackboard.manager["adverbs_rich_analysis"])


def call_prepositions():
    TextileApp.set_text(blackboard.manager["prepositions_rich_text"])
    TextileApp.set_message(blackboard.manager["prepositions_rich_analysis"])


# actions dictionary
button_action = {
    "Nouns": call_nouns,
    "Verbs": call_verbs,
    "Adjectives": call_adjectives,
    "Adverbs": call_adverbs,
    "Prepositions": call_prepositions,
}


class Butt(Button):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        TextileApp.set_message(f"{self.label} pressed")
        button_action[str(self.label)]()


class TextileApp(App):
    """A Textual app as inteface to textile."""

    CSS_PATH = "css/TextileApp.css"
    BINDINGS = bindings

    message = None
    text = blackboard.manager["text"]

    # buttons
    nouns_button = Butt("Nouns")
    verbs_button = Butt("Verbs")
    adjectives_button = Butt("Adjectives")
    adverbs_button = Butt("Adverbs")
    prepositions_button = Butt("Prepositions")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(
            Container(
                RichLog(
                    highlight=True, markup=True, wrap=True, min_width=78, id="text"
                ),
                Container(
                    self.nouns_button,
                    self.verbs_button,
                    self.adjectives_button,
                    self.adverbs_button,
                    self.prepositions_button,
                    id="buttons",
                ),
                id="text_buttons_container",
            ),
            RichLog(highlight=True, markup=True, id="analysis"),
            id="main",
        )

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
            self.analysis_log.write(f"Processing ... {TextileApp.message}")

    @staticmethod
    def set_message(message):
        TextileApp.message = message

    @staticmethod
    def set_text(text: str) -> None:
        TextileApp.text = text


if __name__ == "__main__":
    app = TextileApp()
    app.run()
