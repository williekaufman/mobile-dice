import React from 'react';
import './Styles.css';
import { highlight, unhighlightAll } from './Board';
import { Typography } from '@mui/material';

export default function Intent({ game, setActiveEnemy }) {
    if (!game || !game.enemyTurn) {
        return null;
    }

    return (
        <div className="intent">
            {game.enemyTurn.map((intent, index) => (
                <div key={index} style={{ maxWidth: '30vw', backgroundColor: 'black', color: 'white', borderRadius: '5px', padding: '10px' }} onMouseEnter={() => { setActiveEnemy(index); intent.location && highlight(intent.location)}} onMouseLeave={() => { setActiveEnemy(null); unhighlightAll()}} >
                    <Typography variant="h5">
                        {intent.name}: {intent.description}
                    </Typography>
                </div>
            ))}
        </div>
    )
}
