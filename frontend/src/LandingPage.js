import { useEffect } from 'react';
import { fetchWrapper } from './Helpers';

export default function LandingPage() {
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

    useEffect(() => {
        newGame();
    }, []);
    
    return null;
}