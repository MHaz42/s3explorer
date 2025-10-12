import logging
import json

from pathlib import Path

from textual.widgets import (
    ListView,
    ListItem,
    Label
)


class Bookmark(ListView):
    """Bookmark manager"""
    
    logger = logging.getLogger("Bookmark")
    
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

    def read_bookmark(self) -> dict:
        bookmark_file = self.get_bookmark_file()
        
        self.logger.debug(f"Reading bookmarks from {bookmark_file}")
        with open(bookmark_file) as fd:
            bookmarks = json.load(fd)
        return bookmarks
    
    def write_bookmark(self, bookmarks: dict) -> None:
        bookmark_file = self.get_bookmark_file()
        
        self.logger.debug(f"Writing bookmarks to {bookmark_file}")
        with open(bookmark_file, "w") as fd:
            json.dump(bookmarks, fd)
    
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
        
        try:
            bucket_bookmark = bookmarks[bucket_name]
        except KeyError:
            # No bookmark for this bucket
            return
            
        for i, bookmark in enumerate(bucket_bookmark["bookmarks"]):
            name = Label(bookmark["name"])
            value = bookmark["value"]
            bookmark_id = f"BM{i}"
            self.append(BookmarkListItem(name, id=bookmark_id, value=value))
    
    def add_bookmark(self, bucket_name: str, bookmark_name: str, bookmark_value: str) -> None:
        bookmarks = self.read_bookmark()
        
        # Get bucket bookmarks or create a new one if it not already exists
        bucket_bookmark = bookmarks.get(bucket_name, {"bookmarks": []})
        
        bucket_bookmark["bookmarks"].append({"name": bookmark_name, "value": bookmark_value})
        
        self.write_bookmark(bookmarks)
        self.load_bookmark(bucket_name)


class BookmarkListItem(ListItem):
        """ A bookmark item """
        
        __slots__ = ("value", )
        
        def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True, value: str = ""):
            super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
            self.value = value