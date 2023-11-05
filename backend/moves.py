from board import Square
import random
from square import Direction

class MoveSummary():
    def __init__(self, squares, description):
        self.squares = squares
        self.description = description

    def to_json(self):
        return {'squares': [square.value for square in self.squares], 'description': self.description}

class Move():
    def __init__(self, name, describe, resolve):
        self.name = name
        # Describe is a function from state and enemy location to MoveSummary that doesn't modify the state
        # If it returns a second value, that gets set as self.state if self.state is None for future use
        self.describe = describe
        # Resolve is a function that modifies state and doesn't return anything
        self.resolve = resolve
        # In case you want to set some state in describe and use it in resolve, e.g. for randomness
        # It gets cleared whenever resolve is called
        # If it was just for randomness, it might be easier to just set a seed, but I dunno, maybe this is useful in general
        self.memory = None

def describe_damage_terrain(state, terrain, n):
    squares = [square for square in Square if state.board.get(square).terrain == terrain]
    return MoveSummary(squares, f"Deal {n} damage to all characters on {terrain.value}"), None

def resolve_damage_terrain(state, terrain, n):
    for square in Square:
        if state.board.get(square).terrain == terrain:
            state.board.get(square).unit.take_damage(n)

def damage_terrain(terrain, n):
    return Move(f"Deal {n} damage to units on {terrain.value}", lambda state, location, memory: describe_damage_terrain(state, terrain, n), lambda state, location, memory: resolve_damage_terrain(state, terrain, n))

def describe_transform(state, old_terrain, new_terrain):
    squares = [square for square in Square if state.board.get(square).terrain == old_terrain]
    return MoveSummary(squares, f"Transform all {old_terrain.value} to {new_terrain.value}"), None

def resolve_transform(state, old_terrain, new_terrain):
    for square in Square:
        if state.board.get(square).terrain == old_terrain:
            state.board.set_terrain(square, new_terrain)

def transform(old_terrain, new_terrain):
    return Move(f"Transform {old_terrain.value} into {new_terrain.value}", lambda state, location, memory: describe_transform(state, old_terrain, new_terrain), lambda state, location, memory: resolve_transform(state, old_terrain, new_terrain))

def describe_move(destination):
    return MoveSummary([destination], f"Move to {destination.value}"), None

def resolve_move(state, location, destination):
    state.board.move(location, destination)

def move(destination):
    return Move(f"Move to {destination.value}", lambda state, location, memory: describe_move(destination), lambda state, location, memory: resolve_move(state, location, destination))

def describe_random_direction(state, location, memory):
    direction = memory or random.choice([direction for direction in Direction if location.direction(direction) is not None])
    square = location.direction(direction)
    return MoveSummary([square], f"Move to {square.value}"), direction

def resolve_random_direction(state, location, memory):
    state.board.move_direction(location, memory)

def random_direction():
    return Move("Move in a random direction", lambda state, location, memory: describe_random_direction(state, location, memory), lambda state, location, memory: resolve_random_direction(state, location, memory))

def describe_heal(state, n):
    return MoveSummary([], f"Heal for {n}"), None

def resolve_heal(state, location, n):
    state.board.get(location).unit.heal(n)

def heal(n):
    return Move(f"Heal for {n}", lambda state, location, memory: describe_heal(state, n), lambda state, location, memory: resolve_heal(state, location, n))

moves = {
    'damage_terrain': damage_terrain,
    'transform': transform,
    'move': move,
    'random_direction': random_direction,
    'heal': heal,
}