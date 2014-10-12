
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

"""class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def is_active(self):
	return True
	
    def is_authenticated(self):
	return True
	
    def is_anonymous(self):
	return False
   
    def get_id(self):
	try:
	    return unicode(self.id)
	except:
	    return None
    
    def __init__(self, name):
        self.name = name"""

  
