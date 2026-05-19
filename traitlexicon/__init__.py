"""
TraitLexicon

A context-aware trait-to-module dictionary for plants, algae, and fungi.

TraitLexicon translates human-readable biological trait phrases into curated
candidate gene/pathway module definitions. It is designed as an upstream
interpretation layer for downstream tools such as PhenoSieve.
"""

__version__ = "0.1.0"

from .loader import load_yaml_file, find_yaml_files, load_trait_entries, load_module_definitions
from .resolver import resolve_trait_phrase

__all__ = [
    "__version__",
    "load_yaml_file",
    "find_yaml_files",
    "load_trait_entries",
    "load_module_definitions",
    "resolve_trait_phrase",
]
