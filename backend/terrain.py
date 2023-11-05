from enum import Enum
import random

class Terrain(Enum):
    FOREST = 'forest'
    PLAINS = 'plains'
    PENTAGRAM = 'pentagram'
    WHITE = 'white'
    BLACK = 'black'
    POISON = 'poison'

def random_terrain():
    return random.choice([terrain for terrain in Terrain])
