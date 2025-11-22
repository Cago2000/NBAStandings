// schedule.js
import { createGameRow } from './utils.js';

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
      tbody.appendChild(createGameRow(game, isLive));
    });
  } else if (isLive) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="4" style="text-align:center;">No live games currently</td>`;
    tbody.appendChild(tr);
  }

  if (isLive) liveTableBody = tbody;

  table.appendChild(tbody);
  dayDiv.appendChild(table);
  container.appendChild(dayDiv);
}

export function updateLiveGames(newLiveGames) {
  if (!liveTableBody) return;

  liveTableBody.innerHTML = '';

  if (newLiveGames && Object.keys(newLiveGames).length > 0) {
    Object.values(newLiveGames).forEach(game => {
      liveTableBody.appendChild(createGameRow(game, true));
    });
  } else {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="4" style="text-align:center;">No live games currently</td>`;
    liveTableBody.appendChild(tr);
  }
}
