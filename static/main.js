function refreshPage() {
    window.location.reload();
}

function showGlobalLeaderboard() {
    fetch('/leaderboard')
    .then((res) => res.json())
    .then(globalLeaderboard => {
        const gamesPlayed = document.getElementById('games-played');
        const gamesWon = document.getElementById('games-won');
        const leaderboard = globalLeaderboard['leaderboard'];
        console.log(globalLeaderboard);
                
        document.getElementById('total-player-count').textContent = globalLeaderboard['totalPlayers'];

        // for every player in db, list out their stats (gamesPlayed, gamesWon)
        // continues to append new `p` element, so gotta find workaround to display all stats
        leaderboard.forEach((item) => {
            const pGamesPlayed = document.createElement('p');
            const pGamesWon = document.createElement('p');

            pGamesPlayed.textContent = item['gamesPlayed'];
            pGamesWon.textContent = item['gamesWon'];

            gamesPlayed.append(pGamesPlayed);
            gamesWon.append(pGamesWon);
        })
    })
    .catch((err) => { console.error(err); })
}

