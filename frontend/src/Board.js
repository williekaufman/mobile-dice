import React, { useState } from 'react';
import './Board.css';
import { fetchWrapper, squares_in_order } from './Helpers';

function backgroundImageUrl(unit, terrain) {
  if (unit) {
    return `url("../images/${unit}.jpg"), url("../images/${terrain}.jpg")`;
  }
  return `url("../images/${terrain}.jpg")`;
}

function threatened(square, threatenedSquares) {
  return (threatenedSquares || []).includes(square);
}

function availableTarget(square, availableSpells, casting, hovered) {
  let spell = casting || hovered;
  if (!spell || !availableSpells) {
    return false;
  }
  if (spell in availableSpells) {
    if (availableSpells[spell].includes(square)) {
      return true;
    }
  }
}

function Health({ current, max }) {
  if (current == null || max == null) {
    return null;
  }

  return (
    <div className="health" style={{ color: 'white' }}>
      {current} / {max}
    </div>
  )
}

function cast(gameId, spell, target, setGame, setCasting) {
  fetchWrapper("/cast", { gameId, spell, target }, "POST")
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) {
        console.log(data['error']);
        return;
      }
      setCasting(null);
      setGame(data);
    });
}

function Square({ gameId, name, data, threatenedSquares, setGame, casting, setCasting, availableSpells, hoveredSpell }) {
  let isThreatened = threatened(name, threatenedSquares);
  let isAvailableTarget = availableTarget(name, availableSpells, casting, hoveredSpell);
  let boxShadow = isThreatened ? "0 0 0 5px red inset" : isAvailableTarget ? "0 0 0 5px blue inset" : "none";

  function onClick() {
    if (!casting) {
      return;
    }
    cast(gameId, casting, name, setGame, setCasting);
  }

  return (
    <div id={name} className="square" style={{ backgroundImage: backgroundImageUrl(data.unit.type, data.terrain), boxShadow }} onClick={onClick}>
      {data.unit && <Health current={data.unit.current_health} max={data.unit.max_health} />}
    </div>
  )
}

function Board({ game, setGame, casting, setCasting, hoveredSpell }) {
  let board = game.board;
  let gameId = game.id;
  let availableSpells = game.availableSpells;

  if (!board) {
    return null;
  }

  let x = squares_in_order();

  return (
    <div className="board">
      {x.map((square) => (
        <div key={square}>
          {square &&
            <Square gameId={gameId} name={square} setGame={setGame} data={board.board[square]} threatenedSquares={board.threatenedSquares} casting={casting} setCasting={setCasting} availableSpells={availableSpells} hoveredSpell={hoveredSpell} />
          }
        </div>
      ))}
    </div>
  );
};

export default Board;
