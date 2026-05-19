# TraitLexicon Core Tools v0.2

This pack finishes the main TraitLexicon tool belt before the first run/debug cycle.

## New files

```text
traitlexicon/
├── indexer.py
├── exporter.py
├── scaffold.py
└── cli.py              # updated
```

Also updates:

```text
traitlexicon/__init__.py
```

## New CLI commands

### Show a trait entry

```bash
traitlexicon show-trait "fragrant rice"
traitlexicon show-trait TLX-TRAIT-PLANT-AROMA-0001 --json
```

### Show a module definition

```bash
traitlexicon show-module BADH2
traitlexicon show-module badh2_2ap_aroma_module --json
```

### Export a module to PhenoSieve-compatible YAML

```bash
traitlexicon export-module BADH2 --output data/phenosieve_exports/badh2_2ap_aroma.phenosieve.yaml
```

Or preview JSON:

```bash
traitlexicon export-module BADH2 --json
```

### Scaffold a new trait entry

```bash
traitlexicon scaffold-trait "fragrant rice" \
  --kingdom plant \
  --category aroma \
  --trait-id TLX-TRAIT-PLANT-AROMA-0001 \
  --module-id TLX-MODULE-PLANT-AROMA-0001 \
  --module-name badh2_2ap_aroma_module \
  --output data/traits/plants/aroma/fragrant_rice.yaml
```

### Scaffold a new module definition

```bash
traitlexicon scaffold-module badh2_2ap_aroma_module \
  --display-name "BADH2 / 2-acetyl-1-pyrroline aroma module" \
  --kingdom plant \
  --category aroma \
  --module-id TLX-MODULE-PLANT-AROMA-0001 \
  --gene BADH2 \
  --gene BADH1 \
  --output data/modules/plants/aroma/badh2_2ap_aroma.yaml
```

## Recommended pyproject.toml script block

```toml
[project.scripts]
traitlexicon = "traitlexicon.cli:main"
traitlexicon-validate = "traitlexicon.cli:validate_main"
```

## Recommended commit

```bash
git add traitlexicon/ CORE_TOOLS_v0.2_USAGE.md pyproject.toml
git commit -m "feat: add TraitLexicon indexing export and scaffold tools"
```
