const API_BASE = "http://127.0.0.1:5000";

const statusEl = document.getElementById("status");
const totalEventsEl = document.getElementById("totalEvents");
const totalAlertsEl = document.getElementById("totalAlerts");
const alertsListEl = document.getElementById("alertsList");
const refreshBtn = document.getElementById("refreshBtn");

async function checkStatus() {
  try {
    const res = await fetch(`${API_BASE}/api/status`);
    const data = await res.json();
    statusEl.textContent = `Backend online: ${data.service}`;
    statusEl.style.color = "#4caf50";
  } catch (err) {
    statusEl.textContent = "Backend offline — start the Flask server";
    statusEl.style.color = "#f44336";
  }
}

async function runScan() {
  alertsListEl.innerHTML = "<p>Scanning network...</p>";
  try {
    const res = await fetch(`${API_BASE}/api/alerts`);
    const data = await res.json();

    totalEventsEl.textContent = data.total_events_scanned;
    totalAlertsEl.textContent = data.alerts_found;

    if (data.alerts.length === 0) {
      alertsListEl.innerHTML = "<p>No suspicious activity detected.</p>";
      return;
    }

    alertsListEl.innerHTML = "";
    data.alerts.forEach(alert => {
      const div = document.createElement("div");
      div.className = `alert-item ${alert.priority}`;
      div.innerHTML = `
        <div class="alert-top">
          <span>${alert.priority} — ${alert.zone}</span>
          <span>${alert.device}</span>
        </div>
        <div class="alert-reasons">${alert.reasons.join(", ")}</div>
      `;
      alertsListEl.appendChild(div);
    });
  } catch (err) {
    alertsListEl.innerHTML = "<p>Could not reach backend. Is the Flask server running?</p>";
  }
}

refreshBtn.addEventListener("click", runScan);
checkStatus();
