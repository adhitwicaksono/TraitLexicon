# pyproject.toml script patch

Add the full TraitLexicon CLI entry point.

Replace:

```toml
[project.scripts]
traitlexicon-validate = "traitlexicon.cli:validate_main"
```

with:

```toml
[project.scripts]
traitlexicon = "traitlexicon.cli:main"
traitlexicon-validate = "traitlexicon.cli:validate_main"
```
