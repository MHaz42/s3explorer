from typing import Dict
from humanize import naturalsize

from textual.widgets import DataTable
from textual.widgets.data_table import ColumnKey
from textual.message import Message
from textual.events import Resize

from s3explorer.entities import FileDescription, FileType
from s3explorer.s3 import S3


class ExplorerTable(DataTable):

    # Vars for sorting
    need_reverse = False
    current_sort = "filename"

    # Vars for path and s3
    s3_client = S3()
    bucket = ""
    directory_structure: Dict[str, FileDescription] = {}

    BINDINGS = [
        ("ctrl+f", "sort_by_filename", "Sort by FileName"),
        ("enter", "enter_dir", "Enter directory"),
    ]

    def __init__(self, bucket: str, id: str):
        super().__init__(id=id)
        self.bucket = bucket

    class NavigateBack(Message):
        def __init__(self) -> None:
            super().__init__()

    class NavigateForward(Message):
        def __init__(self, new_dir_level: str) -> None:
            self.new_dir_level = new_dir_level
            super().__init__()

    def update_path(self, new_path: str = ""):
        self.directory_structure = self.s3_client.list_directory_content(
            self.bucket, new_path
        )
        self.clear()
        for filename, file_desc in self.directory_structure.items():
            self.add_row(
                filename,
                file_desc.last_modified.ctime() if file_desc.last_modified else "",
                naturalsize(file_desc.size, gnu=True) if file_desc.size else "",
            )
        self.sort(
            "filename",
            key=lambda filename: filename.lower(),
        )
        self.move_cursor(row=1 if new_path else 0)

    def update_bucket(self, new_bucket: str):
        self.bucket = new_bucket

    def on_resize(self, event: Resize) -> None:
        self.columns[ColumnKey("filename")].auto_width = False
        if event.size.width - 45 > 30:
            self.columns[ColumnKey("filename")].width = event.size.width - 46
        else:
            self.columns[ColumnKey("filename")].width = 30
        self.refresh()

    def on_mount(self):
        self.directory_structure = self.s3_client.list_directory_content("test", "")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.add_column("filename", key="filename")
        self.add_column("last edited", width=30)
        self.add_column("size", width=10)
        self.update_path()

    def action_sort_by_filename(self) -> None:
        if self.current_sort != "filename":
            self.current_sort = "filename"
            self.need_reverse = False
        self.sort(
            "filename", key=lambda filename: filename.lower(), reverse=self.need_reverse
        )
        self.need_reverse = not self.need_reverse

    def action_enter_dir(self) -> None:
        filename = self.get_row_at(self.cursor_row)[0]
        if self.directory_structure[filename].type == FileType.DIRECTORY:
            self.post_message(self.NavigateForward(filename))
        elif self.directory_structure[filename].type == FileType.RETURN:
            self.post_message(self.NavigateBack())
        else:
            return None
