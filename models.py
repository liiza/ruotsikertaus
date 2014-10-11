
from hello import db
from sqlalchemy.dialects.postgresql import JSON


class Expression(db.Model):
    __tablename__ = 'expression'

    id = db.Column(db.Integer, primary_key=True)
    finnish = db.Column(db.String())
    swedish = db.Column(db.String())

    def __init__(self, finnish, swedish):
        self.finnish = finnish
        self.swedish = swedish
