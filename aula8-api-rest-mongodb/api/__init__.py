from flask import Flask
# Importando Flask Restful
from flask_restful import Api
# Importando o PyMongo
from flask_pymongo import PyMongo
# Importando o Marshmallow (validação dos dados)
from flask_marshmallow import Marshmallow
# Carregando o Flask
app = Flask(__name__)
# Carregando o Marshmallow
ma = Marshmallow(app)
# Configurando o Flask com o MongoDB
app.config["MONGO_URI"] = 'mongodb://localhost:27017/api-movies'
# Carregando o Flask-Restful
api = Api(app)
# Carregando o PyMongo
mongo = PyMongo(app)
# Importando os recursos
from .resources import movies_resources