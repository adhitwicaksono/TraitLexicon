"""
Scaffold utilities for TraitLexicon.

These helpers create starter YAML templates for new trait entries and module
definitions.

They do not guarantee biological correctness. They only provide structure.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml


def slugify(text: str) -> str:
    """Convert text into lowercase snake_case."""
    cleaned = []
    last_was_sep = False

    for char in str(text).casefold():
        if char.isalnum():
            cleaned.append(char)
            last_was_sep = False
        else:
            if not last_was_sep:
                cleaned.append("_")
                last_was_sep = True

    return "".join(cleaned).strip("_")


def make_trait_template(
    canonical_name: str,
    kingdom_scope: str,
    trait_category: str,
    trait_id: str = "TLX-TRAIT-PLACEHOLDER-0000",
    module_id: str = "TLX-MODULE-PLACEHOLDER-0000",
    module_name: str = "placeholder_module",
) -> Dict[str, Any]:
    """Create a starter trait-entry template."""
    return {
        "trait_id": trait_id,
        "canonical_name": canonical_name,
        "trait_category": trait_category,
        "kingdom_scope": kingdom_scope,
        "description": "",
        "input_phrases": [
            canonical_name,
        ],
        "recommended_context": {
            "taxon": [],
            "organ": [],
            "tissue": [],
            "developmental_stage": [],
            "stress_condition": [],
            "trait_application": [],
            "phenotype_context": [],
        },
        "candidate_modules": [
            {
                "module_id": module_id,
                "module_name": module_name,
                "confidence": "exploratory",
                "relationship": "exploratory_candidate_module",
                "context_note": "",
            }
        ],
        "warnings": [
            "This is a scaffolded entry and requires biological curation.",
        ],
        "phenosieve_export": {
            "recommended_module_file": "",
        },
        "legacy_source": {
            "source_type": "none",
            "reused_as": "not_applicable",
            "verbatim_text_reused": False,
            "requires_independent_verification": True,
        },
        "curation": {
            "status": "seed",
            "version": "0.1.0",
            "needs_literature_verification": True,
            "ai_assisted": True,
            "human_review_required": True,
        },
    }


def make_module_template(
    module_name: str,
    display_name: str,
    kingdom_scope: str,
    module_category: str,
    module_id: str = "TLX-MODULE-PLACEHOLDER-0000",
    core_gene_symbols: List[str] | None = None,
) -> Dict[str, Any]:
    """Create a starter module-definition template."""
    if core_gene_symbols is None:
        core_gene_symbols = []

    core_genes = [
        {
            "symbol": symbol,
            "full_name": "",
            "aliases": [],
            "expected_role": "primary_candidate",
            "interpretation": "",
        }
        for symbol in core_gene_symbols
    ]

    return {
        "module_id": module_id,
        "module_name": module_name,
        "display_name": display_name,
        "module_category": module_category,
        "kingdom_scope": kingdom_scope,
        "description": "",
        "biological_process": [],
        "core_genes": core_genes,
        "supporting_genes": [],
        "pathway_keywords": [],
        "annotation_queries": {
            "gene_symbols": core_gene_symbols,
            "keywords": [],
            "domains": [],
            "go_terms": [],
            "kegg_terms": [],
            "pfam_terms": [],
            "interpro_terms": [],
        },
        "orthology": {
            "preferred_reference_taxa": [],
            "expected_copy_behavior": "",
            "orthology_notes": "",
        },
        "context_rules": {
            "include_if": {},
            "caution_if": {},
            "exclude_if": {},
        },
        "evidence_level": "exploratory",
        "causal_status": "hypothesis_generating_candidate",
        "warnings": [
            "This is a scaffolded module and requires biological curation.",
        ],
        "phenosieve_compatibility": {
            "export_ready": False,
            "reason": "requires_literature_verification",
            "required_fields": [
                "core_genes",
                "annotation_queries",
                "pathway_keywords",
            ],
            "suggested_output_name": f"{module_name}.phenosieve.yaml",
        },
        "legacy_source": {
            "source_type": "none",
            "reused_as": "not_applicable",
            "verbatim_text_reused": False,
            "requires_independent_verification": True,
        },
        "curation": {
            "status": "seed",
            "version": "0.1.0",
            "needs_literature_verification": True,
            "ai_assisted": True,
            "human_review_required": True,
        },
    }


def write_yaml_template(data: Dict[str, Any], output_path: str | Path) -> Path:
    """Write a scaffold dictionary to YAML."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)

    return output_path
