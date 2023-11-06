import React from 'react';
import './Styles.css';
import { Typography } from '@mui/material';

export default function PlayerInfo({ game }) {
    if (!game || !game.player) {
        return null;
    }

    return (
        <div className="player-info-container">
            <Typography variant="h5">Strength: {game.player.temporary.strength}</Typography>
            <Typography variant="h5">Spell damage: {game.player.temporary.spell_damage}</Typography>
            <Typography variant="h5">Dexterity: {game.player.temporary.dexterity}</Typography>
        </div>
    )
}