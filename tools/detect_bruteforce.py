#!/usr/bin/env python3
"""Détecte des échecs d'authentification répétés dans des journaux JSONL fictifs."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


def parse_timestamp(value: str, line_number: int) -> datetime:
    """Parse un timestamp ISO 8601 qui doit comporter une zone horaire."""
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"Ligne {line_number} : timestamp invalide.") from error
    if timestamp.tzinfo is None:
        raise ValueError(f"Ligne {line_number} : le timestamp doit inclure une zone horaire.")
    return timestamp


def load_events(path: Path) -> list[dict[str, Any]]:
    """Charge des objets JSONL et refuse explicitement les lignes invalides."""
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, raw_line in enumerate(stream, start=1):
            if not raw_line.strip():
                continue
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Ligne {line_number} : JSON invalide.") from error
            if not isinstance(event, dict):
                raise ValueError(f"Ligne {line_number} : chaque événement doit être un objet JSON.")

            missing = [key for key in ("timestamp", "source_ip", "outcome") if not event.get(key)]
            if missing:
                raise ValueError(
                    f"Ligne {line_number} : champ(s) obligatoire(s) absent(s) : {', '.join(missing)}."
                )

            event["_parsed_timestamp"] = parse_timestamp(str(event["timestamp"]), line_number)
            events.append(event)
    return events


def detect_bruteforce(
    events: list[dict[str, Any]], threshold: int = 5, window_minutes: int = 10
) -> list[dict[str, Any]]:
    """Retourne une alerte par IP au premier groupe atteignant le seuil dans la fenêtre."""
    if threshold < 2:
        raise ValueError("Le seuil doit être supérieur ou égal à 2.")
    if window_minutes < 1:
        raise ValueError("La fenêtre doit durer au moins une minute.")

    events_by_ip: dict[str, list[dict[str, Any]]] = defaultdict(list)
    failures_by_ip: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        source_ip = str(event["source_ip"])
        timestamp = event.get("_parsed_timestamp")
        if not isinstance(timestamp, datetime):
            timestamp = parse_timestamp(str(event["timestamp"]), 0)
        normalized = {**event, "_parsed_timestamp": timestamp}
        events_by_ip[source_ip].append(normalized)
        if str(event.get("outcome", "")).lower() != "failure":
            continue
        failures_by_ip[source_ip].append(normalized)

    window = timedelta(minutes=window_minutes)
    alerts: list[dict[str, Any]] = []
    for source_ip, failures in sorted(failures_by_ip.items()):
        failures.sort(key=lambda event: event["_parsed_timestamp"])
        left = 0
        for right, current in enumerate(failures):
            while (
                current["_parsed_timestamp"] - failures[left]["_parsed_timestamp"] > window
            ):
                left += 1
            if right - left + 1 < threshold:
                continue

            burst = failures[left : right + 1]
            last_failure = burst[-1]["_parsed_timestamp"]
            successful_logins = sorted(
                (
                    event
                    for event in events_by_ip[source_ip]
                    if str(event.get("outcome", "")).lower() == "success"
                ),
                key=lambda event: event["_parsed_timestamp"],
            )
            follow_up_success = next(
                (
                    event
                    for event in successful_logins
                    if last_failure
                    < event["_parsed_timestamp"]
                    <= last_failure + window
                ),
                None,
            )
            evidence_event_ids = [
                str(event.get("event_id", "inconnu")) for event in burst
            ]
            if follow_up_success:
                evidence_event_ids.append(
                    str(follow_up_success.get("event_id", "inconnu"))
                )
            alerts.append(
                {
                    "rule_id": "SOC-AUTH-001",
                    "title": "Échecs d'authentification répétés",
                    "severity": "high",
                    "source_ip": source_ip,
                    "failed_attempts": len(burst),
                    "distinct_usernames": len(
                        {str(event.get("username", "")) for event in burst if event.get("username")}
                    ),
                    "first_seen": burst[0]["timestamp"],
                    "last_seen": burst[-1]["timestamp"],
                    "success_after_failures": (
                        follow_up_success["timestamp"] if follow_up_success else None
                    ),
                    "success_username": (
                        follow_up_success.get("username") if follow_up_success else None
                    ),
                    "mitre_attack": {"id": "T1110", "name": "Brute Force"},
                    "status": "à investiguer",
                    "evidence_event_ids": evidence_event_ids,
                }
            )
            break
    return alerts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Détecte des rafales fictives d'échecs d'authentification dans un fichier JSONL."
    )
    parser.add_argument("input", type=Path, help="Chemin d'un fichier JSON Lines")
    parser.add_argument("--threshold", type=int, default=5, help="Nombre minimal d'échecs (défaut : 5)")
    parser.add_argument(
        "--window-minutes", type=int, default=10, help="Fenêtre glissante en minutes (défaut : 10)"
    )
    args = parser.parse_args()

    try:
        events = load_events(args.input)
        alerts = detect_bruteforce(events, args.threshold, args.window_minutes)
    except (OSError, ValueError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 2

    print(json.dumps(alerts, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
