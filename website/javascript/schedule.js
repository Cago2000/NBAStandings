// schedule.js
import { getScoreHTML, createGameRow } from './utils.js';

let liveTableBody; // private variable inside this module

export function fillSchedule(scheduleData, liveGames) {
  const container = document.getElementById('schedule-grid');
  container.innerHTML = '';

  for (const [date, games] of Object.entries(scheduleData)) {
    if (date.includes("Today")) {
      appendScheduleDay(container, date, liveGames, true);
    } else {
      appendScheduleDay(container, date, games, false);
    }
  }
}

export function appendScheduleDay(container, headingText, games, isLive = false) {
  const dayDiv = document.createElement('div');
  dayDiv.classList.add('schedule-day');

  const heading = document.createElement('h2');
  heading.textContent = headingText;
  dayDiv.appendChild(heading);

  const table = document.createElement('table');
  table.innerHTML = `
    <thead>
      <tr>
        <th>Time</th>
        <th>Away</th>
        <th>Home</th>
        <th>Score</th>
      </tr>
    </thead>
  `;

  const tbody = document.createElement('tbody');

  if (games && Object.keys(games).length > 0) {
    Object.values(games).forEach(game => {
      // Generate a unique ID for each game row
      const gameId = `${game.away}-${game.home}-${game.time}`;
      const row = createGameRow({ ...game, id: gameId }, isLive);
      tbody.appendChild(row);
    });
  } else if (isLive) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="4" style="text-align:center;">No live games currently</td>`;
    tbody.appendChild(tr);
  }

  if (isLive) liveTableBody = tbody; // store reference for updates

  table.appendChild(tbody);
  dayDiv.appendChild(table);
  container.appendChild(dayDiv);

  return tbody; // return tbody so it can be reused or updated later
}


export function updateLiveGames(newLiveGames) {
  if (!liveTableBody) return;

  newLiveGames.forEach(game => {
    const gameId = `${game.away}-${game.home}-${game.time}`;
    const row = liveTableBody.querySelector(`tr[data-game-id="${gameId}"]`);

    if (row) {
      const scoreCell = row.querySelector('td.score-cell');
      if (scoreCell) {
        scoreCell.innerHTML = getScoreHTML(game); // now bold + live status updates
      }
    } else {
      liveTableBody.appendChild(createGameRow(game, true));
    }
  });
}


