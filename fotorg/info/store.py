from pathlib import Path
from sqlalchemy import Column, DateTime, Integer, String, Float  # , ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from PIL import Image

from fotorg.info.data.file import File
from fotorg.info.data.exif import Exif

Base = declarative_base()


class BadeDir(Base):
    __tablename__ = 'base_dir'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, default='/')

    def __str__(self) -> str:
        return str(self.path)


class FotoItem(Base):
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

    def __str__(self) -> str:
        return f'{self.relative_path}/{self.file_name} {self.camera_make} {self.camera_model}'


class Store:
    def __init__(self, item: Path, directory: Path):
        self.__item = item
        self.__directory = directory

    def prepare_store(self) -> FotoItem:
        file = File(self.__item, self.__directory)
        try:
            image = Image.open(file.path, mode='r')
            foto = Exif(image.getexif())
        except Exception:
            foto = Exif({})
        return FotoItem(
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
