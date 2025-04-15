from bson import ObjectId
from api import mongo
from ..models import movie_model
# Método para cadastrar
def add_movie(movie):
    result=mongo.db.movies.insert_one({
        'title': movie.title,
        'description': movie.description,
        'year': movie.year
    })
    # Buscar o filme recém adicionado
    new_movie = mongo.db.movies.find_one({'_id': result.inserted_id})
    return new_movie
# Métodos para listar

# Métodos estáticos não precisam de instância
@staticmethod
def get_movies():
    return list(mongo.db.movies.find())
@staticmethod
def delete_movie(id):
    mongo.db.movies.delete_one({'_id':ObjectId(id)})
def get_movie_by_id(id):
    return mongo.db.movies.find_one({'_id': ObjectId(id)})