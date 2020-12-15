from pathlib import Path, PurePath
from typing import Iterator, Union
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from sqlalchemy import desc

from fotorg.info.store import Store, FotoItem, BaseDir

log = logging.getLogger('fotorg.scan')


class Scan:
    """Class for setup scanning the folder structure and receive files for considerations."""

    def __init__(self, directory: Union[PurePath, Path, str] = None, ignore_list=None) -> None:
        """
        Constructor
        :param directory: Start path for the scan
        :param ignore_list: list of ignore patterns
                'ignored.file' just this file on every folder
                '*.all_files_with_this_ext' all files with this extension
                'ignored_folder/' all folders with this name
                '/just/this/folder/'
                '/just/this/file.ext'
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
        :return: iterator of path items. steps through the paths skipping items in the ignore list
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
        # full path file name in the list
        if '/' + str(item.parent / item.name) in self.__ignored_file_list:
            return False

        return True

    @property
    def scanned_items(self) -> int:
        """
        :return: Number of scanned items regarding the ignore list
        """
        return self.__item_counter

    def run(self, session: Session = None):
        if session is not None:
            base_dir = session.query(BaseDir).filter_by(path=str(self.directory)).order_by(
                desc('created')).first()
            if base_dir:
                log.debug(f"update for {self.directory}")
                base_dir.scan_start = datetime.now()
                base_dir.last_used = datetime.now()
            else:
                log.debug(f"new record for {self.directory}")
                session.add(BaseDir(path=str(self.directory), user_name='class'))
            session.commit()

        for item in self.items():
            store = Store(item=item, directory=self.directory)
            foto_item: FotoItem = store.prepare_store()
            if session is not None:
                session.add(foto_item)
                session.commit()

        if session is not None:
            base_dir = session.query(BaseDir).filter_by(path=str(self.directory)).order_by('created').first()
            base_dir.last_used = datetime.now()
            session.commit()
