import React from 'react';
import './Styles.css';
import { color } from './GamePage';

export default function Intent({ game }) {
    if (!game || !game.enemyTurn) {
        return null;
    }

    return (
        <div className="intent">
            <h1>Intents</h1>
            {Object.keys(game.enemyTurn).map((name, index) => (
                <div key={index} style={{color: color(index)}}>
                    <h2>{name}: {game.enemyTurn[name].description}</h2>
                </div>
            ))}
        </div>
    )
}
