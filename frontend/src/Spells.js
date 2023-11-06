import React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import styled from '@mui/material/styles/styled';

function Cost({ cost }) {
    if (!cost) {
        return null;
    }

    return (
        <div className="cost">
            <Typography variant="body1">
                Cost: {cost.amount} {cost.resource}
            </Typography>
        </div>
    )
}

function Spell({ spell, availableSpells, casting, setCasting, setHoveredSpell }) {
    if (!spell || !availableSpells) {
        return null;
    }

    const LargeButton = styled(Button)({
        padding: '10px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '30vw',
    });

    return (
        <div>
            <LargeButton
                style={casting === spell.name ? { backgroundColor: 'red' } : {}}
                variant="contained"
                disabled={!Object.keys(availableSpells).includes(spell.name)}
                onClick={() => {
                    if (casting !== spell.name) {
                        setCasting(spell.name)
                    }
                    else {
                        setCasting(null)
                    }
                }}
                onMouseEnter={() => {
                    setHoveredSpell(spell.name)
                }}
                onMouseLeave={() => {
                    setHoveredSpell(null);
                }}>
                <Box>
                    <Typography variant="h5" component="h2">
                        {spell.name}
                        {spell.cost.map((cost, index) => (
                            <Cost key={index} cost={cost} />
                        ))}
                    </Typography>
                    <Typography variant="body1">
                        {spell.description}
                    </Typography>
                </Box>
            </LargeButton>
        </div>
    )
}
export default function Spells({ spells, game, casting, setCasting, setHoveredSpell }) {
    if (!game || !spells) {
        return null;
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {spells.map((spell, index) => (
                <div key={index} className="spell">
                    <Spell spell={spell} availableSpells={game.availableSpells} casting={casting} setCasting={setCasting} setHoveredSpell={setHoveredSpell} />
                </div>
            ))}
        </div>
    )
}

