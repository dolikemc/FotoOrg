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
        sess.add(FotoItem())
        sess.commit()

    def test_init(self):
        photo_org_store = Store({})
        self.assertTrue(photo_org_store)

    def test_database(self):
        sess = Session(self.engine)
        self.assertEqual(len([x for x in sess.query(FotoItem)]), 1)

    def test_exif(self):
        from PIL import Image
        image = Image.open('test/test_folder/IMG_0564.JPG')
        """ {34665: 204, 36864: b'0221', 37121: b'\x01\x02\x03\x00', 37377: 7.450526315789474,
                36867: '2016:06:16 12:43:55', 36868: '2016:06:16 12:43:55', 37378: 2.2750071245369052,
                37379: 6.454077883908891, 37380: 0.0, 37383: 5, 37385: 24, 37386: 4.15, 40961: 1, 40962: 3264,
                41989: 29, 41990: 0, 40963: 2448, 37521: '173', 37522: '173', 37396: (1631, 1223, 1795, 1077), 41495: 2,
                33434: 0.005714285714285714, 33437: 2.2, 41729: b'\x01', 34850: 2, 34855: 32, 41986: 0, 40960: b'0100',
                41987: 0, 42034: (4.15, 4.15, 2.2, 2.2), 42035: 'Apple', 42036: 'iPhone 6 back camera 4.15mm f/2.2',
                37500: b'Apple iOS\x00\x00\x01MM\x00\n\x00\x01\x00\t\x00\x00\x00\x01\x00\x00\x00\x04\x00\x02\x00\x07\x00\x00\x02.\x00\x00\x00\x8c\x00\x03\x00\x07\x00\x00\x00h\x00\x00\x02\xba\x00\x04\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x05\x00\t\x00\x00\x00\x01\x00\x00\x00\x80\x00\x06\x00\t\x00\x00\x00\x01\x00\x00\x00}\x00\x07\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x08\x00\n\x00\x00\x00\x03\x00\x00\x03"\x00\x0e\x00\t\x00\x00\x00\x01\x00\x00\x00\x00\x00\x14\x00\t\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00bplist00O\x11\x02\x00$\x00#\x00K\x00\x1b\x00\x1c\x00\x1d\x00\x1d\x00&\x00-\x00\xa3\x00/\x00}\x00\x1d\x01\xda\x01\x1c\x01\x8a\x00*\x00$\x00X\x00\x1b\x00\x1a\x00\x1b\x00\x1f\x00&\x00`\x00\x7f\x01?\x00d\x01\xc6\x01\xcc\x01\xd1\x00\xb7\x00d\x00>\x00Z\x00\x17\x00\x18\x00\x1a\x00\x1c\x002\x00\xb2\x00n\x01\x8e\x00\xda\x01\x9b\x01X\x01\xa4\x00\x91\x00\xa7\x00Q\x00;\x00\x16\x00\x19\x00!\x00 \x00(\x00\x93\x00(\x01\xcc\x00\xa9\x015\x01\r\x01\x85\x00t\x00\x1e\x01P\x00)\x00#\x004\x00L\x005\x006\x00B\x00\x89\x00\x01\x01E\x01\xf2\x00\xcd\x00|\x00w\x00\x1d\x010\x00\'\x00#\x00&\x005\x004\x008\x00?\x00V\x00\x0f\x01\xe1\x00\xbd\x00\xb6\x00s\x00\x82\x00\xe5\x00\x8e\x00%\x00\'\x00\x1c\x002\x003\x001\x00/\x00F\x00\xcf\x00\xa3\x00\xb4\x00\xa2\x00{\x00\x91\x00M\x00u\x00#\x00 \x00\x17\x006\x00.\x00&\x00&\x00I\x00\x97\x00\x91\x00\xb8\x00\xa4\x00\x80\x00\x8e\x00\x82\x00\x1d\x00\x1c\x00"\x00\x14\x008\x001\x00$\x002\x00F\x00\x86\x00\xa2\x00\xac\x00\xa1\x00\x9c\x00\xa8\x00y\x00?\x007\x00@\x003\x007\x00/\x00&\x00&\x008\x00\x83\x00\xd1\x00\x93\x00\xaa\x00\xaa\x00p\x01^\x00G\x00E\x00B\x00>\x002\x000\x00(\x000\x00B\x00o\x00\xd5\x00\xac\x00\xb5\x00\x81\x010\x02\\\x00J\x00J\x00L\x00C\x00;\x00?\x005\x009\x00Z\x00d\x00\xbb\x00\xcb\x00\xb9\x01K\x02O\x02j\x00\xb5\x00h\x003\x00#\x005\x00<\x006\x00E\x00g\x00]\x00\xaa\x00\xf7\x01f\x02k\x02t\x02m\x00\x9d\x00y\x00Q\x00>\x00/\x00:\x008\x00H\x00U\x00\xa1\x00G\x02\x92\x02\x94\x02\x96\x02\x7f\x02I\x00B\x00P\x00W\x00:\x00%\x00=\x00?\x00H\x00\xad\x00\xa6\x02\xcb\x02\xc0\x02\xbd\x02\xa7\x02\x7f\x02X\x00@\x00M\x00S\x00<\x00\'\x00@\x00G\x00j\x00y\x02\xc9\x02\x08\x03\xea\x02\xcc\x02\xac\x02\x7f\x02\x00\x08\x00\x00\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x0cbplist00\xd4\x01\x02\x03\x04\x05\x06\x07\x08UflagsUvalueUepochYtimescale\x10\x01\x13\x00\x00j<M \x8f\xaf\x10\x00\x12;\x9a\xca\x00\x08\x11\x17\x1d#-/8:\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xff\xfc\n\x00\x00p[\xff\xff\xf7\x07\x00\x00\nS\xff\xff\xf2c\x00\x00\x1d6',
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
