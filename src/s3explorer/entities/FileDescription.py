import datetime
from s3explorer.entities import FileType


class FileDescription:
    def __init__(self, type: FileType, size=None, last_modified=None) -> None:
        self.type: FileType = type
        self.size: int | None = size
        self.last_modified: datetime.datetime | None = last_modified
