from board import Square
import random
from square import Direction
from terrain import Terrain

class MoveSummary():
    def __init__(self, squares, description):
        self.squares = squares
        self.description = description

    def to_json(self):
        return {'squares': [square.value for square in self.squares], 'description': self.description}
    
    def compose(move_summary1, move_summary2):
        return MoveSummary(move_summary1.squares + move_summary2.squares, f"{move_summary1.description} then {move_summary2.description[0].lower() + move_summary2.description[1:]}")

class Move():
    def __init__(self, name, describe, resolve):
        self.name = name
        # Describe is a function from state and enemy location to MoveSummary that doesn't modify the state
        # If it returns a second value, that gets set as self.state if self.state is None for future use
        self.describe = describe
        # Resolve is a function that modifies state and doesn't return anything
        self.resolve = resolve

    # The description won't work for things that rely on changed state, like moving and then attacking relative to the new location
    # Resolve should work fine
    def compose(move1, move2):
        return Move(f"{move1.name} then {move2.name[0].lower() + move2.name[1:]}", lambda state, location: MoveSummary.compose(move1.describe(state, location), move2.describe(state, location)), lambda state, location: (move1.resolve(state, location), move2.resolve(state, location)))

def describe_pass_turn():
    return MoveSummary([], "Do nothing")

def resolve_pass_turn(state, location):
    pass

def pass_turn():
    return Move("Do nothing", lambda state, location: describe_pass_turn(), lambda state, location: resolve_pass_turn(state, location))

def describe_damage_terrain(state, terrain, n):
    squares = [square for square in Square if state.board.get(square).terrain == terrain]
    return MoveSummary(squares, f"Deal {n} damage to all characters on {terrain.value}")

def resolve_damage_terrain(state, terrain, n):
    for square in Square:
        if state.board.get(square).terrain == terrain:
            state.board.get(square).unit.take_damage(n)

def damage_terrain(terrain, n):
    return Move(f"Deal {n} damage to units on {terrain.value}", lambda state, location: describe_damage_terrain(state, terrain, n), lambda state, location: resolve_damage_terrain(state, terrain, n))

def describe_damage_all(state, n):
    return MoveSummary(list(Square), f"Deal {n} damage to all characters")

def resolve_damage_all(state, n):
    for square in Square:
        state.board.get(square).unit.take_damage(n)

def damage_all(n):
    return Move(f"Deal {n} damage to all units", lambda state, location: describe_damage_all(state, n), lambda state, location: resolve_damage_all(state, n))

def describe_transform(state, old_terrain, new_terrain):
    squares = [square for square in Square if state.board.get(square).terrain == old_terrain]
    return MoveSummary(squares, f"Transform all {old_terrain.value} to {new_terrain.value}")

def resolve_transform(state, old_terrain, new_terrain):
    for square in Square:
        if state.board.get(square).terrain == old_terrain:
            state.board.set_terrain(square, new_terrain)

def transform(old_terrain, new_terrain):
    return Move(f"Transform {old_terrain.value} into {new_terrain.value}", lambda state, location: describe_transform(state, old_terrain, new_terrain), lambda state, location: resolve_transform(state, old_terrain, new_terrain))

def describe_move(destination):
    return MoveSummary([destination], f"Move to {destination.value}")

def resolve_move(state, location, destination):
    state.board.move(location, destination)

def move(destination):
    return Move(f"Move to {destination.value}", lambda state, location: describe_move(destination), lambda state, location: resolve_move(state, location, destination))

def describe_random_direction(state, location):
    r = random.Random(state.game_info.seed())
    square = location.direction(r.choice([direction for direction in Direction if location.direction(direction) is not None]))
    return MoveSummary([square], f"Move to {square.value}")

def resolve_random_direction(state, location):
    r = random.Random(state.game_info.seed())
    direction = r.choice([direction for direction in Direction if location.direction(direction) is not None])
    state.board.move_direction(location, direction)

def random_direction():
    return Move("Move in a random direction", lambda state, location: describe_random_direction(state, location), lambda state, location: resolve_random_direction(state, location))

def describe_heal(n):
    return MoveSummary([], f"Heal for {n}")

def resolve_heal(state, location, n):
    state.board.get(location).unit.heal(n)

def heal(n):
    return Move(f"Heal for {n}", lambda state, location: describe_heal(n), lambda state, location: resolve_heal(state, location, n))

def describe_cross_attack(location):
    squares = [square for square in location.row() + location.column() if square != location]
    return MoveSummary(squares, f"Deal 3 damage to all characters in the same row and column")

def resolve_cross_attack(state, location):
    for square in location.row() + location.column():
        if square != location:
            state.board.get(square).unit.take_damage(3)

def cross_attack():
    return Move("Deal 3 damage to all characters in the same row and column", lambda state, location: describe_cross_attack(location), lambda state, location: resolve_cross_attack(state, location))

def describe_move_then_cross_attack(state, location):
    r = random.Random(state.game_info.seed())
    direction = r.choice([direction for direction in Direction if location.direction(direction) is not None])
    destination = location.direction(direction)
    squares = [square for square in destination.row() + destination.column() if square != destination]
    return MoveSummary([destination] + squares, f"Move to {destination.value} and then deal 3 damage to all characters in the same row and column")

def resolve_move_then_cross_attack(state, location):
    r = random.Random(state.game_info.seed()) 
    direction = r.choice([direction for direction in Direction if location.direction(direction) is not None])
    destination = location.direction(direction)
    state.board.move(location, destination)
    for square in destination.row() + destination.column():
        if square != destination:
            state.board.get(square).unit.take_damage(3)

def move_then_cross_attack():
    return Move("Move in a random direction and then deal 3 damage to all characters in the same row and column", lambda state, location: describe_move_then_cross_attack(state, location), lambda state, location: resolve_move_then_cross_attack(state, location))

moves = {
    'damage_terrain': damage_terrain,
    'transform': transform,
    'move': move,
    'random_direction': random_direction,
    'heal': heal,
    'cross_attack': cross_attack,
    'move_then_cross_attack': move_then_cross_attack,
    'damage_all': damage_all,
    'pass_turn': pass_turn,
}