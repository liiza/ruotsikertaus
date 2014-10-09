from app import db
from sqlalchemy.dialects.postgresql import JSON


class Expression(db.Model):
    __tablename__ = 'expression'

    id = db.Column(db.Integer, primary_key=True)
    finnish_translation = db.Column(db.String())
    swedish_translation = db.Column(db.String())

    def __init__(self, finnish, swedish):
        self.finnish_translation = finnish
        self.swedish_translation = swedish
