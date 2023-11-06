from enum import Enum
import random

class Terrain(Enum):
    FOREST = 'forest'
    BURNT_FOREST = 'burnt_forest'
    PLAINS = 'plains'
    PENTAGRAM = 'pentagram'
    WHITE = 'white'
    BLACK = 'black'
    POISON = 'poison'

    def starting_terrain(self):
        return self != Terrain.BURNT_FOREST

def random_terrain():
    return random.choice([terrain for terrain in Terrain if terrain.starting_terrain()])
