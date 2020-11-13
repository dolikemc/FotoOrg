from pathlib import Path, PurePath
from typing import Iterator, List, Union


class Scan:
    def __init__(self, directory: Union[PurePath, Path, str] = None, ignore_list: List[str] = None):
        if directory is None:
            self.directory: Path = Path.cwd()
        elif isinstance(directory, Path):
            self.directory: Path = directory
        elif isinstance(directory, str):
            self.directory: Path = Path(directory)
        self.ignore_list = ignore_list
        if self.ignore_list is None:
            self.ignore_list = []

    @property
    def items(self) -> Iterator:
        return []
