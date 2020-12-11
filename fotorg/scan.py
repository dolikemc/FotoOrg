from pathlib import Path, PurePath
from typing import Iterator, Union


class Scan:
    """Class for setup scanning the folder structure and receive files for considerations."""

    def __init__(self, directory: Union[PurePath, Path, str] = None, ignore_list=None) -> None:
        """
        Constructor
        :param directory:
        :param ignore_list:
        """
        if ignore_list is None:
            ignore_list = []
        if directory is None:
            self.directory: Path = Path.cwd()
        elif isinstance(directory, Path):
            self.directory: Path = directory
        elif isinstance(directory, str):
            self.directory: Path = Path(directory)
        self.__item_counter = 0
        self.__ignored_dir_list = []
        self.__ignored_file_list = []
        for pattern in ignore_list:
            if pattern.endswith('/'):
                self.__ignored_dir_list.append(pattern)
            else:
                self.__ignored_file_list.append(pattern)

    def items(self, path: Path = None) -> Iterator[Path]:
        """
        Iterator for all items in the given path except if they are in the ignore
        list or pattern
        :param path:
        :return:
        """
        if path is None:
            path = self.directory

        for item in path.iterdir():
            self.__item_counter += 1
            if item.is_dir():
                if not self.__ignore_dir(item):
                    yield from self.items(item)
            elif item.is_file() and self.__not_ignore(item):
                yield item

    def __ignore_dir(self, item: Union[PurePath, Path]) -> bool:
        for ignore in self.__ignored_dir_list:
            if ignore.startswith('/'):
                if str(item).startswith(ignore[1:]):
                    return True
            elif ignore.replace('/', '') in item.parts:
                return True
        return False

    def __not_ignore(self, item: Union[PurePath, Path]) -> bool:
        # all other file types are excluded always
        if item.is_symlink() or item.is_block_device() or item.is_char_device():
            return False
        # file name in ignore list. Pattern ^/text^/
        if item.name in self.__ignored_file_list:
            return False
        if '*' + item.suffix in self.__ignored_file_list:
            return False
        if self.__ignore_dir(item):
            return False
        return True

    @property
    def scanned_items(self) -> int:
        """
        Number of scanned items regarding the ignore list
        :return:
        """
        return self.__item_counter
