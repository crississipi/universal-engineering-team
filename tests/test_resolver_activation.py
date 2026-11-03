"""Regression tests for resolver alignment with canonical activation rules."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "SKILLS-RESOLVER.md"
ACTIVATION_RULES = ROOT / "docs/team/role-activation-rules.md"


class ResolverActivationAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resolver = RESOLVER.read_text(encoding="utf-8")
        cls.activation = ACTIVATION_RULES.read_text(encoding="utf-8")

    def test_resolver_uses_canonical_activation_rules(self):
        reference = "docs/team/role-activation-rules.md"
        self.assertIn(reference, self.resolver)

    def test_qa_is_not_a_universal_activation_requirement(self):
        self.assertIn("Do not activate QA automatically for every change", self.resolver)
        self.assertIn("QA inactivity never waives required verification", self.resolver)
        self.assertIn("May remain inactive when:", self.activation)
        self.assertIn("QA Manager", self.activation)

    def test_technical_writer_is_not_a_universal_activation_requirement(self):
        self.assertIn(
            "Do not activate this role automatically for every change",
            self.resolver,
        )
        self.assertIn(
            "Specialist inactivity never waives an explicit documentation deliverable",
            self.resolver,
        )
        self.assertIn("May remain inactive when:", self.activation)
        self.assertIn("Technical Writer/Knowledge Engineer", self.activation)

    def test_task_examples_apply_specialist_triggers(self):
        self.assertIn("when its verification triggers apply", self.resolver)
        self.assertIn("only if a documentation/knowledge trigger applies", self.resolver)
        self.assertIn("Do not activate every role by default", self.resolver)


if __name__ == "__main__":
    unittest.main()
