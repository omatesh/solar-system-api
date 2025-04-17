class Planet:
    def __init__(self, id, name, description, distance):
        self.id = id
        self.name = name
        self.description = description
        self.distance = distance
    
planets = [
    Planet(1, "Mars", "Dusty, desolate, red planet", "fourth planet from the Sun" ),
    Planet(2, "Venus", "Hot, hostile, clouded planet", "second planet from the Sun"),
    Planet(3, "Jupiter", "Massive, stormy, gas giant planet", "fifth planet from the Sun")
]