#!/usr/bin/python3

from flask import Flask, jsonify, request, make_response, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS, cross_origin
from secrets import compare_digest, token_hex
from redis_utils import redis, rget_json, rset_json, rset, rget, recurse_to_json
from board import Board
from square import Square, Direction
from dice import Dice
from state import GameInfo, State
from spells import spell_definitions, n_spells
from enemy import get_enemy, all_enemies
import random
import traceback
from functools import wraps

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


# decorator that takes in an api endpoint and calls recurse_to_json on its result
def api_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(traceback.print_exc())
            return jsonify({"error": "Unexpected error"}), 500
    return wrapper


def success(data):
    return jsonify({'success': True, **data})


def failure(data):
    return jsonify({'success': False, **data})


def new_game_id():
    return token_hex(16)


@app.route('/new_game', methods=['POST'])
@api_endpoint
def new_game():
    num_spells = request.json.get('numSpells') or 6
    game_id = new_game_id()
    state = State(
        GameInfo(game_id, 1),
        Board(),
        Dice(),
        3,
        {}
    )
    rset('num_spells', num_spells, game_id)
    state.write()
    return jsonify({'gameId': game_id})


@app.route('/state', methods=['GET'])
@api_endpoint
def get_board():
    game_id = request.args.get('gameId')
    return success(State.of_game_id(game_id).to_frontend())


@app.route('/roll', methods=['POST'])
@api_endpoint
def roll():
    game_id = request.json.get('gameId')
    locks = request.json.get('locks')
    state = State.of_game_id(game_id)
    if state.rolls <= 0:
        return failure({'error': 'No rolls left', **state.to_frontend()})
    if state.board.check_game_over() is not None:
        return failure({'error': 'Game is already over', **state.to_frontend()})
    state.rolls -= 1
    print([die.active for die in state.dice.dice])
    state.dice.roll(locks)
    state.write()
    return success(state.to_frontend())


@app.route('/cast', methods=['POST'])
@api_endpoint
def cast():
    game_id = request.json.get('gameId')
    if not game_id:
        return {'success': False, 'error': 'No game id'}
    spell = request.json.get('spell')
    target = Square(request.json.get('target'))
    state = State.of_game_id(game_id)
    if state.board.check_game_over() is not None:
        return failure({'error': 'Game is already over', **state.to_frontend()})
    if spell not in spell_definitions:
        return failure({'error': 'Unknown spell', **state.to_frontend()})
    if not spell_definitions[spell].resolve(state, target):
        return failure({'error': 'Failed to cast spell', **state.to_frontend()})
    state.add_spell_cast(spell)
    state.write()
    return success(state.to_frontend())


@app.route('/submit', methods=['POST'])
@api_endpoint
def submit():
    game_id = request.json.get('gameId')
    state = State.of_game_id(game_id)
    if state.board.check_game_over() is not None:
        return failure({'error': 'Game is already over', **state.to_frontend()})
    state.roll_turn()
    state.write()
    return success(state.to_frontend())

@app.route('/spells', methods=['GET'])
@api_endpoint
def all_spells():
    game_id = request.args.get('gameId')
    if not game_id:
        return failure({'error': 'No game id'})
    seed = GameInfo.of_game_id(game_id).seed()
    num_spells = rget_json('num_spells', game_id)
    spells = n_spells(num_spells, seed)
    return success({'spells': [spell_definitions[spell].to_frontend() for spell in spells]})

@app.route('/enemy', methods=['GET'])
@api_endpoint
def enemy_info():
    enemy = request.args.get('enemy')
    return success({'enemy': get_enemy(enemy).to_frontend()})

@app.route('/enemy/all', methods=['GET'])
@api_endpoint
def all_enemies():
    return success({'enemies': [enemy.describe() for enemy in all_enemies()]})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5005, debug=True)
