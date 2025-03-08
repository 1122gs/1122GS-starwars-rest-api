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
from models import db, User, People, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify(people)


@app.route('/people/<int:id>')
def get_one_person(id):
    people = People.query.get(id)
    return jsonify(people)


@app.route('/planet')
def get_planets():
    planet = Planet.query.all()
    return jsonify(planet)


@app.route('/planet/<int:id>')
def get_one_planet(id):
    get_planet = Planet.query.get(id)
    return jsonify(get_planet)


@app.route('/users')
def get_user():
    this_user = User.query.all()
    return jsonify(this_user)


@app.route('/users/favorite')
def get_user_favorite():
    user_id = Favorite().user_favorite
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify(favorites)


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify(new_favorite.serialize()), 201


@app.route('/favorite/people/<int:id>', methods=["POST"])
def add_people_favorite(id):
     user_id = request.json.get()
     new_favorite = Favorite(user_id=user_id, people_id=id)     
     db.session.add(new_favorite)
     db.session.commit()

     return jsonify({"message": "Favorite added successfully", "favorite": {
        "id": new_favorite.id,
        "people_favorite": new_favorite.people_favorite,
    }}), 201



@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet removed"}), 200



@app.route('/favorite/people/<int:id>', methods=["DELETE"])
def delete_people_favorite(people_id):
    user_id = request.json.get("user_id")
    people_fav = Favorite.query.filter_by(user_id=user_id, people_favorite=people_id).first
    db.session.delete(people_fav)
    db.session.commit()


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
