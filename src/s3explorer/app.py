import logging

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Input, Label, Select, ListView, ListItem
from textual.containers import Container

from s3explorer.s3 import S3
from s3explorer.version import VERSION
from s3explorer.widgets import ExplorerTable, Bookmark, BookmarkListItem


class S3Explorer(App):
    """A Textual app to explore s3 buckets"""

    CSS_PATH = "styles/app.tcss"

    TITLE = "S3Explorer"
    
    BINDINGS = [
        ("ctrl+b", "add_bookmark", "Add bookmark"),
    ]
    
    logger = logging.getLogger("Bookmark")

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
            Bookmark(
                id="bookmarks",
                name="Bookmarks"
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
        self.logger.info(f"{event.value = }")
        table = self.query_one(ExplorerTable)
        table.update_bucket(str(event.value))
        bookmark = self.query_one(Bookmark)
        bookmark.load_bookmark(str(event.value))
    
    @on(Bookmark.Selected)
    def bookmark_selected(self, event: Bookmark.Selected) -> None:
        self.logger.info(f"Enter pressed on Bookmark: {event.item.value = }")
        bookmark_path = event.item.value
        input_widget = self.query_one(Input)
        input_widget.clear()
        input_widget.insert(bookmark_path, 0)
        input_widget.post_message(input_widget.Submitted(input_widget, bookmark_path))
    
    def action_add_bookmark(self) -> None:
        # TODO: Create a new dialog with an Input to ask user for the bookmark name
        select_widget = self.query_one(Select)
        bucket_name = select_widget.value
        input_widget = self.query_one(Input)
        bookmark_value = input_widget.value
        bookmark_name = ""
        
        bookmark_widget = self.query_one(Bookmark)
        bookmark_widget.add_bookmark(bucket_name, bookmark_name, bookmark_value)
