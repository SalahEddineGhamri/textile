# representation layer --------------------------------
from textual.app import App, ComposeResult
from textual.widgets import RichLog
from textual.widgets import Button
from textual.containers import Container
from textile.config import INPUT_PATH, bindings
from textile.text import Blackboard, TextAnalyzer
from textile.utils import get_logger
from textual.reactive import reactive
from textual.message_pump import MessagePump
from textual import on

# create blackboard
blackboard = Blackboard(INPUT_PATH)

# logger
logger = get_logger()
logger.info("[tui] starting textile")

# analyze text
TextAnalyzer(blackboard.manager)


class StatusLog(RichLog):

    status_update = reactive(blackboard.stages(), always_update=True)

    message_pump = MessagePump()

    def __init__(self):
        super().__init__(highlight=True, markup=True, wrap=True, max_lines=3, min_width=78, id="status")
        timer = self.message_pump.set_interval(0.09, self.update)

    def update(self):
        self.clear()
        self.status_update = blackboard.stages()
        self.write(self.status_update)


class TextileApp(App):
    """A Textual app as interface to textile."""

    CSS_PATH = "TextileApp.css"
    BINDINGS = bindings

    message = None
    text = blackboard.manager["text"]

    # buttons
    nouns_button = Button("Nouns", id ="nouns")
    verbs_button = Button("Verbs", id = "verbs")
    adjectives_button = Button("Adjectives", id = "adjectives")
    adverbs_button = Button("Adverbs", id = "adverbs")
    prepositions_button = Button("Prepositions", id = "prepositions")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.text_log = RichLog(highlight=True, markup=True, wrap=True, min_width=78, id="text")
        self.status_log = StatusLog()
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
        self.text_log.clear()
        self.analysis_log.clear()
        self.text_log.write(self.text)

        if isinstance(self.message, list):
            for element in self.message:
                self.analysis_log.write(element)
        else:
            self.analysis_log.write(f"Processing ... {self.message}")

    @on(Button.Pressed, "#nouns")
    def call_nouns(self):
        self.text = blackboard.manager["nouns_rich_text"]
        self.message = blackboard.manager["nouns_rich_analysis"]


    @on(Button.Pressed, "#verbs")
    def call_verbs(self):
        self.text = blackboard.manager["verbs_rich_text"]
        self.message = blackboard.manager["verbs_rich_analysis"]


    @on(Button.Pressed, "#adjectives")
    def call_adjectives(self):
        self.text = blackboard.manager["adjectives_rich_text"]
        self.message = blackboard.manager["adjectives_rich_analysis"]


    @on(Button.Pressed, "#adverbs")
    def call_adverbs(self):
        self.text = blackboard.manager["adverbs_rich_text"]
        self.message = blackboard.manager["adverbs_rich_analysis"]


    @on(Button.Pressed, "#prepositions")
    def call_prepositions(self):
        self.text = blackboard.manager["prepositions_rich_text"]
        self.message = blackboard.manager["prepositions_rich_analysis"]

if __name__ == "__main__":
    app = TextileApp()
    app.run()
