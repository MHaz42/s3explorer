import logging

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Input, Label, Select
from textual.containers import Container

from s3explorer.s3 import S3
from s3explorer.version import VERSION
from s3explorer.widgets import ExplorerTable, Bookmark, AddBookmarkScreen, URIInput


class S3Explorer(App):
    """A Textual app to explore s3 buckets"""

    CSS_PATH = "styles/app.tcss"

    TITLE = "S3Explorer"

    BINDINGS = [
        ("ctrl+b", "add_bookmark", "Add bookmark"),
    ]

    logger = logging.getLogger("S3Explorer")

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
                URIInput(id="patheditorinput", placeholder="S3 path here"),
                id="patheditor",
            ),
            Bookmark(id="bookmarks", name="Bookmarks"),
            ExplorerTable(id="explorer", bucket=self.s3_client.list_bucket()[0]),
            id="app",
        )
        yield Footer()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.logger.info(f"Selected bucket: {event.value}")
        table = self.query_one(ExplorerTable)
        table.update_bucket(str(event.value))
        bookmark = self.query_one(Bookmark)
        bookmark.load_bookmark(str(event.value))
        uri_input = self.query_one(URIInput)
        uri_input.update_path("")

    @on(Bookmark.Selected)
    def bookmark_selected(self, event: Bookmark.Selected) -> None:
        self.logger.info(f"Selected bookmark: {event.item.value = }")
        bookmark_path = event.item.value
        input_widget = self.query_one(URIInput)
        input_widget.update_path(bookmark_path)

    @on(URIInput.Submitted)
    def input_submitted(self, event: URIInput.Submitted) -> None:
        table = self.query_one(ExplorerTable)
        table.update_path(event.value)

    @on(ExplorerTable.NavigateBack)
    def explorer_table_navigate_back(self) -> None:
        uri_input = self.query_one(URIInput)
        uri_input.navigate_back()

    @on(ExplorerTable.NavigateForward)
    def explorer_table_navigate_forward(
        self, event: ExplorerTable.NavigateForward
    ) -> None:
        uri_input = self.query_one(URIInput)
        uri_input.navigate_forward(event.new_dir_level)

    def action_add_bookmark(self) -> None:
        select_widget = self.query_one(Select)
        bucket_name = str(select_widget.value)
        input_widget = self.query_one(Input)
        bookmark_value = input_widget.value

        def add_bookmark(bookmark_name: str | None) -> None:
            bookmark_widget = self.query_one(Bookmark)
            if bookmark_name:
                self.logger.info("Bookmark added")
                bookmark_widget.add_bookmark(bucket_name, bookmark_name, bookmark_value)
        
        self.push_screen(AddBookmarkScreen(), callback=add_bookmark)
