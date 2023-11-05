from unit import UnitType

class Temporary():
    def __init__(self, block=0, strength=0, spell_damage=0, dexterity=0):
        self.block = block
        self.strength = strength
        self.spell_damage = spell_damage 
        self.dexterity = dexterity

    def to_json(self):
        return {'block': self.block, 'strength': self.strength, 'dexterity': self.dexterity, 'spell_damage': self.spell_damage}
    
    def of_json(j):
        return Temporary(**j)
    
class Player():
    def __init__(self, current_health, max_health, temporary=Temporary()):
        self.type = UnitType.PLAYER
        self.current_health = current_health
        self.max_health = max_health
        self.temporary = temporary

    def empty(self):
        return False

    def to_json(self):
        return {'type': self.type.value, 'current_health': self.current_health, 'max_health': self.max_health, 'temporary': self.temporary.to_json()}

    def of_json(j):
        j['temporary'] = Temporary.of_json(j['temporary'])
        return Player(**{k: v for k, v in j.items() if k != 'type'})

    def get_attribute(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        if hasattr(self.temporary, key):
            return getattr(self.temporary, key)
        return None

    def set_attribute(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        if hasattr(self.temporary, key):
            setattr(self.temporary, key, value)

    def strength(self):
        return self.temporary.strength
    
    def gain_strength(self, n):
        self.temporary.strength += n

    def dexterity(self):
        return self.temporary.dexterity

    def gain_dexterity(self, n):
        self.temporary.dexterity += n

    def spell_damage(self):
        return self.temporary.spell_damage

    def gain_spell_damage(self, n):
        self.temporary.spell_damage += n

    def block(self):
        return self.temporary.block

    def gain_block(self, amount):
        self.temporary.block += amount + self.temporary.dexterity
    
    def take_damage(self, damage):
        block = self.temporary.block
        if block < damage:
            self.current_health = max(
                0, self.current_health - (damage - block))
            self.temporary.block = 0
        else:
            self.temporary.block -= damage

    def heal(self, amount):
        self.current_health = min(
            self.max_health, self.current_health + amount)
    
    # Including state in case it becomes relevant later
    def roll_turn(self, state):
        self.temporary = Temporary()