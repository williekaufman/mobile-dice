class State():
    def __init__(self, board, dice, rolls=3):
        self.board = board
        self.dice = dice
        self.rolls = rolls

    def roll_turn(self):
        self.rolls = 3
        self.dice.roll([])

    def to_frontend(self):
        return {'success': True, 'board': self.board.to_frontend(), 'dice': self.dice.to_json(), 'rolls': self.rolls}