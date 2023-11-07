from unit import UnitType, EmptyUnit
from player import Player
from enemy import Enemy
from city import City

def unit_of_json(j):
    if j['type'] == UnitType.PLAYER.value:
        return Player.of_json(j)
    elif j['type'] == UnitType.ENEMY.value:
        return Enemy.of_json(j)
    elif j['type'] == UnitType.EMPTY.value:
        return EmptyUnit()
    elif j['type'] == UnitType.CITY.value:
        return City.of_json(j)
    else:
        raise Exception('Unknown unit type: ' + j['type'])

