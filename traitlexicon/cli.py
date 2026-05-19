"""
Command-line interface for TraitLexicon.

v0.1 commands:

    traitlexicon resolve "fragrant rice"
    traitlexicon list-traits
    traitlexicon list-modules
    traitlexicon validate

The pyproject created earlier includes:

    traitlexicon-validate = "traitlexicon.cli:validate_main"

For the full CLI, add this to pyproject.toml later:

    traitlexicon = "traitlexicon.cli:main"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from .loader import load_module_definitions, load_trait_entries
from .resolver import resolve_trait_phrase
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
    entries = load_trait_entries(args.repo)

    rows: List[Dict[str, Any]] = []
    for entry in entries:
        rows.append(
            {
                "trait_id": entry.get("trait_id"),
                "canonical_name": entry.get("canonical_name"),
                "trait_category": entry.get("trait_category"),
                "kingdom_scope": entry.get("kingdom_scope"),
                "file": entry.get("_file"),
            }
        )

    if args.json:
        print_json(rows)
        return 0

    print("TraitLexicon trait entries")
    print("-" * 72)
    for row in rows:
        print(f"{row['trait_id']} | {row['kingdom_scope']} | {row['canonical_name']}")
        print(f"  {row['file']}")

    return 0


def cmd_list_modules(args: argparse.Namespace) -> int:
    """List module definitions."""
    modules = load_module_definitions(args.repo)

    rows: List[Dict[str, Any]] = []
    for module in modules:
        rows.append(
            {
                "module_id": module.get("module_id"),
                "module_name": module.get("module_name"),
                "display_name": module.get("display_name"),
                "module_category": module.get("module_category"),
                "kingdom_scope": module.get("kingdom_scope"),
                "evidence_level": module.get("evidence_level"),
                "file": module.get("_file"),
            }
        )

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
        print(f"  {row['file']}")

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
