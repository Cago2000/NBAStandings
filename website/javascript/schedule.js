import { createGameRow, getScoreHTML } from './utils.js';

let gameRowsMap = {};

// Render full schedule from data.Schedule
export function fillSchedule(scheduleData) {
  const container = document.getElementById('schedule-grid');
  container.innerHTML = '';

  // Add wrapper class for CSS
  container.classList.add('schedule-container', 'schedule-grid');

  gameRowsMap = {}; // reset map

  for (const [date, games] of Object.entries(scheduleData)) {
    appendScheduleDay(container, date, games);
  }
}

// Append a single day
export function appendScheduleDay(container, headingText, games) {
  const dayDiv = document.createElement('div');
  dayDiv.classList.add('schedule-day'); // CSS background, padding, shadow

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

  Object.values(games).forEach(game => {
    // Use Schedule data to populate the row initially
    const row = createGameRow(game);

    // Add CSS class for score cell depending on game status
    const scoreCell = row.querySelector('td.score-cell');
    if (scoreCell) {
      if (game.game_status === 'Final') scoreCell.classList.add('game-over-score');
      else if (game.game_status && !game.game_status.includes('ET')) scoreCell.classList.add('live-score');
      // games not started (ET) keep default styling
    }

    tbody.appendChild(row);

    // Store reference for live updates
    gameRowsMap[game.game_id] = row;
  });

  table.appendChild(tbody);
  dayDiv.appendChild(table);
  container.appendChild(dayDiv);
}

// Update only scores for live games
export function updateLiveGames(liveGames) {
  if (!liveGames) return;

  liveGames.forEach(game => {
    const row = gameRowsMap[game.game_id];

    if (row) {
      const scoreCell = row.querySelector('td.score-cell');
      if (scoreCell) {
        // Overwrite Schedule score with live score if the game is actually live
        scoreCell.innerHTML = getScoreHTML(game);

        // Update CSS classes dynamically
        scoreCell.classList.remove('game-over-score', 'live-score');
        if (game.game_status === 'Final') scoreCell.classList.add('game-over-score');
        else if (game.game_status && !game.game_status.includes('ET')) scoreCell.classList.add('live-score');
      }
    } else {
      console.warn('Live game not found in schedule:', game.game_id);
    }
  });
}
