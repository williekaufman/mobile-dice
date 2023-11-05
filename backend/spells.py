from square import Square
from terrain import Terrain
from dice import Resource


class Cost():
    def __init__(self, cost):
        self.cost = cost

    def can_afford(self, state):
        resources = state.dice.resources()
        for resource, amount in self.cost:
            if resources.count(resource) < amount:
                return False
        return True

    def pay(self, state):
        if not self.can_afford(state):
            return False
        for resource, amount in self.cost:
            for _ in range(amount):
                state.dice.pay(resource)
        return True

    def to_json(self):
        return [{'resource': resource.value, 'amount': amount} for resource, amount in self.cost]


class Spell():
    def __init__(self, name, description, cost, effect):
        self.name = name
        self.description = description
        self.cost = cost
        self.effect = effect

    def resolve(self, state, target):
        if not self.cost.can_afford(state):
            return False
        if not self.effect(state, target):
            return False
        self.cost.pay(state)
        return True

    def to_frontend(self):
        return {'name': self.name, 'description': self.description, 'cost': self.cost.to_json()}

    def to_json(self):
        return self.name

    def of_json(j):
        return spells[j]


# An effect is a function that takes a state and a target square, and either returns false if it's invalid, or returns true and modifies the state
# Even things that don't really have a target, like heal, will be used for generating available spells on the frontend
# Dry run is used for checking possible spells without modifying state
def heal(state, target, dry_run=False):
    board = state.board
    if board.player_location() != target:
        return False
    if dry_run:
        return True
    board.player().heal(1)
    return True

def block(state, target, dry_run=False):
    board = state.board
    if board.player_location() != target:
        return False
    if dry_run:
        return True
    board.player().gain_block(2)
    return True


def fireball(state, target, dry_run=False):
    board = state.board
    if state.board.player_location().distance(target) > 3:
        return False
    if dry_run:
        return True
    for square in target.adjacent_squares():
        state.board.get(square).unit.take_damage(2)
    not dry_run and state.board.get(target).unit.take_damage(2)
    return True


def walk(state, target, dry_run=False):
    board = state.board
    if board.player_location().distance(target) != 1:
        return False
    if dry_run:
        return True
    board.move(board.player_location(), target)
    return True


def teleport(state, target, dry_run=False):
    board = state.board
    if board.get(board.player_location()).terrain != Terrain.PENTAGRAM or board.get(target).terrain != Terrain.PENTAGRAM:
        return False
    if dry_run:
        return True
    board.move(board.player_location(), target)
    return True


def strike(state, target, dry_run=False):
    board = state.board
    if board.player_location().distance(target) != 1:
        return False
    board.get(target).unit.take_damage(3)
    return True

heal_spell = Spell(
    'heal',
    'Restore one health',
    Cost([(Resource.MAGIC, 1)]),
    heal)

block_spell = Spell(
    'block',
    'Gain two block',
    Cost([(Resource.DEFEND, 1)]),
    block
)

fireball_spell = Spell(
    'fireball',
    'Deals 2 damage in a 1-radius circle to a target within 3',
    Cost([(Resource.MAGIC, 1)]),
    fireball)

walk_spell = Spell(
    'walk',
    'Take a step to an adjacent square',
    Cost([(Resource.MOVE, 1)]),
    walk)

teleport_spell = Spell(
    'teleport',
    'Teleport between pentagrams. Only castable from and to a pentagram.',
    Cost([(Resource.MAGIC, 1)]),
    teleport)

strike_spell = Spell(
    'strike',
    'Strike an adjacent square for 3 damage',
    Cost([(Resource.ATTACK, 1)]),
    strike)

spells = {
    'heal': heal_spell,
    'block': block_spell,
    'fireball': fireball_spell,
    'walk': walk_spell,
    'teleport': teleport_spell,
    'strike': strike_spell
}

# Not super efficient to check all the squares even when it's obviously invalid, but it's not a big deal (yet)


def available_spells(state):
    ret = {}
    for spell in spells.values():
        if spell.cost.can_afford(state):
            squares = [square for square in Square if spell.effect(
                state, square, dry_run=True)]
            if squares:
                ret[spell.name] = [square.to_json() for square in squares]
    return ret
