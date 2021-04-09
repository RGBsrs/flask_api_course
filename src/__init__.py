from flask import Flask
from .routes import FilmListApi


def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', view_func=FilmListApi.as_view(''), strict_slashes = False)

    return app


