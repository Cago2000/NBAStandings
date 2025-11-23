// utils.js
export function sortTruthTeams(teams) {
  return teams.slice().sort((a, b) => {
    const winPctA = a.wins / (a.wins + a.losses);
    const winPctB = b.wins / (b.wins + b.losses);
    if (winPctB !== winPctA) return winPctB - winPctA;
    return a.games_behind - b.games_behind;
  });
}

export function createGameRow(game, isLive = false) {
    const tr = document.createElement('tr');
    const awayScore = game.away_score ?? '';
    const homeScore = game.home_score ?? '';
    let score = '';
    let gameStatusClass = '';

    if (game.game_status === "Final") {
      // Finished game
      score = `${awayScore} - ${homeScore}`;
      gameStatusClass = 'game-over-score';
    } else {
      const hasStarted = game.game_status && !game.game_status.includes("ET");
      if (hasStarted) {
        // Live game
        score = `${awayScore} - ${homeScore}<br>${game.game_status}`;
        gameStatusClass = 'live-score';
      } else {
        // Not started
        score = "";
        gameStatusClass = '';
      }
    }

  tr.innerHTML = `
    <td>${game.time}</td>
    <td>
      <img src="assets/logos/${game.away}.svg" alt="${game.away} Logo" width="30" height="30">
      ${game.away}
    </td>
    <td>
      <img src="assets/logos/${game.home}.svg" alt="${game.home} Logo" width="30" height="30">
      ${game.home}
    </td>
    <td class="${gameStatusClass}">${score}</td>
  `;
  return tr;
}
