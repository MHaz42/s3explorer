from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Placeholder, Input, Label, ListView
from textual.containers import Container


class S3Explorer(App):
    """A Textual app to explore s3 buckets"""

    CSS_PATH = "main.tcss"

    TITLE = "S3Explorer"

    def compose(self) -> ComposeResult:
        yield Header(icon="*")
        yield Container(
            Container(
                Label("s3://", id="patheditorlabel"),
                Input(id="patheditorinput", placeholder="S3 path here"),
                id="patheditor",
            ),
            ListView(id="bookmarks", name="Bookmarks"),
            Placeholder(id="explorer"),
            id="app",
        )
        yield Footer()


def main():
    app = S3Explorer()
    app.run()


if __name__ == "__main__":
    main()
