from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src.schemas.users import UserSchema
from src import db

class AuthRegister(MethodView):
    user_schema = UserSchema

    def post(self):
        try:
            user = self.user_schema.load(request.json, session = db.session)
        except ValidationError as e:
            return {'Message' : f'Error : {e}'}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {'Message' : 'Such user exists'}, 409
        return jsonify(self.user_schema.dump(user)), 201