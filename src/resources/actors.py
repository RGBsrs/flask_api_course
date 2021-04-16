from flask.views import MethodView
from flask import request, jsonify
from marshmallow import ValidationError

from src import db
from src.schemas.actors import ActorSchema
from src.services.actor_service import ActorService


class ActorListApi(MethodView):
    actor_shema = ActorSchema()

    def get(self, name = None):
        if not name:
            actors = ActorService.fetch_all_actors(db.session).all()
            return jsonify(self.actor_shema.dump(actors, many = True)), 200
        actor = ActorService.fetch_actor_by_name(db.session, name)
        if not actor:
            return '', 404
        return jsonify(self.actor_shema.dump(actor)), 200
        
    def post(self):
        try:
            actor = self.actor_shema.load(request.json, session = db.session)
        except ValidationError as e:
            return {'Message': f'error: {e}'}, 400
        db.session.add(actor)
        db.session.commit()
        return jsonify(self.actor_shema.dump(actor)), 201

    def put(self, name):
        actor = ActorService.fetch_actor_by_name(db.session, name)
        if not actor:
            return '', 404
        try:
            actor = self.actor_shema.load(request.json, instance = actor, session = db.session)
        except ValidationError as e:
            return {'Message': f'error: {e}'}, 400
        db.session.add(actor)
        db.session.commit()    
        return jsonify(self.actor_shema.dump(actor)), 200

    def patch(self, name):
        actor = ActorService.fetch_actor_by_name(db.session, name)
        if not actor:
            return '', 404
        try:
            actor = self.actor_shema.load(request.json, instance = actor, session = db.session,
                partial = True)
        except ValidationError as e:
            return {'Message': f'error: {e}'}, 400
        db.session.add(actor)
        db.session.commit()    
        return jsonify(self.actor_shema.dump(actor)), 200


    def delete(self, name):
        actor = ActorService.fetch_actor_by_name(db.session, name)
        if not actor:
            return '', 404
        db.session.delete(actor)
        db.session.commit()
        return '', 204
