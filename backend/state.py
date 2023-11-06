from spells import available_spells
from redis_utils import rget, rget_json, rset_json, rset, recurse_to_json
from board import Board
from dice import Dice

class GameInfo():
    def __init__(self, id, turn):
        self.id = id
        self.turn = turn

    def of_game_id(game_id):
        try:
            turn = int(rget('turn', game_id))
        except:
            raise Exception('Invalid game id')
        return GameInfo(game_id, turn)
    
    def seed(self):
        return self.id + str(self.turn)
    
    def to_json(self):
        return {'id': self.id, 'turn': self.turn}

class State():
    def __init__(self, game_info, board, dice, rolls=3, spells_cast={}):
        self.game_info = game_info
        self.board = board
        self.dice = dice
        self.rolls = rolls
        self.spells_cast = spells_cast

    def of_game_id(game_id):
        game_info = GameInfo.of_game_id(game_id)
        board = Board.of_json(rget_json('board', game_id))
        dice = Dice.of_json(rget_json('dice', game_id))
        rolls = rget_json('rolls', game_id)
        spells_cast = rget_json('spells_cast', game_id)
        return State(game_info, board, dice, rolls, spells_cast)

    def add_spell_cast(self, spell):
        self.spells_cast.setdefault(self.game_info.turn, []).append(spell)

    def roll_turn(self):
        self.rolls = 3
        self.dice.reset()
        self.board.enemy_turn(self)
        self.board.terrain_turn()
        self.board.player_turn(self)
        self.dice.roll()
        self.game_info.turn += 1

    def to_frontend(self):
        result = {} if self.board.check_game_over() is None else {'result': self.board.check_game_over().value}
        return {'game_info': self.game_info.to_json(), **self.board.to_frontend(self), 'dice': self.dice.to_json(), 'rolls': self.rolls, 'availableSpells': available_spells(self), **result}

    def write(self):
        rset('turn', self.game_info.turn, self.game_info.id)
        rset_json('board', recurse_to_json(self.board.to_json()), self.game_info.id)
        rset_json('dice', self.dice.to_json(), self.game_info.id)
        rset('rolls', self.rolls, self.game_info.id)
        rset_json('spells_cast', self.spells_cast, self.game_info.id)