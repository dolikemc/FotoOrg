import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fotorg.info.store import FotoItem, Base


class TestInfoStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine('sqlite:///test.db', echo=True)
        Base.metadata.drop_all(cls.engine)
        Base.metadata.create_all(cls.engine)
        sess = Session(cls.engine)
        sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                          file_size=123, relative_path='/'))
        sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                          file_size=123, relative_path='/sub'))
        sess.commit()
        sess = Session(cls.engine)
        cls.results = [x for x in sess.query(FotoItem)]

    def test_database(self):
        self.assertEqual(len(self.results), 2)
        self.assertEqual(self.results[0].file_name, 'X.jpg')
        self.assertEqual(self.results[1].file_name, 'X.jpg')

    def test_to_str(self):
        self.assertGreater(len(self.results), 0)
        self.assertEqual('//X.jpg None None', str(self.results[0]))
