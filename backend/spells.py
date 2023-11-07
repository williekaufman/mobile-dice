from square import Square
from terrain import Terrain
from dice import Resource
from redis_utils import rget_json
import random
from enum import Enum

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

class LimitType(Enum):
    PER_GAME = 'per_game'
    PER_TURN = 'per_turn' 

class Limit():
    def __init__(self, type, limit):
        self.type = type
        self.limit = limit

    def can_cast(self, times_cast):
        if self.type == LimitType.PER_GAME:
            return times_cast['total'] < self.limit
        if self.type == LimitType.PER_TURN:
            return times_cast['turn'] < self.limit
    
    def to_json(self):
        return {'type': self.type.value, 'limit': self.limit}

class Spell():
    def __init__(self, name, description, cost, effect, limits=[]):
        self.name = name
        self.description = description
        self.cost = cost
        self.effect = effect
        self.limits = limits

    def times_cast(self, state):
        total = 0
        for v in state.spells_cast.values():
            total += v.count(self.name)
        return {'total': total, 'turn': state.spells_cast.get(state.game_info.turn, []).count(self.name)}

    def can_cast(self, state):
        return all(limit.can_cast(self.times_cast(state)) for limit in self.limits) and self.cost.can_afford(state)

    def resolve(self, state, target):
        # check if we can resolve it, then pay costs, then actually resolve it. A little inefficient but way more intuitive
        if not (self.can_cast(state) and self.effect(state, target, dry_run=True)):
            return False
        self.cost.pay(state)
        self.effect(state, target)
        return True

    def to_frontend(self):
        limits = {'limits': [limit.to_json() for limit in self.limits]} if self.limits else {}
        return {'name': self.name, 'description': self.description, 'cost': self.cost.to_json(), **limits}

    def to_json(self):
        return self.name

    def of_json(j):
        return spell_definitions[j]


# An effect is a function that takes a state and a target square, and either returns false if it's invalid, or returns true and modifies the state
# Even things that don't really have a target, like heal, will be used for generating available spells on the frontend
# Dry run is used for checking possible spells without modifying state
def heal(state, target, dry_run=False):
    board = state.board
    if board.player_location() != target or board.player().current_health == board.player().max_health:
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
    damage = 2 + board.player().spell_damage()
    for square in target.adjacent_squares() + [target]:
        contents = state.board.get(square)
        if contents.terrain == Terrain.FOREST:
            board.set_terrain(square, Terrain.BURNT_FOREST)
        contents.unit.take_damage(damage)
    return True


def walk(state, target, dry_run=False):
    board = state.board
    if target not in board.player_location().adjacent_squares() or not board.get(target).unit.empty():
        return False
    if dry_run:
        return True
    board.move(board.player_location(), target)
    return True

def road(state, target, dry_run=False):
    board = state.board
    if target not in board.player_location().adjacent_squares() or not board.get(target).unit.empty() or not board.get(target).terrain == Terrain.ROAD:
        return False
    if dry_run:
        return True
    board.move(board.player_location(), target)
    return True

def teleport(state, target, dry_run=False):
    board = state.board
    if not (board.get(board.player_location()).terrain == Terrain.PENTAGRAM == board.get(target).terrain):
        return False
    if dry_run:
        return True
    board.move(board.player_location(), target)
    return True


def strike(state, target, dry_run=False):
    board = state.board
    if board.player_location().distance(target) != 1:
        return False
    board.get(target).unit.take_damage(3 + board.player().strength())
    return True

def gain_strength(state, target, dry_run=False):
    board = state.board
    if board.player_location() != target:
        return False
    if dry_run:
        return True
    board.player().gain_strength(1)
    return True

def gain_dexterity(state, target, dry_run=False):
    board = state.board
    if board.player_location() != target:
        return False
    if dry_run:
        return True
    board.player().gain_dexterity(1)
    return True

def overheat(state, target, dry_run=False):
    board = state.board
    if board.player_location() != target:
        return False
    if dry_run:
        return True
    board.player().take_damage(1)
    board.player().gain_spell_damage(3)
    board.player().gain_strength(3)
    return True

def innervate(state, target, dry_run=False):
    board = state.board
    if board.player_location() != target:
        return False
    if dry_run:
        return True
    for die in state.dice.dice:
        die.live = True
    return True

def ray_of_fire(state, target, dry_run=False):
    board = state.board
    if board.player_location().distance(target) != 1:
        return False
    if dry_run:
        return True
    damage = 1 + board.player().spell_damage()
    # Ray from player through target
    direction = board.player_location().direction_to(target)
    square = board.player_location()
    while square.direction(direction) is not None:
        square = square.direction(direction)
        contents = board.get(square)
        contents.unit.take_damage(damage)
    return True

def cataclysm(state, target, dry_run=False):
    board = state.board
    if board.player_location() == target:
        return False
    if dry_run:
        return False
    damage = 3 + board.player().spell_damage() + board.player().strength()
    for square, contents in board.board.items():
        if square != target:
            contents.unit.take_damage(3)
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

ray_of_fire_spell = Spell(
    'ray of fire',
    'Deals 1 damage in a line',
    Cost([(Resource.MAGIC, 1)]),
    ray_of_fire
)

cataclysm_spell = Spell(
    'cataclysm',
    'Deals 3 damage to ALL other characters. Scales with strength and spell damage. Castable once per game.',
    Cost([(Resource.MAGIC, 1), (Resource.ATTACK, 1)]),
    cataclysm,
    [Limit(LimitType.PER_GAME, 1)]
)

walk_spell = Spell(
    'walk',
    'Take a step to an adjacent square',
    Cost([(Resource.MOVE, 1)]),
    walk)

road_spell = Spell(
    'road',
    'Take a step to an adjacent road',
    Cost([]),
    road
)

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

strength_spell = Spell(
    'strength',
    'Gain 1 strength. Castable once per turn.',
    Cost([]),
    gain_strength, 
    [Limit(LimitType.PER_TURN, 1)]
)

dexterity_spell = Spell(
    'dexterity',
    'Gain 1 dexterity. Castable once per turn',
    Cost([]),
    gain_dexterity, 
    [Limit(LimitType.PER_TURN, 1)]
)

overheat_spell = Spell(
    'overheat',
    'Take 1 damage, gain 3 spell damage and 3 strength. Castable once per game.',
    Cost([(Resource.MAGIC, 1)]),
    overheat,
    [Limit(LimitType.PER_GAME, 1)]
)

innervate_spell = Spell(
    'innervate',
    'Refresh all dice. Castable once per game.',
    Cost([(Resource.MAGIC, 1)]),
    innervate,
    [Limit(LimitType.PER_GAME, 1)]
)

spell_definitions = {
    'heal': heal_spell,
    'block': block_spell,
    'fireball': fireball_spell,
    'ray of fire': ray_of_fire_spell,
    'cataclysm': cataclysm_spell,
    'walk': walk_spell,
    'road': road_spell,
    'teleport': teleport_spell,
    'strike': strike_spell,
    'strength': strength_spell,
    'dexterity': dexterity_spell,
    'overheat': overheat_spell,
    'innervate': innervate_spell
}

# Not super efficient to check all the squares even when it's obviously invalid, but it's not a big deal (yet)
def available_spells(state):
    ret = {}
    spells = n_spells(rget_json('num_spells', game_id=state.game_info.id), seed=state.game_info.seed())
    for spell in spells:
        spell = spell_definitions[spell]
        if spell.can_cast(state):
            squares = [square for square in Square if spell.effect(
                state, square, dry_run=True)]
            if squares:
                ret[spell.name] = [square.to_json() for square in squares]
    return ret

def n_spells(n, seed=None):
    if seed:
        r = random.Random(seed)
    return r.sample(list(spell_definitions.keys()), n)