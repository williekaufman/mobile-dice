import React, { useState, useEffect } from 'react';
import './Styles.css';
import { color } from './GamePage';

export default function Intent({ game }) {
    if (!game || !game.enemyTurn) {
        return null;
    }

    return (
        <div className="intent">
            <h1>Intents</h1>
            {game.enemyTurn.map((intent, index) => (
                <div key={index} style={{color: color(index)}}>
                    <h2>{intent.description}</h2>
                </div>
            ))}
        </div>
    )
}
