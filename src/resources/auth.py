import datetime
from functools import wraps

import jwt
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import check_password_hash
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src import db,app
from src.schemas.users import UserSchema
from src.database.models import User

class AuthRegister(MethodView):
    user_schema = UserSchema()

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


class AuthLogin(MethodView):
    def get(self):
        auth = request.authorization
        if not auth:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = User.find_user_by_username(auth.get('username', ''))    
        if not user or not check_password_hash(user.password, auth.get('password','')):
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        token = jwt.encode(
            {
                'user_id' : user.uuid,
                'exp' : datetime.datetime.now() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY']
        )
        return jsonify(
            {
                "token": token
            }
        )


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-API-KEY', '')
        if not token:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        try:
            uuid = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = User.find_user_by_uuid(uuid)
        if not user:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        return func(self, *args, **kwargs)

    return wrapper