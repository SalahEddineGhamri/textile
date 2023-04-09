# representation layer --------------------------------
from textual.app import App, ComposeResult
from textual.widgets import TextLog
from textual.widgets import Button
from textual.containers import Container
from bindings import bindings
from text import generate_rich_text, colorize_text, ANALYZED_TEXT

# PROGRESS in Tui------------------------------------
# TODO: show messages
# TODO: change the scheme of the text based on the button
# TODO: manager arguments in the TUI script
# TODO: add buttons functionality
# TODO: select the word and show its analysis
# ---------------------------------------------------

TEXT_WIDTH = 80


# routines definiton when button is presed
def call_nouns():
    TextileApp.set_text(generate_rich_text(colorize_text(ANALYZED_TEXT, "NOUN"), width=TEXT_WIDTH))


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
    message = ""
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
        self.analysis_log.write(TextileApp.message)

    @staticmethod
    def set_message(message: str) -> None:
        TextileApp.message = message

    @staticmethod
    def set_text(text: str) -> None:
        TextileApp.text = text


if __name__ == "__main__":
    app = TextileApp()
    app.run()
