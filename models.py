
from index import db
from sqlalchemy.dialects.postgresql import JSON


class Expression(db.Model):
    __tablename__ = 'expression'

    id = db.Column(db.Integer, primary_key=True)
    finnish = db.Column(db.String())
    swedish = db.Column(db.String())
 
    def __init__(self, finnish, swedish):
        self.finnish = finnish
        self.swedish = swedish

class Favorites(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    expression_id = db.Column(db.Integer, db.ForeignKey('expression.id'))
    user_name = db.Column(db.String(50))  
 
    def __init__(self, user_name, expression_id):
        self.user_name = user_name
        self.expression_id = expression_id
