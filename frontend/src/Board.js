import React, { useState } from 'react';
import './Board.css';
import { squares_in_order } from './Helpers';

function backgroundImageUrl(unit, terrain) {
  if (unit) {
    return `url("../images/${unit}.jpg"), url("../images/${terrain}.jpg")`;
  }
  return `url("../images/${terrain}.jpg")`;
}

function threatened(square, hovered, threatened_squares) {
  if (!hovered || !threatened_squares) {
    return false;
  }
  if (hovered in threatened_squares) {
    if (threatened_squares[hovered].includes(square)) {
      return true;
    }
  }
  return false;
}

function Health({ current, max }) {
  if (!current || !max) { 
    return null;
  }

  return (
    <div className="health" style={{color: 'white'}}>
      {current} / {max}
    </div>
  )
}

function Square({ name, data, hovered, threatened_squares }) {
  let boxShadow = threatened(name, hovered, threatened_squares) ? "0 0 0 5px red inset" : "none";
  return (
    <div className="square" style={{ backgroundImage: backgroundImageUrl(data.unit.type, data.terrain), boxShadow }}>
      {data.unit && <Health current={data.unit.current_health} max={data.unit.max_health} />}
    </div>
  )
}

function Board({ board }) {
  let [hoveredSquare, setHoveredSquare] = useState(null);

  if (!board) {
    return null;
  }

  let x = squares_in_order();

  return (
    <div className="board">
      {x.map((square) => (
        <div key={square} id={square} onMouseEnter={() => setHoveredSquare(square)} onMouseLeave={() => setHoveredSquare(null)}>
          {square &&
            <Square name={square} data={board.board[square]} hovered={hoveredSquare} threatened_squares={board.threatened_squares} />
          }
        </div>
      ))}
    </div>
  );
};

export default Board;
