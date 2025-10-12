from typing import List
from textual.widgets import Input
from textual.message import Message


class URIInput(Input):
    def __init__(self, id, placeholder, path=""):
        super().__init__(id=id, placeholder=placeholder)
        self.value = path

    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value: str = value
            super().__init__()

    def update_path(self, new_path: str) -> None:
        if new_path:
            self.value = new_path if new_path.endswith("/") else new_path + "/"
        else:
            self.value = new_path
        self.post_message(self.Submitted(self.value))

    def navigate_back(self):
        temp: List[str] = self.value.strip("/").split("/")
        temp.pop()
        if temp:
            self.update_path("/".join(temp))
        else:
            self.update_path("")

    def navigate_forward(self, new_dir_level: str):
        print(f"{self.value = }")
        print(f"{new_dir_level = }")

        self.update_path(self.value + new_dir_level)
