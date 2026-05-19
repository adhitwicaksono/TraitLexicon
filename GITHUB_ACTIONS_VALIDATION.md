# GitHub Actions YAML Validation

This workflow automatically validates TraitLexicon YAML files against the JSON Schemas.

## File added

```text
.github/workflows/validate-yaml.yml
```

## What it does

On every push or pull request to `main` or `master`, GitHub Actions will:

1. check out the repository
2. set up Python 3.11
3. install dependencies from `requirements-dev.txt`
4. run:

```bash
python scripts/validate_yaml.py
```

## Manual run

The workflow also supports manual runs through the GitHub Actions tab because it includes:

```yaml
workflow_dispatch:
```

## Requirements

Make sure these files already exist in the repository:

```text
scripts/validate_yaml.py
requirements-dev.txt
schema/trait_entry.schema.json
schema/module.schema.json
schema/phenosieve_export.schema.json
```

## Recommended commit

```bash
git add .github/workflows/validate-yaml.yml
git commit -m "ci: validate TraitLexicon YAML files"
```
