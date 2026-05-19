# TraitLexicon Schema v0.1

This folder contains the initial JSON Schema files for TraitLexicon YAML validation.

Files:

- `trait_entry.schema.json` — validates trait-entry YAML files under `data/traits/`
- `module.schema.json` — validates module-definition YAML files under `data/modules/`
- `phenosieve_export.schema.json` — draft schema for future PhenoSieve handoff exports

These schemas are intentionally permissive in v0.1 because the TraitLexicon format is still evolving.
They check key required fields while allowing additional fields for biological nuance.
