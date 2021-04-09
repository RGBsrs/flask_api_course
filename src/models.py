import uuid
from . import db

class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    release_date = db.Column(db.Date, index = True, nullable = False)
    uuid = db.Column(db.String(36), unique = True)
    description = db.Column(db.Text)
    ditributed_by = db.Column(db.String(120), nullable = False)
    length = db.Column(db.Float)
    rating = db.Column(db.Float)

    def __init__(self, title, release_date, description, ditributed_by, length, rating ):
        self.title = title
        self.release_date = release_date
        self.description = description
        self.ditributed_by = ditributed_by
        self.length = length
        self.rating = rating
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Film({self.title}, {self.uuid}, {self.ditributed_by}, {self.release_date})' 
    
    def serialize(self):
        return {
            'title' : self.title,
            'uuid' : self.uuid,
            'release_date' : self.release_date,
            'description' : self.description,
            'distributed_by' : self.ditributed_by,
            'length' : self.length,
            'rating' : self.rating
        }