import React from 'react';
import './Styles.css';
import { Typography } from '@mui/material';
import { color } from './GamePage';

export default function PlayerInfo({ game }) {
    if (!game || !game.player) {
        return null;
    }

    function color(n) {
        if (n > 0) {
            return "green";
        } else if (n < 0) {
            return "red";
        } else {
            return "black";
        }
    }

    let strength = game.player.temporary.strength;
    let spell_damage = game.player.temporary.spell_damage;
    let dexterity = game.player.temporary.dexterity;

    return (
        <div className="player-info-container">
            <Typography color={{ color: color(strength) }} variant="h5">Strength: {strength}</Typography>
            <Typography color={{ color: color(spell_damage) }} variant="h5">Spell damage: {spell_damage}</Typography>
            <Typography color={{ color: color(dexterity) }} variant="h5">Dexterity: {dexterity}</Typography>
        </div>
    )
}