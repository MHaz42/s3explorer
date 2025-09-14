from textual.app import App, ComposeResult
from textual.events import Resize
from textual.widgets import (
    Footer,
    Input,
    Label,
    ListView,
    ListItem,
    DataTable,
)
from textual.widgets.data_table import ColumnKey
from textual.containers import Container

from s3explorer.version import VERSION
from datetime import datetime


class ExplorerTable(DataTable):
    def on_resize(self, event: Resize) -> None:
        self.columns[ColumnKey("filename")].auto_width = False
        if event.size.width - 45 > 30:
            self.columns[ColumnKey("filename")].width = event.size.width - 46
        else:
            self.columns[ColumnKey("filename")].width = 30
        self.refresh()


class S3Explorer(App):
    """A Textual app to explore s3 buckets"""

    CSS_PATH = "app.tcss"

    TITLE = "S3Explorer"

    ROWS = [
        ("toto.txt", datetime.now(), "55Ko"),
        ("titi.txt", datetime(2025, 9, 10, 12, 0, 0), "100Ko"),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Label(f"[b]S3Explorer[/] [dim]{VERSION}[/]", id="header", classes="box"),
            Container(
                Label("s3://", id="patheditorlabel", classes="box"),
                Input(id="patheditorinput", placeholder="S3 path here", classes="box"),
                id="patheditor",
                classes="box",
            ),
            ListView(
                ListItem(Label("Bookmark1")),
                id="bookmarks",
                name="Bookmarks",
                classes="box",
            ),
            ExplorerTable(id="explorer"),
            id="app",
        )
        yield Footer()

    def on_mount(self):
        table = self.query_one(ExplorerTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_column("filename", key="filename")
        table.add_column("last edited", width=30)
        table.add_column("size", width=10)
        table.add_rows(self.ROWS)
