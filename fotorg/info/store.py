from sqlalchemy import Column, DateTime, Integer, String  # , ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from typing import Dict
from datetime import datetime
from geopy.point import Point

Base = declarative_base()


class FotoItem(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    created = Column(DateTime)
    size = Column(Integer)


class Store:
    def __init__(self, data: Dict):
        self.__data = data

    """
       
        # GPSInfo = {
        1: 'N', 2: (44.0, 49.0, 20.06), 
        3: 'E', 4: (20.0, 24.0, 38.94), 
        5: b'\x00', 
        6: 89.0, 
        7: (10.0, 43.0, 54.37), 
        12: 'K', 13: 0.0, 16: 'T', 17: 246.48684210526315, 23: 'T', 
        24: 246.48684210526315, 29: '2016:06:16', 31: 65.0}
     0: "GPSVersionID",
    1: "GPSLatitudeRef",
    2: "GPSLatitude",
    3: "GPSLongitudeRef",
    4: "GPSLongitude",
    5: "GPSAltitudeRef",
    6: "GPSAltitude",
    7: "GPSTimeStamp",
    

    """

    @property
    def image_description(self) -> str:
        """010e	ImageDescription	Titel des Bildes und kurze Bildbeschreibung"""
        return self.__data.get(0x010e, 'N/A')

    @property
    def artist(self) -> str:
        """013B	Artist	Ersteller/Photograph"""
        return self.__data.get(0x013B, 'N/A')

    @property
    def copyright(self) -> str:
        """8298	Copyright	Urheberrechts-Information"""
        return self.__data.get(0x8298, 'N/A')

    @property
    def user_comment(self) -> str:
        """9286	UserComment	Allgemeiner Kommentar oder Bildbeschreibung. Unicode-fähig"""
        return self.__data.get(0x9286, 'N/A')

    @property
    def metering_mode(self) -> int:
        """9207	MeteringMode	Belichtungsmessverfahren Mittelwert/Spot/Multisegment"""
        return int(self.__data.get(0x9207, 0))

    @property
    def iso_speed(self) -> int:
        """8833	ISOSpeed	Empfindlichkeit des Bildsensors"""
        return int(self.__data.get(0x8833, 0))

    @property
    def exposure_time(self) -> float:
        """829A	ExposureTime	Belichtungszeit, e.g. 1/175"""
        return float(self.__data.get(0x829A, 0.0))

    @property
    def f_number(self) -> str:
        """829D	FNumber	Blendenzahl, e.g. f/2,2"""
        return self.__data.get(0x8290, 'N/A')

    @property
    def exif_version(self) -> str:
        """9000	ExifVersion	Version des Exif-Standards"""
        return self.__data.get(0x9000, 'N/A')

    @property
    def make(self) -> str:
        """010F	Make	Name des Kameraherstellers"""
        return self.__data.get(0x010F, 'N/A')

    @property
    def camera_model(self) -> str:
        """0110	Model	Name des Kamera-Modells"""
        return self.__data.get(0x0110, 'N/A')

    @property
    def orientation(self) -> int:
        """0112	Orientation	Bild-Ausrichtung Hochformat / Querformat"""
        return int(self.__data.get(0x0112, 0))

    @property
    def resolution_unit(self) -> int:
        """Optional resolution unit"""
        return int(self.__data.get(0x0128, 0))

    @property
    def resolution_x(self) -> float:
        """Optional resolution, x axis"""
        return float(self.__data.get(0x011A, 0.0))

    @property
    def resolution_y(self) -> float:
        """Optional resolution, x axis"""
        return float(self.__data.get(0x011B, 0.0))

    @property
    def height(self) -> int:
        """Optional image height"""
        return int(self.__data.get(0xA003, 0))

    @property
    def width(self) -> int:
        """Optional image width"""
        return int(self.__data.get(0xA002, 0))

    @property
    def brightness(self) -> float:
        """Optional brightness"""
        return float(self.__data.get(0x9203, 0.0))

    @property
    def created(self) -> datetime:
        """9003	DateTimeOriginal	Aufnahmedatum
        # DateTimeOriginal = 2016:06:16 12:43:55"""
        date_values = [int(x) for x in self.__data.get(0x9003, '1970:01:01 00:00:00').replace(' ', ':').split(':')]
        return datetime(date_values[0], date_values[1], date_values[2], date_values[3], date_values[4], date_values[5])

    @property
    def gps_info(self) -> Point:
        """0x8825: "GPSInfo"""
        geo_data = self.__data.get(0x8825, None)
        if geo_data is None:
            return Point()
        latitude = Point.parse_degrees(*geo_data[2], geo_data[1])
        longitude = Point.parse_degrees(*geo_data[4], geo_data[3])
        alt_unit = 'km'
        if str(geo_data[5]).lower() in ['m', 'mi', 'ft', 'nm', 'nmi']:
            alt_unit = str(geo_data[5]).lower()
        altitude = Point.parse_altitude(geo_data[6], alt_unit)
        # GPSInfo = {1: 'N', 2: (44.0, 49.0, 20.06), 3: 'E', 4: (20.0, 24.0, 38.94), 5: b'\x00', 6: 89.0, 7: (10.0, 43.0, 54.37), 12: 'K', 13: 0.0, 16: 'T', 17: 246.48684210526315, 23: 'T', 24: 246.48684210526315, 29: '2016:06:16', 31: 65.0}
        return Point(latitude=latitude, longitude=longitude, altitude=altitude)
