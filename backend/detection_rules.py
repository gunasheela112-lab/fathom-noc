# Detection thresholds
FAILED_LOGIN_THRESHOLD = 5
BYTES_SENT_THRESHOLD = 300_000
CONNECTION_ATTEMPT_THRESHOLD = 30

# Zone risk weights - the same suspicious activity is scored differently by zone.
ZONE_RISK_WEIGHT = {
    "Guest_WiFi": 1,
    "Crew_Systems": 2,
    "POS_Payment": 4,
    "Bridge_Adjacent_IT": 5,
}


def evaluate_event(event):
    """Evaluate one simulated network event and return an alert when suspicious."""
    reasons = []
    severity_score = 0

    if event.get("failed_logins", 0) >= FAILED_LOGIN_THRESHOLD:
        reasons.append("High number of failed login attempts")
        severity_score += 3

    if event.get("bytes_sent", 0) > BYTES_SENT_THRESHOLD:
        reasons.append("Unusually large data transfer")
        severity_score += 3

    if event.get("connection_attempts", 0) > CONNECTION_ATTEMPT_THRESHOLD:
        reasons.append("High connection attempt rate (possible scan)")
        severity_score += 2

    if not reasons:
        return None

    zone = event.get("zone", "Unknown")
    zone_weight = ZONE_RISK_WEIGHT.get(zone, 1)
    final_score = severity_score * zone_weight

    if final_score >= 15:
        priority = "CRITICAL"
    elif final_score >= 8:
        priority = "HIGH"
    else:
        priority = "MEDIUM"

    return {
        "timestamp": event.get("timestamp"),
        "zone": zone,
        "device": event.get("device", "Unknown"),
        "source_ip": event.get("source_ip", "Unknown"),
        "reasons": reasons,
        "priority": priority,
        "score": final_score,
    }


def scan_events(events):
    """Evaluate a batch of events and return only events that triggered alerts."""
    return [alert for event in events if (alert := evaluate_event(event))]
