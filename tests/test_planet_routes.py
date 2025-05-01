import pytest
from app.models.planet import Planet

def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "XMars",
        "description": "watr 4evr",
        "distance": "x1"
    }

def test_get_planet_with_no_valid_id(client, two_saved_planets ):
    # Act
    response = client.get("/planets/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

def test_get_all_planets(client, two_saved_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "XMars",
        "description": "watr 4evr",
        "distance": "x1"
    }
    assert response_body[1] == {
        "id": 2,
        "name": "XEarth",
        "description": "i luv 2 climb rocks",
        "distance": "x2"
    }

def test_create_one_planet(client):
    # Act
    response = client.post("/planets", json={
        "name": "Planet XVenus",
        "description": "The Best Planet!",
        "distance": "So far"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Planet XVenus",
        "description": "The Best Planet!",
        "distance": "So far"
    }