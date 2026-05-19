"""
Indexing and lookup utilities for TraitLexicon.

The indexer builds lightweight in-memory lookup dictionaries for trait entries
and module definitions.

It supports lookup by:

- trait_id / module_id
- canonical_name / module_name
- display_name
- normalized names
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .loader import load_module_definitions, load_trait_entries


def normalize_key(text: str) -> str:
    """Normalize a string into a lookup key."""
    return " ".join(str(text).casefold().replace("_", " ").replace("-", " ").split())


def _add_index_key(index: Dict[str, Dict[str, Any]], key: Optional[str], record: Dict[str, Any]) -> None:
    """Add one key to an index if available."""
    if not key:
        return

    raw_key = str(key)
    normalized = normalize_key(raw_key)

    index[raw_key] = record
    index[normalized] = record


def build_trait_index(repo_root: str | Path | None = None) -> Dict[str, Dict[str, Any]]:
    """Build a lookup index for trait entries."""
    index: Dict[str, Dict[str, Any]] = {}

    for entry in load_trait_entries(repo_root):
        _add_index_key(index, entry.get("trait_id"), entry)
        _add_index_key(index, entry.get("canonical_name"), entry)

        input_phrases = entry.get("input_phrases", [])
        if isinstance(input_phrases, list):
            for phrase in input_phrases:
                if isinstance(phrase, str):
                    _add_index_key(index, phrase, entry)

    return index


def build_module_index(repo_root: str | Path | None = None) -> Dict[str, Dict[str, Any]]:
    """Build a lookup index for module definitions."""
    index: Dict[str, Dict[str, Any]] = {}

    for module in load_module_definitions(repo_root):
        _add_index_key(index, module.get("module_id"), module)
        _add_index_key(index, module.get("module_name"), module)
        _add_index_key(index, module.get("display_name"), module)

        core_genes = module.get("core_genes", [])
        if isinstance(core_genes, list):
            for gene in core_genes:
                if isinstance(gene, dict):
                    _add_index_key(index, gene.get("symbol"), module)
                    aliases = gene.get("aliases", [])
                    if isinstance(aliases, list):
                        for alias in aliases:
                            if isinstance(alias, str):
                                _add_index_key(index, alias, module)

    return index


def find_trait(identifier: str, repo_root: str | Path | None = None) -> Optional[Dict[str, Any]]:
    """Find a trait entry by ID, canonical name, or input phrase."""
    index = build_trait_index(repo_root)
    return index.get(identifier) or index.get(normalize_key(identifier))


def find_module(identifier: str, repo_root: str | Path | None = None) -> Optional[Dict[str, Any]]:
    """Find a module definition by ID, module name, display name, or core gene alias."""
    index = build_module_index(repo_root)
    return index.get(identifier) or index.get(normalize_key(identifier))


def list_trait_summary(repo_root: str | Path | None = None) -> List[Dict[str, Any]]:
    """Return a compact summary of all trait entries."""
    rows: List[Dict[str, Any]] = []

    for entry in load_trait_entries(repo_root):
        rows.append(
            {
                "trait_id": entry.get("trait_id"),
                "canonical_name": entry.get("canonical_name"),
                "trait_category": entry.get("trait_category"),
                "kingdom_scope": entry.get("kingdom_scope"),
                "candidate_module_count": len(entry.get("candidate_modules", []) or []),
                "file": entry.get("_file"),
            }
        )

    return rows


def list_module_summary(repo_root: str | Path | None = None) -> List[Dict[str, Any]]:
    """Return a compact summary of all module definitions."""
    rows: List[Dict[str, Any]] = []

    for module in load_module_definitions(repo_root):
        rows.append(
            {
                "module_id": module.get("module_id"),
                "module_name": module.get("module_name"),
                "display_name": module.get("display_name"),
                "module_category": module.get("module_category"),
                "kingdom_scope": module.get("kingdom_scope"),
                "evidence_level": module.get("evidence_level"),
                "core_gene_count": len(module.get("core_genes", []) or []),
                "file": module.get("_file"),
            }
        )

    return rows
