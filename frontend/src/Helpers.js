import { baseURL } from './settings';

export function admin() {
    return window.location.href.includes('localhost') || localStorage.getItem('mobile-dice-admin');
}

export function makeRequestOptions(body, method = 'POST') {
    if (method === 'GET') {
        return {
            method,
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
        };
    }
    return {
        method,
        mode: 'cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    };
}

export function fetchWrapper(url, body, method = 'POST') {
    url = `${baseURL}${url}`;
    if (method === 'GET') {
        if (body) {
            url = `${url}?`;
        }
        for (var key in body) {
            url = `${url}${key}=${body[key]}&`;
        }
    }
    return fetch(url, makeRequestOptions(body, method)).catch((error) => {
        console.log(error);
    });
}

export function squares_in_order() {
    return [
        'F1',
        'F2',
        'F3',
        'F4',
        'F5',
        'F6',
        'E1',
        'E2',
        'E3',
        'E4',
        'E5',
        'E6',
        'D1',
        'D2',
        'D3',
        'D4',
        'D5',
        'D6',
        'C1',
        'C2',
        'C3',
        'C4',
        'C5',
        'C6',
        'B1',
        'B2',
        'B3',
        'B4',
        'B5',
        'B6',
        'A1',
        'A2',
        'A3',
        'A4',
        'A5',
        'A6',
    ]
}