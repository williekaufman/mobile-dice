from enum import Enum
import random


class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Square(Enum):
    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
    A4 = 'A4'
    A5 = 'A5'
    A6 = 'A6'
    B1 = 'B1'
    B2 = 'B2'
    B3 = 'B3'
    B4 = 'B4'
    B5 = 'B5'
    B6 = 'B6'
    C1 = 'C1'
    C2 = 'C2'
    C3 = 'C3'
    C4 = 'C4'
    C5 = 'C5'
    C6 = 'C6'
    D1 = 'D1'
    D2 = 'D2'
    D3 = 'D3'
    D4 = 'D4'
    D5 = 'D5'
    D6 = 'D6'
    E1 = 'E1'
    E2 = 'E2'
    E3 = 'E3'
    E4 = 'E4'
    E5 = 'E5'
    E6 = 'E6'
    F1 = 'F1'
    F2 = 'F2'
    F3 = 'F3'
    F4 = 'F4'
    F5 = 'F5'
    F6 = 'F6'

    def index(self):
        return (ord(self.value[0]) - ord('A'), int(self.value[1]) - 1)

    def of_index(i, j):
        return Square(chr(ord('A') + i) + str(j + 1))

    def __lt__(self, other):
        return self.value < other.value

    def offset(self, rows, columns):
        try:
            i, j = self.index()
            return Square.of_index(i + rows, j + columns)
        except:
            return None

    def color(self):
        i, j = self.index()
        return 'white' if (i + j) % 2 == 0 else 'black'

    def direction(self, direction):
        if direction == Direction.UP:
            return self.offset(1, 0)
        elif direction == Direction.DOWN:
            return self.offset(-1, 0)
        elif direction == Direction.LEFT:
            return self.offset(0, -1)
        elif direction == Direction.RIGHT:
            return self.offset(0, 1)
        else:
            return None

    def adjacent_squares(self):
        return [x for x in (self.direction(direction) for direction in Direction) if x]


class Contents():
    def __init__(self, unit, terrain):
        self.unit = unit
        self.terrain = terrain

    def to_json(self):
        return {'unit': self.unit.to_json(), 'terrain': self.terrain.value}


class Terrain(Enum):
    FOREST = 'forest'
    PLAINS = 'plains'
    PENTAGRAM = 'pentagram'
    # HOLE = 'hole'
    WHITE = 'white'
    BLACK = 'black'


def random_terrain():
    return random.choice([terrain for terrain in Terrain])


class UnitType(Enum):
    PLAYER = 'player'
    ENEMY = 'enemy'
    EMPTY = 'empty'

class Unit():
    def __init__(self, type, max_health, current_health=None):
        self.type = type
        self.max_health = max_health
        self.current_health = max_health if current_health is None else current_health

    def to_json(self):
        return {'type': self.type.value, 'current_health': self.current_health, 'max_health': self.max_health}

    def of_json(json):
        return Unit(UnitType(json['type']), json['max_health'], json['current_health'])

    def player():
        return Unit(UnitType.PLAYER, 10)
    
    def enemy():
        return Unit(UnitType.ENEMY, 5)

    def empty():
        return Unit(UnitType.EMPTY, None)
    
    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)


class Board():
    def __init__(self, initialize_board=True):
        self.board = {}
        if not initialize_board:
            return
        for square in Square:
            self.board[square] = Contents(Unit.empty(), random_terrain())
        self.board[Square('A1')] = Contents(Unit.player(), Terrain.FOREST)
        self.board[Square('F6')] = Contents(Unit.enemy(), Terrain.PLAINS)

    def get(self, square):
        return self.board[square]

    def set(self, square, contents):
        self.board[square] = contents

    def player_location(self):
        for square, contents in self.board.items():
            if contents.unit.type == UnitType.PLAYER:
                return square

    def move(self, square, direction):
        if square.direction(direction) is None:
            return False
        else:
            self.board[square.direction(direction)] = self.board[square]
            self.board[square] = None
            return True

    def threatened_squares(self):
        ret = {}
        for square in Square:
            if self.board[square].unit.type == UnitType.ENEMY:
                ret[square.value] = [x.value for x in square.adjacent_squares()]
        return ret
    
    def enemy_turn(self):
        for square, contents in self.board.items():
            if contents.unit.type == UnitType.ENEMY:
                self.enemy_move(square)

    def enemy_move(self, square):
        for square in square.adjacent_squares():
            if self.board[square].unit.type == UnitType.PLAYER:
                self.board[square].unit.take_damage(1)

    def to_json(self):
        ret = {k.value: v.to_json() for k, v in self.board.items()}
        return ret

    def of_json(j):
        b = Board(False)
        b.board = {Square(k): Contents(
            Unit.of_json(v['unit']), Terrain(v['terrain'])) for k, v in j.items()}
        return b

    def to_frontend(self):
        return {
            'board': self.to_json(),
            'threatened_squares': self.threatened_squares()
        }
