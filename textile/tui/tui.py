# representation layer --------------------------------
from textual.app import App, ComposeResult
from textual.widgets import RichLog
from textual.widgets import Button
from textual.containers import Container
from textile.config import INPUT_PATH, bindings
from textile.text import Blackboard, TextAnalyzer
from textual.reactive import reactive

# create blackboard
blackboard = Blackboard(INPUT_PATH)

# analyze text
TextAnalyzer(blackboard.manager)


# routines definiton when button is presed
def call_nouns():
    TextileApp.text = blackboard.manager["nouns_rich_text"]
    TextileApp.message = blackboard.manager["nouns_rich_analysis"]


def call_verbs():
    TextileApp.text = blackboard.manager["verbs_rich_text"]
    TextileApp.message = blackboard.manager["verbs_rich_analysis"]


def call_adjectives():
    TextileApp.text = blackboard.manager["adjectives_rich_text"]
    TextileApp.message = blackboard.manager["adjectives_rich_analysis"]


def call_adverbs():
    TextileApp.text = blackboard.manager["adverbs_rich_text"]
    TextileApp.message = blackboard.manager["adverbs_rich_analysis"]


def call_prepositions():
    TextileApp.text = blackboard.manager["prepositions_rich_text"]
    TextileApp.message = blackboard.manager["prepositions_rich_analysis"]


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
        TextileApp.message = f"{self.label} pressed"
        button_action[str(self.label)]()


class TextileApp(App):
    """A Textual app as inteface to textile."""

    CSS_PATH = "TextileApp.css"
    BINDINGS = bindings

    message = None
    text = blackboard.manager["text"]

    # always reactive
    status_update = reactive(0, always_update=False)

    # buttons
    nouns_button = Butt("Nouns")
    verbs_button = Butt("Verbs")
    adjectives_button = Butt("Adjectives")
    adverbs_button = Butt("Adverbs")
    prepositions_button = Butt("Prepositions")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.text_log = RichLog(highlight=True, markup=True, wrap=True, min_width=78, id="text")
        self.status_log = RichLog(highlight=True, markup=True, wrap=True, min_width=78, id="status")
        self.analysis_log = RichLog(highlight=True, markup=True, id="analysis")
        yield Container(
            Container(
                self.text_log,
                Container(
                    self.nouns_button,
                    self.verbs_button,
                    self.adjectives_button,
                    self.adverbs_button,
                    self.prepositions_button,
                    id="buttons",
                ),self.status_log,
                id="text_buttons_container",
            ), self.analysis_log,
            id="main",
        )

    def on_ready(self) -> None:
        """called  when the DOM is ready."""
        self.text_log.write(self.text)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.status_update += 1
        self.text_log.clear()
        self.analysis_log.clear()
        self.text_log.write(TextileApp.text)

        if isinstance(TextileApp.message, list):
            for element in TextileApp.message:
                self.analysis_log.write(element)
        else:
            self.analysis_log.write(f"Processing ... {TextileApp.message}")

    def watch_status_update(self):
        self.status_log.write("gooo {}".format(self.status_update))

if __name__ == "__main__":
    app = TextileApp()
    app.run()
