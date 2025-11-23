export function fillStandings(tableId, teams, includeWL = false) {
  const tbody = document.getElementById(tableId).querySelector('tbody');
  tbody.innerHTML = '';

  teams.forEach((team, i) => {
    const tr = document.createElement('tr');
    const seed = includeWL ? i + 1 : team.seed;
    if (seed === 1) tr.classList.add('conference-leader');
    else if (seed >= 2 && seed <= 6) tr.classList.add('playoff-seed');
    else if (seed >= 7 && seed <= 10) tr.classList.add('playin-seed');

    if (includeWL) {
      tr.innerHTML = `
        <td>${i + 1}</td>
        <td>${team.team}</td>
        <td class="win">${team.wins}</td>
        <td class="loss">${team.losses}</td>
        <td>${team.games_behind}</td>
      `;
    } else {
      tr.innerHTML = `<td>${team.seed}</td><td>${team.team}</td>`;
    }

    tbody.appendChild(tr);
  });
}

export function fillPredictionsStandings(tableId, predictedTeams, truthTeams) {
  const tbody = document.getElementById(tableId).querySelector('tbody');
  tbody.innerHTML = '';
  predictedTeams.forEach((team, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${team.seed}</td><td>${team.team}</td>`;
    const truthPos = truthTeams.findIndex(t => t.team === team.team);
    if (truthPos === i) tr.classList.add('match');
    else if (Math.abs(truthPos - i) === 1) tr.classList.add('almost-match');
    tbody.appendChild(tr);
  });
}
