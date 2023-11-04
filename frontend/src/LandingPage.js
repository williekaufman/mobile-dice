import React, { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import { fetchWrapper } from './Helpers';

export default function LandingPage() {
    function newGame() {
        fetchWrapper("/new_game", {}, "POST")
            .then((response) => response.json())
            .then((data) => {
                window.location.href = `/game/${data.gameId}`;
            }
        )
    } 
    
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <Button variant="contained" onClick={newGame}>New Game</Button>
        </div>
        )
}