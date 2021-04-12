from flask.globals import session
from flask.views import MethodView
from flask import request, jsonify
from marshmallow import ValidationError
from src import app, db
from src.models import Film
from src.schemas import FilmSchema, ActorSchema

class FilmListApi(MethodView):
    film_shema = FilmSchema()

    def get(self, uuid = None):
        if not uuid:
            films = db.session.query(Film).all()
            return jsonify(self.film_shema.dump(films, many = True)), 200
        film = db.session.query(Film).filter_by(uuid = uuid).first()
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
        film = db.session.query(Film).filter_by(uuid = uuid).first()
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
        film = db.session.query(Film).filter_by(uuid = uuid).first()
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
        film = db.session.query(Film).filter(uuid==uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204


class FilmListApi(MethodView):
    film_shema = FilmSchema()

    def get(self, uuid = None):
        if not uuid:
            films = db.session.query(Film).all()
            return jsonify(self.film_shema.dump(films, many = True)), 200
        film = db.session.query(Film).filter_by(uuid = uuid).first()
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
        film = db.session.query(Film).filter_by(uuid = uuid).first()
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
        film = db.session.query(Film).filter_by(uuid = uuid).first()
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
        film = db.session.query(Film).filter(uuid==uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204


film_list_api = FilmListApi.as_view('films')
app.add_url_rule('/films', view_func=film_list_api, strict_slashes = False)
app.add_url_rule('/films/<uuid>', view_func=film_list_api, strict_slashes = False)