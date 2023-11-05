from board import Square

class MoveSummary():
    def __init__(self, squares, description):
        self.squares = squares
        self.description = description

    def to_json(self):
        return {'squares': [square.value for square in self.squares], 'description': self.description}

class Move():
    def __init__(self, describe, resolve):
        # Describe is a function from state and enemy location to MoveSummary that doesn't modify the state
        self.describe = describe
        # Resolve is a function that modifies state and doesn't return anything
        self.resolve = resolve

def describe_damage_terrain(state, terrain, n):
    squares = [square for square in Square if state.board.get(square).terrain == terrain]
    return MoveSummary(squares, f"Deal {n} damage to all characters on {terrain.value}")

def resolve_damage_terrain(state, terrain, n):
    for square in Square:
        if state.board.get(square).terrain == terrain:
            state.board.get(square).unit.take_damage(n)

def damage_terrain(terrain, n):
    return Move(lambda state, location: describe_damage_terrain(state, terrain, n), lambda state, location: resolve_damage_terrain(state, terrain, n))

def describe_transform(state, old_terrain, new_terrain):
    squares = [square for square in Square if state.board.get(square).terrain == old_terrain]
    return MoveSummary(squares, f"Transform all {old_terrain.value} to {new_terrain.value}")

def resolve_transform(state, old_terrain, new_terrain):
    for square in Square:
        if state.board.get(square).terrain == old_terrain:
            state.board.set_terrain(square, new_terrain)

def transform(old_terrain, new_terrain):
    return Move(lambda state, location: describe_transform(state, old_terrain, new_terrain), lambda state, location: resolve_transform(state, old_terrain, new_terrain))