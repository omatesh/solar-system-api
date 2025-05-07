from flask import Blueprint, abort, make_response, jsonify, request, Response
from sqlalchemy import func
from app.models.planet import Planet
from app.models.moon import Moon
from .route_utilities import validate_model
from ..db import db

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.post("")
def create_planet():

    request_body = request.get_json()

    try:
        new_planet = Planet.from_dict(request_body)
    except KeyError as error:
        message = {
            "message": f"Missing '{error.args[0]}' attribute"
        }
        abort(make_response(message, 400))
    db.session.add(new_planet)
    db.session.commit()

    response = new_planet.to_dict()
    return response, 201

@planet_bp.post("/<planet_id>/moons")
def create_moon_with_planet(planet_id):
    
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()

    try:
       new_moon = Moon.from_dict(request_body)
    except KeyError as error:
        message = {"message": f"Missing '{error.args[0]}' attribute."}
        abort(make_response(message, 400))
    
    new_moon.planet_id = planet_id

    planet.moons.append(new_moon)

    db.session.add(new_moon)
    db.session.commit()

    return Response(status=201, mimetype='application/json')



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
        planets_response.append(planet.to_dict())

    return planets_response


@planet_bp.get("/<planet_id>")
def read_single_planet(planet_id):

    planet = validate_model(Planet, planet_id)

    return planet.to_dict()

@planet_bp.get("/<planet_id>/moons")
def read_moons_with_planet(planet_id):

    planet = validate_model(Planet, planet_id)

    query = db.select(Moon).where(Moon.planet_id == planet_id)

    moons = db.session.scalars(query)

    results = []

    for moon in moons:
        results.append(moon.to_dict())

    return results

@planet_bp.put("/<planet_id>")
def update_planet(planet_id):

    planet = validate_planet(planet_id)

    request_body = request.get_json()

    try:
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.distance = request_body["distance"]
    except KeyError as error:
        message = {
            "message": f"Missing '{error.args[0]}' attribute"
        }
        abort(make_response(message, 400))

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

    elif sort_by:

        message = {
            "message": f"Sort query {sort_by} was not recognized. Valid sort options are 'id', 'name'."
        }
        abort(make_response(message, 400))
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
