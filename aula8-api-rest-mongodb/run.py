# Importar o Flask do pacote api
from api import app, mongo
# Importando a classe Movie que está no model
from api.models.movie_model import Movie
# Importando o service
from api.services import movies_services
# Rodando a aplicação
if __name__ == "__main__":
    # Criando o banco com suas coleções
    with app.app_context():
        # Cria a coleção caso ela não exista
        if 'movies' not in mongo.db.list_collection_names():
            movie = Movie(title='',description='',year=0)
            movies_services.add_movie(movie)
            
    app.run(host="localhost",port="5000",debug=True)