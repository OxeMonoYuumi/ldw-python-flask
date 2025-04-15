# Importando a classe Resource do Flask-restful
from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from ..schemas import movie_schema
from ..models import movie_model
from ..services import movies_services
class MovieList(Resource):
    def get(self):
        movies = movies_services.get_movies()
        mv = movie_schema.MovieSchema(many=True)
        return make_response(mv.jsonify(movies), 200) 
        # Retornando status de OK
    def post(self):
        mv = movie_schema.MovieSchema()
        validate = mv.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
            # 400 = Bad Request
        else:
            # Validação bem sucedida, irá realizar o cadastro
            title = request.json["title"]
            description = request.json["description"]
            year = request.json["year"]
            new_movie = movie_model.Movie(title=title,description=description,year=year)
            result = movies_services.add_movie(new_movie)
            res = mv.jsonify(result)
            return make_response(res,201) # 201 = Create
class MovieDetail(Resource):
    def delete(self, id):
        movie = movies_services.get_movie_by_id(id)
        if movie is None:
            return make_response(jsonify("Filme não encontrado"),400)
        movies_services.delete_movie(id)
        return make_response(jsonify("Filme excluído com sucesso"),204) #204 = No content
        
api.add_resource(MovieList, '/movies')
api.add_resource(MovieDetail, '/movie/<id>')