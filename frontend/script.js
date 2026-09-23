const API_BASE = window.FATHOM_API_BASE || "https://fathom-noc.onrender.com";

const statusEl = document.getElementById("status");
const totalEventsEl = document.getElementById("totalEvents");
const totalAlertsEl = document.getElementById("totalAlerts");
const criticalAlertsEl = document.getElementById("criticalAlerts");
const highAlertsEl = document.getElementById("highAlerts");
const mediumAlertsEl = document.getElementById("mediumAlerts");
const alertsListEl = document.getElementById("alertsList");
const refreshBtn = document.getElementById("refreshBtn");

function createTextElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.textContent = text;
  return element;
}

function formatTimestamp(timestamp) {
  if (!timestamp) return "Unknown time";
  const date = new Date(timestamp * 1000);
  return Number.isNaN(date.getTime()) ? "Unknown time" : date.toLocaleTimeString();
}

function renderAlerts(alerts) {
  alertsListEl.replaceChildren();

  if (alerts.length === 0) {
    alertsListEl.appendChild(createTextElement("p", null, "No suspicious activity detected."));
    return;
  }

  alerts.forEach(alert => {
    const item = createTextElement("article", "alert-item " + alert.priority);
    const top = createTextElement("div", "alert-top");
    top.append(
      createTextElement("span", null, alert.priority + " — " + alert.zone),
      createTextElement("span", "alert-score", "Score: " + alert.score)
    );

    const details = createTextElement("div", "alert-details");
    details.append(
      createTextElement("span", null, "Device: " + alert.device),
      createTextElement("span", null, "Source: " + alert.source_ip),
      createTextElement("span", null, formatTimestamp(alert.timestamp))
    );

    const reasons = createTextElement("div", "alert-reasons", alert.reasons.join(", "));
    item.append(top, details, reasons);
    alertsListEl.appendChild(item);
  });
}

async function fetchJson(path, options = {}) {
  const res = await fetch(API_BASE + path, options);
  if (!res.ok) throw new Error("HTTP " + res.status);
  return res.json();
}

async function checkStatus() {
  try {
    const data = await fetchJson("/api/status");
    statusEl.textContent = "Backend online: " + data.service;
    statusEl.className = "online";
  } catch (err) {
    statusEl.textContent = "Backend offline — start the Flask server";
    statusEl.className = "offline";
  }
}

async function runScan() {
  refreshBtn.disabled = true;
  refreshBtn.textContent = "Scanning...";
  alertsListEl.replaceChildren(createTextElement("p", null, "Scanning network..."));

  try {
    const data = await fetchJson("/api/scan", { method: "POST" });
    totalEventsEl.textContent = data.total_events_scanned;
    totalAlertsEl.textContent = data.alerts_found;

    const counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0 };
    data.alerts.forEach(alert => {
      if (counts[alert.priority] !== undefined) counts[alert.priority]++;
    });

    criticalAlertsEl.textContent = counts.CRITICAL;
    highAlertsEl.textContent = counts.HIGH;
    mediumAlertsEl.textContent = counts.MEDIUM;

    renderAlerts(data.alerts);
  } catch (err) {
    alertsListEl.replaceChildren(
      createTextElement("p", "error", "Could not reach backend. Check the server and try again.")
    );
  } finally {
    refreshBtn.disabled = false;
    refreshBtn.textContent = "Run New Scan";
  }
}

refreshBtn.addEventListener("click", runScan);
checkStatus();
