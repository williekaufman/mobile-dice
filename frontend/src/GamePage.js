import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWrapper } from './Helpers';
import Board from './Board';
import Dice from './Dice';
import Spells from './Spells';
import Intent from './Intent';
import Toast from './Toast';
import PlayerInfo from './PlayerInfo';
import './Styles.css';
import Button from '@mui/material/Button';
import { Typography } from '@mui/material';

let colors = ["black", "black", "black"];

export function color(index) {
    return colors[index];
}

function newGame() {
    let board = localStorage.getItem("board");
    let numSpells = localStorage.getItem("numSpells");
    fetchWrapper("/new_game", { numSpells , board }, "POST")
        .then((response) => response.json())
        .then((data) => {
            window.location.href = `/game/${data.gameId}`;
        }
        )
}

function Result({ result }) {
    if (!result) {
        return null;
    }

    let color = result === "win" ? "green" : "red";

    return (
        <div className="result">
            <h1 style={{ color: color }}>You {result}</h1>
        </div>
    )
}

export default function GamePage() {
    let { gameId } = useParams();
    let [game, setGame] = useState(null);
    let [spells, setSpells] = useState([]);
    let [casting, setCasting] = useState(null);
    let [hoveredSpell, setHoveredSpell] = useState(null);
    let [locks, setLocks] = useState([false, false, false, false, false]);
    let [error, setError] = useState(null);
    let [activeEnemy, setActiveEnemy] = useState(null);

    const showErrorToast = (message) => {
        console.log("Setting error");
        setError(message);

        setTimeout(() => {
            setError(null);
        }, 5000);
    };

    const updateGame = useCallback(() => {
        fetchWrapper("/state", { gameId }, "GET")
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    showErrorToast(data['error']);
                    return;
                }
                setGame(data);
            });
    }, [gameId]);

    const getSpells = useCallback(() => {
        fetchWrapper("/spells", { gameId }, "GET")
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    showErrorToast(data['error']);
                    return;
                }
                setSpells(data.spells);
            });
    }, [gameId]);

    const locksArg = useCallback(() => {
        return locks.map((lock, i) => lock ? i : null).filter((lock) => lock !== null);
    }, [locks])

    const roll = useCallback(() => {
        fetchWrapper("/roll", { gameId, locks: locksArg() }, "POST")
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    showErrorToast(data['error']);
                    return;
                }
                setGame(data);
                setCasting(null);
            });
    }, [gameId, locksArg])

    const submitTurn = useCallback(() => {
        fetchWrapper("/submit", { gameId }, "POST")
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    showErrorToast(data['error']);
                    return;
                }
                setLocks([false, false, false, false, false]);
                setGame(data);
                setCasting(null);
                getSpells();
            });
    }, [gameId, getSpells])
    
    useEffect(() => {
        updateGame();
        getSpells();
    }, [gameId, updateGame, getSpells]);

    useEffect(() => {
        function handleKeyDown(e) {
            if (e.key === "r") {
                roll();
            } else if (e.key === "Enter") {
                submitTurn();
            } else if (e.key === "N") {
                newGame();
            }
        }

        document.addEventListener("keydown", handleKeyDown);
        return () => document.removeEventListener("keydown", handleKeyDown);
    }, [roll, submitTurn]);


    let canRoll = game && game.rolls > 0;

    if (!game) {
        return null
    }

    return (
        <div>
            <div className="vertical-container">
                <div className="horizontal-container">
                    <div className="vertical-container" style={{ marginTop: '1vh' }}>
                        <Toast message={error} onClose={() => setError(null)} />
                        <div className="horizontal-container" style={{ marginBottom: '10px' }}>
                            <Result result={game.result} />
                            <Button variant="contained" style={{ backgroundColor: 'blue' }} onClick={newGame}>
                                New Game
                            </Button>
                        </div>
                        <div className="horizontal-container">
                            <Button style={{ color: 'white', backgroundColor: canRoll ? 'blue' : 'red' }} variant="contained" onClick={roll} disabled={!canRoll} >
                                Roll {game ? `(${game.rolls})` : null}
                            </Button>
                            <Button style={{ color: 'white', backgroundColor: 'blue', marginLeft: '1vw' }}
                                variant="contained" onClick={submitTurn}>
                                Submit Turn
                            </Button>
                            <Typography variant="h5">
                                Turn {game.game_info.turn}
                            </Typography>
                        </div>
                        <Dice game={game} locks={locks} setLocks={setLocks} />
                        <PlayerInfo game={game} />
                        <Intent game={game} setActiveEnemy={setActiveEnemy} />
                        <Spells game={game} spells={spells} casting={casting} setCasting={setCasting} hoveredSpell={hoveredSpell} setHoveredSpell={setHoveredSpell} />
                    </div>
                    <Board game={game} setGame={setGame} casting={casting} setCasting={setCasting} hoveredSpell={hoveredSpell} showErrorToast={showErrorToast} activeEnemy={activeEnemy} />
                </div>
            </div>
        </div>
    )
}