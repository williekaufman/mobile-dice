import React, { useState, useEffect } from 'react';

export default function Intent({ game }) {
    if (!game || !game.enemyTurn) {
        return null;
    }

    return (
        <div className="intent">
            <h1>Enemy intent: {game.enemyTurn.description}</h1>
        </div>
    )
}
