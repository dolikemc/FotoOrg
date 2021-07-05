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
        self.scanner = scan.Scan(directory='./test/test_folder', ignore_list=None)
        items = [x.name for x in self.scanner.items()]
        self.assertIn('CIMG3602.jpeg', items)
        self.assertIn('CIMG3602_DUP.jpeg', items)
        self.assertIn('CIMG3602_SUB_DUP.jpeg', items)
        self.assertIn('CIMG3602_TRIP.jpeg', items, 'not excluded yet')
        self.assertEqual(19, self.scanner.scanned_items)

    def test_ignored_files(self) -> None:
        self.scanner = scan.Scan(directory='./test/test_folder',
                                 ignore_list=['ignored_and_excluded.txt'])
        items = [x.name for x in self.scanner.items()]
        self.assertIn('CIMG3602.jpeg', items)
        self.assertIn('CIMG3602_DUP.jpeg', items)
        self.assertIn('CIMG3602_SUB_DUP.jpeg', items)
        self.assertNotIn('symlink.txt', items, 'always excluded')
        self.assertNotIn('ignored_and_excluded.txt', items, 'excluded now')
        self.assertEqual(19, self.scanner.scanned_items)

    def test_ignored_in_directories(self) -> None:
        # test/test_folder/includes_sub_folder
        # test/test_folder/includes_sub_folder/sub_sub
        # test/test_folder/excluded
        self.scanner = scan.Scan(directory='./test/test_folder', ignore_list=['excluded/'])
        items = [x.name for x in self.scanner.items()]
        self.assertIn('CIMG3602.jpeg', items)
        self.assertIn('CIMG3602_DUP.jpeg', items)
        self.assertIn('CIMG3602_SUB_DUP.jpeg', items)
        self.assertNotIn('CIMG3602_TRIP.jpeg', items, 'excluded now')
        self.assertEqual(17, self.scanner.scanned_items)

    def test_ignored_base_directories(self) -> None:
        # test/test_folder/includes_sub_folder
        # test/test_folder/includes_sub_folder/sub_sub
        # test/test_folder/excluded
        self.scanner = scan.Scan(directory='./test/test_folder', ignore_list=['/test/'])
        items = [x.name for x in self.scanner.items()]
        self.assertNotIn('CIMG3602.jpeg', items)
        self.assertNotIn('CIMG3602_DUP.jpeg', items)
        self.assertNotIn('CIMG3602_SUB_DUP.jpeg', items)
        self.assertNotIn('CIMG3602_TRIP.jpeg', items, 'excluded now')
        self.assertEqual(12, self.scanner.scanned_items)

    def test_ignored_file_extension(self) -> None:
        self.scanner = scan.Scan(directory='./test/test_folder', ignore_list=['*.txt'])
        items = [x.name for x in self.scanner.items()]
        self.assertIn('CIMG3602.jpeg', items)
        self.assertIn('CIMG3602_DUP.jpeg', items)
        self.assertIn('CIMG3602_SUB_DUP.jpeg', items)
        self.assertIn('CIMG3602_TRIP.jpeg', items, 'excluded now')
        self.assertNotIn('symlink.txt', items, 'always excluded')
        self.assertEqual(19, self.scanner.scanned_items)
        self.assertNotIn('ignored_and_excluded.txt', items, 'excluded now')

    def test_root_folder(self) -> None:
        self.scanner = scan.Scan(directory='./test/test_folder/includes_sub_folder', ignore_list=['*.txt'])
        items = [x.name for x in self.scanner.items()]
        self.assertNotIn('CIMG3602.jpeg', items)
        self.assertIn('CIMG3602_DUP.jpeg', items)
        self.assertIn('CIMG3602_SUB_DUP.jpeg', items)
        self.assertNotIn('CIMG3602_TRIP.jpeg', items, 'excluded now')
        self.assertNotIn('ignored_and_excluded.txt', items, 'always excluded')
        self.assertEqual(5, self.scanner.scanned_items)

    def test_ignored_exact_this_file(self) -> None:
        self.scanner = scan.Scan(directory='./test/test_folder',
                                 ignore_list=['excluded/',
                                              '/test/test_folder/includes_sub_folder/ignored_and_excluded.txt'])
        items = [x.name for x in self.scanner.items()]
        self.assertIn('CIMG3602.jpeg', items)
        self.assertIn('CIMG3602_DUP.jpeg', items)
        self.assertIn('CIMG3602_SUB_DUP.jpeg', items)
        self.assertNotIn('ignored_and_excluded.txt', items, 'excluded now')
        self.assertEqual(17, self.scanner.scanned_items)
