#!/usr/bin/env python3
"""
validate_yaml.py

Validate TraitLexicon YAML files against JSON Schemas.

Expected repository layout:

TraitLexicon/
├── data/
│   ├── traits/
│   └── modules/
├── schema/
│   ├── trait_entry.schema.json
│   ├── module.schema.json
│   └── phenosieve_export.schema.json
└── scripts/
    └── validate_yaml.py

Usage:

    python scripts/validate_yaml.py

Validate only trait entries:

    python scripts/validate_yaml.py --kind traits

Validate only module definitions:

    python scripts/validate_yaml.py --kind modules

Validate a specific file:

    python scripts/validate_yaml.py --file data/traits/plants/aroma/fragrant_rice.yaml --schema schema/trait_entry.schema.json

Dependencies:

    pip install pyyaml jsonschema
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: PyYAML\n"
        "Install with: pip install pyyaml jsonschema"
    ) from exc

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: jsonschema\n"
        "Install with: pip install pyyaml jsonschema"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_PATHS = {
    "traits": {
        "data_dir": REPO_ROOT / "data" / "traits",
        "schema": REPO_ROOT / "schema" / "trait_entry.schema.json",
    },
    "modules": {
        "data_dir": REPO_ROOT / "data" / "modules",
        "schema": REPO_ROOT / "schema" / "module.schema.json",
    },
    "phenosieve_exports": {
        "data_dir": REPO_ROOT / "data" / "phenosieve_exports",
        "schema": REPO_ROOT / "schema" / "phenosieve_export.schema.json",
    },
}


def load_json(path: Path) -> dict:
    """Load a JSON file."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"Schema file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in schema file: {path}\n{exc}") from exc


def load_yaml(path: Path) -> dict:
    """Load a YAML file."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except FileNotFoundError:
        raise SystemExit(f"YAML file not found: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"Invalid YAML syntax in file: {path}\n{exc}") from exc

    if data is None:
        raise ValueError("YAML file is empty")

    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping/object")

    return data


def find_yaml_files(directory: Path) -> List[Path]:
    """Find YAML files under a directory."""
    if not directory.exists():
        return []

    return sorted(
        list(directory.rglob("*.yaml")) +
        list(directory.rglob("*.yml"))
    )


def format_validation_error(error: ValidationError) -> str:
    """Format a JSON Schema validation error for human-readable output."""
    path = ".".join(str(part) for part in error.absolute_path)
    schema_path = ".".join(str(part) for part in error.absolute_schema_path)

    if not path:
        path = "<root>"

    return (
        f"Path: {path}\n"
        f"Message: {error.message}\n"
        f"Schema rule: {schema_path}"
    )


def validate_file(yaml_path: Path, schema_path: Path) -> Tuple[bool, List[str]]:
    """Validate one YAML file against one JSON Schema."""
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)

    try:
        data = load_yaml(yaml_path)
    except Exception as exc:
        return False, [str(exc)]

    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))

    if not errors:
        return True, []

    return False, [format_validation_error(error) for error in errors]


def validate_many(files: Iterable[Path], schema_path: Path) -> Tuple[int, int]:
    """Validate many YAML files against the same schema."""
    passed = 0
    failed = 0

    for yaml_path in files:
        ok, errors = validate_file(yaml_path, schema_path)

        relative = yaml_path.relative_to(REPO_ROOT) if yaml_path.is_relative_to(REPO_ROOT) else yaml_path

        if ok:
            print(f"[PASS] {relative}")
            passed += 1
        else:
            print(f"[FAIL] {relative}")
            for error in errors:
                print("  " + error.replace("\n", "\n  "))
            failed += 1

    return passed, failed


def validate_kind(kind: str) -> Tuple[int, int]:
    """Validate all files of a given kind."""
    config = DEFAULT_PATHS[kind]
    data_dir = config["data_dir"]
    schema_path = config["schema"]

    files = find_yaml_files(data_dir)

    if not files:
        print(f"[WARN] No YAML files found for kind '{kind}' in {data_dir}")
        return 0, 0

    print(f"\nValidating {kind} using {schema_path.relative_to(REPO_ROOT)}")
    print("-" * 72)

    return validate_many(files, schema_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate TraitLexicon YAML files against JSON Schemas."
    )

    parser.add_argument(
        "--kind",
        choices=["all", "traits", "modules", "phenosieve_exports"],
        default="all",
        help="Which YAML group to validate. Default: all."
    )

    parser.add_argument(
        "--file",
        type=Path,
        help="Validate a single YAML file."
    )

    parser.add_argument(
        "--schema",
        type=Path,
        help="Schema to use with --file."
    )

    args = parser.parse_args()

    if args.file:
        if not args.schema:
            raise SystemExit("When using --file, you must also provide --schema.")

        yaml_path = args.file
        schema_path = args.schema

        if not yaml_path.is_absolute():
            yaml_path = REPO_ROOT / yaml_path

        if not schema_path.is_absolute():
            schema_path = REPO_ROOT / schema_path

        ok, errors = validate_file(yaml_path, schema_path)

        if ok:
            print(f"[PASS] {yaml_path}")
            return 0

        print(f"[FAIL] {yaml_path}")
        for error in errors:
            print(error)
        return 1

    kinds = ["traits", "modules", "phenosieve_exports"] if args.kind == "all" else [args.kind]

    total_passed = 0
    total_failed = 0

    for kind in kinds:
        passed, failed = validate_kind(kind)
        total_passed += passed
        total_failed += failed

    print("\nValidation summary")
    print("-" * 72)
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")

    if total_failed > 0:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
