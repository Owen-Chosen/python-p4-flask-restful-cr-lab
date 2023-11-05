#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    
    def get(self):
        plant_dict = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plant_dict), 200)
    
    def post(self):
        new_plant = Plant(name=request.form.get('name'),
                          image=request.form.get('image'),
                          price=request.form.get('price'))
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)
    
api.add_resource(Plants, ('/plants'))


class PlantByID(Resource):
    def get(self, id):
        plant_by_id = Plant.query.filter_by(id==id).first()
        plant_by_id_dict = plant_by_id.to_dict()
        return make_response(jsonify(plant_by_id_dict), 200)
    
api.add_resource(PlantByID, ('/plants/<int:id>'))
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
