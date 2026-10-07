import unittest
from datetime import datetime, timedelta, timezone

from tools.detect_bruteforce import detect_bruteforce


def make_event(index: int, minutes_before: int, outcome: str = "failure") -> dict[str, object]:
    timestamp = datetime(2026, 10, 6, 15, 10, tzinfo=timezone.utc) - timedelta(
        minutes=minutes_before
    )
    return {
        "event_id": f"TEST-{index}",
        "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "source_ip": "203.0.113.77",
        "username": f"user{index % 3}",
        "outcome": outcome,
        "_parsed_timestamp": timestamp,
    }


class DetectBruteforceTests(unittest.TestCase):
    def test_alerts_when_threshold_is_reached_in_window(self) -> None:
        alerts = detect_bruteforce([make_event(i, 5 - i) for i in range(5)])

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["failed_attempts"], 5)
        self.assertEqual(alerts[0]["mitre_attack"]["id"], "T1110")

    def test_does_not_alert_below_threshold(self) -> None:
        alerts = detect_bruteforce([make_event(i, 4 - i) for i in range(4)])

        self.assertEqual(alerts, [])

    def test_does_not_combine_failures_outside_window(self) -> None:
        alerts = detect_bruteforce([make_event(i, i * 15) for i in range(5)])

        self.assertEqual(alerts, [])

    def test_successful_logins_do_not_count_as_failures(self) -> None:
        events = [make_event(i, 5 - i) for i in range(4)]
        events.append(make_event(5, 0, outcome="success"))

        self.assertEqual(detect_bruteforce(events), [])

    def test_rejects_invalid_threshold(self) -> None:
        with self.assertRaisesRegex(ValueError, "supérieur ou égal à 2"):
            detect_bruteforce([], threshold=1)


if __name__ == "__main__":
    unittest.main()
