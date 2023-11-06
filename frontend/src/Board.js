import React from 'react';
import './Board.css';
import { fetchWrapper, squares_in_order } from './Helpers';
import { color } from './GamePage';

function backgroundImageUrl(unit, terrain, threatened) {
  if (unit === "enemy") {
    unit = `enemy-${color(0)}`;
  }
  unit = unit ? `url("../images/${unit}.jpg"),` : "";
  terrain = `url("../images/${terrain}.jpg")`;
  threatened = threatened || threatened === 0 ? `url("../images/target-${color(threatened)}.jpg"),` : "";
  return `${threatened}${unit}${terrain}`;
}

function threatened(square, threatenedSquares) {
  for (let i = 0; i < threatenedSquares.length; i++) {
    if (threatenedSquares[i].includes(square)) {
      return i;
    }
  }
  return false;
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

function Name({ name }) {
  if (!name) {
    return null;
  }

  return (
    <div className="name">
      {name}
    </div>
  );
};

function cast(gameId, spell, target, setGame, setCasting, showErrorToast) {
  fetchWrapper("/cast", { gameId, spell, target }, "POST")
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) {
        console.log('toast time')
        showErrorToast(data['error'])
        return;
      }
      setCasting(null);
      setGame(data);
    });
}

function Square({ gameId, name, data, threatenedSquares, setGame, casting, setCasting, availableSpells, hoveredSpell , showErrorToast }) {
  let isThreatened = threatened(name, threatenedSquares);
  let isAvailableTarget = availableTarget(name, availableSpells, casting, hoveredSpell);
  let className = isAvailableTarget ? "square shadow-on" : "square";

  function onClick() {
    if (!casting || !isAvailableTarget) {
      return;
    }
    cast(gameId, casting, name, setGame, setCasting, showErrorToast);
  }

  return (
    <div id={name} className={className} style={{ backgroundImage: backgroundImageUrl(data.unit.type, data.terrain, isThreatened)}} onClick={onClick}>
      {data.unit && <HealthBar current={data.unit.current_health} max={data.unit.max_health} block={data.unit.temporary?.block} />}
      {data.unit && <Name name={data.unit.name} />}
    </div>
  )
}

function Board({ game, setGame, casting, setCasting, hoveredSpell , showErrorToast }) {
  let board = game.board.board;
  let gameId = game.game_info?.id;
  let availableSpells = game.availableSpells;

  if (!board) {
    return null;
  }

  let x = squares_in_order();

  let threatenedSquares = Object.values(game.enemyTurn).map((turn) => turn.squares);

  return (
    <div className="board">
      {x.map((square) => (
        <div key={square}>
          {square &&
            <Square gameId={gameId} name={square} setGame={setGame} data={board[square]} threatenedSquares={threatenedSquares} casting={casting} setCasting={setCasting} availableSpells={availableSpells} hoveredSpell={hoveredSpell} showErrorToast={showErrorToast}/>
          }
        </div>
      ))}
    </div>
  );
};

export default Board;
