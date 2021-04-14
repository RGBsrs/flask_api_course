import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + f"{BASE_DIR}/data/db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'very secret key'