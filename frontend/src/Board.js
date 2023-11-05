import React, { useState } from 'react';
import './Board.css';
import { fetchWrapper, squares_in_order } from './Helpers';

function backgroundImageUrl(unit, terrain, threatened) {
  unit = unit ? `url("../images/${unit}.jpg"),` : "";
  terrain = `url("../images/${terrain}.jpg")`;
  threatened = threatened ? `url("../images/target.jpg"),` : "";
  return `${threatened}${unit}${terrain}`;
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

function display(health) {
  return health || health === 0;
}

function HealthBar({ current, max, block }) {
  if (!display(current) || !display(max)) {
    return null;
  }

  const healthPercentage = (current / max) * 100;

  return (
    <div className="health-bar-container">
      {!!block && <div className="health-bar-block">{block}</div>}
      <div className="health-bar-fill" style={{ width: `${healthPercentage}%` }}></div>
      <div className="health-bar-text">
        {current} / {max}
      </div>
    </div>
  );
};

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
  let className = isAvailableTarget ? "square shadow-on" : "square";

  function onClick() {
    if (!casting || !isAvailableTarget) {
      return;
    }
    cast(gameId, casting, name, setGame, setCasting);
  }

  return (
    <div id={name} className={className} style={{ backgroundImage: backgroundImageUrl(data.unit.type, data.terrain, isThreatened)}} onClick={onClick}>
      {data.unit && <HealthBar current={data.unit.current_health} max={data.unit.max_health} block={data.unit.block} />}
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
            <Square gameId={gameId} name={square} setGame={setGame} data={board[square]} threatenedSquares={game.enemyTurn.squares} casting={casting} setCasting={setCasting} availableSpells={availableSpells} hoveredSpell={hoveredSpell} />
          }
        </div>
      ))}
    </div>
  );
};

export default Board;
