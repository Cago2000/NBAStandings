export function sortTruthTeams(teams) {
  return teams.slice().sort((a, b) => {
    const winPctA = a.wins / (a.wins + a.losses);
    const winPctB = b.wins / (b.wins + b.losses);
    if (winPctB !== winPctA) return winPctB - winPctA;
    return a.games_behind - b.games_behind;
  });
}

export function createGameRow(game) {
  const tr = document.createElement('tr');
  tr.dataset.gameId = game.game_id;

  let gameStatusClass = '';
  if (game.game_status === "Final") gameStatusClass = 'game-over-score';
  else if (game.game_status && !game.game_status.includes("ET")) gameStatusClass = 'live-score';

  const score = getScoreHTML(game);

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
    <td class="score-cell ${gameStatusClass}">${score}</td>
  `;

  return tr;
}

export function getScoreHTML(game) {
  const awayScore = game.away_score ?? 0;
  const homeScore = game.home_score ?? 0;

  if (awayScore === 0 && homeScore === 0 && game.game_status.includes("ET")) {
    return '';
  }

  let scoreHTML = '';

  if (awayScore !== '' && homeScore !== '') {
    if (awayScore > homeScore) {
      scoreHTML = `<span style="font-weight:bold">${awayScore}</span> - <span>${homeScore}</span>`;
    } else if (homeScore > awayScore) {
      scoreHTML = `<span>${awayScore}</span> - <span style="font-weight:bold">${homeScore}</span>`;
    } else {
      scoreHTML = `<span>${awayScore}</span> - <span>${homeScore}</span>`;
    }
  }

  if (game.game_status && !game.game_status.includes("ET") && game.game_status !== "Final") {
    scoreHTML += `<br><span class="game-status">${game.game_status}</span>`;
  }

  return scoreHTML;
}
