#!/usr/bin/env python3
"""Validate skill metadata, expected roles, role index, and local Markdown links."""

from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML is missing. Run: "
        "python -m pip install -r requirements-dev.txt"
    )
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
POLICY_PATH = ROOT / ".skill-policy.yml"
ROLES_PATH = ROOT / "docs/team/expected-roles.yml"

errors = []
warnings = []


def load_yaml(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    except (OSError, UnicodeError) as exc:
        errors.append(
            f"Cannot read {path.relative_to(ROOT)}: {exc}"
        )
    except yaml.YAMLError as exc:
        errors.append(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}")
    return None


def parse_skill(path):
    """Parse one skill's YAML frontmatter without leaking parser exceptions."""
    relative_path = path.relative_to(ROOT).as_posix()

    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{relative_path}: cannot read skill file: {exc}")
        return None

    lines = content.splitlines()

    if not lines or lines[0].strip() != "---":
        errors.append(
            f"{relative_path}: missing YAML frontmatter opener"
        )
        return None

    closing_index = next(
        (
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        ),
        None,
    )

    if closing_index is None:
        errors.append(
            f"{relative_path}: missing YAML frontmatter closer"
        )
        return None

    frontmatter = "\n".join(lines[1:closing_index])

    try:
        metadata = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        problem = getattr(exc, "problem", None) or str(exc)
        errors.append(
            f"{relative_path}: invalid YAML frontmatter: {problem}"
        )
        return None

    if not isinstance(metadata, dict):
        errors.append(
            f"{relative_path}: frontmatter must be a YAML mapping"
        )
        return None

    for field in ("name", "description"):
        value = metadata.get(field)

        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"{relative_path}: missing or invalid {field!r}"
            )

    return metadata


def validate_markdown_links():
    link_re = re.compile(r"!?[[^\]]*\]\(([^)]+)\)")
    fenced_code_re = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)

    for markdown_file in ROOT.rglob("*.md"):
        if any(
            part in {".git", ".venv", "node_modules", "__pycache__"}
            for part in markdown_file.parts
        ):
            continue

        content = markdown_file.read_text(
            encoding="utf-8",
            errors="replace",
        )

        content = fenced_code_re.sub("", content)

        for raw in link_re.findall(content):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")

            if not target or target.startswith(
                ("http://", "https://", "mailto:", "#", "data:")
            ):
                continue

            target = target.split("#", 1)[0].split("?", 1)[0]

            if not target:
                continue

            candidate = (markdown_file.parent / target).resolve()

            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"{markdown_file.relative_to(ROOT)}: "
                    f"link escapes repository: {raw}"
                )
                continue

            if not candidate.exists():
                errors.append(
                    f"{markdown_file.relative_to(ROOT)}: "
                    f"broken local link: {raw}"
                )


def main():
    policy = load_yaml(POLICY_PATH)
    role_data = load_yaml(ROLES_PATH)

    if not isinstance(policy, dict):
        errors.append(".skill-policy.yml must contain a YAML mapping")
        policy = {}

    if not isinstance(role_data, dict):
        errors.append("expected-roles.yml must contain a YAML mapping")
        role_data = {}

    skill_policy = policy.get("skill", {})
    inventory_policy = policy.get("inventory", {})

    if not isinstance(skill_policy, dict):
        errors.append("Policy skill section must be a mapping")
        skill_policy = {}

    if not isinstance(inventory_policy, dict):
        errors.append("Policy inventory section must be a mapping")
        inventory_policy = {}

    required_fields = skill_policy.get(
        "expected_frontmatter_fields",
        ["name", "description"],
    )

    max_words = skill_policy.get("description_max_words", 18)
    expected_count = inventory_policy.get("expected_skill_count", 17)

    if (
        not isinstance(required_fields, list)
        or any(not isinstance(item, str) for item in required_fields)
    ):
        errors.append("expected_frontmatter_fields must be a list of strings")
        required_fields = ["name", "description"]

    if (
        not isinstance(max_words, int)
        or isinstance(max_words, bool)
        or max_words < 1
    ):
        errors.append("description_max_words must be a positive integer")
        max_words = 18

    if (
        not isinstance(expected_count, int)
        or isinstance(expected_count, bool)
        or expected_count < 1
    ):
        errors.append("expected_skill_count must be a positive integer")
        expected_count = 17

    expected_roles = role_data.get("roles", [])

    if (
        not isinstance(expected_roles, list)
        or not expected_roles
        or any(
            not isinstance(role, str)
            or not re.fullmatch(r"[a-z][a-z0-9-]*", role)
            for role in expected_roles
        )
    ):
        errors.append("expected-roles.yml must contain valid role slugs")
        expected_roles = []

    if len(expected_roles) != len(set(expected_roles)):
        errors.append("expected-roles.yml contains duplicate role slugs")

    if expected_roles and len(expected_roles) != expected_count:
        errors.append(
            "Policy expected_skill_count does not match expected-roles.yml"
        )

    files = sorted(SKILLS.glob("*/SKILL.md"))

    if not files:
        errors.append("No skills found under skills/*/SKILL.md")

    actual_roles = [path.parent.name for path in files]

    for missing in sorted(set(expected_roles) - set(actual_roles)):
        errors.append(f"Missing expected role skill: {missing}")

    for unexpected in sorted(set(actual_roles) - set(expected_roles)):
        errors.append(f"Unexpected role skill folder: {unexpected}")

    if len(files) != expected_count:
        errors.append(
            f"Expected {expected_count} skill files; found {len(files)}"
        )

    names = {}

    for path in files:
        metadata = parse_skill(path)

        if not metadata:
            continue

        for field in required_fields:
            value = metadata.get(field)

            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"{path.relative_to(ROOT)}: required field "
                    f"{field!r} is missing or invalid"
                )

        name = metadata.get("name")
        description = metadata.get("description")

        if isinstance(name, str):
            if name != path.parent.name:
                errors.append(
                    f"{path.relative_to(ROOT)}: name {name!r} "
                    f"does not match folder {path.parent.name!r}"
                )

            if name in names:
                errors.append(
                    f"Duplicate skill name {name!r}: "
                    f"{names[name]} and {path.relative_to(ROOT)}"
                )

            names[name] = path.relative_to(ROOT).as_posix()

        if isinstance(description, str):
            word_count = len(description.split())

            if word_count > max_words:
                errors.append(
                    f"{path.relative_to(ROOT)}: description has "
                    f"{word_count} words; maximum is {max_words}"
                )

    index_path = ROOT / "ROLE-INDEX.md"

    if not index_path.exists():
        errors.append("Missing ROLE-INDEX.md")
    else:
        index_content = index_path.read_text(encoding="utf-8")
        links = set(
            re.findall(
                r"\]\((skills/[^)]+/SKILL\.md)\)",
                index_content,
            )
        )

        expected_links = {
            f"skills/{role}/SKILL.md" for role in expected_roles
        }

        for missing in sorted(expected_links - links):
            errors.append(f"ROLE-INDEX.md: missing skill link {missing}")

        for unexpected in sorted(links - expected_links):
            errors.append(f"ROLE-INDEX.md: invalid skill link {unexpected}")

    validate_markdown_links()

    for warning in warnings:
        print(f"WARNING: {warning}")

    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(
            f"\nValidation failed: {len(errors)} error(s), "
            f"{len(warnings)} warning(s)."
        )
        return 1

    print(
        f"Validation passed: {len(files)} skills, expected roles, "
        "frontmatter policy, role index, and local Markdown links checked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
