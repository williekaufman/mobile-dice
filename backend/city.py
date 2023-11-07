from unit import UnitType
from enum import Enum

class City():
    def __init__(self, name, description, current_health, max_health, take_turn=lambda self, state: None):
        self.type = UnitType.CITY
        self.name = name
        self.description = description
        self.current_health = current_health
        self.max_health = max_health
        self.take_turn = take_turn

    def empty(self):
        return False

    def copy(self):
        return City(self.name, self.description, self.current_health, self.max_health, self.take_turn)

    def to_json(self):
        return {
            'type': self.type.value,
            'name': self.name,
            'current_health': self.current_health,
            'max_health': self.max_health,
        }

    def of_json(json):
        city = cities[json['name']]
        city.current_health = json['current_health']
        return city

    def describe(self):
        return {
            'name': self.name,
            'max_health': self.max_health,
            'description': self.description,
        }
    
    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def lose_life(self, damage):
        self.take_damage(damage)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount) 

    def resolve_turn(self, state):
        self.take_turn(self, state)

def atrophy(self, state):
    self.take_damage(1)

cities = {
    'City': City('City', 'A basic city. Takes 1 damage every turn.', 10, 10, take_turn=atrophy),
}

def get_city(name):
    try:
        return cities[name].copy()
    except:
        return None

def all_cities():
    return [city.copy() for city in cities.values()]