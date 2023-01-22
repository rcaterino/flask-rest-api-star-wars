"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, planet_favourites, people_favourites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# get all people
@app.route('/allpeople', methods=['GET'])
def getAllPeople():
    try:
        people = People.query.all()
        people_serialize = list(map(lambda x: x.serialize(), people))
        return jsonify(people_serialize), 200
    except:
        raise APIException('No hay personajes en la BBDD', 404)


# get one people
@app.route('/allpeople/<int:people_id>')
def getOnePeople(people_id):
    try:
        people = People.query.get(people_id)
        return jsonify(people.serialize()), 200
    except:
        raise APIException('Personaje no encontrado', 404)


# get all planets
@app.route('/allplanets', methods=['GET'])
def getAllPlanets():
    try:
        planet = Planet.query.all()
        planet_serialize = list(map(lambda x: x.serialize(), planet))
        return jsonify(planet_serialize), 200
    except:
        raise APIException('No hay planetas en la BBDD', 404)

# get one planet
@app.route('/allplanets/<int:planet_id>')
def getOnePlanet():
    try:
        planet = Planet.query.get(planet_id)
        return jsonify(planet.serialize())
    except:
        raise APIException('Planeta no encontrado', 404)

# get all users
@app.route('/allusers', methods=['GET'])
def getAllUsers():
    try:
        users = User.query.all()
        users_serialize = list(map(lambda x: x.serialize(), users))
        return jsonify(people_serialize), 200
    except:
        raise APIException('No hay usuarios en la BBDD', 404)

# get user favourites
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def getUserFavorites(user_id):
    user = User.query.get(user_id)

    if not user:
        raise APIException('Usuario no existe', 404)

    favourites = [fav.serialize() for fav in user.planet_favourites + user.people_favourites]

    return jsonify(favourites), 200


# Add favourite planet
@app.route('/favourite/planet/<int:planet_id>', methods=['POST'])
def addFavouritePlanet(planet_id):
    #Asumimos que nos llega un body -> {"User": id}
    resquest_body = request.json.get('User')

    user = User.query.get(resquest_body)
    if not user:
        raise APIException('Usuario no existe', 404)

    planet = Planet.query.get(planet_id)
    if not planet:
        raise APIException('Planeta no existe', 404)

    if planet in user.planet_favourites:
        raise APIException('Planeta ya está en favoritos', 404)

    user.planet_favourites.append(planet)
    db.session.commit()
    return jsonify(f"Planeta {planet} añadido"), 200


# add favourite character
@app.route('/favourite/character/<int:people_id>', methods=['POST'])
def addFavouriteCharacter(people_id):
    #Asumimos que nos llega un body -> {"User": id}
    resquest_body = request.json.get('User')

    user = User.query.get(resquest_body)
    if not user:
        raise APIException('Usuario no existe', 404)

    people = People.query.get(people_id)
    if not people:
        raise APIException('Personaje no existe', 404)

    if people in user.people_favourites:
        raise APIException('Personaje ya está en favoritos', 404)

    user.people_favourites.append(people)
    db.session.commit()
    return jsonify(f"Personaje {people} añadido"), 200


# delete favourite planet
@app.route('/favourite/planet/<int:planet_id>', methods=['DELETE'])
def deleteFavouritePlanet(planet_id):

    #Asumimos que nos llega un body -> {"User": id}
    resquest_body = request.json.get('User')

    user = User.query.get(resquest_body)
    if not user:
        raise APIException('Usuario no existe', 404)

    planet = Planet.query.get(planet_id)
    if not planet:
        raise APIException('Planeta no existe', 404)

    if planet not in user.planet_favourites:
        raise APIException('Planeta no existe en favoritos', 404)

    user.planet_favourites.remove(planet)
    db.session.commit()
    return jsonify(f'El planeta {planet} ha sido eliminado de favoritos'), 200

# delete favourite people
@app.route('/favourite/planet/<int:people_id>', methods=['DELETE'])
def deleteFavouritePeople(people_id):

    #Asumimos que nos llega un body -> {"User": id}
    resquest_body = request.json.get('User')

    user = User.query.get(resquest_body)
    if not user:
        raise APIException('Usuario no existe', 404)

    people = People.query.get(people_id)
    if not people:
        raise APIException('Personaje no existe', 404)

    if people not in user.people_favourites:
        raise APIException('El personaje no existe en favoritos', 404)

    user.people_favourites.remove(people)
    db.session.commit()
    return jsonify(f'El personaje {people} ha sido eliminado de favoritos'), 200


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)