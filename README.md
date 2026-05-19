# TraitLexicon

**TraitLexicon** is a curated plant trait dictionary that translates human-readable plant trait phrases into standardized candidate gene and pathway module definitions.

It is designed as an upstream companion to **PhenoSieve**.

Where **PhenoSieve** extracts sequences and generates BUSCO-like module statistics, **TraitLexicon** defines what the trait-associated module should be.

---

## Concept

Many biological questions begin as human-readable trait phrases:

- "fragrant rice"
- "red color"
- "yellow color"
- "drought tolerance"
- "Rafflesia warts"
- "large flower"
- "thickened cell wall"
- "purple leaf"

However, these phrases are not directly usable by bioinformatics pipelines.

TraitLexicon converts these phrases into curated, structured, context-aware module definitions.

```text
"fragrant rice"
        ↓
TraitLexicon
        ↓
BADH2 / 2-acetyl-1-pyrroline aroma module
        ↓
PhenoSieve
        ↓
Sequence extraction, orthogroup checking, and module statistics
```

TraitLexicon does **not** extract sequences directly.

Instead, it outputs module definitions that can later be used by downstream tools such as PhenoSieve.

---

## TraitLexicon vs PhenoSieve

| Project | Purpose | Input | Output |
|---|---|---|---|
| **TraitLexicon** | Trait phrase to module definition | Human-readable trait phrase | Curated gene/pathway module |
| **PhenoSieve** | Module-guided sequence extraction | Module definition, annotation, orthogroups, FASTA | Extracted sequences and module statistics |

TraitLexicon answers:

> What biological module should this trait phrase point to?

PhenoSieve answers:

> Can I find and extract the genes or sequences belonging to this module?

---

## Relationship to Pheno2Geno

**Pheno2Geno** is reserved as a possible future umbrella name for a broader ecosystem connecting trait phrases, curated gene/pathway modules, sequence extraction, and candidate gene prioritization.

In that future ecosystem:

```text
Pheno2Geno
├── TraitLexicon     # trait phrase → standardized module definition
├── PhenoSieve       # module definition → sequence extraction + statistics
├── TraitRanker      # optional future candidate prioritization
└── TraitViewer      # optional visualization/report layer
```

TraitLexicon remains focused on trait-to-module translation.

---

## Example mappings

| Human-readable trait phrase | TraitLexicon output |
|---|---|
| fragrant rice | BADH2 / aroma / 2-acetyl-1-pyrroline-associated module |
| red color | Anthocyanin, carotenoid, betalain, or chlorophyll-loss modules depending on context |
| yellow color | Carotenoid, flavonol, or chlorophyll-loss modules depending on context |
| Rafflesia warts | Epidermal patterning, floral surface development, cuticle, and cell wall remodeling modules |

---

## Why context matters

A phrase such as **"red color"** is biologically ambiguous.

Depending on the organism, tissue, and developmental stage, red pigmentation may involve:

- anthocyanins
- carotenoids
- betalains
- chlorophyll degradation or pigment unmasking
- stress-associated pigmentation

TraitLexicon therefore stores context-aware candidate modules instead of forcing a single trait-to-gene answer.

This is especially important for plant biology, where similar phenotypes can arise from different molecular mechanisms depending on taxon, organ, tissue type, developmental stage, and ecological context.

---

## Design philosophy

TraitLexicon is not a simple one-trait-one-gene lookup table.

It is designed around:

- trait phrase interpretation
- biological context
- curated candidate modules
- evidence-aware annotation
- downstream compatibility with PhenoSieve
- transparent uncertainty for exploratory traits

The project is especially useful for:

- plant comparative genomics
- non-model plant systems
- candidate gene discovery
- pathway-guided sequence extraction
- trait-oriented omics exploration
- hypothesis generation in unusual plant lineages

---

## Repository structure

```text
TraitLexicon/
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── traitlexicon/
│   ├── __init__.py
│   ├── cli.py
│   ├── resolver.py
│   ├── validator.py
│   └── export.py
│
├── data/
│   ├── traits/
│   │   ├── aroma/
│   │   │   └── fragrant_rice.yaml
│   │   ├── pigmentation/
│   │   │   ├── red_color.yaml
│   │   │   └── yellow_color.yaml
│   │   └── morphology/
│   │       └── rafflesia_warts.yaml
│   │
│   ├── modules/
│   │   ├── aroma/
│   │   │   └── badh2_2ap_aroma.yaml
│   │   ├── pigmentation/
│   │   │   ├── anthocyanin_core.yaml
│   │   │   ├── carotenoid_core.yaml
│   │   │   ├── betalain_core.yaml
│   │   │   ├── flavonol_yellow.yaml
│   │   │   └── chlorophyll_loss.yaml
│   │   └── morphology/
│   │       ├── epidermal_patterning.yaml
│   │       ├── floral_surface_development.yaml
│   │       ├── cuticle_development.yaml
│   │       └── cell_wall_remodeling.yaml
│   │
│   ├── vocab/
│   │   ├── trait_synonyms.yaml
│   │   ├── gene_aliases.yaml
│   │   ├── pathway_aliases.yaml
│   │   ├── tissue_terms.yaml
│   │   └── context_rules.yaml
│   │
│   └── ontology_maps/
│       ├── plant_trait_ontology.yaml
│       ├── plant_ontology.yaml
│       ├── go_terms.yaml
│       ├── kegg_terms.yaml
│       └── mapman_terms.yaml
│
├── schema/
│   ├── trait_entry.schema.json
│   ├── module.schema.json
│   └── phenosieve_export.schema.json
│
├── examples/
│   ├── query_fragrant_rice.yaml
│   ├── query_red_flower.yaml
│   ├── query_yellow_leaf.yaml
│   ├── query_rafflesia_warts.yaml
│   └── phenosieve_export_example.yaml
│
├── docs/
│   ├── concept.md
│   ├── curation_guidelines.md
│   ├── module_format.md
│   ├── context_aware_traits.md
│   ├── evidence_levels.md
│   └── traitlexicon_vs_phenosieve.md
│
└── tests/
    ├── test_schema_validation.py
    ├── test_trait_resolution.py
    └── test_phenosieve_export.py
```

For the earliest version, the Python package is optional. The main scientific asset of v0.1 is the curated dictionary and module format.

---

## Minimal v0.1 repository layout

```text
TraitLexicon/
├── README.md
├── data/
│   ├── traits/
│   │   ├── aroma/fragrant_rice.yaml
│   │   ├── pigmentation/red_color.yaml
│   │   ├── pigmentation/yellow_color.yaml
│   │   └── morphology/rafflesia_warts.yaml
│   └── modules/
│       ├── aroma/badh2_2ap_aroma.yaml
│       ├── pigmentation/anthocyanin_core.yaml
│       ├── pigmentation/carotenoid_core.yaml
│       ├── pigmentation/betalain_core.yaml
│       ├── pigmentation/chlorophyll_loss.yaml
│       └── morphology/cell_wall_remodeling.yaml
├── docs/
│   ├── curation_guidelines.md
│   └── evidence_levels.md
└── examples/
    └── phenosieve_export_example.yaml
```

---

## Trait entry format

Trait entries describe how human-readable trait phrases map to one or more candidate modules.

Example:

```yaml
trait_id: TLX-TRAIT-AROMA-0001
canonical_name: fragrant rice
trait_category: aroma

description: >
  Grain aroma phenotype commonly associated with accumulation of
  2-acetyl-1-pyrroline in aromatic rice varieties.

input_phrases:
  - fragrant rice
  - aromatic rice
  - rice aroma
  - pandan-like rice smell
  - scented rice

recommended_context:
  taxon:
    - Oryza sativa
  organ:
    - grain
    - seed
  developmental_stage:
    - mature grain

candidate_modules:
  - module_id: TLX-MODULE-AROMA-0001
    module_name: badh2_2ap_aroma_module
    confidence: high
    relationship: primary_candidate_module
    context_note: >
      Most appropriate for rice grain aroma associated with
      2-acetyl-1-pyrroline accumulation.

warnings:
  - This module is trait-associated and context-dependent.
  - Aroma phenotypes in non-rice plants may involve different volatile pathways.

phenosieve_export:
  recommended_module_file: data/modules/aroma/badh2_2ap_aroma.yaml

curation:
  status: seed
  version: 0.1.0
  curator: Adhityo Wicaksono
  last_updated: 2026-05-19
```

---

## Module definition format

Module definitions describe candidate genes, aliases, pathways, annotation keywords, context rules, and PhenoSieve export fields.

Example:

```yaml
module_id: TLX-MODULE-AROMA-0001
module_name: badh2_2ap_aroma_module
display_name: BADH2 / 2-acetyl-1-pyrroline aroma module

module_category: aroma

biological_process:
  - grain aroma
  - volatile compound metabolism
  - 2-acetyl-1-pyrroline-associated metabolism

description: >
  Candidate module for fragrant rice aroma, centered on BADH2 and
  2-acetyl-1-pyrroline-associated aroma biology.

core_genes:
  - symbol: BADH2
    full_name: betaine aldehyde dehydrogenase 2
    aliases:
      - OsBADH2
      - fgr
      - fragrance gene
    expected_role: primary_candidate
    interpretation: >
      Loss or reduction of BADH2 function is commonly associated with
      aromatic rice phenotypes.

supporting_genes:
  - symbol: BADH1
    full_name: betaine aldehyde dehydrogenase 1
    expected_role: paralog_context
    interpretation: >
      Useful for paralog comparison and distinguishing BADH2-like hits.

pathway_keywords:
  - 2-acetyl-1-pyrroline
  - aroma
  - fragrance
  - aldehyde dehydrogenase
  - betaine aldehyde dehydrogenase
  - proline metabolism
  - polyamine metabolism

annotation_queries:
  gene_symbols:
    - BADH2
    - BADH1
  keywords:
    - betaine aldehyde dehydrogenase
    - aldehyde dehydrogenase
    - fragrance
    - 2-acetyl-1-pyrroline
  domains:
    - aldehyde dehydrogenase domain

orthology:
  preferred_reference_taxa:
    - Oryza sativa
  expected_copy_behavior: >
    BADH-like genes may occur as paralogs; BADH2-specific resolution
    should use orthology, synteny, or reciprocal similarity when possible.

context_rules:
  include_if:
    taxon:
      - Oryza
      - Poaceae
    organ:
      - grain
      - seed
  caution_if:
    taxon:
      - non-Poaceae
    reason: >
      Aroma traits outside rice may involve unrelated volatile pathways.

evidence_level: high
causal_status: known_major_candidate_in_rice
curation_status: seed

phenosieve_compatibility:
  export_ready: true
  required_fields:
    - core_genes
    - annotation_queries
    - pathway_keywords
  suggested_output_name: badh2_2ap_aroma.phenosieve.yaml

curation:
  version: 0.1.0
  curator: Adhityo Wicaksono
  last_updated: 2026-05-19
```

---

## Context-aware example: red color

The phrase **"red color"** should not be mapped automatically to one pathway.

Example trait entry logic:

```yaml
trait_id: TLX-TRAIT-PIGMENT-0001
canonical_name: red color
trait_category: pigmentation

input_phrases:
  - red color
  - red pigmentation
  - red flower
  - red fruit
  - red leaf
  - red stem
  - red pericarp

candidate_modules:
  - module_id: TLX-MODULE-PIGMENT-ANTHOCYANIN-0001
    module_name: anthocyanin_core_module
    confidence: high
    use_when:
      tissue:
        - flower
        - leaf
        - stem
        - fruit skin
      taxon_context: most angiosperms
    note: >
      Common module for red, purple, or blue pigmentation in many plant tissues.

  - module_id: TLX-MODULE-PIGMENT-CAROTENOID-0001
    module_name: carotenoid_core_module
    confidence: medium
    use_when:
      tissue:
        - fruit flesh
        - chromoplast-rich tissue
      examples:
        - tomato-like red fruit
        - pepper-like red fruit

  - module_id: TLX-MODULE-PIGMENT-BETALAIN-0001
    module_name: betalain_core_module
    confidence: high
    use_when:
      taxon_context:
        - Caryophyllales
      examples:
        - beetroot-like red pigmentation

  - module_id: TLX-MODULE-PIGMENT-CHLOROPHYLL-LOSS-0001
    module_name: chlorophyll_loss_unmasking_module
    confidence: low_to_medium
    use_when:
      phenotype:
        - red/yellow unmasking due to chlorophyll degradation
      tissue:
        - senescent leaf
        - ripening fruit

warnings:
  - Red pigmentation is context-dependent.
  - Tissue, taxon, developmental stage, and compound class should be specified when possible.
```

---

## Exploratory example: Rafflesia warts

Some traits are not known causal gene modules. TraitLexicon should represent these honestly as exploratory or hypothesis-generating modules.

Example:

```yaml
trait_id: TLX-TRAIT-MORPH-RAFFLESIA-0001
canonical_name: Rafflesia warts
trait_category: floral_surface_morphology

input_phrases:
  - Rafflesia warts
  - perigone warts
  - floral warts
  - Rafflesia perigone surface
  - Rafflesia wart patterning
  - Rafflesia floral surface structures

recommended_context:
  taxon:
    - Rafflesia
    - Rafflesiaceae
  organ:
    - perigone lobe
    - floral surface
  tissue:
    - epidermis
    - subepidermal tissue

candidate_modules:
  - module_id: TLX-MODULE-MORPH-EPIDERMAL-PATTERNING-0001
    module_name: epidermal_patterning_module
    confidence: exploratory
    relationship: candidate_developmental_module

  - module_id: TLX-MODULE-MORPH-FLORAL-SURFACE-0001
    module_name: floral_surface_development_module
    confidence: exploratory
    relationship: candidate_developmental_module

  - module_id: TLX-MODULE-MORPH-CUTICLE-0001
    module_name: cuticle_development_module
    confidence: exploratory
    relationship: candidate_surface_module

  - module_id: TLX-MODULE-MORPH-CELL-WALL-REMODELING-0001
    module_name: cell_wall_remodeling_module
    confidence: exploratory
    relationship: candidate_structural_module

warnings:
  - This is a hypothesis-generating module, not a validated causal module.
  - Rafflesia warts may involve species-specific floral morphology, epidermal patterning, cell expansion, cuticle formation, and host-influenced developmental context.
  - Spatial transcriptomics or tissue-specific expression would greatly improve interpretation.

phenosieve_export:
  recommended_combined_module:
    - epidermal_patterning_module
    - floral_surface_development_module
    - cuticle_development_module
    - cell_wall_remodeling_module

curation:
  status: exploratory_seed
  version: 0.1.0
  curator: Adhityo Wicaksono
  last_updated: 2026-05-19
```

---

## Evidence levels

TraitLexicon modules should declare their evidence level.

| Evidence level | Meaning |
|---|---|
| causal | Direct functional evidence exists |
| strong_association | Strong genetic or phenotypic association |
| pathway_supported | Pathway is known to produce related phenotype |
| orthology_inferred | Candidate inferred from homologs or orthologs |
| expression_supported | Candidate supported by expression data |
| morphology_inferred | Candidate inferred from developmental or morphological analogy |
| exploratory | Hypothesis-generating only |

This is especially important for non-model organisms and unusual traits.

---

## Mapping confidence classes

TraitLexicon mappings may be classified as:

| Class | Meaning |
|---|---|
| precise | Trait phrase points to a relatively specific candidate gene/module |
| context-dependent | Multiple modules are plausible depending on biological context |
| broad pathway | Trait phrase maps to a general pathway rather than a single candidate |
| hypothesis-generating | Trait phrase can guide candidate module construction but lacks direct validation |
| exploratory | Useful for structured exploration, but evidence remains limited |

Examples:

| Trait phrase | Suggested mapping class |
|---|---|
| fragrant rice | precise |
| red color | context-dependent |
| yellow color | context-dependent |
| Rafflesia warts | hypothesis-generating / exploratory |

---

## Planned seed modules

### Aroma

- BADH2 / 2-acetyl-1-pyrroline aroma module

### Pigmentation

- Anthocyanin core module
- Carotenoid core module
- Betalain core module
- Flavonol/yellow pigmentation module
- Chlorophyll-loss/unmasking module

### Morphology

- Epidermal patterning module
- Floral surface development module
- Cuticle development module
- Cell wall remodeling module

### Future categories

- Stress tolerance
- Cell wall architecture
- Floral organ identity
- Seed/grain quality
- Plant architecture
- Parasitic plant traits
- Specialized metabolism
- Domestication traits

---

## Future command-line concept

A future TraitLexicon resolver may allow commands such as:

```bash
traitlexicon resolve "red color" --organ flower --taxon Arabidopsis
```

Possible output:

```yaml
query: red color
context:
  taxon: Arabidopsis
  organ: flower

recommended_modules:
  - anthocyanin_core_module

secondary_modules:
  - flavonol_yellow_module

excluded_or_lower_priority_modules:
  - carotenoid_core_module
  - betalain_core_module
  - chlorophyll_loss_unmasking_module

note: >
  For Arabidopsis floral red/purple pigmentation, anthocyanin-related modules
  are prioritized over carotenoid or betalain modules.
```

---

## Roadmap

### v0.1 — Curated dictionary seed

- Define trait entry format
- Define module definition format
- Add initial YAML examples
- Add curation guidelines
- Add seed modules for aroma, pigmentation, and Rafflesia floral surface traits

### v0.2 — Validation layer

- Add JSON schemas
- Add YAML validation script
- Add basic tests for required fields
- Add controlled vocabulary for evidence levels and trait categories

### v0.3 — Trait resolver prototype

- Add command-line trait resolver
- Resolve phrase to candidate modules
- Support optional context such as taxon, organ, tissue, and developmental stage

### v0.4 — PhenoSieve export

- Export module definitions in PhenoSieve-compatible format
- Add `phenosieve_export.yaml`
- Test TraitLexicon → PhenoSieve handoff

### v0.5 — Expanded plant trait library

- Add stress traits
- Add cell wall traits
- Add floral morphology traits
- Add seed/grain quality traits
- Add parasitic plant trait modules

### v1.0 — Stable curated release

- Stable schema
- Versioned module library
- Documentation
- Example workflows
- Citation file
- Manuscript-ready description

---

## Suggested first commit sequence

```bash
git init
git add README.md
git commit -m "docs: initialize TraitLexicon concept"

mkdir -p data/traits/aroma data/traits/pigmentation data/traits/morphology
mkdir -p data/modules/aroma data/modules/pigmentation data/modules/morphology
mkdir -p docs examples schema tests

git add data docs examples schema tests
git commit -m "chore: add initial repository structure"

git add data/traits/aroma/fragrant_rice.yaml
git add data/modules/aroma/badh2_2ap_aroma.yaml
git commit -m "data: add fragrant rice aroma seed module"

git add data/traits/pigmentation/
git add data/modules/pigmentation/
git commit -m "data: add context-aware pigmentation seed modules"

git add data/traits/morphology/rafflesia_warts.yaml
git add data/modules/morphology/
git commit -m "data: add exploratory Rafflesia floral surface modules"
```

---

## Author

**Adhityo Wicaksono**  
Plant molecular biologist and bioinformatician  
Aether Biomics  
Indonesia

---

## AI assistance declaration

This project concept, repository structure, README draft, and initial module-format design were developed with assistance from **OpenAI ChatGPT**, used as an AI writing, structuring, and brainstorming assistant.

The scientific direction, project framing, biological examples, and final responsibility for curation belong to the author. AI assistance was used to help organize ideas, improve documentation clarity, draft initial text, and propose structured formats for trait-to-module mapping.

All biological claims, module definitions, gene/pathway associations, and future curated entries should be manually reviewed, revised, and validated by the author or domain experts before scientific use, publication, or downstream analysis.

---

## Project status

Early-stage concept and curated data-structure design.

TraitLexicon is currently intended for plant biology, comparative genomics, non-model organisms, and hypothesis-guided bioinformatics.
