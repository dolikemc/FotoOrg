""" Store module containing the entity classes and the store"""
import logging
from pathlib import Path
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Float, UniqueConstraint, Index
# for SQLAlchemy >= 1.4 switch to this
# from sqlalchemy.orm import declarative_base
# https://github.com/kvesteri/sqlalchemy-continuum/issues/255
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_continuum import make_versioned

from PIL import Image, UnidentifiedImageError

# FileNotFoundError: If the file cannot be found.
#     :exception PIL.UnidentifiedImageError

from fotorg.info.data.file import File
from fotorg.info.data.exif import Exif

make_versioned(user_cls=None)
Base = declarative_base()
log = logging.getLogger('fotorg.info.store')


class BaseDir(Base):
    """
    Base directory entity
    """
    __tablename__ = 'base_dir'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, default='/', unique=True)
    user_name = Column(String, default='')
    created = Column(DateTime, default=datetime.now())
    scan_start = Column(DateTime, default=datetime.now())
    last_used = Column(DateTime, default=datetime.now())

    @property
    def as_path(self) -> Path:
        return Path(self.path)

    def __str__(self) -> str:
        return self.path


class FotoItem(Base):
    """
    Foto item entity
    """
    __versioned__ = {}
    __tablename__ = 'foto_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    relative_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_created = Column(DateTime, nullable=False)
    file_modified = Column(DateTime)
    foto_created = Column(DateTime)
    camera_make = Column(String)
    camera_model = Column(String)
    gps_longitude = Column(Float)
    gps_latitude = Column(Float)
    gps_altitude = Column(Float)

    UniqueConstraint(file_name, relative_path)
    Index(file_name, relative_path)

    @property
    def as_path(self) -> Path:
        return Path(self.relative_path) / self.file_name

    def __str__(self) -> str:
        return f'{self.relative_path}/{self.file_name} {self.camera_make} {self.camera_model}'


class Store:
    """
    Store class to extract from given file name a storable foto item object
    """

    def __init__(self, item: Path, directory: Path):
        self.__item = item
        self.__directory = directory

    def prepare_store(self) -> FotoItem:
        """
        :return: Storable entity
        :exception FileNotFoundError: If the file cannot be found.
        """
        file = File(self.__item, self.__directory)
        try:
            with Image.open(file.path, mode='r') as image:
                log.debug(f"{self.__item} scanned for foto information")
                foto = Exif(image.getexif())
        except UnidentifiedImageError:
            log.warning(f"PIL can't identify {self.__item} as a image file format")
            foto = Exif({})
        return FotoItem(
            file_name=file.name,
            relative_path=file.relative_path.as_posix(),
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

    def __str__(self) -> str:
        return (self.__directory / self.__item).as_posix()
