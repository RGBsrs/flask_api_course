import config
from flask import Flask
from .routes import FilmListApi
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(config.Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
film_list_api = FilmListApi.as_view('films')
app.add_url_rule('/films', view_func=film_list_api, strict_slashes = False)
app.add_url_rule('/films/<uuid>', view_func=film_list_api, strict_slashes = False)