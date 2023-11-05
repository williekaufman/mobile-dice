from square import Square
from terrain import Terrain
from unit import UnitType, EmptyUnit
from dice import Dice, Resource
from enum import Enum
from moves import MoveSummary, damage_terrain, transform
import random

class Enemy():
    def __init__(self, name, current_health, max_health, moves, transition, move_index=0):
        self.type = UnitType.ENEMY
        self.name = name
        self.current_health = current_health
        self.max_health = max_health
        self.moves = moves
        self.move_index = move_index
        self.transition = transition

    def to_json(self):
        # Intentionally omitting moves
        return {
            'type': self.type.value,
            'name': self.name,
            'current_health': self.current_health,
            'max_health': self.max_health,
            'move_index': self.move_index,
        }

    def of_json(j):
        enemy = get_enemy(j['name'])
        enemy.current_health = j['current_health']
        enemy.move_index = j['move_index']
        return enemy

    def location(self, state):
        for square, contents in state.board.board.items():
            if contents.unit == self:
                return square

    def describe_turn(self, state):
        return self.moves[self.move_index].describe(state, self.location(state))
    
    def resolve_turn(self, state):
        self.moves[self.move_index].resolve(state, self.location(state))
        self.transition(self)

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def copy(self):
        return Enemy(self.name, self.current_health, self.max_health, self.moves, self.transition, self.move_index)

def next_move(enemy):
    enemy.move_index = (enemy.move_index + 1) % len(enemy.moves)

def random_move(enemy):
    enemy.move_index = random.randint(0, len(enemy.moves) - 1)

# You need to make a copy if you interact with this! So probably use get_enemy.
enemies = {
    'orc': Enemy('orc', 5, 5, [damage_terrain(Terrain.PLAINS, 2), transform(Terrain.FOREST, Terrain.PLAINS)], next_move),
    'goblin': Enemy('goblin', 3, 3, [damage_terrain(Terrain.PLAINS, 1), transform(Terrain.FOREST, Terrain.PLAINS)], random_move),
}

def get_enemy(name):
    return enemies[name].copy()