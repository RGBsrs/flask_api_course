from flask.views import MethodView
from sqlalchemy import func

from src import db
from src.database.models import Film

class AggregationApi(MethodView):
    def get(self):
        films_count = db.session.query(func.count(Film.id)).scalar()
        max_rating = db.session.query(func.max(Film.rating)).scalar()
        min_rating = db.session.query(func.min(Film.rating)).scalar()
        avg_rating = db.session.query(func.avg(Film.rating)).scalar()
        sum_rating = db.session.query(func.sum(Film.rating)).scalar()
        return {
            'count': films_count,
            'max': max_rating, 
            'min': min_rating,
            'avg' : avg_rating,
            'sum' :sum_rating
        }