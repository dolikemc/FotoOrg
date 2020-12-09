import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fotorg.info.store import Store, FotoItem, Base


class TestInfoStore(unittest.TestCase):
    engine = None

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

    def test_init(self):
        photo_org_store = Store({})
        self.assertTrue(photo_org_store)

    def test_database(self):
        sess = Session(self.engine)
        results = [x for x in sess.query(FotoItem)]
        self.assertEqual(len(results), 2)
        # print(results[1])
        self.assertEqual(results[0].file_name, 'X.jpg')
        self.assertEqual(results[1].file_name, 'X.jpg')

    def test_no_info(self):
        item = Store({})
        self.assertEqual(item.gps_info.longitude, 0)
        item2 = Store({34853: {1: 'N', 2: (44.0, 49.0, 20.06), 3: 'E', 4: (20.0, 24.0, 38.94), 5: 'm', 6: 89.0, }})
        self.assertEqual(item2.gps_info.altitude, 0.089)

    def test_exif(self):
        from PIL import Image
        image = Image.open('test/test_folder/IMG_0564.JPG')
        """ {34665: 204, 36864: b'0221', 37121: b'\x01\x02\x03\x00', 37377: 7.450526315789474,
                36867: '2016:06:16 12:43:55', 36868: '2016:06:16 12:43:55', 37378: 2.2750071245369052,
                37379: 6.454077883908891, 37380: 0.0, 37383: 5, 37385: 24, 37386: 4.15, 40961: 1, 40962: 3264,
                41989: 29, 41990: 0, 40963: 2448, 37521: '173', 37522: '173', 37396: (1631, 1223, 1795, 1077), 41495: 2,
                33434: 0.005714285714285714, 33437: 2.2, 41729: b'\x01', 34850: 2, 34855: 32, 41986: 0, 40960: b'0100',
                41987: 0, 42034: (4.15, 4.15, 2.2, 2.2), 42035: 'Apple', 42036: 'iPhone 6 back camera 4.15mm f/2.2',
                296: 2, 282: 72.0,
                34853: {1: 'N', 2: (44.0, 49.0, 20.06), 3: 'E', 4: (20.0, 24.0, 38.94), 5: b'\x00', 6: 89.0,
                        7: (10.0, 43.0, 54.37), 12: 'K', 13: 0.0, 16: 'T', 17: 246.48684210526315, 23: 'T',
                        24: 246.48684210526315, 29: '2016:06:16', 31: 65.0}, 271: 'Apple', 272: 'iPhone 6',
                305: '9.3.2', 274: 6, 306: '2016:06:16 12:43:55', 531: 1, 283: 72.0}
        
        # self.assertDictEqual(data, image.info)"""
        item = Store(image.getexif())
        self.assertEqual(item.camera_model, 'iPhone 6')
        self.assertEqual(item.make, 'Apple')
        self.assertEqual(item.created, datetime(2016, 6, 16, 12, 43, 55))
        self.assertEqual(item.orientation, 6)
        self.assertEqual(item.resolution_unit, 2)
        self.assertEqual(item.resolution_x, 72.0)
        self.assertEqual(item.resolution_y, 72.0)
        self.assertEqual(item.height, 2448)
        self.assertEqual(item.width, 3264)
        self.assertEqual(item.brightness, 6.454077883908891)
        self.assertEqual(item.exif_version, b'0221')
        self.assertEqual(item.f_number, 'N/A', 'but should be f/2,2')
        self.assertAlmostEqual(item.exposure_time, 1.0 / 175.0, 2)
        self.assertEqual(item.iso_speed, 0)
        self.assertEqual(item.metering_mode, 5)
        self.assertEqual(item.artist, 'N/A')
        self.assertEqual(item.copyright, 'N/A')
        self.assertEqual(item.image_description, 'N/A')
        self.assertEqual(item.user_comment, 'N/A')
        self.assertAlmostEqual(item.gps_info.longitude, 20, 0)
        self.assertAlmostEqual(item.gps_info.latitude, 44.8, 1)
        self.assertEqual(item.gps_info.altitude, 89.0, 'km')
        # print(item.gps_info)
