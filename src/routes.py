from flask.views import MethodView
from flask import request

data = [
    {
        'id': '1',
        'titile': 'new film',
        'release_date':'1.01.01'
    },
    {
        'id': '2',
        'titile': 'new film 2',
        'release_date':'1.01.02'
    }
]


def get_all_films():
    return data[0]

def get_film_by_uuid(uuid: str) -> dict:
    films =get_all_films()
    film = list(filter(lambda f: f['id'] == uuid, films))
    return film[0] if film else {}

def create_film():
    pass

class FilmListApi(MethodView):
    def get(self, uuid = None):
        if not uuid:
            films = get_all_films()
            return films,200
        film = get_film_by_uuid(uuid)
        if not film:
            return '', 404
        return film, 200
        
    def post(self):
        film_json = request.json
        return create_film(film_json),200

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass



