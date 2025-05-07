from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    distance: Mapped[str]
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "distance": self.distance,
            "id": self.id
        }
    
    @classmethod
    def from_dict(cls, planet_data):
        new_planet = Planet(name=planet_data["name"], 
                            description=planet_data["description"], 
                            distance=planet_data["distance"])
        return new_planet
    

#     def __init__(self, id, name, description, distance):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.distance = distance
    
# planets = [
#     Planet(1, "Mars", "Dusty, desolate, red planet", "fourth planet from the Sun" ),
#     Planet(2, "Venus", "Hot, hostile, clouded planet", "second planet from the Sun"),
#     Planet(3, "Jupiter", "Massive, stormy, gas giant planet", "fifth planet from the Sun")
# ]