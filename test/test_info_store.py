import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fotorg.info.store import FotoItem, Base
from fotorg.info.data.file import File
from fotorg.info.data.exif import Exif
from fotorg.scan import Scan


class TestInfoStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine('sqlite:///test.db', echo=True)
        Base.metadata.drop_all(cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.sess = Session(cls.engine)
        cls.sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                              file_size=123, relative_path='/'))
        cls.sess.add(FotoItem(file_name='X.jpg', file_created=datetime.now(),
                              file_size=123, relative_path='/sub'))
        cls.sess.commit()
        cls.results = [x for x in cls.sess.query(FotoItem)]

    def test_database(self) -> None:
        self.assertEqual(len(self.results), 2)
        self.assertEqual(self.results[0].file_name, 'X.jpg')
        self.assertEqual(self.results[1].file_name, 'X.jpg')

    def test_to_str(self) -> None:
        self.assertGreater(len(self.results), 0)
        self.assertEqual('//X.jpg None None', str(self.results[0]))

    def test_store_one_scan(self) -> None:
        from PIL import Image
        scanner = Scan(directory='./test/test_folder', ignore_list=['*.txt', '.DS_Store'])
        self.assertIsInstance(scanner, Scan)
        for item in scanner.items():
            file = File(item, scanner.directory)
            foto = Exif(Image.open(file.path).getexif())
            entry = FotoItem(
                file_name=file.name,
                relative_path=str(file.relative_path),
                file_created=file.created,
                file_modified=file.modified,
                file_size=file.size,
                foto_created=foto.created,
                camera_make=foto.make,
                camera_model=foto.camera_model,
                gps_longitude=foto.gps_info.longitude,
                gps_latitude=foto.gps_info.latitude,
                gps_altitude=foto.gps_info.altitude
            )
            self.sess.add(entry)
            self.assertIsInstance(entry, FotoItem)
        self.sess.commit()
