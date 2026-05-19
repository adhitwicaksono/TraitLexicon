"""
Validation utilities for TraitLexicon YAML files.

This module mirrors the standalone script in scripts/validate_yaml.py, but exposes
functions that can be imported or called by the package CLI.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


DEFAULT_KINDS = {
    "traits": {
        "data_dir": Path("data") / "traits",
        "schema": Path("schema") / "trait_entry.schema.json",
    },
    "modules": {
        "data_dir": Path("data") / "modules",
        "schema": Path("schema") / "module.schema.json",
    },
    "phenosieve_exports": {
        "data_dir": Path("data") / "phenosieve_exports",
        "schema": Path("schema") / "phenosieve_export.schema.json",
    },
}


def load_json(path: Path) -> Dict:
    """Load a JSON file."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: Path) -> Dict:
    """Load a YAML file."""
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if data is None:
        raise ValueError("YAML file is empty")

    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping/object")

    return data


def find_yaml_files(directory: Path) -> List[Path]:
    """Find YAML files under a directory."""
    if not directory.exists():
        return []

    return sorted(list(directory.rglob("*.yaml")) + list(directory.rglob("*.yml")))


def format_validation_error(error: ValidationError) -> str:
    """Format a JSON Schema validation error."""
    path = ".".join(str(part) for part in error.absolute_path) or "<root>"
    schema_path = ".".join(str(part) for part in error.absolute_schema_path)

    return f"Path: {path}\\nMessage: {error.message}\\nSchema rule: {schema_path}"


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


def validate_many(files: Iterable[Path], schema_path: Path) -> Tuple[int, int, List[str]]:
    """Validate many YAML files against one schema."""
    passed = 0
    failed = 0
    messages: List[str] = []

    for yaml_path in files:
        ok, errors = validate_file(yaml_path, schema_path)

        if ok:
            messages.append(f"[PASS] {yaml_path}")
            passed += 1
        else:
            messages.append(f"[FAIL] {yaml_path}")
            for error in errors:
                messages.append("  " + error.replace("\\n", "\\n  "))
            failed += 1

    return passed, failed, messages


def validate_repo(repo_root: str | Path = ".", kind: str = "all") -> Tuple[int, int, List[str]]:
    """Validate TraitLexicon YAML files in a repository."""
    root = Path(repo_root).resolve()

    if kind == "all":
        kinds = ["traits", "modules", "phenosieve_exports"]
    else:
        kinds = [kind]

    total_passed = 0
    total_failed = 0
    messages: List[str] = []

    for item in kinds:
        config = DEFAULT_KINDS[item]
        data_dir = root / config["data_dir"]
        schema_path = root / config["schema"]

        yaml_files = find_yaml_files(data_dir)

        if not yaml_files:
            messages.append(f"[WARN] No YAML files found for kind '{item}' in {data_dir}")
            continue

        messages.append(f"Validating {item} using {schema_path}")
        passed, failed, item_messages = validate_many(yaml_files, schema_path)
        messages.extend(item_messages)

        total_passed += passed
        total_failed += failed

    return total_passed, total_failed, messages
