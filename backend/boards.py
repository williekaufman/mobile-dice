from square import Square, Contents
from unit import UnitType, EmptyUnit
from terrain import Terrain, random_terrain
from player import Player
from enemy import Enemy, get_enemy
from city import get_city

def tile(terrain):
    return {
        square: Contents(EmptyUnit(), terrain) for square in Square
    }

poison_swamp = {
    **tile(Terrain.POISON),
    Square.A1: Contents(Player(10, 10), Terrain.POISON),
    Square.F6: Contents(get_enemy('Goblin'), Terrain.POISON)
}

burning_forest = {
    **tile(Terrain.FOREST),
    Square.A1: Contents(Player(10, 10), Terrain.BURNT_FOREST),
}

city_test = {
    **tile(Terrain.FOREST),
    Square.A1: Contents(Player(10, 10), Terrain.FOREST),
    Square.F6: Contents(get_city('City'), Terrain.FOREST),
    Square.F1: Contents(get_enemy('Rook Man'), Terrain.PLAINS)
}

board_configs = {
   'example': {
        Square.A1: Contents(Player(10, 10), Terrain.PLAINS),
        Square.F1: Contents(get_enemy('Rook Man'), Terrain.PLAINS),
        Square.F6: Contents(get_enemy('Rook Man'), Terrain.PLAINS),
    },
    'poison swamp': poison_swamp,
    'burning forest': burning_forest,
    'cities': city_test,
}

non_board_enemies = {
    'burning forest': [get_enemy('Win Preventer 6')],
    'cities': [get_enemy('Trap Room')],
}

board_configs = {
    k: (v, non_board_enemies.get(k, [])) for k, v in board_configs.items()
}

def make_board(config):
    return {
        square: config[0].get(square) or Contents(EmptyUnit(), random_terrain()) for square in Square 
    }, config[1]