import unittest
import logging

from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, configure_mappers

from fotorg.info.store import Base, BaseDir, FotoItem, Store
from fotorg.scan import Scan

logging.basicConfig(format='%(asctime)-15s %(message)s')
log = logging.getLogger('test.info.store')
log.setLevel(logging.DEBUG)


class TestInfoStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global engine
        engine = create_engine('sqlite:///test.db', echo=True)
        # configure_mappers()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        sess = Session(engine)
        sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                          file_size=123, relative_path='/'))
        sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                          file_size=123, relative_path='/sub'))
        sess.commit()
        log.warning('class setup done')

    def setUp(self) -> None:
        self.session = Session(engine)

    def test_database(self) -> None:
        self.results = self.session.query(FotoItem).all()
        self.assertEqual(len(self.results), 2)
        self.assertEqual(self.results[0].file_name, 'X.jpg')
        self.assertEqual(self.results[1].file_name, 'X.jpg')

    def test_to_str(self) -> None:
        self.results = self.session.query(FotoItem).all()
        self.assertGreater(len(self.results), 0)
        self.assertEqual('//X.jpg None None', str(self.results[0]))

    def test_store_one_scan_include_no_foto(self) -> None:

        scanner = Scan(directory='./test/test_folder', ignore_list=['included_sub_folder'])
        self.assertIsInstance(scanner, Scan)
        for item in scanner.items():
            entry = Store(item, scanner.directory).prepare_store()
            existing: FotoItem = self.session.query(FotoItem).filter_by(file_name=entry.file_name,
                                                                        relative_path=entry.relative_path).first()
            if existing:
                existing.file_modified = datetime.now()
            self.assertIsInstance(entry, FotoItem)
        self.session.commit()

    def test_store_directory(self) -> None:
        directory = Path('./test/test_folder')
        self.session.commit()
        self.assertGreater(len(self.session.query(BaseDir).all()), 0)
        self.assertEqual(str(self.session.query(BaseDir).first().path), str(directory))
        self.assertGreaterEqual(len(self.session.query(BaseDir).all()), 1)
        self.assertEqual(str(self.session.query(BaseDir).first()), str(directory))
        scanner = Scan(directory='./test/test_folder', ignore_list=[])
        scanner.run(self.session)
        self.assertGreaterEqual(len(self.session.query(BaseDir).all()), 1)
        # self.assertEqual(1, 0)

    def test_scan_run(self):
        scanner = Scan(directory='./test/test_folder', ignore_list=['excluded/', ])
        scanner.run(self.session)
        self.assertGreaterEqual(len(self.session.query(FotoItem).all()), 15)
        self.assertEqual(len(self.session.query(BaseDir).all()), 1)
        scanner.run(self.session)
        # self.assertEqual(len(self.sess.query(FotoItem).all()), )
        self.assertEqual(len(self.session.query(BaseDir).all()), 1, 'is re used')
