"""
TraitLexicon

A context-aware trait-to-module dictionary for plants, algae, and fungi.

TraitLexicon translates human-readable biological trait phrases into curated
candidate gene/pathway module definitions. It is designed as an upstream
interpretation layer for downstream tools such as PhenoSieve.
"""

__version__ = "0.2.0"

from .loader import load_yaml_file, find_yaml_files, load_trait_entries, load_module_definitions
from .resolver import resolve_trait_phrase
from .indexer import build_trait_index, build_module_index, find_trait, find_module
from .exporter import module_to_phenosieve_export, export_module_to_file
from .scaffold import make_trait_template, make_module_template, write_yaml_template

__all__ = [
    "__version__",
    "load_yaml_file",
    "find_yaml_files",
    "load_trait_entries",
    "load_module_definitions",
    "resolve_trait_phrase",
    "build_trait_index",
    "build_module_index",
    "find_trait",
    "find_module",
    "module_to_phenosieve_export",
    "export_module_to_file",
    "make_trait_template",
    "make_module_template",
    "write_yaml_template",
]
