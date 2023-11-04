import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWrapper } from './Helpers';
import Board from './Board';
import Dice from './Dice';
import './Styles.css';
import Button from '@mui/material/Button';

export default function GamePage() {
    let { gameId } = useParams();
    const [game, setGame] = useState({});
    let [locks, setLocks] = useState([false, false, false, false, false]);

    function updateGame() {
        fetchWrapper("/state", { gameId }, "GET")
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    console.log(data['error']);
                    return;
                }
                setGame(data);
            });
    }

    useEffect(() => {
        updateGame();
    }, [gameId]);

    function locksArg() {
        return locks.map((lock, i) => lock ? i : null).filter((lock) => lock !== null);
    }

    function Roll() {
        fetchWrapper("/roll", { gameId, locks: locksArg() }, "POST")
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    console.log(data['error']);
                    return;
                }
                setGame(data);
            });
    }

    function SubmitTurn() {
        fetchWrapper("/submit", { gameId }, "POST")
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    console.log(data['error']);
                    return;
                }
                setLocks([false, false, false, false, false]);
                setGame(data);
            });
    }

    let canRoll = game && game.rolls > 0;

    if (!game) {
        return null
    }

    return (
        <div>
            <div className="centered-container" style={{ marginTop: '1vh' }}>
                <Button style={{ color: 'white', backgroundColor: canRoll ? 'blue' : 'red' }} variant="contained" onClick={Roll} disabled={!canRoll} >
                    Roll {game ? `(${game.rolls})` : null}
                </Button>
                <Button style={{ color: 'white', backgroundColor: 'blue', marginLeft: '1vw' }}
                    variant="contained" onClick={SubmitTurn}>
                    Submit Turn
                </Button>
            </div>
            <div className="centered-container">
                <Dice game={game} locks={locks} setLocks={setLocks} />
            </div>
            <div className="centered-container">
                <Board board={game.board} />
            </div>
        </div>
    )
}