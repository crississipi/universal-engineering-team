#!/usr/bin/env python3
"""Generate a reproducible skill inventory from a clean Git checkout."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
import sys

from validation_common import ROOT, expected_roles, load_yaml

OUTPUT = ROOT / "tests/baseline/inventory.json"


def git_output(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Git command failed: git {' '.join(args)}\n{result.stderr.strip()}"
        )

    return result.stdout.strip()


def main():
    try:
        status = git_output("status", "--porcelain", "--untracked-files=all")

        if status:
            raise RuntimeError(
                "Working tree is not clean. Commit or remove all changes "
                "before generating the inventory."
            )

        commit = git_output("rev-parse", "HEAD")

        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise RuntimeError(
                f"Expected a full 40-character Git SHA; received: {commit!r}"
            )

        policy = load_yaml(ROOT / ".skill-policy.yml")
        roles = expected_roles()

        expected_count = policy.get("inventory", {}).get("expected_skill_count")

        if not isinstance(expected_count, int) or isinstance(expected_count, bool):
            raise RuntimeError("Policy expected_skill_count must be an integer")

        if expected_count != len(roles):
            raise RuntimeError(
                "Policy expected_skill_count does not match expected-roles.yml"
            )

        skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
        actual_slugs = [path.parent.name for path in skill_files]

        if set(actual_slugs) != set(roles):
            raise RuntimeError(
                "Skill folders do not match docs/team/expected-roles.yml"
            )

        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError(
                "PyYAML is required. Install requirements-dev.txt."
            ) from exc

        skill_records = []

        for path in skill_files:
            content = path.read_text(encoding="utf-8")

            if not content.startswith("---\n"):
                raise RuntimeError(f"Missing frontmatter: {path.relative_to(ROOT)}")

            end = content.find("\n---", 4)

            if end < 0:
                raise RuntimeError(
                    f"Missing frontmatter closer: {path.relative_to(ROOT)}"
                )

            metadata = yaml.safe_load(content[4:end])

            if not isinstance(metadata, dict):
                raise RuntimeError(
                    f"Invalid frontmatter: {path.relative_to(ROOT)}"
                )

            name = metadata.get("name")
            description = metadata.get("description")

            if name != path.parent.name:
                raise RuntimeError(
                    f"Skill name/folder mismatch: {path.relative_to(ROOT)}"
                )

            if not isinstance(description, str) or not description.strip():
                raise RuntimeError(
                    f"Missing description: {path.relative_to(ROOT)}"
                )

            skill_records.append(
                {
                    "slug": path.parent.name,
                    "name": name,
                    "description_words": len(description.split()),
                    "bytes": len(content.encode("utf-8")),
                    "sha256": sha256(content.encode("utf-8")).hexdigest(),
                }
            )

        try:
            import tiktoken

            encoder = tiktoken.get_encoding("cl100k_base")
            token_method = "tiktoken-cl100k_base"
            total_tokens = sum(
                len(encoder.encode(path.read_text(encoding="utf-8")))
                for path in skill_files
            )
        except ImportError:
            token_method = "not-measured"
            total_tokens = None

        inventory = {
            "schema_version": 1,
            "commit": commit,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "role_count": len(skill_records),
            "token_method": token_method,
            "total_tokens": total_tokens,
            "skills": skill_records,
        }

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(
            json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        print(f"Inventory written: {OUTPUT.relative_to(ROOT)}")
        print(f"Commit: {commit}")
        print(f"Roles: {len(skill_records)}")
        print(f"Token method: {token_method}")

    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())