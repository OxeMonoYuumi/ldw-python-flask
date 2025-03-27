from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    type = db.Column(db.String(75))
    color = db.Column(db.String(75))
    rarity = db.Column(db.String(50))
    qtd = db.Column(db.Integer)
    collection = db.Column(db.String(100))
    
    def __init__(self,name,type,color,rarity,qtd,collection):
        self.name = name
        self.type = type
        self.color = color
        self.rarity = rarity
        self.qtd = qtd
        self.collection = collection
    