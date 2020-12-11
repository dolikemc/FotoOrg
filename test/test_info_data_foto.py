import unittest
from datetime import datetime

from fotorg.info.data.exif import Exif


class TestInfoDataFoto(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.item = Exif({34665: 204, 36864: b'0221', 37121: b'\x01\x02\x03\x00', 37377: 7.450526315789474,
                         36867: '2016:06:16 12:43:55', 36868: '2016:06:16 12:43:55', 37378: 2.2750071245369052,
                         37379: 6.454077883908891, 37380: 0.0, 37383: 5, 37385: 24, 37386: 4.15, 40961: 1, 40962: 3264,
                         41989: 29, 41990: 0, 40963: 2448, 37521: '173', 37522: '173', 37396: (1631, 1223, 1795, 1077),
                         41495: 2,
                         33434: 0.005714285714285714, 33437: 2.2, 41729: b'\x01', 34850: 2, 34855: 32, 41986: 0,
                         40960: b'0100',
                         41987: 0, 42034: (4.15, 4.15, 2.2, 2.2), 42035: 'Apple',
                         42036: 'iPhone 6 back camera 4.15mm f/2.2',
                         296: 2, 282: 72.0,
                         34853: {1: 'N', 2: (44.0, 49.0, 20.06), 3: 'E', 4: (20.0, 24.0, 38.94), 5: b'\x00', 6: 89.0,
                                 7: (10.0, 43.0, 54.37), 12: 'K', 13: 0.0, 16: 'T', 17: 246.48684210526315, 23: 'T',
                                 24: 246.48684210526315, 29: '2016:06:16', 31: 65.0}, 271: 'Apple', 272: 'iPhone 6',
                         305: '9.3.2', 274: 6, 306: '2016:06:16 12:43:55', 531: 1, 283: 72.0})

    def test_init(self):
        photo_org_store = Exif({})
        self.assertTrue(photo_org_store)

    def test_no_info(self):
        item = Exif({})
        self.assertEqual(item.gps_info.longitude, 0)
        item2 = Exif({34853: {1: 'N', 2: (44.0, 49.0, 20.06), 3: 'E', 4: (20.0, 24.0, 38.94), 5: 'm', 6: 89.0, }})
        self.assertEqual(item2.gps_info.altitude, 0.089)

    def test_info_data_foto_camera_model(self) -> None:
        self.assertEqual(self.item.camera_model, 'iPhone 6')

    def test_info_data_foto_make(self) -> None:
        self.assertEqual(self.item.make, 'Apple')

    def test_info_data_foto_created(self) -> None:
        self.assertEqual(self.item.created, datetime(2016, 6, 16, 12, 43, 55))

    def test_info_data_foto_orientation(self) -> None:
        self.assertEqual(self.item.orientation, 6)

    def test_info_data_foto_resolution(self) -> None:
        self.assertEqual(self.item.resolution_unit, 2)

    def test_info_data_foto_resolution_x(self) -> None:
        self.assertEqual(self.item.resolution_x, 72.0)

    def test_info_data_foto_resolution_y(self) -> None:
        self.assertEqual(self.item.resolution_y, 72.0)

    def test_info_data_foto_height(self) -> None:
        self.assertEqual(self.item.height, 2448)

    def test_info_data_foto_width(self) -> None:
        self.assertEqual(self.item.width, 3264)

    def test_info_data_foto_brightness(self) -> None:
        self.assertEqual(self.item.brightness, 6.454077883908891)

    def test_info_data_foto_exif_version(self) -> None:
        self.assertEqual(self.item.exif_version, b'0221')

    def test_info_data_foto_f_number(self) -> None:
        self.assertEqual(self.item.f_number, 'N/A', 'but should be f/2,2')

    def test_info_data_foto_exposure_time(self) -> None:
        self.assertAlmostEqual(self.item.exposure_time, 1.0 / 175.0, 2)

    def test_info_data_foto_speed(self) -> None:
        self.assertEqual(self.item.iso_speed, 0)

    def test_info_data_foto_m_mode(self) -> None:
        self.assertEqual(self.item.metering_mode, 5)

    def test_info_data_foto_artist(self) -> None:
        self.assertEqual(self.item.artist, 'N/A')

    def test_info_data_foto_c_r(self) -> None:
        self.assertEqual(self.item.copyright, 'N/A')

    def test_info_data_foto_description(self) -> None:
        self.assertEqual(self.item.image_description, 'N/A')

    def test_info_data_foto_comment(self) -> None:
        self.assertEqual(self.item.user_comment, 'N/A')

    def test_info_data_foto_longitude(self) -> None:
        self.assertAlmostEqual(self.item.gps_info.longitude, 20, 0)

    def test_info_data_foto_latitude(self) -> None:
        self.assertAlmostEqual(self.item.gps_info.latitude, 44.8, 1)

    def test_info_data_foto_altitude(self) -> None:
        self.assertEqual(self.item.gps_info.altitude, 89.0, 'km')
