from flask import Blueprint, abort, make_response, jsonify, request, Response
# from ..models.planet import planets

from app.models.planet import Planet
from ..db import db

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.post("")
def create_planet():

    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    distance = request_body["distance"]

    new_planet = Planet(name=name, description=description, distance=distance)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "distance": new_planet.distance
    }
    return response, 201

# @planet_bp.get("")
# def get_all_planets():
#     planet_response = []
#     for planet in planets:
#         planet_response.append(dict(
#             id = planet.id,
#             name = planet.name,
#             description = planet.description,
#             distance = planet.distance
#         ))
#     return jsonify(planet_response)

# @planet_bp.get("/<planet_id>")
# def get_one_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return dict(
#             id = planet.id,
#             name = planet.name,
#             description = planet.description,
#             distance = planet.distance
#         )


# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         response = {"message" : f"planet {planet_id} invalid"}
#         abort(make_response(response, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
        
#     response = {"message" : f"planet {planet_id} not found"}
#     abort(make_response(response, 404))

