from enum import Enum
import random


class Resource(Enum):
    MOVE = 'move'
    ATTACK = 'attack'
    MAGIC = 'magic'
    DEFEND = 'defend'


class Die():
    def __init__(self):
        self.faces = [Resource.MOVE, Resource.ATTACK,
                      None, Resource.MAGIC, Resource.DEFEND, None]
        self.active = None
        self.live = True
        self.roll()

    def roll(self):
        if self.live:
            self.active = random.randint(0, len(self.faces) - 1)

    def to_json(self):
        return {'active': self.active, 'live': self.live, 'faces': [face.value if face is not None else None for face in self.faces]}

    def of_json(json):
        dice = Die()
        dice.active = json['active']
        dice.live = json['live']
        dice.faces = [
            Resource(face) if face is not None else None for face in json['faces']]
        return dice


class Dice():
    def __init__(self, dice=None):
        self.dice = dice or [Die() for _ in range(5)]

    def roll(self, locks=[]):
        for i, die in enumerate(self.dice):
            if i not in locks:
                die.roll()

    def reset(self):
        for die in self.dice:
            die.live = True

    def resources(self):
        return [die.faces[die.active] for die in self.dice if die.live]

    def pay(self, resource):
        for die in self.dice:
            if die.faces[die.active] == resource and die.live:
                die.live = False
                return
        raise Exception(f"No die with resource {resource}") 

    def to_json(self):
        return [die.to_json() for die in self.dice]

    def of_json(json):
        return Dice([Die.of_json(die) for die in json])
