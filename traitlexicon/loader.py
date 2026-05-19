"""
YAML loading utilities for TraitLexicon.

These functions intentionally stay simple in v0.1.

They load YAML files from the expected repository layout:

data/
├── traits/
├── modules/
├── vocab/
└── ontology_maps/
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml


def repo_root_from_path(path: str | Path | None = None) -> Path:
    """Return the TraitLexicon repository root.

    Parameters
    ----------
    path:
        Optional path to the repository root. If omitted, the current working
        directory is used.
    """
    if path is None:
        return Path.cwd()
    return Path(path).resolve()


def load_yaml_file(path: str | Path) -> Dict[str, Any]:
    """Load one YAML file and return a dictionary.

    Raises
    ------
    ValueError
        If the YAML file is empty or does not contain a mapping/object.
    """
    path = Path(path)

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if data is None:
        raise ValueError(f"YAML file is empty: {path}")

    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping/object: {path}")

    return data


def find_yaml_files(directory: str | Path) -> List[Path]:
    """Find YAML files recursively under a directory."""
    directory = Path(directory)

    if not directory.exists():
        return []

    return sorted(list(directory.rglob("*.yaml")) + list(directory.rglob("*.yml")))


def load_yaml_collection(directory: str | Path) -> List[Dict[str, Any]]:
    """Load all YAML files under a directory.

    Each returned dictionary receives a private `_file` field containing the
    source file path as a string. This helps users inspect where a match came from.
    """
    records: List[Dict[str, Any]] = []

    for path in find_yaml_files(directory):
        data = load_yaml_file(path)
        data["_file"] = str(path)
        records.append(data)

    return records


def load_trait_entries(repo_root: str | Path | None = None) -> List[Dict[str, Any]]:
    """Load all trait-entry YAML files from data/traits."""
    root = repo_root_from_path(repo_root)
    return load_yaml_collection(root / "data" / "traits")


def load_module_definitions(repo_root: str | Path | None = None) -> List[Dict[str, Any]]:
    """Load all module-definition YAML files from data/modules."""
    root = repo_root_from_path(repo_root)
    return load_yaml_collection(root / "data" / "modules")


def load_vocab(repo_root: str | Path | None = None, filename: str = "trait_synonyms_seed.yaml") -> Dict[str, Any]:
    """Load one vocabulary YAML file from data/vocab.

    Returns an empty dictionary if the file does not exist.
    """
    root = repo_root_from_path(repo_root)
    path = root / "data" / "vocab" / filename

    if not path.exists():
        return {}

    return load_yaml_file(path)


def iter_input_phrases(trait_entry: Dict[str, Any]) -> Iterable[str]:
    """Yield searchable phrases from a trait entry."""
    canonical_name = trait_entry.get("canonical_name")
    if isinstance(canonical_name, str):
        yield canonical_name

    input_phrases = trait_entry.get("input_phrases", [])
    if isinstance(input_phrases, list):
        for phrase in input_phrases:
            if isinstance(phrase, str):
                yield phrase
