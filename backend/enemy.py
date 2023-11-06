from square import Square
from terrain import Terrain
from unit import UnitType, EmptyUnit
from dice import Dice, Resource
from enum import Enum
from moves import moves
import random

class Enemy():
    def __init__(self, name, current_health, max_health, moves, transition, move_index=0, prevent_win=lambda state: False):
        self.type = UnitType.ENEMY
        self.name = name
        self.current_health = current_health
        self.max_health = max_health
        self.moves = moves
        self.move_index = move_index
        self.transition = transition
        self.prevent_win = prevent_win

    def empty(self):
        return False

    def to_json(self):
        # Intentionally omitting moves
        return {
            'type': self.type.value,
            'name': self.name,
            'current_health': self.current_health,
            'max_health': self.max_health,
            'move_index': self.move_index,
        }
    
    def describe(self):
        return {
            'name': self.name,
            'max_health': self.max_health,
            'moves': [move.name for move in self.moves],
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
        return None

    def describe_turn(self, state):
        return self.moves[self.move_index].describe(state, self.location(state))

    def resolve_turn(self, state):
        move = self.moves[self.move_index]
        move.resolve(state, self.location(state))
        self.transition(self, state)

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def copy(self):
        return Enemy(self.name, self.current_health, self.max_health, self.moves, self.transition, self.move_index, self.prevent_win)

def next_move(enemy, state):
    enemy.move_index = (enemy.move_index + 1) % len(enemy.moves)

def random_move(enemy, state):
    enemy.move_index = random.randint(0, len(enemy.moves) - 1)

def prevent_win_until_turn_four(state):
    return "Must live until turn 4" if state.game_info.turn < 4 else False

damage_terrain = moves['damage_terrain']
transform = moves['transform']
move = moves['move']
random_direction = moves['random_direction']
cross_attack = moves['cross_attack']
move_then_cross_attack = moves['move_then_cross_attack']
damage_all = moves['damage_all']
pass_turn = moves['pass_turn']

# You need to make a copy if you interact with this! So probably use get_enemy.
enemies = {
    'orc': Enemy('orc', 5, 5, [damage_terrain(Terrain.PLAINS, 2), transform(Terrain.FOREST, Terrain.PLAINS)], random_move),
    'goblin': Enemy('goblin', 3, 3, [move(Square('A1'))], random_move),
    'skeleton': Enemy('skeleton', 2, 2, [random_direction()], next_move),
    'rook man': Enemy('rook man', 1, 7, [cross_attack(), move_then_cross_attack()], next_move),
    'trap room': Enemy('trap room', 1, 1, [damage_all(1), pass_turn()], next_move, prevent_win=prevent_win_until_turn_four),
}

def get_enemy(name):
    try:
        return enemies[name].copy()
    except KeyError:
        return None
    
def all_enemies():
    return [enemy.copy() for enemy in enemies.values()]