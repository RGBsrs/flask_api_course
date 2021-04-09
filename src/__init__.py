from flask import Flask
from .routes import FilmListApi


def create_app():
    app = Flask(__name__)
    
    film_list_api = FilmListApi.as_view('films')
    app.add_url_rule('/films', view_func=film_list_api, strict_slashes = False)
    app.add_url_rule('/films/<uuid>', view_func=film_list_api, strict_slashes = False)

    return app


