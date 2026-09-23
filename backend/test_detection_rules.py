import unittest

from detection_rules import (
    BYTES_SENT_THRESHOLD,
    CONNECTION_ATTEMPT_THRESHOLD,
    FAILED_LOGIN_THRESHOLD,
    evaluate_event,
)


def make_event(zone="Guest_WiFi", **overrides):
    event = {
        "timestamp": 0,
        "zone": zone,
        "device": "test-device",
        "source_ip": "10.0.0.1",
        "bytes_sent": 1000,
        "failed_logins": 0,
        "connection_attempts": 1,
    }
    event.update(overrides)
    return event


class DetectionRuleTests(unittest.TestCase):
    def test_normal_event_has_no_alert(self):
        self.assertIsNone(evaluate_event(make_event()))

    def test_failed_login_threshold(self):
        alert = evaluate_event(make_event(failed_logins=FAILED_LOGIN_THRESHOLD))
        self.assertIsNotNone(alert)
        self.assertIn("failed login", alert["reasons"][0].lower())

    def test_large_transfer_threshold(self):
        alert = evaluate_event(make_event(bytes_sent=BYTES_SENT_THRESHOLD + 1))
        self.assertIsNotNone(alert)
        self.assertIn("data transfer", alert["reasons"][0].lower())

    def test_connection_attempt_threshold(self):
        alert = evaluate_event(
            make_event(connection_attempts=CONNECTION_ATTEMPT_THRESHOLD + 1)
        )
        self.assertIsNotNone(alert)
        self.assertIn("connection attempt", alert["reasons"][0].lower())

    def test_zone_weight_changes_score(self):
        guest = evaluate_event(make_event(zone="Guest_WiFi", failed_logins=5))
        pos = evaluate_event(make_event(zone="POS_Payment", failed_logins=5))
        self.assertGreater(pos["score"], guest["score"])

    def test_multiple_rules_are_combined(self):
        alert = evaluate_event(
            make_event(
                zone="Bridge_Adjacent_IT",
                failed_logins=FAILED_LOGIN_THRESHOLD,
                bytes_sent=BYTES_SENT_THRESHOLD + 1,
                connection_attempts=CONNECTION_ATTEMPT_THRESHOLD + 1,
            )
        )
        self.assertEqual(alert["score"], 40)
        self.assertEqual(alert["priority"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
