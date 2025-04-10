from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    image = db.Column(db.String(150),unique=True,nullable=False)
    collection = db.Column(db.String(150))
    
    def __init__(self,name,image,collection):
        self.name = name
        self.image = image
        self.collection = collection