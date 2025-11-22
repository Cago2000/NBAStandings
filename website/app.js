async function loadData() {
  try {
    let res = await fetch('data.json');
    const data = await res.json();

    res = await fetch('live_data.json');
    const live_data = await res.json();

    const users = ["Can", "Marlon", "Ole"];
    const conferences = ["East", "West"];

    function sortTruthTeams(teams) {
      return teams.slice().sort((a, b) => {
        const winPctA = a.wins / (a.wins + a.losses);
        const winPctB = b.wins / (b.wins + b.losses);
        if (winPctB !== winPctA) return winPctB - winPctA;
        return a.games_behind - b.games_behind;
      });
    }

    function fillStandings(tableId, teams, includeWL = false) {
      const tbody = document.getElementById(tableId).querySelector('tbody');
      tbody.innerHTML = '';

      teams.forEach((team, i) => {
        const tr = document.createElement('tr');

        // Determine seed (use index+1 for includeWL, otherwise team.seed)
        let seed = includeWL ? i + 1 : team.seed;

        // Add appropriate class based on seed
        if (seed >= 1 && seed <= 6) {
          tr.classList.add('playoff_seed');
        } else if (seed >= 7 && seed <= 10) {
          tr.classList.add('playin_seed');
        }

        // Fill row content
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

    function fillPredictionsStandings(tableId, predictedTeams, truthTeams) {
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

    function fillSchedule(schedule, live_schedule) {
      const container = document.getElementById('schedule-grid');
      container.innerHTML = '';

      for (const [date, games] of Object.entries(schedule)) {
        if (date.includes("Today")){
          fillLiveGames(date, live_schedule, container)
          continue;
        }
        const dayDiv = document.createElement('div');
        dayDiv.classList.add('schedule-day');

        const heading = document.createElement('h2');
        heading.textContent = date;
        dayDiv.appendChild(heading);

        const table = document.createElement('table');
        const thead = document.createElement('thead');
        thead.innerHTML = `
        <tr>
          <th>Time</th>
          <th>Away</th>
          <th>Home</th>
          <th>Score</th>
        </tr>`;
        table.appendChild(thead);

        const tbody = document.createElement('tbody');

        games.forEach(game => {
          const tr = document.createElement('tr');

          const awayScore = game.away_score !== null ? game.away_score : '';
          const homeScore = game.home_score !== null ? game.home_score : '';
          let score = game.game_status === "Final" ? `${awayScore} - ${homeScore}`: '';

          const awayCell = `
          <td>
            <img src="assets/logos/${game.away}.svg" alt="${game.away} Logo" width="30" height="30">
            ${game.away}
          </td>`;
          const homeCell = `
          <td>
            <img src="assets/logos/${game.home}.svg" alt="${game.home} Logo" width="30" height="30">
            ${game.home}
          </td>`;

          tr.innerHTML = `
          <td>${game.time}</td>
          ${awayCell}
          ${homeCell}
          <td>${score}</td>
        `;

          tbody.appendChild(tr);
        });

        table.appendChild(tbody);
        dayDiv.appendChild(table);
        container.appendChild(dayDiv);
      }
    }

    function fillLiveGames(headingTextContent, liveGames, container) {
      const dayDiv = document.createElement('div');
      dayDiv.classList.add('schedule-day');

      const heading = document.createElement('h2');
      heading.textContent = headingTextContent;
      dayDiv.appendChild(heading);

      const table = document.createElement('table');
      const thead = document.createElement('thead');
      thead.innerHTML = `
        <tr>
          <th>Time</th>
          <th>Away</th>
          <th>Home</th>
          <th>Score</th>
        </tr>`;
      table.appendChild(thead);

      const tbody = document.createElement('tbody');

      for (const [key, game] of Object.entries(liveGames)) {
        const tr = document.createElement('tr');

        const awayScore = game.away_score !== null ? game.away_score : '';
        const homeScore = game.home_score !== null ? game.home_score : '';

        // Determine live/final/empty
        let score = "";
        let liveClass = "";
        const hasStarted = game.game_status && !game.game_status.includes("ET") && game.game_status !== "TBD";

        if (hasStarted) {

          score =
              `${awayScore} - ${homeScore} ${game.game_status}`;
          liveClass = "live-score";
        }

        const awayCell = `
          <td>
            <img src="assets/logos/${game.away}.svg" alt="${game.away} Logo" width="30" height="30">
            ${game.away}
          </td>`;
        const homeCell = `
          <td>
            <img src="assets/logos/${game.home}.svg" alt="${game.home} Logo" width="30" height="30">
            ${game.home}
          </td>`;

        tr.innerHTML = `
          <td>${game.time}</td>
          ${awayCell}
          ${homeCell}
          <td class="${liveClass}">${score}</td>
        `;

        tbody.appendChild(tr);
      }

      table.appendChild(tbody);
      dayDiv.appendChild(table);
      container.appendChild(dayDiv);
    }


    function fillMVPLadder(players) {
      const tbody = document.getElementById('mvp-table').querySelector('tbody');
      tbody.innerHTML = '';
      players.forEach(player => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${player.rank}</td><td>${player.player}</td><td>${player.team}</td>`;
        tbody.appendChild(tr);
      });
    }

    function fillMVPPredictions(tableId, predictedPlayers, truthPlayers) {
      const tbody = document.getElementById(tableId).querySelector('tbody');
      tbody.innerHTML = '';
      const topTruth = truthPlayers.find(t => t.rank === 1);
      predictedPlayers.forEach((player, i) => {
        const tr = document.createElement('tr');
        if (topTruth && topTruth.player === player.player && i === 0) {
          tr.classList.add('mvp_match');
        }
        tr.innerHTML = `<td>${player.player}</td><td>${player.team}</td>`;
        tbody.appendChild(tr);
      });
    }

    const sortedTruth = {};
    conferences.forEach(conf => {
      sortedTruth[conf] = sortTruthTeams(data.Standings[conf]);
      fillStandings(`truth-${conf.toLowerCase()}-table`, sortedTruth[conf], true);
    });

    users.forEach(user => {
      let totalPoints = 0;
      let maxPoints = 0;

      conferences.forEach(conf => {
        const predTeams = data.Standings_Predictions[user][conf] || [];
        const truthTeams = sortedTruth[conf] || [];
        fillPredictionsStandings(`${user.toLowerCase()}-${conf.toLowerCase()}-table`, predTeams, truthTeams);

        predTeams.forEach((team, i) => {
          const truthPos = truthTeams.findIndex(t => t.team === team.team);
          if (truthPos === i) totalPoints += 2;
          else if (Math.abs(truthPos - i) === 1) totalPoints += 1;
        });
        maxPoints += predTeams.length * 2;
      });

      const userMVPPred = data.MVP_Predictions[user] || [];
      const truthMVP = data.MVP_Ladder || [];
      const topTruth = truthMVP.find(t => t.rank === 1);
      const topPred = userMVPPred[0];
      if (topTruth && topPred && topTruth.player === topPred.player) totalPoints += 5;
      maxPoints += 5;

      fillMVPPredictions(`${user.toLowerCase()}-mvp-prediction-table`, userMVPPred, truthMVP);
      document.getElementById(`${user.toLowerCase()}-header`).textContent = `${user} (${totalPoints}/${maxPoints})`;
    });

    fillMVPLadder(data.MVP_Ladder);
    fillSchedule(data.Schedule, live_data.Live_Games)

  } catch (err) {
    console.error(err);
  }
}

// Load everything on page load
loadData();

