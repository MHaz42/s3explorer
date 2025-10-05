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
    
    def get_user_config_dir(self) -> Path:
        """Return the user config directory for this application"""
        user_config_dir = Path.home() / ".config" / "s3explorer"
        if not user_config_dir.exists():
            user_config_dir.mkdir(parents=True, exist_ok=True)
        return user_config_dir
    
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
        
        user_config_dir = self.get_user_config_dir()
        bookmark_file = user_config_dir / f"bookmarks.json"
        
        if bookmark_file.exists():
            self.logger.debug(f"Loading bookmarks from {bookmark_file}")
            with open(bookmark_file) as fd:
                data = json.load(fd)
            
            try:
                bucket_bookmark = data[bucket_name]
            except KeyError:
                # No bookmark for this bucket
                return
                
            for i, bookmark in enumerate(bucket_bookmark["bookmarks"]):
                name = Label(bookmark["name"])
                value = bookmark["value"]
                bookmark_id = f"BM{i}"
                self.append(BookmarkListItem(name, id=bookmark_id, value=value))
        else:
            self.logger.debug(f"Creating bookmark file at {bookmark_file}")
            bookmark_file.touch()


class BookmarkListItem(ListItem):
        """ A bookmark item """
        
        __slots__ = ("value", )
        
        def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True, value = None):
            super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
            self.value = value