import random
import time

# Ship network zones - each has different risk sensitivity
ZONES = ["Guest_WiFi", "Crew_Systems", "POS_Payment", "Bridge_Adjacent_IT"]

# Sample device pool per zone
DEVICES = {
    "Guest_WiFi": ["guest-laptop-01", "guest-phone-02", "guest-tablet-03"],
    "Crew_Systems": ["crew-pc-01", "crew-pc-02", "crew-terminal-03"],
    "POS_Payment": ["pos-terminal-01", "pos-terminal-02"],
    "Bridge_Adjacent_IT": ["nav-support-01", "comms-relay-02"]
}

def generate_traffic_event():
    """
    Generates one fake network traffic event, simulating
    what a real ship's network monitor would log.
    """
    zone = random.choice(ZONES)
    device = random.choice(DEVICES[zone])

    event = {
        "timestamp": time.time(),
        "zone": zone,
        "device": device,
        "bytes_sent": random.randint(100, 500000),
        "failed_logins": random.randint(0, 15),
        "connection_attempts": random.randint(1, 50),
        "source_ip": f"10.0.{random.randint(1,254)}.{random.randint(1,254)}"
    }
    return event

def generate_batch(count=20):
    """
    Generates a batch of fake events, simulating a snapshot
    of recent network activity across the ship.
    """
    return [generate_traffic_event() for _ in range(count)]
