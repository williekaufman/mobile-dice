from enum import Enum

class UnitType(Enum):
    PLAYER = 'player'
    ENEMY = 'enemy'
    CITY = 'city'
    EMPTY = 'empty'

class EmptyUnit():
    def __init__(self):
        self.type = UnitType.EMPTY

    def to_json(self):
        return {'type': self.type.value}

    def of_json(j):
        return EmptyUnit()
    
    def take_damage(self, n):
        pass

    def lose_life(self, n):
        pass
    
    def heal(self, n):
        pass

    def gain_block(self, n):
        pass

    def empty(self):
        return True