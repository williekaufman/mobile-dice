from enum import Enum
from square import Square
import random

class Terrain(Enum):
    FOREST = 'forest'
    BURNT_FOREST = 'burnt_forest'
    PLAINS = 'plains'
    PENTAGRAM = 'pentagram'
    BLACK = 'black'
    POISON = 'poison'
    ROAD = 'road'

    def starting_terrain(self):
        return self != Terrain.BURNT_FOREST
    
    def take_turn(self, state):
        (turn := turns.get(self)) and turn(state)

def poison_turn(state):
    for square, contents in state.board.board.items():
        if contents.terrain == Terrain.POISON:
            contents.unit.take_damage(1)

def burnt_forest_turn(state):
    board = state.board
    for square in Square:
        if board.get(square).terrain == Terrain.BURNT_FOREST:
            board.get(square).unit.take_damage(1)
    squares = [square for square in Square if state.board.get(square).terrain == Terrain.FOREST and any([state.board.get(adjacent_square).terrain == Terrain.BURNT_FOREST for adjacent_square in square.adjacent_squares()])]
    for square in squares:
        board.set_terrain(square, Terrain.BURNT_FOREST)

turns = {
    Terrain.POISON: poison_turn,
    Terrain.BURNT_FOREST: burnt_forest_turn,
}        

def random_terrain():
    return random.choice([terrain for terrain in Terrain if terrain.starting_terrain()])
