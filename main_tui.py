# representation layer --------------------------------
from textual.app import App, ComposeResult
from textual.widgets import TextLog
from textual.widgets import Button
from textual.containers import Container
from bindings import bindings
from text import generate_rich_text, colorize_text, ANALYZED_TEXT, generate_rich_analysis
from rich.table import Table

# PROGRESS IN TUI------------------------------------
# TODO: show messages
# TODO: fill the tables once we get the text
# TODO: manager arguments in the TUI script
# TODO: select the word and show its analysis
# ---------------------------------------------------

TEXT_WIDTH = 80


# routines definiton when button is presed
def call_nouns():
    TextileApp.set_text(generate_rich_text(colorize_text(ANALYZED_TEXT, "NOUN"), width=TEXT_WIDTH))
    rich_analysis = generate_rich_analysis(ANALYZED_TEXT)
    TextileApp.set_message(rich_analysis)


def call_verbs():
    TextileApp.set_text(generate_rich_text(colorize_text(ANALYZED_TEXT, "VERB"), width=TEXT_WIDTH))


# dict of all button actions
button_action = {'Nouns': call_nouns,
                 'Verbs': call_verbs,
                 'Adjectives': lambda: None,
                 'Adverbs': lambda: None,
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
    message = None
    text = generate_rich_text(ANALYZED_TEXT, width=TEXT_WIDTH)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(Container(TextLog(highlight=True,
                                          markup=True,
                                          id="text"),
                                  Container(Butt("Nouns"),
                                            Butt("Verbs"),
                                            Butt("Adjectives"),
                                            Butt("Adverbs"),
                                            Butt("Conjunctions"),
                                            Butt("Prepositions"),
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
