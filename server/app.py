#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants_dict_list = []
        for plant in Plant.query.all():
            plant_dict = plant.to_dict()
            plants_dict_list.append(plant_dict)
        response = make_response(jsonify(plants_dict_list), 200)
        return response
    
    def post(self):
        new_plant = Plant(
            name=request.form['name'],
            image=request.form['image'],
            price=request.form['price']
        )
        db.session.add(new_plant)
        db.session.commit()

        new_plant_dict = new_plant.to_dict()
        response = make_response(jsonify(new_plant_dict), 201)
        return response
        
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id==id).first()
        plant_dict = plant.to_dict()
        response = make_response(jsonify(plant_dict), 200)
        return response
        
api.add_resource(PlantByID, '/plant/<int:id>')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
