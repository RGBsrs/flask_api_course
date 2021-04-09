import pathlib

BASE_DIR = pathlib.Path(__file__).parent

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + f"{BASE_DIR}/data/db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATONS = False