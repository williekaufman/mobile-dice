from unit import UnitType, EmptyUnit
from player import Player
from enemy import Enemy

def unit_of_json(j):
    if j['type'] == UnitType.PLAYER.value:
        return Player.of_json(j)
    elif j['type'] == UnitType.ENEMY.value:
        return Enemy.of_json(j)
    elif j['type'] == UnitType.EMPTY.value:
        return EmptyUnit()
