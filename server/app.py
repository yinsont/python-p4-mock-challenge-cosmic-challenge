#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'testing'

class Scientists(Resource):
    def get(self):
        scientists_list = [scientist.to_dict() for scientist in Scientist.query.all()]

        return make_response(scientists_list, 200)
        
    def post(self):
        data = request.get_json()
        new_scientist = Scientist(
            name = data['name'],
            field_of_study = data['field_of_study'],
            avatar = data['avatar']
        )
        db.session.add(new_scientist)
        db.session.commit()

        return make_response(new_scientist.to_dict(), 201)

Api.add_resource(Scientists, '/scientists')

class ScientistByID(Resource):
    
    def get(self, id):
        scientist = Scientist.query.filter_by(id = id).first().to_dict()

        if scientist == None:
            return make_response({"error": "Scientist not found"}, 404)
        
        return make_response(scientist, 200)
    
    def patch(self, id):
        scientist = Scientist.query.filter_by(id = id).first()
        data = request.get_json()
        if scientist == None:
            return make_response({"error": "Scientist not found"}, 404)
        
        for attr in data:
            setattr(scientist, attr, data[attr])

        db.session.add(scientist)
        db.session.commit()

        return make_response(scientist.to_dict(), 202)
    
    def delete(self, id):
        scientist = Scientist.query.filter_by(id = id).first()

        if scientist == None:
            return make_response({"error": "Scientist not found"}, 404)
        
        db.session.delete(scientist)
        db.session.commit()

        return make_response('', 200)

Api.add_resource(ScientistByID, '/scientists/<int:id>')

class Planets(Resource):
    def get(self):
        planets_list = [planet.to_dict() for planet in Planet.query.all()]

        return make_response(planets_list, 200)

Api.add_resource(Planets, '/planets')

class Missions(Resource):
    def get(self):
        missions_list = [mission.to_dict() for mission in Mission.query.all()]

        return make_response(missions_list, 200)
    
    def post(self):
        new_mission = Mission(
            name = request.form['name'],
            distance_from_earth = request.form['distance_from_earth'],
            nearest_star = request.form['nearest_star'],
            image = request.form['image']
        )
        db.session.add(new_mission)
        db.session.commit()


        return make_response(new_mission.to_dict(), 201)

Api.add_resource(Missions, '/missions')

class PlanetByID(Resource):
    def get(self, id):
        planet = Planet.query.filter_by(id = id).first().to_dict()

        if planet == None: return make_response({"error": "404: Scientist not found"}, 404)

        return make_response(planet, 200)
    
    def patch(self, id):
        planet = Planet.query.filter_by(id = id).first()
        for attr in request.form:
            setattr(planet, attr, request.form[attr])
        db.session.add(planet)
        db.session.commit()
        return make_response(planet.to_dict(), 201)
    
    def delete(self, id):
        planet = Planet.query.filter_by(id = id).first()
        db.session.delete(planet)
        db.session.commit()

Api.add_resource(PlanetByID, '/planets/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
