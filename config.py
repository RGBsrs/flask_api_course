import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or \
        'sqlite:///' + f"{BASE_DIR}/data/db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'very secret key'