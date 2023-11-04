import React, { useState, useEffect } from 'react';
import './Dice.css';
import Button from '@mui/material/Button';

function backgroundImageUrl(face) {
    return `url("../images/${face}.jpg")`;
}

function Die({ faces, active , live }) {
    if (faces.length !== 6) {
        return null;
    }

    let className = live ? "die" : "die dead";

    return (
        <div className={className}>
            {faces.map((face, index) => (
                <div key={index} style={{ backgroundImage: backgroundImageUrl(face) }} className={active === index && live ? "face active" : "face"}>
                </div>
            ))}
        </div>
    );
}

function Lock({ index, live, locks, setLocks }) {
    function toggleLock() {
        console.log(locks);
        let newLocks = [...locks];
        newLocks[index] = !newLocks[index];
        setLocks(newLocks);
    }

    function styles() {
        if (live) {
            return { backgroundColor: locks[index] ? "red" : "blue" }
        } return {}
    }

    return (
        <div className="lock" style={{ marginBottom: '8px' }}>
            <Button style={styles()} variant={live ? "contained" : "outlined"} onClick={toggleLock} disabled={!live}>
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
                    <Lock index={index} live={die.live} locks={locks} setLocks={setLocks} />
                    <Die live={die.live} active={die.active} faces={die.faces} />
                </div>
            ))}
        </div>
    );
}