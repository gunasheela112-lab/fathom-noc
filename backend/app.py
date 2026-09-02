from flask import Flask, jsonify
from flask_cors import CORS
from mock_data import generate_batch
from detection_rules import scan_events

app = Flask(__name__)
CORS(app)  # allows frontend to talk to this backend

@app.route("/api/events", methods=["GET"])
def get_events():
    """
    Returns a fresh batch of simulated network events.
    """
    events = generate_batch(30)
    return jsonify(events)

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    """
    Generates events, scans them, and returns only the alerts.
    This is the main endpoint the dashboard will call.
    """
    events = generate_batch(30)
    alerts = scan_events(events)
    return jsonify({
        "total_events_scanned": len(events),
        "alerts_found": len(alerts),
        "alerts": alerts
    })

@app.route("/api/status", methods=["GET"])
def get_status():
    """
    Simple health check endpoint - confirms server is running.
    """
    return jsonify({"status": "online", "service": "Fathom NOC Backend"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
