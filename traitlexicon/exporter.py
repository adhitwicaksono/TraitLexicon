"""
PhenoSieve export utilities for TraitLexicon.

TraitLexicon itself does not extract sequences.

This module converts a curated TraitLexicon module definition into a
PhenoSieve-compatible export draft containing gene symbols, keywords, domain
hints, warnings, and curation metadata.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .indexer import find_module


def _unique_strings(items: List[Any]) -> List[str]:
    """Return unique non-empty strings while preserving order."""
    seen = set()
    output: List[str] = []

    for item in items:
        if item is None:
            continue
        text = str(item).strip()
        if not text:
            continue
        key = text.casefold()
        if key not in seen:
            seen.add(key)
            output.append(text)

    return output


def _gene_symbols_from_module(module: Dict[str, Any]) -> List[str]:
    """Extract gene symbols from core and supporting genes."""
    symbols: List[str] = []

    for field in ["core_genes", "supporting_genes"]:
        genes = module.get(field, [])
        if not isinstance(genes, list):
            continue

        for gene in genes:
            if not isinstance(gene, dict):
                continue

            symbol = gene.get("symbol")
            if symbol:
                symbols.append(symbol)

            aliases = gene.get("aliases", [])
            if isinstance(aliases, list):
                symbols.extend(aliases)

    return _unique_strings(symbols)


def _annotation_query_list(module: Dict[str, Any], key: str) -> List[str]:
    """Extract one list from annotation_queries."""
    annotation_queries = module.get("annotation_queries", {})
    if not isinstance(annotation_queries, dict):
        return []

    values = annotation_queries.get(key, [])
    if not isinstance(values, list):
        return []

    return _unique_strings(values)


def module_to_phenosieve_export(
    module: Dict[str, Any],
    export_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Convert a TraitLexicon module definition into a PhenoSieve export draft."""
    module_id = module.get("module_id", "UNKNOWN_MODULE")
    module_name = module.get("module_name", "unknown_module")

    if export_id is None:
        export_id = f"TLX-PHENOSIEVE-EXPORT-{module_id.replace('TLX-MODULE-', '')}"

    gene_symbols = _unique_strings(
        _gene_symbols_from_module(module)
        + _annotation_query_list(module, "gene_symbols")
    )

    keywords = _unique_strings(
        list(module.get("pathway_keywords", []) or [])
        + _annotation_query_list(module, "keywords")
    )

    domains = _annotation_query_list(module, "domains")
    go_terms = _annotation_query_list(module, "go_terms")
    kegg_terms = _annotation_query_list(module, "kegg_terms")
    pfam_terms = _annotation_query_list(module, "pfam_terms")
    interpro_terms = _annotation_query_list(module, "interpro_terms")

    warnings = list(module.get("warnings", []) or [])
    if module.get("curation", {}).get("needs_literature_verification", False):
        warnings.append("This module still requires literature verification.")

    export = {
        "export_id": export_id,
        "source_module_id": module_id,
        "module_name": module_name,
        "display_name": module.get("display_name"),
        "kingdom_scope": module.get("kingdom_scope"),
        "module_category": module.get("module_category"),
        "description": module.get("description", ""),
        "evidence_level": module.get("evidence_level"),
        "causal_status": module.get("causal_status", "unknown"),
        "query_terms": {
            "gene_symbols": gene_symbols,
            "keywords": keywords,
            "domains": domains,
            "go_terms": go_terms,
            "kegg_terms": kegg_terms,
            "pfam_terms": pfam_terms,
            "interpro_terms": interpro_terms,
        },
        "recommended_inputs": {
            "annotation_files": [
                "GFF3",
                "functional_annotation_table",
                "BLAST_or_DIAMOND_annotation",
                "InterProScan_annotation",
            ],
            "orthogroups": [
                "OrthoFinder_Orthogroups.tsv",
            ],
            "fasta": [
                "protein_fasta",
                "coding_sequence_fasta",
                "gene_sequence_fasta",
            ],
        },
        "expected_outputs": [
            "extracted_module_sequences.fasta",
            "module_presence_absence_table.tsv",
            "module_copy_number_summary.tsv",
            "module_annotation_hits.tsv",
            "module_warning_report.md",
        ],
        "context_rules": module.get("context_rules", {}),
        "orthology": module.get("orthology", {}),
        "warnings": _unique_strings(warnings),
        "curation": {
            "status": module.get("curation", {}).get("status", "unknown"),
            "version": module.get("curation", {}).get("version", "0.1.0"),
            "needs_literature_verification": module.get("curation", {}).get(
                "needs_literature_verification", True
            ),
            "ai_assisted": module.get("curation", {}).get("ai_assisted", True),
            "human_review_required": module.get("curation", {}).get(
                "human_review_required", True
            ),
        },
    }

    return export


def write_yaml(data: Dict[str, Any], output_path: str | Path) -> Path:
    """Write a dictionary as YAML."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)

    return output_path


def export_module_to_file(
    module_identifier: str,
    repo_root: str | Path | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Find a module and export it to a PhenoSieve-compatible YAML draft."""
    module = find_module(module_identifier, repo_root=repo_root)

    if module is None:
        raise ValueError(f"Could not find module: {module_identifier}")

    export = module_to_phenosieve_export(module)

    if output_path is None:
        module_name = module.get("module_name", "module_export")
        output_path = Path("data") / "phenosieve_exports" / f"{module_name}.phenosieve.yaml"

    root = Path(repo_root or ".").resolve()
    output_path = Path(output_path)

    if not output_path.is_absolute():
        output_path = root / output_path

    return write_yaml(export, output_path)
