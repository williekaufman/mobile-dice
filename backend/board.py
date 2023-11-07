from enum import Enum
from square import Square, Contents
from unit import UnitType, EmptyUnit
from enemy import Enemy, get_enemy
from player import Player
from terrain import Terrain, random_terrain
from helpers import unit_of_json
from boards import board_configs, make_board
import random


class Board():
    def __init__(self, initialize_board=True, name=None):
        self.board = {}
        self.non_board_enemies = []
        if not initialize_board:
            return
        config = board_configs.get(name) or random.choice(
            list(board_configs.values()))
        self.board, self.non_board_enemies = make_board(config)

    def get(self, square):
        return self.board[square]

    def set(self, square, contents):
        self.board[square] = contents

    def set_unit(self, square, unit):
        self.board[square].unit = unit

    def set_terrain(self, square, terrain):
        self.board[square].terrain = terrain

    def cleanup_dead_enemies(self):
        for square, contents in self.board.items():
            if contents.unit.type in [UnitType.ENEMY, UnitType.CITY] and contents.unit.current_health <= 0:
                self.set_unit(square, EmptyUnit())

    def player_location(self):
        for square, contents in self.board.items():
            if contents.unit.type == UnitType.PLAYER:
                return square

    def player(self):
        return self.board[self.player_location()].unit

    def player_turn(self, state):
        self.player().roll_turn(state)

    def enemies(self, include_non_board_enemies=True):
        return [contents.unit for contents in self.board.values() if contents.unit.type == UnitType.ENEMY] + (self.non_board_enemies if include_non_board_enemies else [])

    def cities(self):
        return [contents.unit for contents in self.board.values() if contents.unit.type == UnitType.CITY]

    def move(self, square, target):
        if not target or self.get(target).unit.type != UnitType.EMPTY:
            return False
        self.set_unit(target, self.get(square).unit)
        self.set_unit(square, EmptyUnit())

    def move_direction(self, square, direction):
        return self.move(square, square.direction(direction))

    def terrain_turn(self, state):
        # Terrain turns happen all at once by terrain, so things like spreading wildfire doesn't chain
        for terrain in Terrain:
            terrain.take_turn(state)

    def city_turn(self, state):
        for square, contents in self.board.items():
            if contents.unit.type == UnitType.CITY:
                contents.unit.resolve_turn(state)

    def describe_enemy_turn(self, state):
        return [{'name': enemy.name, **enemy.describe_turn(state)} for enemy in self.enemies()]

    def enemy_turn(self, state):
        for enemy in self.enemies():
            enemy.resolve_turn(state)

    def to_json(self):
        return {'board': {k.value: v.to_json() for k, v in self.board.items()}, 'non_board_enemies': [enemy.to_json() for enemy in self.non_board_enemies]}

    def of_json(j):
        b = Board(False)
        b.board = {Square(k): Contents(
            unit_of_json(v['unit']), Terrain(v['terrain'])) for k, v in j['board'].items()}
        b.non_board_enemies = [unit_of_json(enemy)
                               for enemy in j['non_board_enemies']]
        return b

    def to_frontend(self, state):
        return {
            'board': self.to_json(),
            'enemyTurn': self.describe_enemy_turn(state),
            'player': self.player().to_json(),
        }
