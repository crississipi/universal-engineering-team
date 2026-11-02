"""Shared helpers for repository governance validators."""

from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ROLE_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
REQUIREMENT_ID_RE = re.compile(r"^REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*$")


def load_yaml(path: Path):
    try:
        import yaml
    except ImportError:
        print(
            "ERROR: PyYAML is missing. Run: "
            "python -m pip install -r requirements-dev.txt"
        )
        sys.exit(2)

    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing required file: {path.relative_to(ROOT)}")
    except yaml.YAMLError as exc:
        raise ValueError(
            f"Invalid YAML in {path.relative_to(ROOT)}: {exc}"
        ) from exc


def expected_roles():
    data = load_yaml(ROOT / "docs/team/expected-roles.yml")

    if not isinstance(data, dict) or not isinstance(data.get("roles"), list):
        raise ValueError("expected-roles.yml must contain a roles list")

    roles = data["roles"]

    if not roles or any(
        not isinstance(role, str) or not ROLE_SLUG_RE.fullmatch(role)
        for role in roles
    ):
        raise ValueError("Expected roles must be non-empty safe role slugs")

    if len(roles) != len(set(roles)):
        raise ValueError("expected-roles.yml contains duplicate role slugs")

    return roles


def safe_repo_path(raw_path, required_prefix=None):
    """Resolve a safe repository-relative POSIX path."""
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError("Path must be a non-empty string")

    value = raw_path.strip()

    # Reject Windows separators/drives as well as POSIX traversal.
    if "\\" in value or ":" in value:
        raise ValueError(f"Path must use safe repository-relative POSIX syntax: {value}")

    path = PurePosixPath(value)

    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ValueError(f"Unsafe repository-relative path: {value}")

    resolved = (ROOT / Path(*path.parts)).resolve()

    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes repository: {value}") from exc

    if required_prefix:
        prefix = Path(required_prefix).resolve()
        try:
            resolved.relative_to(prefix)
        except ValueError as exc:
            raise ValueError(
                f"Path must be inside {required_prefix}: {value}"
            ) from exc

    return resolved


def requirement_id(value):
    return isinstance(value, str) and bool(REQUIREMENT_ID_RE.fullmatch(value))


def report(errors, warnings, label):
    for warning in warnings:
        print(f"WARNING: {warning}")

    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(
            f"\n{label} failed: {len(errors)} error(s), "
            f"{len(warnings)} warning(s)."
        )
        return 1

    print(
        f"\n{label} passed: {len(warnings)} warning(s)."
    )
    return 0
