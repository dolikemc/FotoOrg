from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from PIL.ExifTags import TAGS, GPSTAGS
from typing import Dict
from datetime import datetime

Base = declarative_base()


class Item(Base):
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
       
        # GPSInfo = {1: 'N', 2: (44.0, 49.0, 20.06), 3: 'E', 4: (20.0, 24.0, 38.94), 5: b'\x00', 6: 89.0, 7: (10.0, 43.0, 54.37), 12: 'K', 13: 0.0, 16: 'T', 17: 246.48684210526315, 23: 'T', 24: 246.48684210526315, 29: '2016:06:16', 31: 65.0}
 
    """

    @staticmethod
    def __get_tag(name: str) -> str:
        return next(filter(lambda x: TAGS[x] == name, TAGS), None)

    @property
    def camera_model(self) -> str:
        tag = self.__get_tag('Model')
        if tag is None:
            return ''
        return self.__data[tag]

    @property
    def orientation(self) -> int:
        tag = self.__get_tag('Orientation')
        if tag is None:
            return 0
        return int(self.__data[tag])

    @property
    def resolution_unit(self) -> int:
        tag = self.__get_tag('ResolutionUnit')
        if tag is None:
            return 0
        return int(self.__data[tag])

    @property
    def resolution_x(self) -> float:
        tag = self.__get_tag('XResolution')
        if tag is None:
            return 0.0
        return float(self.__data[tag])

    @property
    def resolution_y(self) -> float:
        tag = self.__get_tag('YResolution')
        if tag is None:
            return 0.0
        return float(self.__data[tag])

    @property
    def height(self) -> int:
        tag = self.__get_tag('ExifImageHeight')
        if tag is None:
            return 0
        return int(self.__data[tag])

    @property
    def width(self) -> int:
        tag = self.__get_tag('ExifImageWidth')
        if tag is None:
            return 0
        return int(self.__data[tag])

    @property
    def brightness(self) -> float:
        tag = self.__get_tag('BrightnessValue')
        if tag is None:
            return 0.0
        return float(self.__data[tag])

    @property
    def created(self) -> datetime:
        """# DateTimeOriginal = 2016:06:16 12:43:55"""
        tag = self.__get_tag('DateTimeOriginal')
        if tag is None:
            return datetime(1970, 1, 1, 0, 0, 0, 0)
        date_values = [int(x) for x in self.__data[tag].replace(' ', ':').split(':')]
        return datetime(date_values[0], date_values[1], date_values[2], date_values[3], date_values[4], date_values[5])
