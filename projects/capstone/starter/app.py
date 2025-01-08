#import os
from flask import Flask,jsonify
from flask_cors import CORS
from models import setup_db, Actors,Movies
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors')
    @requires_auth('get:ActorsAndMovies')
    def get_actors():
      try:
        actors = Actors.query.order_by(Actors.id).all()
        print (f"actors: {actors}")
        formated_actors= [actor.format() for actor in actors]
        print (f'formated_actors:{formated_actors}')    
        if len(formated_actors) ==0:
            return not_found(404)
        else:
            return jsonify({ "success": True, "actors": formated_actors})
      except Exception as ex:
        print(ex)
      return unprocessable(422)

    @app.route('/movies')
    @requires_auth('get:ActorsAndMovies')
    def get_movies():
      try:
        movies = Movies.query.order_by(Movies.id).all()
        print (f"movies: {movies}")
        formated_movies= [movie.format() for movie in movies]
        print (f'formated_actors:{formated_movies}')    
        if len(formated_movies) ==0:
            return not_found(404)
        else:
            return jsonify({ "success": True, "movies": formated_movies})
      except Exception as ex:
        print(ex)
      return unprocessable(422)
   
   # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": 404,
                        "message": "resource not found",
                    }
                ),
                404,
            )
# @app.errorhandler(405)
# def method_not_allowed(error):
#         return (
#             jsonify(
#                 {
#                     "success": False,
#                     "error": 405,
#                     "message": "method not allowed",
#                 }
#             ),
#             405,
#         )

    @app.errorhandler(400)
    def bad_request(error):
            return (
                jsonify({"success": False, "error": 400, "message": "bad request"}),
                400,
            )

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response =  jsonify({"success":False,"error":ex.status_code,"message":ex.error}),ex.status_code
        #response.status_code = ex.status_code
        return response
        return app
  
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)