#!/usr/bin/python3

from flask import Flask, jsonify, request, make_response, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS, cross_origin
from secrets import compare_digest, token_hex
from redis_utils import redis, rget_json, rset_json, rset, rget
from board import Board, Square, Direction
from dice import Dice
from state import State
import traceback
from functools import wraps

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

def recurse_to_json(obj):
    if isinstance(obj, dict):
        return {k: recurse_to_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recurse_to_json(v) for v in obj]
    elif hasattr(obj, 'to_json'):
        return obj.to_json()
    else:
        return obj

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

def new_game_id():
    return token_hex(16)

@app.route('/new_game', methods=['POST'])
@api_endpoint
def new_game():
    game_id = new_game_id()
    board = Board()
    dice = Dice()
    rset_json('board', recurse_to_json(board.to_json()), game_id)
    rset_json('dice', dice.to_json(), game_id)
    rset('rolls', 3, game_id)
    return jsonify({'gameId': game_id})

@app.route('/state', methods=['GET'])
@api_endpoint
def get_board():
    game_id = request.args.get('gameId')
    board = Board.of_json(rget_json('board', game_id))
    dice = Dice.of_json(rget_json('dice', game_id))
    rolls = rget_json('rolls', game_id)
    return State(board, dice, rolls).to_frontend()

@app.route('/roll', methods=['POST'])
@api_endpoint
def roll():
    game_id = request.json.get('gameId')
    locks = request.json.get('locks')
    rolls = rget_json('rolls', game_id=game_id)
    dice = Dice.of_json(rget_json('dice', game_id))
    board = Board.of_json(rget_json('board', game_id))
    if rolls <= 0:
        return {'success': False, 'error': 'No rolls left', **State(board, dice, rolls).to_frontend()}
    rolls -= 1
    rset('rolls', rolls, game_id)
    dice.roll(locks)
    rset_json('dice', dice.to_json(), game_id)
    return State(board, dice, rolls).to_frontend()

@app.route('/submit', methods=['POST'])
@api_endpoint
def submit():
    game_id = request.json.get('gameId')
    board = Board.of_json(rget_json('board', game_id))
    dice = Dice.of_json(rget_json('dice', game_id))
    rolls = rget_json('rolls', game_id)
    state = State(board, dice, rolls)
    state.roll_turn()
    rset('rolls', state.rolls, game_id)
    rset_json('board', recurse_to_json(state.board.to_json()), game_id)
    rset_json('dice', state.dice.to_json(), game_id)
    return state.to_frontend()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5005, debug=True)
