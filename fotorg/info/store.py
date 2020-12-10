from sqlalchemy import Column, DateTime, Integer, String, Float  # , ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BadeDir(Base):
    __tablename__ = 'base_dir'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, default='/')


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


