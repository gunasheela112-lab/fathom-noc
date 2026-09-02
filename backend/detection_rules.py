# Zone risk weights - same suspicious activity is scored differently by zone
ZONE_RISK_WEIGHT = {
    "Guest_WiFi": 1,
    "Crew_Systems": 2,
    "POS_Payment": 4,
    "Bridge_Adjacent_IT": 5
}

def evaluate_event(event):
    """
    Looks at one network event and decides if it's suspicious.
    Returns an alert dict if something looks wrong, otherwise None.
    """
    reasons = []
    severity_score = 0

    # Rule 1: Too many failed logins = possible brute-force attack
    if event["failed_logins"] >= 5:
        reasons.append("High number of failed login attempts")
        severity_score += 3

    # Rule 2: Unusually high data sent = possible data exfiltration
    if event["bytes_sent"] > 300000:
        reasons.append("Unusually large data transfer")
        severity_score += 3

    # Rule 3: Too many connection attempts = possible port scan
    if event["connection_attempts"] > 30:
        reasons.append("High connection attempt rate (possible scan)")
        severity_score += 2

    if not reasons:
        return None  # nothing suspicious

    # Apply zone risk weight - same issue is worse in sensitive zones
    zone_weight = ZONE_RISK_WEIGHT.get(event["zone"], 1)
    final_score = severity_score * zone_weight

    if final_score >= 15:
        priority = "CRITICAL"
    elif final_score >= 8:
        priority = "HIGH"
    else:
        priority = "MEDIUM"

    alert = {
        "timestamp": event["timestamp"],
        "zone": event["zone"],
        "device": event["device"],
        "source_ip": event["source_ip"],
        "reasons": reasons,
        "priority": priority,
        "score": final_score
    }
    return alert


def scan_events(events):
    """
    Runs evaluate_event on a whole batch of events.
    Returns only the ones that triggered an alert.
    """
    alerts = []
    for event in events:
        alert = evaluate_event(event)
        if alert:
            alerts.append(alert)
    return alerts
