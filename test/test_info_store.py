import unittest
import logging

from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, configure_mappers

from fotorg.info.store import BaseDir, FotoItem, Base, Store
from fotorg.scan import Scan


class TestInfoStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(format='%(asctime)-15s %(message)s')
        log = logging.getLogger('test.info.store')
        log.setLevel(logging.DEBUG)
        configure_mappers()
        cls.engine = create_engine('sqlite:///test.db', echo=True)
        Base.metadata.drop_all(cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.sess = Session(cls.engine)
        cls.sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                              file_size=123, relative_path='/'))
        cls.sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                              file_size=123, relative_path='/sub'))
        cls.sess.commit()
        cls.results = cls.sess.query(FotoItem).all()

    def test_database(self) -> None:
        self.assertEqual(len(self.results), 2)
        self.assertEqual(self.results[0].file_name, 'X.jpg')
        self.assertEqual(self.results[1].file_name, 'X.jpg')

    def test_to_str(self) -> None:
        self.assertGreater(len(self.results), 0)
        self.assertEqual('//X.jpg None None', str(self.results[0]))

    def test_store_one_scan_include_no_foto(self) -> None:
        scanner = Scan(directory='./test/test_folder', ignore_list=['included_sub_folder'])
        self.assertIsInstance(scanner, Scan)
        for item in scanner.items():
            entry = Store(item, scanner.directory).prepare_store()
            existing: FotoItem = self.sess.query(FotoItem).filter_by(file_name=entry.file_name,
                                                                     relative_path=entry.relative_path).first()
            if existing:
                existing.file_modified = datetime.now()
            self.assertIsInstance(entry, FotoItem)
        self.sess.commit()

    def test_store_directory(self) -> None:
        directory = Path('./test/test_folder')
        self.sess.commit()
        self.assertEqual(str(self.sess.query(BaseDir).first().path), str(directory))
        self.assertGreaterEqual(len(self.sess.query(BaseDir).all()), 1)
        self.assertEqual(str(self.sess.query(BaseDir).first()), str(directory))
        scanner = Scan(directory='./test/test_folder', ignore_list=[])
        scanner.run(self.sess)
        self.assertGreaterEqual(len(self.sess.query(BaseDir).all()), 1)
        # self.assertEqual(1, 0)

    def test_scan_run(self):
        scanner = Scan(directory='./test/test_folder', ignore_list=['excluded/', ])
        scanner.run(self.sess)
        self.assertEqual(len(self.sess.query(FotoItem).all()), 16)
        self.assertEqual(len(self.sess.query(BaseDir).all()), 1)
        scanner.run(self.sess)
        # self.assertEqual(len(self.sess.query(FotoItem).all()), )
        self.assertEqual(len(self.sess.query(BaseDir).all()), 1, 'is re used')
