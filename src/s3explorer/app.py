from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Input, Label, Select, ListView, ListItem
from textual.containers import Container

from s3explorer.s3 import S3
from s3explorer.version import VERSION
from s3explorer.widgets import ExplorerTable


class S3Explorer(App):
    """A Textual app to explore s3 buckets"""

    CSS_PATH = "styles/app.tcss"

    TITLE = "S3Explorer"

    s3_client = S3()

    def compose(self) -> ComposeResult:
        yield Container(
            Label(f"[b]S3Explorer[/] [dim]{VERSION}[/]", id="header"),
            Container(
                Label("s3://", id="patheditorlabel"),
                Select(
                    ((bucket, bucket) for bucket in self.s3_client.list_bucket()),
                    value=self.s3_client.list_bucket()[0],
                    allow_blank=False,
                ),
                Input(id="patheditorinput", placeholder="S3 path here"),
                id="patheditor",
            ),
            ListView(
                ListItem(Label("Bookmark1")),
                id="bookmarks",
                name="Bookmarks",
            ),
            ExplorerTable(id="explorer", bucket=self.s3_client.list_bucket()[0]),
            id="app",
        )
        yield Footer()

    @on(ExplorerTable.PathUpdate)
    def explorer_table_path_update(self, message: ExplorerTable.PathUpdate) -> None:
        input_widget = self.query_one(Input)
        input_widget.value = message.path

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        table = self.query_one(ExplorerTable)
        table.update_bucket(str(event.value))
