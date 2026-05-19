# TraitLexicon Python Package v0.1

This package adds the first minimal Python code for TraitLexicon.

## Files

```text
traitlexicon/
├── __init__.py
├── cli.py
├── loader.py
├── resolver.py
└── validator.py
```

## Install locally

From the TraitLexicon repo root:

```bash
pip install -e .
```

## Recommended pyproject.toml script update

The earlier `pyproject.toml` already includes:

```toml
traitlexicon-validate = "traitlexicon.cli:validate_main"
```

Add this line too for the full CLI:

```toml
traitlexicon = "traitlexicon.cli:main"
```

So the full block should become:

```toml
[project.scripts]
traitlexicon = "traitlexicon.cli:main"
traitlexicon-validate = "traitlexicon.cli:validate_main"
```

## Example commands

Resolve a phrase:

```bash
traitlexicon resolve "fragrant rice" --kingdom plant
```

Print JSON:

```bash
traitlexicon resolve "red flower" --kingdom plant --json
```

List trait entries:

```bash
traitlexicon list-traits
```

List module definitions:

```bash
traitlexicon list-modules
```

Validate YAML files:

```bash
traitlexicon validate
```

Or use the validation shortcut:

```bash
traitlexicon-validate
```

## Development note

This v0.1 resolver only performs simple exact, substring, and token-overlap matching.

It is intentionally conservative.

Future versions may add:

- synonym expansion
- ontology-aware matching
- context-aware ranking
- module bundling
- PhenoSieve export generation
