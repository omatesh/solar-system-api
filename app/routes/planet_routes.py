from flask import Blueprint, abort, make_response, jsonify, request, Response
from sqlalchemy import func
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


@planet_bp.get("")
def get_all_planets():
    description_param = request.args.get("description")
    distance_param = request.args.get("distance")
    sort_by = request.args.get("sort_by")

    query = sort_planets_by(sort_by)

    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    if distance_param:
        query = query.where(Planet.distance.ilike(f"%{distance_param}%"))

    planet = db.session.scalars(query)

    planets_response = []
    for planet in planet:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "distance": planet.distance
        })

    return planets_response


@planet_bp.get("/<planet_id>")
def read_single_planet(planet_id):

    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance": planet.distance
    }


@planet_bp.put("/<planet_id>")
def update_planet(planet_id):

    planet = validate_planet(planet_id)

    request_body = request.get_json()
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.distance = request_body["distance"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@planet_bp.delete("/<planet_id>")
def remove_planet(planet_id):

    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_planet(planet_id):

    try:
        planet_id = int(planet_id)
    except:
        message = {
            "message": f"Planet ID ({planet_id}) is invalid type."
        }
        abort(make_response(message, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        message = {
            "message": f"Planet ID ({planet_id}) not found."
        }

        abort(make_response(message, 404))

    return planet


def sort_planets_by(sort_by):

    valid_sorts = ["id", "name"]

    if sort_by and sort_by in valid_sorts:

        if sort_by == "id":
            query = db.select(Planet).order_by(Planet.id)
        elif sort_by == "name":
            query = db.select(Planet).order_by(func.lower(Planet.name))

    else:

        query = db.select(Planet)

    return query

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
