"""Tests for the sanitized webhook ingress/security logger."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_script():
    spec = importlib.util.spec_from_file_location(
        "log_ingress_security_event", SCRIPTS / "log-ingress-security-event.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


logger = load_script()


class IngressSecurityLoggerTests(unittest.TestCase):
    def args(self, **overrides):
        values = {
            "event_type": "invalid_signature",
            "signature_status": "invalid",
            "reason_code": "signature_mismatch",
            "payload_size": 128,
            "request_id": None,
            "source": "merchantcloud",
            "correlation_id": "corr-123"
        }
        values.update(overrides)
        return type("Args", (), values)()

    def test_event_contains_only_sanitized_metadata(self):
        event = logger.build_event(self.args())
        self.assertEqual(event["event_type"], "invalid_signature")
        self.assertEqual(event["signature_status"], "invalid")
        self.assertEqual(event["payload_size_bytes"], 128)
        self.assertNotIn("raw_body", event)
        self.assertNotIn("signature", event)
        self.assertNotIn("authorization", event)

    def test_unparseable_payload_event_is_supported(self):
        event = logger.build_event(self.args(
            event_type="unparseable_payload",
            signature_status="valid",
            reason_code="invalid_json"
        ))
        self.assertEqual(event["event_type"], "unparseable_payload")

    def test_payload_derived_unsafe_source_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "source"):
            logger.build_event(self.args(source="merchantcloud\nsecret"))

    def test_negative_payload_size_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            logger.build_event(self.args(payload_size=-1))

    def test_event_is_appended_as_jsonl(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            path = Path(temp) / "security" / "events.jsonl"
            logger.append_event(path, logger.build_event(self.args()))
            logger.append_event(path, logger.build_event(self.args(event_type="unparseable_payload")))
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["event_type"], "invalid_signature")
            self.assertEqual(records[1]["event_type"], "unparseable_payload")


if __name__ == "__main__":
    unittest.main()
