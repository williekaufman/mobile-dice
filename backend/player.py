from unit import UnitType


class Player():
    def __init__(self, current_health, max_health, block=0):
        self.type = UnitType.PLAYER
        self.current_health = current_health
        self.max_health = max_health
        self.block = block

    def to_json(self):
        return {'type': self.type.value, 'current_health': self.current_health, 'max_health': self.max_health, 'block': self.block}

    def of_json(j):
        return Player(**{k: v for k, v in j.items() if k != 'type'})

    def take_damage(self, damage):
        if self.block < damage:
            self.current_health = max(
                0, self.current_health - (damage - self.block))
            self.block = 0
        else:
            self.block -= damage

    def heal(self, amount):
        self.current_health = min(
            self.max_health, self.current_health + amount)
    
    def gain_block(self, amount):
        self.block += amount

    # Including state in case it becomes relevant later
    def roll_turn(self, state):
        self.block = 0