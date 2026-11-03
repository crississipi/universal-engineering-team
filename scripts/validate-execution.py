#!/usr/bin/env python3
"""Run the complete deterministic validation stack for one execution."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from validation_common import ROOT


RECORD_FILES = {
    "execution.yml": ("execution", "schemas/executions/execution.schema.json"),
    "work-items.yml": ("work_items", "schemas/executions/work-items.schema.json"),
    "role-activations.yml": ("role_activations", "schemas/executions/role-activations.schema.json"),
    "dependencies.yml": ("dependencies", "schemas/executions/dependencies.schema.json"),
    "handoff-executions.yml": ("handoff_executions", "schemas/executions/handoff-executions.schema.json"),
    "decisions.yml": ("decisions", "schemas/executions/decisions.schema.json"),
    "evidence.yml": ("evidence", "schemas/executions/evidence.schema.json"),
    "blockers.yml": ("blockers", "schemas/executions/blockers.schema.json"),
    "replans.yml": ("replans", "schemas/executions/replans.schema.json"),
    "closure.yml": ("closure", "schemas/executions/closure.schema.json"),
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "found an unhashable mapping key", key_node.start_mark,
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"found duplicate key {key!r}", key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def load_yaml_document(path: Path):
    """Load one YAML document while rejecting duplicate keys."""
    with path.open("r", encoding="utf-8") as stream:
        return yaml.load(stream, Loader=UniqueKeyLoader)


def load_schema_catalog(root: Path = ROOT):
    """Load and meta-validate all execution schemas and local references."""
    schema_paths = sorted((root / "schemas/executions").rglob("*.schema.json"))
    required_paths = {
        *[schema_path for _, schema_path in RECORD_FILES.values()],
        "schemas/executions/definitions/common-values.schema.json",
        "schemas/executions/definitions/identifiers.schema.json",
        "schemas/executions/definitions/timestamps.schema.json",
    }
    discovered_paths = {path.relative_to(root).as_posix() for path in schema_paths}
    missing_paths = sorted(required_paths - discovered_paths)
    if missing_paths:
        raise ValueError("Missing required execution schemas: " + ", ".join(missing_paths))

    schemas = {}
    resources = []

    for path in schema_paths:
        relative = path.relative_to(root).as_posix()
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot load schema {relative}: {exc}") from exc

        if not isinstance(schema, dict):
            raise ValueError(f"{relative} must contain a JSON object schema")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError(f"{relative} must declare JSON Schema Draft 2020-12")
        if not isinstance(schema.get("$id"), str) or not schema["$id"]:
            raise ValueError(f"{relative} must declare a non-empty $id")

        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            raise ValueError(f"Invalid JSON Schema {relative}: {exc}") from exc

        schemas[relative] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))

    registry = Registry().with_resources(resources)

    def iter_references(value):
        if isinstance(value, dict):
            reference = value.get("$ref")
            if isinstance(reference, str):
                yield reference
            for child in value.values():
                yield from iter_references(child)
        elif isinstance(value, list):
            for child in value:
                yield from iter_references(child)

    for relative, schema in schemas.items():
        resolver = registry.resolver(base_uri=schema["$id"])
        for reference in iter_references(schema):
            try:
                resolver.lookup(reference)
            except Exception as exc:
                raise ValueError(
                    f"Unresolved schema reference in {relative}: {reference} ({exc})"
                ) from exc

    for filename, (_, schema_path) in RECORD_FILES.items():
        if schema_path not in schemas:
            raise ValueError(f"Missing schema for {filename}: {schema_path}")

    return {
        filename: (wrapper, schemas[schema_path])
        for filename, (wrapper, schema_path) in RECORD_FILES.items()
    }, registry


def parse_execution_documents(directory: Path):
    records = {}
    errors = []
    for filename, (wrapper, _) in RECORD_FILES.items():
        path = directory / filename
        if not path.is_file():
            errors.append(f"[EXV002] Required execution record file is missing: {path.relative_to(ROOT)}")
            continue
        try:
            value = load_yaml_document(path)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"[EXV003] Could not parse {path.relative_to(ROOT)}: {exc}")
            continue
        if not isinstance(value, dict) or set(value) != {wrapper}:
            errors.append(
                f"[EXV004] {path.relative_to(ROOT)} must contain only the top-level {wrapper!r} key"
            )
            continue
        records[filename] = value
    return records, errors


def validate_documents(directory: Path, records, schema_catalog, registry):
    errors = []
    for filename, (wrapper, schema) in schema_catalog.items():
        if filename not in records:
            continue
        validator = Draft202012Validator(schema, registry=registry)
        instance = records[filename]
        for error in sorted(
            validator.iter_errors(instance),
            key=lambda item: (list(map(str, item.absolute_path)), item.message),
        ):
            location = ".".join(str(part) for part in error.absolute_path) or "<document>"
            errors.append(
                f"[EXV005] {filename}:{location}: {error.message}"
            )
    return errors


def load_existing_validator(filename: str, module_name: str):
    path = ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_execution


def run_validator(label: str, validator, directory: Path):
    output = io.StringIO()
    try:
        with redirect_stdout(output):
            exit_code = validator(directory)
    except Exception as exc:
        return [f"[EXV090] {label} validator raised {type(exc).__name__}: {exc}"], []

    errors, warnings = [], []
    for line in output.getvalue().splitlines():
        if line.startswith("ERROR:"):
            errors.append(f"{label}: {line[len('ERROR:'):].strip()}")
        elif line.startswith("WARNING:"):
            warnings.append(f"{label}: {line[len('WARNING:'):].strip()}")

    if exit_code and not errors:
        errors.append(f"[EXV091] {label} validator exited with status {exit_code} without a reported finding")
    return errors, warnings


def validate_execution(directory: Path, schema_catalog=None, registry=None, validators=None):
    """Validate one execution and return a structured, deterministic report."""
    report = {
        "execution_directory": str(directory.relative_to(ROOT).as_posix()),
        "checks": {
            "parsing": "passed",
            "schema": "pending",
            "cross_record": "skipped",
            "lifecycle": "skipped",
        },
        "errors": [],
        "warnings": [],
        "info": [],
    }

    records, parse_errors = parse_execution_documents(directory)
    report["errors"].extend(parse_errors)
    if parse_errors:
        report["checks"]["parsing"] = "failed"
        report["checks"]["schema"] = "skipped"
        report["info"].append("Schema, cross-record, and lifecycle checks were skipped because parsing or required-file validation failed.")
        return report

    if schema_catalog is None:
        schema_catalog, registry = load_schema_catalog()

    schema_errors = validate_documents(directory, records, schema_catalog, registry)
    report["errors"].extend(schema_errors)
    if schema_errors:
        report["checks"]["schema"] = "failed"
        report["info"].append("Cross-record and lifecycle checks were skipped because one or more records failed JSON Schema validation.")
        return report

    report["checks"]["schema"] = "passed"

    if validators is None:
        validators = (
            ("cross_record", "validate-execution-references.py", "execution_reference_validator"),
            ("lifecycle", "validate-execution-lifecycle.py", "execution_lifecycle_validator"),
        )

    for check_name, filename, module_name in validators:
        try:
            validator = load_existing_validator(filename, module_name)
        except Exception as exc:
            report["checks"][check_name] = "failed"
            report["errors"].append(f"[EXV092] Could not load {check_name} validator: {exc}")
            continue
        errors, warnings = run_validator(check_name, validator, directory)
        report["errors"].extend(errors)
        report["warnings"].extend(warnings)
        report["checks"][check_name] = "failed" if errors else "passed"

    return report


def render_report(result):
    print(f"Execution validation: {result['execution_directory']}")
    for name, status in result["checks"].items():
        print(f"  {name.replace('_', ' ').title()}: {status.upper()}")

    for finding in result["warnings"]:
        print(f"WARNING: {finding}")
    for finding in result["info"]:
        print(f"INFO: {finding}")
    for finding in result["errors"]:
        print(f"ERROR: {finding}")

    errors = len(result["errors"])
    warnings = len(result["warnings"])
    if errors:
        print(f"\nExecution validation failed: {errors} error(s), {warnings} warning(s).")
        return 1
    print(f"\nExecution validation passed: {warnings} warning(s).")
    return 0


def resolve_execution_directory(raw_path: str):
    candidate = (ROOT / raw_path).resolve()
    executions_root = (ROOT / "executions").resolve()
    try:
        candidate.relative_to(executions_root)
    except ValueError as exc:
        raise ValueError("Execution directory must be inside executions/.") from exc
    if candidate.parent != executions_root:
        raise ValueError("Execution directory must be a direct child of executions/.")
    if not candidate.is_dir():
        raise ValueError(f"Execution directory does not exist: {raw_path}")
    return candidate


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run parsing, JSON Schema, cross-record, and lifecycle validation for one execution."
    )
    parser.add_argument(
        "execution_directory",
        nargs="?",
        help="Repository-relative path such as executions/EXE-<UUID>",
    )
    parser.add_argument(
        "--check-schemas",
        action="store_true",
        help="Meta-validate all ten execution schemas and shared definitions without an execution directory.",
    )
    args = parser.parse_args(argv)

    try:
        schema_catalog, registry = load_schema_catalog()
        if args.check_schemas:
            print(
                f"Execution schemas passed: {len(schema_catalog)} record schemas "
                "and all shared definitions are valid Draft 2020-12 documents."
            )
            return 0
        if not args.execution_directory:
            parser.error("execution_directory is required unless --check-schemas is used")
        directory = resolve_execution_directory(args.execution_directory)
        result = validate_execution(directory, schema_catalog, registry)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: [EXV001] {exc}")
        return 2

    return render_report(result)


if __name__ == "__main__":
    sys.exit(main())
