from typing import List, Any


class TestedState:

    def __init__(self):
        self._artifacts = list()
        self._error = None

    @property
    def artifacts(self):
        return self._artifacts

    @property
    def error(self):
        return self._error

    @artifacts.setter
    def artifacts(self, value: List[Any]):
        self._artifacts = value

    @error.setter
    def error(self, value: str):
        self._error = value
