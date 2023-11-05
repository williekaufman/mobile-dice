import React, { useState, useEffect } from 'react';
import { HealthBar } from './Board.js';
import './Styles.css';
import { Typography } from '@mui/material';

export default function PlayerInfo({ game }) {
    if (!game || !game.player) {
        return null;
    }

    return (
        <div className="player-info-container">
            <Typography variant="h5">Health: {game.player.current_health}/{game.player.max_health}</Typography>
            <Typography variant="h5">Strength: {game.player.temporary.strength}</Typography>
            <Typography variant="h5">Spell damage: {game.player.temporary.spell_damage}</Typography>
            <Typography variant="h5">Dexterity: {game.player.temporary.dexterity}</Typography>
        </div>
    )
}