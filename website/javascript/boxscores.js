export function fillBoxscores(boxscore_data) {
  const container = document.getElementById("boxscores-container");

  if (!container) {
    console.error("Boxscores container not found!");
    return;
  }

  console.log("Clearing previous boxscores...");
  container.innerHTML = ''; // clear previous

  if (!boxscore_data || Object.keys(boxscore_data).length === 0) {
    console.warn("No boxscore data available to render.");
    container.innerHTML = '<p>No games available.</p>';
    return;
  }

  console.log(`Rendering ${Object.keys(boxscore_data).length} game(s)...`);

  Object.keys(boxscore_data).forEach(game_id => {
    const game = boxscore_data[game_id];
    console.log(`Processing game: ${game.home} vs ${game.away} (ID: ${game_id})`);

    // Create wrapper for each game
    const gameDiv = document.createElement('div');
    gameDiv.classList.add('boxscore-game');

    // Game header
    const header = document.createElement('h3');
    header.textContent = `${game.home} vs ${game.away} - ${game.game_status}`;
    gameDiv.appendChild(header);

    // Table
    const table = document.createElement('table');
    table.id = `game-${game_id}-table`;

    // Table headers
    const thead = document.createElement('thead');
    thead.innerHTML = `
      <tr>
        <th>Player</th><th>Team</th><th>MIN</th><th>PTS</th><th>REB</th>
        <th>AST</th><th>STL</th><th>BLK</th><th>TO</th><th>PLUS_MINUS</th>
      </tr>
    `;
    table.appendChild(thead);

    const tbody = document.createElement('tbody');

    if (game.boxscore && game.boxscore.length) {
      console.log(`Adding ${game.boxscore.length} players for this game.`);
      game.boxscore.forEach(player => {
        console.log("Player data:", player);
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${player.PLAYER_NAME}</td>
          <td>${player.TEAM_ABBREVIATION}</td>
          <td>${player.MIN || 0}</td>
          <td>${player.PTS || 0}</td>
          <td>${player.REB || 0}</td>
          <td>${player.AST || 0}</td>
          <td>${player.STL || 0}</td>
          <td>${player.BLK || 0}</td>
          <td>${player.TOV || 0}</td>
          <td>${player.PLUS_MINUS || 0}</td>
        `;
        tbody.appendChild(tr);
      });
    } else {
      console.warn(`No boxscore available for game ${game_id}`);
      const tr = document.createElement('tr');
      tr.innerHTML = `<td colspan="10">No boxscore available</td>`;
      tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    gameDiv.appendChild(table);
    container.appendChild(gameDiv);
  });

  console.log("Boxscores rendering complete.");
}
