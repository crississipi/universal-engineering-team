#!/usr/bin/env python3
"""Append a sanitized webhook ingress/security event as one JSONL record."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import uuid

SAFE_TOKEN_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
EVENT_TYPES = {"invalid_signature", "unparseable_payload"}
SIGNATURE_STATUSES = {"valid", "invalid", "missing", "not_checked"}


def validate_token(value: str, field: str) -> str:
    if not SAFE_TOKEN_RE.fullmatch(value):
        raise ValueError(f"{field} must contain only safe identifier characters (1-128 chars)")
    return value


def build_event(args) -> dict:
    if args.event_type not in EVENT_TYPES:
        raise ValueError(f"event_type must be one of: {', '.join(sorted(EVENT_TYPES))}")
    if args.signature_status not in SIGNATURE_STATUSES:
        raise ValueError(
            f"signature_status must be one of: {', '.join(sorted(SIGNATURE_STATUSES))}"
        )
    if args.payload_size < 0:
        raise ValueError("payload_size cannot be negative")

    event = {
        "schema_version": 1,
        "request_id": validate_token(args.request_id, "request_id") if args.request_id else str(uuid.uuid4()),
        "received_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": validate_token(args.source, "source") if args.source else None,
        "event_type": args.event_type,
        "reason_code": validate_token(args.reason_code, "reason_code"),
        "signature_status": args.signature_status,
        "payload_size_bytes": args.payload_size,
        "correlation_id": validate_token(args.correlation_id, "correlation_id") if args.correlation_id else None,
    }
    return event


def append_event(output_path: Path, event: dict):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    descriptor = os.open(output_path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=True, separators=(",", ":")) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        # fdopen owns the descriptor after it succeeds.
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Append one sanitized ingress/security event to a JSON Lines log."
    )
    parser.add_argument("--output", required=True, help="Restricted JSONL log destination.")
    parser.add_argument("--event-type", required=True, choices=sorted(EVENT_TYPES))
    parser.add_argument("--reason-code", required=True)
    parser.add_argument("--signature-status", choices=sorted(SIGNATURE_STATUSES), default="not_checked")
    parser.add_argument("--payload-size", type=int, default=0)
    parser.add_argument("--request-id")
    parser.add_argument("--source", help="Trusted integration identifier, not payload-derived.")
    parser.add_argument("--correlation-id", help="Safe correlation token, not payload-derived.")
    args = parser.parse_args(argv)

    try:
        event = build_event(args)
        append_event(Path(args.output), event)
    except (OSError, ValueError) as exc:
        print(f"ERROR: ingress security event was not persisted: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"recorded": True, "request_id": event["request_id"], "event_type": event["event_type"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
