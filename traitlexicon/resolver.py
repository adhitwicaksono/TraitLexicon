"""
Simple trait phrase resolver for TraitLexicon v0.1.

This is intentionally conservative.

The resolver performs basic exact and substring matching against:

1. data/traits/**.yaml entries
2. data/vocab/trait_synonyms_seed.yaml, when available

It does not perform semantic search or AI-based interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from .loader import iter_input_phrases, load_trait_entries, load_vocab


@dataclass
class ResolutionMatch:
    """One resolver match."""

    match_type: str
    score: float
    trait_id: Optional[str]
    canonical_name: Optional[str]
    trait_category: Optional[str]
    kingdom_scope: Optional[str]
    source_file: Optional[str]
    candidate_modules: List[Dict[str, Any]]
    matched_phrase: str
    note: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


def normalize_phrase(text: str) -> str:
    """Normalize a phrase for simple matching."""
    return " ".join(text.casefold().replace("_", " ").replace("-", " ").split())


def _context_matches(entry: Dict[str, Any], kingdom: Optional[str]) -> bool:
    """Check coarse kingdom context."""
    if kingdom is None:
        return True

    entry_kingdom = entry.get("kingdom_scope")
    if entry_kingdom is None:
        return True

    return normalize_phrase(str(entry_kingdom)) == normalize_phrase(kingdom)


def _score_phrase(query: str, candidate: str) -> Optional[float]:
    """Return a simple match score or None."""
    q = normalize_phrase(query)
    c = normalize_phrase(candidate)

    if not q or not c:
        return None

    if q == c:
        return 1.0

    if q in c or c in q:
        return 0.75

    q_tokens = set(q.split())
    c_tokens = set(c.split())

    if not q_tokens or not c_tokens:
        return None

    overlap = len(q_tokens & c_tokens) / len(q_tokens | c_tokens)

    if overlap >= 0.5:
        return round(overlap, 3)

    return None


def resolve_trait_phrase(
    trait_phrase: str,
    repo_root: str | Path | None = None,
    kingdom: Optional[str] = None,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """Resolve a human-readable trait phrase to candidate TraitLexicon entries.

    Parameters
    ----------
    trait_phrase:
        Natural-language phrase, e.g. "fragrant rice" or "red flower".
    repo_root:
        TraitLexicon repository root. Defaults to current working directory.
    kingdom:
        Optional kingdom filter: plant, algae, fungi, or cross_kingdom.
    max_results:
        Maximum number of matches to return.

    Returns
    -------
    list of dict
        Sorted resolver matches.
    """
    matches: List[ResolutionMatch] = []

    trait_entries = load_trait_entries(repo_root)

    for entry in trait_entries:
        if not _context_matches(entry, kingdom):
            continue

        best_score = None
        best_phrase = None

        for phrase in iter_input_phrases(entry):
            score = _score_phrase(trait_phrase, phrase)
            if score is not None and (best_score is None or score > best_score):
                best_score = score
                best_phrase = phrase

        if best_score is not None:
            matches.append(
                ResolutionMatch(
                    match_type="trait_entry",
                    score=best_score,
                    trait_id=entry.get("trait_id"),
                    canonical_name=entry.get("canonical_name"),
                    trait_category=entry.get("trait_category"),
                    kingdom_scope=entry.get("kingdom_scope"),
                    source_file=entry.get("_file"),
                    candidate_modules=entry.get("candidate_modules", []),
                    matched_phrase=best_phrase or "",
                    note="Matched against data/traits input phrases.",
                )
            )

    # Also try seed synonym dictionary as a fallback/hint source.
    vocab = load_vocab(repo_root, "trait_synonyms_seed.yaml")
    synonyms = vocab.get("synonyms", {}) if isinstance(vocab, dict) else {}

    for synonym_key, synonym_record in synonyms.items():
        if not isinstance(synonym_record, dict):
            continue

        canonical = synonym_record.get("canonical_name", synonym_key)
        phrases = synonym_record.get("phrases", [])
        if not isinstance(phrases, list):
            continue

        best_score = None
        best_phrase = None

        for phrase in [canonical] + phrases:
            if not isinstance(phrase, str):
                continue
            score = _score_phrase(trait_phrase, phrase)
            if score is not None and (best_score is None or score > best_score):
                best_score = score
                best_phrase = phrase

        if best_score is not None:
            matches.append(
                ResolutionMatch(
                    match_type="vocab_synonym_hint",
                    score=best_score,
                    trait_id=None,
                    canonical_name=canonical,
                    trait_category=None,
                    kingdom_scope=kingdom,
                    source_file="data/vocab/trait_synonyms_seed.yaml",
                    candidate_modules=[],
                    matched_phrase=best_phrase or "",
                    note=(
                        "Matched seed synonym vocabulary. "
                        "This is a hint, not a curated trait-entry match."
                    ),
                )
            )

    # Sort by score, then prefer curated trait entries over vocab hints.
    matches.sort(
        key=lambda m: (
            m.score,
            1 if m.match_type == "trait_entry" else 0,
            m.canonical_name or "",
        ),
        reverse=True,
    )

    return [match.to_dict() for match in matches[:max_results]]
