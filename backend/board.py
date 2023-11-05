from enum import Enum
from square import Square, Contents
from unit import UnitType, EmptyUnit
from enemy import Enemy, get_enemy
from player import Player
from terrain import Terrain, random_terrain
from helpers import unit_of_json


class Result(Enum):
    WIN = 'win'
    LOSE = 'lose'


class Board():
    def __init__(self, initialize_board=True):
        self.board = {}
        if not initialize_board:
            return
        for square in Square:
            self.board[square] = Contents(EmptyUnit(), random_terrain())
        self.set_unit(Square('A1'), Player(10, 10))
        self.set_unit(Square('F6'), get_enemy('goblin'))

    def get(self, square):
        return self.board[square]

    def set(self, square, contents):
        self.board[square] = contents

    def set_unit(self, square, unit):
        self.board[square].unit = unit

    def set_terrain(self, square, terrain):
        self.board[square].terrain = terrain

    def player_location(self):
        for square, contents in self.board.items():
            if contents.unit.type == UnitType.PLAYER:
                return square

    def player(self):
        return self.board[self.player_location()].unit

    def player_turn(self, state):
        self.player().roll_turn(state)

    def move(self, square, target):
        if not target or self.get(target).unit.type != UnitType.EMPTY:
            return False
        self.set_unit(target, self.get(square).unit)
        self.set_unit(square, EmptyUnit())

    def move_direction(self, square, direction):
        return self.move(square, square.direction(direction))

    def threatened_squares(self):
        ret = []
        for square in Square:
            if self.board[square].unit.type == UnitType.ENEMY:
                ret.extend(square.adjacent_squares())
        return [square.value for square in set(ret)]

    def terrain_turn(self):
        for square, contents in self.board.items():
            if contents.terrain == Terrain.POISON:
                self.board[square].unit.take_damage(1)

    def describe_enemy_turn(self, state):
        for contents in self.board.values():
            if contents.unit.type == UnitType.ENEMY:
                return contents.unit.describe_turn(state)

    def enemy_turn(self, state):
        for contents in self.board.values():
            if contents.unit.type == UnitType.ENEMY:
                contents.unit.resolve_turn(state)

    def to_json(self):
        ret = {k.value: v.to_json() for k, v in self.board.items()}
        return ret

    def of_json(j):
        b = Board(False)
        b.board = {Square(k): Contents(
            unit_of_json(v['unit']), Terrain(v['terrain'])) for k, v in j.items()}
        return b

    def to_frontend(self, state):
        return {
            'board': self.to_json(),
            'enemyTurn': self.describe_enemy_turn(state).to_json(),
        }

    def check_game_over(self):
        if self.player().current_health <= 0:
            return Result.LOSE
        enemy = False
        for square in Square:
            if self.get(square).unit.type == UnitType.ENEMY and self.get(square).unit.current_health > 0:
                enemy = True
        if not enemy:
            return Result.WIN
        return None
