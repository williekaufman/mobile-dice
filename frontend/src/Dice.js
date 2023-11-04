import React, { useState, useEffect } from 'react';
import './Dice.css';
import Button from '@mui/material/Button';

function backgroundImageUrl(face) {
    return `url("../images/${face}.jpg")`;
}

function Die({ faces, active }) {
    if (faces.length !== 6) {
        return null;
    }

    return (
        <div className="die">
            {faces.map((face, index) => (
                <div key={index} style={{ backgroundImage: backgroundImageUrl(face) }} className={active === index ? "face active" : "face"}>
                </div>
            ))}
        </div>
    );
}

function Lock({ index, locks, setLocks }) {
    function toggleLock() {
        console.log(locks);
        let newLocks = [...locks];
        newLocks[index] = !newLocks[index];
        setLocks(newLocks);
    }

    return (
        <div className="lock" style={{ marginBottom: '8px' }}>
            <Button style={{ backgroundColor: locks[index] ? "red" : "blue" }} variant="contained" onClick={toggleLock}>
                {locks[index] ? "Unlock" : "Lock"}
            </Button>
        </div>
    );
}

export default function Dice({ game, locks, setLocks }) {
    if (!game || !game.dice) { 
        return null;
    }
    return (
        <div className="dice">
            {game.dice.map((die, index) => (
                <div key={index} className="container">
                    <Lock index={index} locks={locks} setLocks={setLocks} />
                    <Die active={die.active} faces={die.faces} />
                </div>
            ))}
        </div>
    );
}