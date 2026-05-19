# TraitLexicon YAML Validator

This package adds the first YAML validation script for TraitLexicon.

## Files

```text
scripts/
└── validate_yaml.py

requirements-dev.txt
```

## Install dependencies

```bash
pip install -r requirements-dev.txt
```

Or manually:

```bash
pip install pyyaml jsonschema
```

## Run validation

From the TraitLexicon repo root:

```bash
python scripts/validate_yaml.py
```

Validate only trait entries:

```bash
python scripts/validate_yaml.py --kind traits
```

Validate only module definitions:

```bash
python scripts/validate_yaml.py --kind modules
```

Validate one file manually:

```bash
python scripts/validate_yaml.py \
  --file data/traits/plants/aroma/fragrant_rice.yaml \
  --schema schema/trait_entry.schema.json
```

## Recommended commit

```bash
git add scripts/validate_yaml.py requirements-dev.txt
git commit -m "scripts: add YAML schema validator"
```
