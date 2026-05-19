"""
Command-line interface for TraitLexicon.

Core commands:

    traitlexicon resolve "fragrant rice"
    traitlexicon list-traits
    traitlexicon list-modules
    traitlexicon show-trait TLX-TRAIT-PLANT-AROMA-0001
    traitlexicon show-module BADH2
    traitlexicon export-module BADH2 --output data/phenosieve_exports/badh2.phenosieve.yaml
    traitlexicon scaffold-trait "fragrant rice" --kingdom plant --category aroma --output draft.yaml
    traitlexicon scaffold-module badh2_2ap_aroma_module --display-name "BADH2 aroma module" --kingdom plant --category aroma --gene BADH2
    traitlexicon validate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from .exporter import export_module_to_file, module_to_phenosieve_export, write_yaml
from .indexer import find_module, find_trait, list_module_summary, list_trait_summary
from .loader import load_module_definitions, load_trait_entries
from .resolver import resolve_trait_phrase
from .scaffold import make_module_template, make_trait_template, slugify, write_yaml_template
from .validator import validate_repo


def print_json(data: Any) -> None:
    """Print JSON with readable formatting."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_resolve(args: argparse.Namespace) -> int:
    """Resolve a trait phrase."""
    results = resolve_trait_phrase(
        trait_phrase=args.phrase,
        repo_root=args.repo,
        kingdom=args.kingdom,
        max_results=args.max_results,
    )

    if args.json:
        print_json(results)
        return 0

    if not results:
        print(f"No TraitLexicon match found for: {args.phrase}")
        return 1

    print(f"TraitLexicon matches for: {args.phrase}")
    print("-" * 72)

    for result in results:
        print(f"Score: {result['score']}")
        print(f"Match type: {result['match_type']}")
        print(f"Canonical name: {result.get('canonical_name')}")
        print(f"Trait ID: {result.get('trait_id')}")
        print(f"Kingdom: {result.get('kingdom_scope')}")
        print(f"Source: {result.get('source_file')}")
        print(f"Matched phrase: {result.get('matched_phrase')}")

        candidate_modules = result.get("candidate_modules") or []
        if candidate_modules:
            print("Candidate modules:")
            for module in candidate_modules:
                print(f"  - {module.get('module_name')} ({module.get('module_id')})")
                if module.get("confidence"):
                    print(f"    confidence: {module.get('confidence')}")
        print()

    return 0


def cmd_list_traits(args: argparse.Namespace) -> int:
    """List trait entries."""
    rows = list_trait_summary(args.repo)

    if args.json:
        print_json(rows)
        return 0

    print("TraitLexicon trait entries")
    print("-" * 72)
    for row in rows:
        print(f"{row['trait_id']} | {row['kingdom_scope']} | {row['canonical_name']}")
        print(f"  candidate modules: {row['candidate_module_count']}")
        print(f"  {row['file']}")

    return 0


def cmd_list_modules(args: argparse.Namespace) -> int:
    """List module definitions."""
    rows = list_module_summary(args.repo)

    if args.json:
        print_json(rows)
        return 0

    print("TraitLexicon module definitions")
    print("-" * 72)
    for row in rows:
        print(
            f"{row['module_id']} | {row['kingdom_scope']} | "
            f"{row['module_name']} | evidence={row['evidence_level']}"
        )
        print(f"  core genes: {row['core_gene_count']}")
        print(f"  {row['file']}")

    return 0


def cmd_show_trait(args: argparse.Namespace) -> int:
    """Show one trait entry."""
    entry = find_trait(args.identifier, repo_root=args.repo)

    if entry is None:
        print(f"Trait entry not found: {args.identifier}")
        return 1

    if args.json:
        print_json(entry)
        return 0

    print(f"Trait: {entry.get('canonical_name')}")
    print("-" * 72)
    print(f"Trait ID: {entry.get('trait_id')}")
    print(f"Kingdom: {entry.get('kingdom_scope')}")
    print(f"Category: {entry.get('trait_category')}")
    print(f"File: {entry.get('_file')}")
    print()
    print("Input phrases:")
    for phrase in entry.get("input_phrases", []) or []:
        print(f"  - {phrase}")
    print()
    print("Candidate modules:")
    for module in entry.get("candidate_modules", []) or []:
        print(f"  - {module.get('module_name')} ({module.get('module_id')})")
        print(f"    confidence: {module.get('confidence')}")
        if module.get("relationship"):
            print(f"    relationship: {module.get('relationship')}")

    warnings = entry.get("warnings", []) or []
    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    return 0


def cmd_show_module(args: argparse.Namespace) -> int:
    """Show one module definition."""
    module = find_module(args.identifier, repo_root=args.repo)

    if module is None:
        print(f"Module not found: {args.identifier}")
        return 1

    if args.json:
        print_json(module)
        return 0

    print(f"Module: {module.get('display_name') or module.get('module_name')}")
    print("-" * 72)
    print(f"Module ID: {module.get('module_id')}")
    print(f"Module name: {module.get('module_name')}")
    print(f"Kingdom: {module.get('kingdom_scope')}")
    print(f"Category: {module.get('module_category')}")
    print(f"Evidence level: {module.get('evidence_level')}")
    print(f"Causal status: {module.get('causal_status')}")
    print(f"File: {module.get('_file')}")
    print()

    if module.get("description"):
        print("Description:")
        print(module.get("description"))
        print()

    print("Core genes:")
    for gene in module.get("core_genes", []) or []:
        print(f"  - {gene.get('symbol')}")
        if gene.get("full_name"):
            print(f"    full name: {gene.get('full_name')}")
        if gene.get("expected_role"):
            print(f"    role: {gene.get('expected_role')}")

    keywords = module.get("pathway_keywords", []) or []
    if keywords:
        print()
        print("Pathway keywords:")
        for keyword in keywords:
            print(f"  - {keyword}")

    warnings = module.get("warnings", []) or []
    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    return 0


def cmd_export_module(args: argparse.Namespace) -> int:
    """Export one module into PhenoSieve-compatible YAML."""
    module = find_module(args.identifier, repo_root=args.repo)

    if module is None:
        print(f"Module not found: {args.identifier}")
        return 1

    export = module_to_phenosieve_export(module)

    if args.json:
        print_json(export)
        return 0

    output = args.output
    if output is None:
        module_name = module.get("module_name", "module_export")
        output = Path("data") / "phenosieve_exports" / f"{module_name}.phenosieve.yaml"

    root = Path(args.repo).resolve()
    output_path = Path(output)
    if not output_path.is_absolute():
        output_path = root / output_path

    write_yaml(export, output_path)
    print(f"Wrote PhenoSieve export: {output_path}")
    return 0


def cmd_scaffold_trait(args: argparse.Namespace) -> int:
    """Create a scaffold trait-entry YAML."""
    module_name = args.module_name or f"{slugify(args.name)}_module"

    data = make_trait_template(
        canonical_name=args.name,
        kingdom_scope=args.kingdom,
        trait_category=args.category,
        trait_id=args.trait_id,
        module_id=args.module_id,
        module_name=module_name,
    )

    output = Path(args.output)
    write_yaml_template(data, output)
    print(f"Wrote trait scaffold: {output}")
    return 0


def cmd_scaffold_module(args: argparse.Namespace) -> int:
    """Create a scaffold module-definition YAML."""
    data = make_module_template(
        module_name=args.name,
        display_name=args.display_name,
        kingdom_scope=args.kingdom,
        module_category=args.category,
        module_id=args.module_id,
        core_gene_symbols=args.gene or [],
    )

    output = Path(args.output)
    write_yaml_template(data, output)
    print(f"Wrote module scaffold: {output}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate YAML files."""
    passed, failed, messages = validate_repo(repo_root=args.repo, kind=args.kind)

    for message in messages:
        print(message)

    print()
    print("Validation summary")
    print("-" * 72)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(
        prog="traitlexicon",
        description="TraitLexicon: trait phrase to candidate gene/pathway module resolver.",
    )

    parser.add_argument(
        "--repo",
        default=".",
        help="Path to TraitLexicon repository root. Default: current directory.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve = subparsers.add_parser("resolve", help="Resolve a trait phrase to candidate modules.")
    resolve.add_argument("phrase", help='Trait phrase, e.g. "fragrant rice".')
    resolve.add_argument("--kingdom", choices=["plant", "algae", "fungi", "cross_kingdom"])
    resolve.add_argument("--max-results", type=int, default=10)
    resolve.add_argument("--json", action="store_true", help="Print JSON output.")
    resolve.set_defaults(func=cmd_resolve)

    list_traits = subparsers.add_parser("list-traits", help="List trait entries.")
    list_traits.add_argument("--json", action="store_true", help="Print JSON output.")
    list_traits.set_defaults(func=cmd_list_traits)

    list_modules = subparsers.add_parser("list-modules", help="List module definitions.")
    list_modules.add_argument("--json", action="store_true", help="Print JSON output.")
    list_modules.set_defaults(func=cmd_list_modules)

    show_trait = subparsers.add_parser("show-trait", help="Show one trait entry.")
    show_trait.add_argument("identifier", help="Trait ID, canonical name, or input phrase.")
    show_trait.add_argument("--json", action="store_true", help="Print JSON output.")
    show_trait.set_defaults(func=cmd_show_trait)

    show_module = subparsers.add_parser("show-module", help="Show one module definition.")
    show_module.add_argument("identifier", help="Module ID, module name, display name, or core gene alias.")
    show_module.add_argument("--json", action="store_true", help="Print JSON output.")
    show_module.set_defaults(func=cmd_show_module)

    export_module = subparsers.add_parser(
        "export-module",
        help="Export one module definition to PhenoSieve-compatible YAML.",
    )
    export_module.add_argument("identifier", help="Module ID, module name, display name, or gene alias.")
    export_module.add_argument("--output", help="Output YAML path.")
    export_module.add_argument("--json", action="store_true", help="Print JSON output instead of writing YAML.")
    export_module.set_defaults(func=cmd_export_module)

    scaffold_trait = subparsers.add_parser("scaffold-trait", help="Create a new trait-entry YAML scaffold.")
    scaffold_trait.add_argument("name", help='Canonical trait name, e.g. "fragrant rice".')
    scaffold_trait.add_argument("--kingdom", required=True, choices=["plant", "algae", "fungi", "cross_kingdom"])
    scaffold_trait.add_argument("--category", required=True, help="Trait category.")
    scaffold_trait.add_argument("--trait-id", default="TLX-TRAIT-PLACEHOLDER-0000")
    scaffold_trait.add_argument("--module-id", default="TLX-MODULE-PLACEHOLDER-0000")
    scaffold_trait.add_argument("--module-name", help="Linked candidate module name.")
    scaffold_trait.add_argument("--output", required=True, help="Output YAML path.")
    scaffold_trait.set_defaults(func=cmd_scaffold_trait)

    scaffold_module = subparsers.add_parser("scaffold-module", help="Create a new module-definition YAML scaffold.")
    scaffold_module.add_argument("name", help="Module name in snake_case.")
    scaffold_module.add_argument("--display-name", required=True, help="Human-readable display name.")
    scaffold_module.add_argument("--kingdom", required=True, choices=["plant", "algae", "fungi", "cross_kingdom"])
    scaffold_module.add_argument("--category", required=True, help="Module category.")
    scaffold_module.add_argument("--module-id", default="TLX-MODULE-PLACEHOLDER-0000")
    scaffold_module.add_argument("--gene", action="append", help="Core gene symbol. Can be used multiple times.")
    scaffold_module.add_argument("--output", required=True, help="Output YAML path.")
    scaffold_module.set_defaults(func=cmd_scaffold_module)

    validate = subparsers.add_parser("validate", help="Validate YAML files against schemas.")
    validate.add_argument(
        "--kind",
        choices=["all", "traits", "modules", "phenosieve_exports"],
        default="all",
        help="Which YAML group to validate.",
    )
    validate.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def validate_main(argv: list[str] | None = None) -> int:
    """Compatibility entry point for pyproject's traitlexicon-validate script."""
    if argv is None:
        argv = sys.argv[1:]
    return main(["validate", *argv])


if __name__ == "__main__":
    raise SystemExit(main())
