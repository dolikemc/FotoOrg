from datetime import datetime
# from typing import Dict
from pathlib import Path
import os


class File:
    def __init__(self, item: Path, dir: Path) -> None:
        self.__item = item
        self.__directory = dir

    @property
    def name(self) -> str:
        """
        :return: The file name without any path information but with suffix
        """
        return self.__item.name

    @property
    def relative_path(self) -> Path:
        """
        :return: the path relative to the root directory where the scan started
        """
        return Path(os.path.relpath(self.__item, self.__directory))

    @property
    def size(self) -> int:
        return os.stat(self.__item).st_size

    @property
    def created(self) -> datetime:
        return datetime.fromtimestamp(os.stat(self.__item).st_ctime)

    @property
    def modified(self) -> datetime:
        return datetime.fromtimestamp(os.stat(self.__item).st_mtime)
