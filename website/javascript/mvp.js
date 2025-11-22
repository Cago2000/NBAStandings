// mvp.js
export function fillMVPLadder(players) {
  const tbody = document.getElementById('mvp-table').querySelector('tbody');
  tbody.innerHTML = '';
  players.forEach(player => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${player.rank}</td><td>${player.player}</td><td>${player.team}</td>`;
    tbody.appendChild(tr);
  });
}

export function fillMVPPredictions(tableId, predictedPlayers, truthPlayers) {
  const tbody = document.getElementById(tableId).querySelector('tbody');
  tbody.innerHTML = '';
  const topTruth = truthPlayers.find(t => t.rank === 1);
  predictedPlayers.forEach((player, i) => {
    const tr = document.createElement('tr');
    if (topTruth && topTruth.player === player.player && i === 0) tr.classList.add('mvp_match');
    tr.innerHTML = `<td>${player.player}</td><td>${player.team}</td>`;
    tbody.appendChild(tr);
  });
}
