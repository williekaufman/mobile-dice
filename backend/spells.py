from enum import Enum
from board import Board, Square, Contents, Unit, UnitType, Terrain

class Spell():
    def __init__(self, cost, effect):
        self.cost = cost
        self.effect = effect

# An effect is a function that takes a state and an optional target square, and either returns false if it's invalid, or returns true and modifies the state

def heal(state, target=None):
    state.board.get(target).unit.heal(1)
    return True