import unittest
from fotorg import scan
from pathlib import Path


class TestScan(unittest.TestCase):
    def setUp(self) -> None:
        self.scanner = scan.Scan()

    def test_get_start_directory(self) -> None:
        self.assertTrue(hasattr(self.scanner, 'directory'))
        self.assertIsInstance(self.scanner.directory, Path)
        self.assertEqual(self.scanner.directory.name, 'FotoOrg')
        self.assertTrue(str(self.scanner.directory).endswith('FotoOrg'))

    def test_default_init_directory(self) -> None:
        self.scanner = scan.Scan('./test/test_folder')
        self.assertEqual(self.scanner.directory.name, 'test_folder')
        self.assertEqual(str(self.scanner.directory), 'test/test_folder')

    def test_path_init_directory(self) -> None:
        self.scanner = scan.Scan(Path('./test'))
        self.assertEqual(self.scanner.directory.name, 'test')
        self.assertEqual(str(self.scanner.directory), 'test')

    def test_list_files(self) -> None:
        self.assertTrue(hasattr(self.scanner, 'items'))
        self.assertIn('CIMG3602.jpeg', self.scanner.items)
