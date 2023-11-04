from spells import spells, available_spells
from redis_utils import rset_json, rset, recurse_to_json

class State():
    def __init__(self, id, board, dice, rolls=3):
        self.id = id
        self.board = board
        self.dice = dice
        self.rolls = rolls

    def roll_turn(self):
        self.rolls = 3
        self.dice.reset()
        self.board.enemy_turn()
        self.dice.roll()

    def to_frontend(self):
        if (result := self.board.check_game_over()) is not None:
            return {'success': True, 'id': self.id, 'board': self.board.to_frontend(), 'dice': self.dice.to_json(), 'rolls': self.rolls, 'availableSpells': available_spells(self), 'result': result.value}
        return {'success': True, 'id': self.id, 'board': self.board.to_frontend(), 'dice': self.dice.to_json(), 'rolls': self.rolls, 'availableSpells': available_spells(self)}

    def write(self):
        rset_json('board', recurse_to_json(self.board.to_json()), self.id)
        rset_json('dice', self.dice.to_json(), self.id)
        rset('rolls', self.rolls, self.id)