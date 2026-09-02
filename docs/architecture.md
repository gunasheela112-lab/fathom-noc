# Fathom NOC — Architecture

## Overview

Fathom NOC follows a simple three-layer design: data generation, detection logic, and presentation. Each layer is a separate file so the logic stays easy to read, test, and extend.

## Layer 1: Data Layer — mock_data.py

Simulates network traffic across four ship zones (Guest WiFi, Crew Systems, POS/Payment, Bridge-Adjacent IT). Each event includes device, zone, bytes sent, failed logins, and connection attempts — the same fields a real network monitoring tool would log.

This layer exists because real ship network access isn't available for a student project, but the shape of the data mirrors what an actual maritime monitoring system would produce.

## Layer 2: Detection Layer — detection_rules.py

Applies three threat-detection rules to each event:
- High failed login count → possible brute-force attempt
- Abnormally large data transfer → possible data exfiltration
- High connection attempt rate → possible port scan

Each triggered rule adds to a severity score. That score is then multiplied by a zone risk weight — the core design decision of this project. A suspicious event on Guest WiFi and the identical event on the POS/Payment system are not equally dangerous, so they shouldn't be treated equally. This mirrors real-world triage: limited attention should go to the highest-stakes systems first.

## Layer 3: API Layer — app.py

A lightweight Flask server exposing three endpoints:
- /api/status — health check, confirms the backend is running
- /api/events — raw simulated traffic (for debugging/inspection)
- /api/alerts — the main endpoint; generates events, scans them, and returns only what's flagged

Kept intentionally simple (no database, no auth) since the goal is demonstrating detection and prioritization logic clearly, not building production infrastructure.

## Layer 4: Presentation Layer — frontend/

A vanilla HTML/CSS/JS dashboard (no framework, kept lightweight) that calls /api/alerts and renders results, color-coded by priority (Critical / High / Medium). Styled as a dark control-room interface to match the NOC concept.

## Design Decisions Worth Noting

- Zone-based risk weighting instead of flat detection — the single biggest differentiator from typical student IDS projects
- No ML model — deliberate choice. Rule-based detection is transparent, explainable, and appropriate for this scope; ML would add complexity without adding real value here
- Separation of concerns — data generation, detection logic, and API are in separate files, making each piece independently testable and easy to extend later (e.g., swapping mock data for a real feed)

## Future Extensions

See the Roadmap section in the main README for planned additions (offline-first mode, bandwidth-aware alert batching, cost simulation).
