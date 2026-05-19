# TraitLexicon Repository Status Checklist

This checklist maps the intended repository structure against the files created so far.

## Already created or drafted

```text
README.md
data/traits/
data/modules/
data/seed_batches/
docs/curation_guidelines.md
docs/evidence_levels.md
docs/legacy_seed_conversion.md
schema/trait_entry.schema.json
schema/module.schema.json
schema/phenosieve_export.schema.json
scripts/validate_yaml.py
requirements-dev.txt
.github/workflows/validate-yaml.yml
```

## Added in this metadata pack

```text
LICENSE
CITATION.cff
pyproject.toml
```

## Still to build next

```text
data/vocab/
data/ontology_maps/
examples/
traitlexicon/
tests/
```

## Recommended next order

1. `data/vocab/`
2. `data/ontology_maps/`
3. `examples/`
4. `traitlexicon/`
5. `tests/`

Reason:

The vocabulary layer should come before the resolver code. The code should obey the controlled vocabulary rather than invent its own assumptions.
