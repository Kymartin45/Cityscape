import FingerprintJS from '@fingerprintjs/fingerprintjs-pro';
import 'dotenv/config';

window.onload = function refreshInputFields() {
    document.getElementById('user-submit-guess').addEventListener('click', submitGuess, {once: true});

    if (!localStorage.getItem('currentStreak') && !localStorage.getItem('maxStreak')) {
        localStorage.setItem('currentStreak', '0');
        localStorage.setItem('maxStreak', '0');
        localStorage.setItem('gamesPlayed', '0');
        localStorage.setItem('gamesWon', '0');
        localStorage.setItem('winPercentage', '0');
    }
}

function refreshPage() {
    window.location.reload();
}

