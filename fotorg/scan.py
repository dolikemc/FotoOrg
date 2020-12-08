from pathlib import Path, PurePath
from typing import Iterator, List, Union


class Scan:
    """Class for setup scanning the folder structure and receive files for considerations."""

    def __init__(self, directory: Union[PurePath, Path, str] = None, ignore_list=None):
        if ignore_list is None:
            ignore_list = []
        if directory is None:
            self.directory: Path = Path.cwd()
        elif isinstance(directory, Path):
            self.directory: Path = directory
        elif isinstance(directory, str):
            self.directory: Path = Path(directory)
        self.item_counter = 0
        self.ignored_dir_list = []
        self.ignored_file_list = []
        for pattern in ignore_list:
            if pattern.endswith('/'):
                self.ignored_dir_list.append(pattern)
            else:
                self.ignored_file_list.append(pattern)

    @property
    def items(self) -> Iterator:
        return []
