from flask import Flask, jsonify
from datetime import datetime, timezone
import os
from flask_cors import CORS
from mock_data import generate_batch
from detection_rules import scan_events

app = Flask(__name__)
CORS(app)

BATCH_SIZE = 30
latest_scan = None


def run_scan():
    """Generate and evaluate one coherent simulated network scan."""
    global latest_scan
    events = generate_batch(BATCH_SIZE)
    alerts = scan_events(events)
    latest_scan = {
        "total_events_scanned": len(events),
        "alerts_found": len(alerts),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "events": events,
        "alerts": alerts,
    }
    return latest_scan


@app.route("/api/events", methods=["GET"])
def get_events():
    """Return events from the latest scan, generating one if needed."""
    if latest_scan is None:
        run_scan()
    return jsonify(latest_scan["events"])


@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    """Return the latest scan results."""
    if latest_scan is None:
        run_scan()
    return jsonify({
        "total_events_scanned": latest_scan["total_events_scanned"],
        "alerts_found": latest_scan["alerts_found"],
        "generated_at": latest_scan["generated_at"],
        "alerts": latest_scan["alerts"],
    })


@app.route("/api/scan", methods=["POST"])
def create_scan():
    """Generate a new simulated scan and return its results."""
    scan = run_scan()
    return jsonify({
        "total_events_scanned": scan["total_events_scanned"],
        "alerts_found": scan["alerts_found"],
        "generated_at": scan["generated_at"],
        "alerts": scan["alerts"],
    })


@app.route("/api/status", methods=["GET"])
def get_status():
    """Simple health check endpoint."""
    return jsonify({"status": "online", "service": "Fathom NOC Backend"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
