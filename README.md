# Fathom NOC 🌊

A Network Operations Center dashboard with built-in intrusion detection, purpose-built for the bandwidth-constrained, intermittently-connected reality of maritime IT — not the always-on office network most security tools assume.

## The Problem

Most network security dashboards are designed for offices with unlimited bandwidth and stable connections. A cruise ship's network doesn't work that way: satellite internet is slow, expensive per MB, and drops without warning. A security system that streams every alert in real time or assumes constant connectivity simply doesn't survive at sea.

Fathom NOC is designed around that constraint from the ground up.

## What It Does

- **Simulates a ship's network** across four zones — Guest WiFi, Crew Systems, POS/Payment, and Bridge-Adjacent IT — each with its own risk profile
- **Detects suspicious activity** using rule-based checks: failed login spikes, abnormal data transfers, and high connection-attempt rates (patterns consistent with brute-force attempts, data exfiltration, and port scanning)
- **Applies zone-based risk scoring** — the same suspicious event is scored far more critically on a POS terminal than on Guest WiFi, mirroring how a real ship IT officer would prioritize
- **Displays live alerts** on a dashboard, color-coded by severity (Critical / High / Medium)

## Why This Matters

An IT officer on a ship can't treat every alert equally, and can't assume the network is always reachable. This project models both realities: prioritization under constraint, and resilience when things go offline — the actual operational problem, not just a detection algorithm.

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS
- **Frontend:** HTML, CSS, JavaScript (vanilla, no framework — kept lightweight intentionally)
- **Data:** Simulated network traffic (mock data generator, since real ship network access isn't available for a student project)

## How It Works

1. `mock_data.py` generates simulated network events (device, zone, data sent, failed logins, connection attempts)
2. `detection_rules.py` scans each event against threat rules, then weights the result by zone risk
3. `app.py` exposes this via a Flask API (`/api/alerts`, `/api/events`, `/api/status`)
4. The frontend dashboard calls this API and displays alerts in real time

## Running Locally

```bash
cd backend
pip install -r requirements.txt
python app.py
