"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
import datetime
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Favorites, Planets, Vehicles
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

@app.route('/user', methods=['GET'])
def get_user():

    # get all the user
    result = User.query.all()

    return jsonify(list(map(lambda x: x.serialize(), result))), 200


# [GET] - Getting an spec. User [user]
@app.route('/users/<int:id>', methods=['GET'])
def GetUser(id):
    user = User.query.get(id)

    if user is None:
        raise APIException('User not found.',status_code=403)

    return jsonify(User.serialize(user)), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    request_body = request.get_json()
    if "fullName" in request_body:
        user.fullName = request_body["fullName"]
    if "email" in request_body:
        user.email = request_body["email"]
    if "password" in request_body:
        user.password = request_body["password"]
    if "is_active" in request_body:
        user.is_active = request_body["is_active"]
    db.session.commit()
   
    return jsonify({"Respuesta":"Los datos se modificaron satisfactoriamente"}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    db.session.delete(user)
    db.session.commit()
   
    return jsonify({"Respuesta":"Los datos se eliminaron satisfactoriamente"}), 200

# [POST] - Creating an [user]
@app.route('/user/register', methods=['POST'])
def storeUser():

    data_request = request.get_json()

    user = User.query.filter_by(email=data_request["email"]).first()
    
    # validating if email exists
    if user:
        return jsonify({"msg": "Emails is being used."}), 401

    user = User(fullName = data_request["fullName"],
    email = data_request["email"],
    password = data_request["password"],
    is_active = data_request["is_active"])

    try:
        db.session.add(user)
        db.session.commit()
        
        return jsonify(User.serialize(user)), 201
    
    except AssertionError as exception_message: 
        return jsonify(msg='Error: {}. '.format(exception_message)), 400


# @app.route('/user', methods=['POST'])
# def add_user():
#     request_body = request.get_json()
#     user = User(fullName = request_body["fullName"],
#     email = request_body["email"],
#     password = request_body["password"],
#     is_active = request_body["is_active"])
#     db.session.add(user)
#     db.session.commit()
   
#     return jsonify({"User successfully added"}), 200


# more methods


@app.route('/people', methods=['GET'])
def handle_people():
    # get all the People
    result = People.query.all()

    # map the results and your list of people  inside of the all_user variable
    all_people= list(map(lambda x: x.serialize(), result))

    return jsonify(all_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def handle_peopleid():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def handle_planets():
    result = Planets.query.all()

    # map the results and your list of people  inside of the all_user variable
    all_planets= list(map(lambda x: x.serialize(), result))

    return jsonify(all_planets), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planetsid():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    # get all the Vehicles
    result = Vehicles.query.all()

    # map the results and your list of vehicles  inside of the all_vehicle variable
    all_vehicles= list(map(lambda x: x.serialize(), result))

    return jsonify(all_vehicles), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def handle_vehicleid():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_getfavorites():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def handle_postfavorites():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def handle_favoriteid():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

  
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)