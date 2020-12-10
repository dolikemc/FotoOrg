import unittest
from datetime import datetime
from pathlib import Path

from fotorg.info.data.file import File


class TestInfoDataFile(unittest.TestCase):
    def setUp(self) -> None:
        self.file_name = 'IMG_0564.JPG'
        self.relative_path = 'test/test_folder'
        self.item: Path = Path.cwd() / self.relative_path / self.file_name
        self.file = File(self.item, Path.cwd())

    def test_info_data_file(self) -> None:
        self.assertIsInstance(self.file, File)

    def test_info_data_file_name(self) -> None:
        self.assertEqual(self.file.name, self.file_name)

    # @unittest.skip
    def test_info_data_file_relative_path(self) -> None:
        self.assertEqual(self.file.relative_path, self.relative_path)

    def test_info_data_file_size(self) -> None:
        self.assertEqual(self.file.size, 2323253)

    def test_info_data_file_timestamps(self) -> None:
        self.assertEqual(self.file.created, datetime(2020, 12, 8, 21, 35, 2, 319917))
        self.assertEqual(self.file.modified, self.file.created)
