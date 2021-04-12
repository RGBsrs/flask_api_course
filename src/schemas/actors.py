from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from src.database.models import  Actor


class ActorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        load_instance = True
        include_fk = True
    films = Nested('FilmSchema', many = True, exclude = ('actors',))