from enum import Enum

class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

class Contents():
    def __init__(self, unit, terrain):
        self.unit = unit
        self.terrain = terrain

    def to_json(self):
        return {'unit': self.unit.to_json(), 'terrain': self.terrain.value}

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

    def distance(self, other):
        i1, j1 = self.index()
        i2, j2 = other.index()
        return abs(i1 - i2) + abs(j1 - j2)

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
    
    def to_json(self):
        return self.value
    
    def of_json(j):
        return Square(j)
