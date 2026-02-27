const els = {
  pendingStatus: document.getElementById("pendingStatus"),
  latestPrize: document.getElementById("latestPrize"),
  latestMatches: document.getElementById("latestMatches"),
  regionSelect: document.getElementById("regionSelect"),
  regionSummary: document.getElementById("regionSummary"),
  prizeMatrix: document.getElementById("prizeMatrix"),
  pendingPanel: document.getElementById("pendingPanel"),
  drawNumbers: document.getElementById("drawNumbers"),
  matchedNumbers: document.getElementById("matchedNumbers"),
  metricsPanel: document.getElementById("metricsPanel"),
  historyTable: document.getElementById("historyTable"),
  feedback: document.getElementById("feedback"),
  placeBetBtn: document.getElementById("placeBetBtn"),
  runDrawBtn: document.getElementById("runDrawBtn"),
  resetBtn: document.getElementById("resetBtn"),
  refreshBtn: document.getElementById("refreshBtn"),
  n1: document.getElementById("n1"),
  n2: document.getElementById("n2"),
  n3: document.getElementById("n3"),
  n4: document.getElementById("n4"),
};

let currentState = null;
let currentMetrics = null;

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail || "Request failed");
  }

  return body;
}

function feedback(message, isError = false) {
  els.feedback.textContent = message;
  els.feedback.style.color = isError ? "#ff8f8f" : "#7cd39b";
}

function toCurrency(value) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(value);
}

function renderRegions(regions) {
  els.regionSelect.innerHTML = "";
  regions.forEach((region) => {
    const option = document.createElement("option");
    option.value = region.code;
    option.textContent = `${region.label} (${region.code})`;
    els.regionSelect.appendChild(option);
  });

  renderPrizeMatrix();
}

function renderPrizeMatrix() {
  if (!currentState) return;

  const selectedCode = els.regionSelect.value;
  const region = currentState.regions.find((item) => item.code === selectedCode);
  if (!region) return;

  els.regionSummary.textContent = `${region.label} payout policy`;
  els.prizeMatrix.innerHTML = "";

  [4, 3, 2, 1].forEach((hits) => {
    const card = document.createElement("div");
    card.className = "matrix-item";
    const prize = region.prize_by_matches[hits] || 0;
    card.textContent = `${hits} hits: ${toCurrency(prize)}`;
    els.prizeMatrix.appendChild(card);
  });
}

function balls(container, values) {
  container.innerHTML = "";
  if (!values || values.length === 0) {
    container.innerHTML = '<div class="ball">-</div>';
    return;
  }

  values.forEach((value) => {
    const node = document.createElement("div");
    node.className = "ball";
    node.textContent = String(value);
    container.appendChild(node);
  });
}

function renderState(state) {
  currentState = state;

  const pending = state.pending_bet;
  els.pendingStatus.textContent = pending ? pending.ticket_id.slice(0, 8) : "none";

  if (pending) {
    els.pendingPanel.innerHTML = `
      <strong>Ticket ${pending.ticket_id.slice(0, 8)}</strong><br />
      Region: ${pending.region}<br />
      Numbers: ${pending.numbers.join(", ")}<br />
      Created: ${pending.created_at}
    `;
  } else {
    els.pendingPanel.textContent = "No pending bet. Place a new ticket.";
  }

  const latest = state.history[0];
  if (latest) {
    els.latestPrize.textContent = toCurrency(latest.prize);
    els.latestMatches.textContent = String(latest.matches);
    balls(els.drawNumbers, latest.draw_numbers);
    balls(els.matchedNumbers, latest.matched_numbers);
  } else {
    els.latestPrize.textContent = toCurrency(0);
    els.latestMatches.textContent = "0";
    balls(els.drawNumbers, []);
    balls(els.matchedNumbers, []);
  }

  if (els.regionSelect.options.length === 0) {
    renderRegions(state.regions);
  } else {
    renderPrizeMatrix();
  }

  els.historyTable.innerHTML = "";
  if (!state.history.length) {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="6">No draws processed yet.</td>`;
    els.historyTable.appendChild(row);
  } else {
    state.history.forEach((item) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.created_at}</td>
        <td>${item.region}</td>
        <td>${item.ticket_id.slice(0, 8)}</td>
        <td>${item.draw_numbers.join(", ")}</td>
        <td>${item.matches}</td>
        <td>${toCurrency(item.prize)}</td>
      `;
      els.historyTable.appendChild(row);
    });
  }
}

function renderMetrics(metrics) {
  currentMetrics = metrics;
  const keys = [
    ["bets_placed", "Bets Placed"],
    ["draws_processed", "Draws Processed"],
    ["wins_count", "Wins"],
    ["total_prize_paid", "Total Prize Paid"],
    ["errors", "Errors"],
    ["history_count", "History Entries"],
  ];

  els.metricsPanel.innerHTML = "";
  keys.forEach(([key, label]) => {
    const block = document.createElement("div");
    block.className = "metric";
    const value = key === "total_prize_paid" ? toCurrency(metrics[key] || 0) : String(metrics[key] || 0);
    block.innerHTML = `<span>${label}</span><strong>${value}</strong>`;
    els.metricsPanel.appendChild(block);
  });
}

function readBetNumbers() {
  return [els.n1, els.n2, els.n3, els.n4]
    .map((input) => Number(input.value))
    .filter((value) => Number.isFinite(value));
}

async function refresh() {
  try {
    const [state, metrics] = await Promise.all([
      request("/api/state"),
      request("/api/metrics"),
    ]);

    renderState(state);
    renderMetrics(metrics);
  } catch (error) {
    feedback(error.message, true);
  }
}

async function placeBet() {
  const numbers = readBetNumbers();
  const region = els.regionSelect.value;

  if (numbers.length !== 4) {
    feedback("You must provide exactly 4 valid numbers.", true);
    return;
  }

  try {
    await request("/api/bets/place", {
      method: "POST",
      body: JSON.stringify({ numbers, region }),
    });
    feedback("Bet placed successfully.");
    await refresh();
  } catch (error) {
    feedback(error.message, true);
  }
}

async function runDraw() {
  try {
    const payload = await request("/api/draw", { method: "POST" });
    feedback(`Draw processed. Prize: ${toCurrency(payload.result.prize)}.`);
    await refresh();
  } catch (error) {
    feedback(error.message, true);
  }
}

async function resetSession() {
  try {
    await request("/api/reset", { method: "POST" });
    feedback("Session reset completed.");
    await refresh();
  } catch (error) {
    feedback(error.message, true);
  }
}

els.placeBetBtn.addEventListener("click", placeBet);
els.runDrawBtn.addEventListener("click", runDraw);
els.resetBtn.addEventListener("click", resetSession);
els.refreshBtn.addEventListener("click", refresh);
els.regionSelect.addEventListener("change", renderPrizeMatrix);

refresh();
setInterval(refresh, 6000);
