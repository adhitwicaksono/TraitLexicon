# TraitLexicon Examples

This folder contains example query files and expected downstream export structures for TraitLexicon.

These examples demonstrate how human-readable trait phrases can be represented as structured input for a future TraitLexicon resolver.

TraitLexicon itself does not extract sequences.

Instead, it resolves trait phrases into candidate module definitions that can later be passed to downstream tools such as PhenoSieve.

---

## Example files

```text
examples/
├── query_fragrant_rice.yaml
├── query_red_flower.yaml
├── query_yellow_leaf.yaml
├── query_algal_biofuel.yaml
├── query_fungal_secondary_metabolites.yaml
└── phenosieve_export_example.yaml
```

---

## Query file concept

A query file represents what a user might ask TraitLexicon to interpret.

Example:

```yaml
query_id: TLX-QUERY-EXAMPLE-0001
trait_phrase: fragrant rice
context:
  kingdom_scope: plant
  taxon: Oryza sativa
  organ: grain
```

A future resolver should use this query to find matching trait entries and candidate modules.

---

## Expected resolver behavior

TraitLexicon should not always return one gene.

Instead, it should return context-aware candidate modules.

For example:

```text
red flower
        ↓
anthocyanin_core_module
```

but:

```text
red tomato-like fruit
        ↓
carotenoid_core_module
```

and:

```text
red beetroot-like tissue
        ↓
betalain_core_module
```

Context matters.

---

## PhenoSieve handoff

The file `phenosieve_export_example.yaml` demonstrates the kind of module export that could later be sent to PhenoSieve.

This export contains:

- source TraitLexicon module ID
- gene symbols
- annotation keywords
- domain hints
- warnings
- curation metadata

PhenoSieve would then use this module definition to search annotation tables, orthogroups, and FASTA files.

---

## Development note

These examples are not final biological claims.

They are demonstration files for repository structure, resolver design, and downstream compatibility.
