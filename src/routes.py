from flask.views import MethodView
from flask import request
from typing import List


def get_all_films():
    return [
    {
        'id': '1',
        'title': 'new film',
        'release_date':'1.01.01',
    },
    {
        'id': '2',
        'title': 'new film 2',
        'release_date':'1.01.02',
    },
    ]

def get_film_by_uuid(uuid: str) -> dict:
    films = get_all_films()
    film = list(filter(lambda f: f['id'] == uuid, films))
    return film[0] if film else {}

def create_film(film_json: dict) -> List[dict]:
    films = get_all_films()
    films.append(film_json)
    return str(films)

class FilmListApi(MethodView):
    def get(self, uuid = None):
        if not uuid:
            films = get_all_films()
            return str(films), 200
        film = get_film_by_uuid(uuid)
        if not film:
            return '', 404
        return film, 200
        
    def post(self):
        film_json = request.get_json()
        return create_film(film_json),201

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass



