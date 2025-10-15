import logging
import json

from pathlib import Path

from textual import on
from textual.widgets import (
    ListView,
    ListItem,
    Label,
    Input,
    Select
)
from textual.screen import Screen


class AddBookmarkScreen(Screen[str]):
    def compose(self):
        yield Label("Enter a name for the bookmark:", id="add_bookmark_user_msg")
        yield Input(id="add_bookmark_user_input", placeholder="Input bookmark name here")
    
    @on(Input.Submitted)
    def input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.input.value)


class BookmarkListItem(ListItem):
        """ A bookmark item """
        
        __slots__ = ("value", )
        
        def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True, value: str = ""):
            super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
            self.value = value


class Bookmark(ListView):
    """Bookmark manager"""
    
    logger = logging.getLogger("Bookmark")
    
    BINDINGS = [
        ("delete", "remove_bookmark", "Remove highlighted bookmark"),
    ]
    
    class Selected(ListView.Selected):
        def __init__(self, list_view, item, index):
            self.item: BookmarkListItem = item
            """The selected item."""
            super().__init__(list_view, item, index)
    
    def get_user_config_dir(self) -> Path:
        """Return the user config directory for this application"""
        user_config_dir = Path.home() / ".config" / "s3explorer"
        if not user_config_dir.exists():
            user_config_dir.mkdir(parents=True, exist_ok=True)
        return user_config_dir

    def get_bookmark_file(self) -> Path:
        user_config_dir = self.get_user_config_dir()
        bookmark_file = user_config_dir / "bookmarks.json"
        if not bookmark_file.exists():
            self.logger.debug(f"Creating bookmark file at {bookmark_file}")
            bookmark_file.touch()
        return bookmark_file

    def read_bookmark(self) -> dict[str, dict[str, list[dict[str, str]]]]:
        bookmark_file = self.get_bookmark_file()
        
        bookmarks = {}
        
        self.logger.debug(f"Reading bookmarks from {bookmark_file}")
        with open(bookmark_file) as fd:
            try:
                bookmarks = json.load(fd)
            except json.JSONDecodeError:
                pass
            
        return bookmarks
    
    def write_bookmark(self, bookmarks: dict) -> None:
        bookmark_file = self.get_bookmark_file()
        
        self.logger.debug(f"Writing bookmarks to {bookmark_file}")
        with open(bookmark_file, "w") as fd:
            json.dump(bookmarks, fd, indent=2)
    
    def load_bookmark(self, bucket_name: str) -> None:
        """
        Load bookmark from user config diretory.
        Structure of the bookmark file:
            {
                "bucketname": {
                    "bookmarks": [
                        {
                            "name": "Product"
                            "value": "/product"
                        }
                    ]
                }
            }
        """
        
        self.clear()
        
        bookmarks = self.read_bookmark()
        
        if not bookmarks.get(bucket_name, {}).get("bookmarks", []):
            self.logger.info(f"No bookmark found for bucket: {bucket_name}")
            return
        else:
            bucket_bookmark = bookmarks[bucket_name]
        
        for i, bookmark in enumerate(bucket_bookmark["bookmarks"]):
            name = Label(bookmark["name"])
            value = bookmark["value"]
            self.append(BookmarkListItem(name, value=value))
    
    def add_bookmark(self, bucket_name: str, bookmark_name: str, bookmark_value: str) -> None:
        bookmarks = self.read_bookmark()
        
        # Get bucket bookmarks or create a new one if it not already exists
        bucket_bookmark: dict[str, list[dict[str, str]]] = bookmarks.get(bucket_name, {"bookmarks": []})
        
        bucket_bookmark["bookmarks"].append({"name": bookmark_name, "value": bookmark_value})
        bookmarks[bucket_name] = bucket_bookmark
        
        self.write_bookmark(bookmarks)
        self.load_bookmark(bucket_name)

    def remove_bookmark(self, bucket_name: str) -> None:
        bookmarks = self.read_bookmark()
        
        # Get bucket bookmarks or create a new one if it not already exists
        bucket_bookmark: dict[str, list[dict[str, str]]] = bookmarks[bucket_name]
        
        bucket_bookmark["bookmarks"].pop(self.index)
        bookmarks[bucket_name] = bucket_bookmark
        self.pop(self.index)
        
        self.write_bookmark(bookmarks)
        self.load_bookmark(bucket_name)
    
    def action_remove_bookmark(self) -> None:
        select_widget = self.app.query_one(Select)
        bucket_name = str(select_widget.value)
        
        if self.index is not None:
            self.logger.info(f"Removing bookmark item at index {self.index} from the list view")
            self.remove_bookmark(bucket_name)