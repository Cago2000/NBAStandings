import { fillSchedule, updateLiveGames } from './javascript/schedule.js';
import { fillStandings, fillPredictionsStandings } from './javascript/standings.js';
import { fillMVPLadder, fillMVPPredictions } from './javascript/mvp_ladder.js';
import { sortTruthTeams } from './javascript/utils.js';

const users = ["Can", "Marlon", "Ole"];
const conferences = ["East", "West"];
let data;
let live_data;

async function init() {
  try {
    const resData = await fetch('data.json');
    data = await resData.json();

    const resLive = await fetch('live_data.json');
    live_data = await resLive.json();

    fillSchedule(data.Schedule);

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

    setInterval(async () => {
      try {
        const res = await fetch('live_data.json');
        const live_data_json = await res.json();
        updateLiveGames(live_data_json.Live_Games);
      } catch (err) {
        console.error(err);
      }
    }, 1000);

  } catch (err) {
    console.error(err);
  }
}

// Initialize app
init();
