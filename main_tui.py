from textual.app import App, ComposeResult
from textual.widgets import TextLog
from textual.widgets import Button, Static
from textual.containers import Container
from bindings import bindings
from main_textile import get_colorized_dataframe
from text import generate_rich_text


TEXT = generate_rich_text(get_colorized_dataframe(), 90)

# PROGRESS in Tui------------------------------------
# TODO: manager arguments in the TUI script
# TODO: add buttons functionality
# TODO: select the word and show its analysis
# ---------------------------------------------------


class Butt(Button):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # TODO: change the behavior based on the label
        TextileApp.message = f"{self.label} pressed"


class TextileApp(App):
    """A Textual app as inteface to textile."""

    CSS_PATH = "TextileApp.css"
    BINDINGS = bindings
    message = ""

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
        self.text_log.write(TEXT)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.analysis_log.write(TextileApp.message)


if __name__ == "__main__":
    app = TextileApp()
    app.run()
