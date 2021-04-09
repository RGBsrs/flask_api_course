from operator import ge
from flask.views import MethodView
from flask import request, jsonify
from . import app, db
from .models import Film
from datetime import datetime

class FilmListApi(MethodView):
    def get(self, uuid = None):
        if not uuid:
            films = db.session.query(Film).all()
            return jsonify([f.serialize() for f in films]), 200
        film = db.session.query(Film).filter_by(uuid = uuid).first()
        if not film:
            return '', 404
        return jsonify(film.serialize()), 200
        
    def post(self):
        film_json = request.get_json()
        if not film_json:
            return {'Message' : 'Missed data'}, 400
        try:
            film = Film(
                title = film_json['title'],
                release_date = datetime.strptime(film_json['release_date'], '%B %d, %Y'),
                distributed_by = film_json['distributed_by'],
                description = film_json.get('description'),
                length = film_json.get('length'),
                rating = film_json.get('rating')
            )
            db.session.add(film)
            db.session.commit()
        except (ValueError, KeyError):
            return {'Message' : 'Wrong data error'}, 400
        return {'Message' : 'Created'}, 201

    def put(self, uuid):
        film_json = request.get_json()
        if not film_json:
            return {'Message' : 'Missed data'}, 400
        try:
            db.session.query(Film).filter_by(uuid=uuid).update(
                dict(
                    title = film_json['title'],
                    release_date = datetime.strptime(film_json['release_date'], '%B %d, %Y'),
                    distributed_by = film_json['distributed_by'],
                    description = film_json.get('description'),
                    length = film_json.get('length'),
                    rating = film_json.get('rating')
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            return {'Message' : 'Wrong data error'}, 400
        return {'Message' : 'Updated'}, 200
        

    def patch(self, uuid):
        film = db.session.query(Film).filter(uuid==uuid).first()
        if not film:
            return '', 404
        film_json = request.get_json()
        title = film_json.get('title')
        release_date = datetime.strptime(film_json.get('release_date'), '%B %d, %Y') if film_json.get(
            'release_date') else None
        distributed_by = film_json.get('distributed_by')
        description = film_json.get('description')
        length = film_json.get('length')
        rating = film_json.get('rating')
        if title:
            film.title = title
        elif release_date:
            film.release_date = release_date
        elif distributed_by:
            film.distributed_by = distributed_by
        elif description:
            film.description = description
        elif length:
            film.length = length
        elif rating:
            film.rating = rating
        db.session.add(film)
        db.session.commit()
        return {'Message' : 'Patched'}, 200

    def delete(self, uuid):
        film = db.session.query(Film).filter(uuid==uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204



film_list_api = FilmListApi.as_view('films')
app.add_url_rule('/films', view_func=film_list_api, strict_slashes = False)
app.add_url_rule('/films/<uuid>', view_func=film_list_api, strict_slashes = False)