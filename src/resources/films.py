from flask.views import MethodView
from flask import request, jsonify
from marshmallow import ValidationError

from src import db
from src.database.models import Film
from src.schemas.films import FilmSchema
from src.resources.auth import token_required
from src.services.film_service import FilmService



class FilmListApi(MethodView):
    film_shema = FilmSchema()

    def get(self, uuid = None):
        if not uuid:
            films = FilmService.fetch_all_films(db.session).all()
            return jsonify(self.film_shema.dump(films, many = True)), 200
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        return jsonify(self.film_shema.dump(film)), 200
        
    def post(self):
        try:
            film = self.film_shema.load(request.json, session = db.session)
        except ValidationError as e:
            return {'Message': f'error: {e}'}, 400
        db.session.add(film)
        db.session.commit()
        return jsonify(self.film_shema.dump(film)), 201

    def put(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        try:
            film = self.film_shema.load(request.json, instance = film, session = db.session)
        except ValidationError as e:
            return {'Message': f'error: {e}'}, 400
        db.session.add(film)
        db.session.commit()    
        return jsonify(self.film_shema.dump(film)), 200

    def patch(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        try:
            film = self.film_shema.load(request.json, instance = film, session = db.session,
                partial = True )
        except ValidationError as e:
            return {'Message': f'error: {e}'}, 400
        db.session.add(film)
        db.session.commit()    
        return jsonify(self.film_shema.dump(film)), 200


    def delete(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204

