<p align="center">
  <img src="assets/traitlexicon_bannerV2.png" alt="TraitLexicon banner" width="100%">
</p>

# TraitLexicon

**TraitLexicon** is a curated, context-aware trait-to-module dictionary that translates human-readable biological trait phrases into standardized candidate gene/pathway modules.

It is designed as the **upstream interpretation layer** for **PhenoSieve**.

Where **PhenoSieve** extracts sequences, orthogroups, and module statistics from genomic or transcriptomic resources, **TraitLexicon** defines **what a trait phrase should biologically mean**.

---

## Core idea

Many biological questions begin as natural-language trait phrases such as:

- "fragrant rice"
- "red color"
- "yellow color"
- "drought tolerance"
- "wood density"
- "heavy metal remediation"
- "antibiotic production"
- "Rafflesia warts"

These phrases are meaningful to humans, but they are not directly usable by downstream bioinformatics tools.

**TraitLexicon** bridges that gap by converting trait phrases into curated, evidence-graded, context-aware module definitions.

Example:

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

TraitLexicon itself does **not** extract sequences.

Instead, it outputs structured module definitions that downstream tools can consume.

---

## Scope

TraitLexicon is intentionally broader than the original plant-only concept.

### Current intended scope
- **Plants**
- **Algae**
- **Fungi**

This cross-kingdom scope is motivated by legacy draft trait catalogs covering plant, algae, and fungi genomics, which can now be re-curated into a structured public framework.

### Initial emphasis
TraitLexicon will still begin with a stronger seed focus on **plant biology**, then expand to algae and fungi in staged releases.

---

## TraitLexicon vs PhenoSieve

| Project | Role | Input | Output |
|---|---|---|---|
| **TraitLexicon** | Trait interpretation | Human-readable trait phrase | Curated candidate module definition |
| **PhenoSieve** | Sequence extraction and module calling | Module definition + annotation + orthogroups + FASTA | Extracted sequences and module-level statistics |

TraitLexicon answers:

> “What biological module should this trait phrase point to?”

PhenoSieve answers:

> “Can I detect and extract sequences belonging to this curated module?”

---

## Why context matters

A trait phrase does not always map to a single pathway or gene.

For example:

- **"red color"** may involve anthocyanins, carotenoids, betalains, or chlorophyll-loss context
- **"yellow color"** may involve carotenoids, flavonols, senescence, or chlorophyll degradation
- **"fragrant"** in rice is not the same as floral volatile aroma in ornamental plants
- **"Rafflesia warts"** is best treated as an exploratory morphology-driven module rather than a single known causal gene

TraitLexicon is therefore designed to support:

- **context-aware mapping**
- **multiple candidate modules**
- **evidence grading**
- **downstream export compatibility**

---

## Example mappings

| Trait phrase | Candidate module output |
|---|---|
| fragrant rice | BADH2 / 2-acetyl-1-pyrroline aroma module |
| red color | Anthocyanin, carotenoid, betalain, or chlorophyll-loss context modules |
| yellow color | Carotenoid, flavonol, or chlorophyll-loss modules |
| salt tolerance | Ion homeostasis / HKT-SOS module |
| heavy metal remediation | Metallothionein / phytochelatin / detoxification module |
| antibiotic production | Secondary metabolite / PKS-NRPS module |
| Rafflesia warts | Epidermal patterning / floral surface / cuticle / cell wall remodeling modules |

---

## Cross-kingdom seed direction

### Plants
Examples of strong seed topics:
- flowering time
- drought tolerance
- salt tolerance
- anthocyanin pigmentation
- carotenoid pigmentation
- BADH2-associated aroma
- lignin/wood density
- cuticle thickness
- root architecture
- plant-microbe interactions

### Algae
Examples of strong seed topics:
- pigment/colorant production
- lipid biosynthesis for biofuel
- carbon fixation and sequestration
- heavy metal remediation
- bioactive compounds
- nutraceutical traits

### Fungi
Examples of strong seed topics:
- secondary metabolite production
- PKS/NRPS modules
- enzyme production
- fermentation traits
- biocontrol and mycoparasitism
- remediation and biodegradation

---

## Repository structure

```text
TraitLexicon/
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
│
├── data/
│   ├── traits/
│   │   ├── plants/
│   │   ├── algae/
│   │   └── fungi/
│   │
│   ├── modules/
│   │   ├── plants/
│   │   ├── algae/
│   │   └── fungi/
│   │
│   ├── vocab/
│   └── ontology_maps/
│
├── schema/
│   ├── trait_entry.schema.json
│   ├── module.schema.json
│   └── phenosieve_export.schema.json
│
├── examples/
├── docs/
├── traitlexicon/
└── tests/
```

---

## Core data model

TraitLexicon uses two main conceptual file types:

### 1. Trait entry
A trait entry describes how a natural-language trait phrase maps to one or more candidate modules.

Example:

```yaml
trait_id: TLX-TRAIT-PLANT-AROMA-0001
canonical_name: fragrant rice
trait_category: aroma
kingdom_scope: plant

input_phrases:
  - fragrant rice
  - aromatic rice
  - rice aroma
  - scented rice

recommended_context:
  taxon:
    - Oryza sativa
  organ:
    - grain
    - seed

candidate_modules:
  - module_id: TLX-MODULE-PLANT-AROMA-0001
    module_name: badh2_2ap_aroma_module
    confidence: high
    relationship: primary_candidate_module

phenosieve_export:
  recommended_module_file: data/modules/plants/aroma/badh2_2ap_aroma.yaml

curation:
  status: seed
  version: 0.1.0
```

### 2. Module definition
A module definition describes the biological components of a candidate module.

Example:

```yaml
module_id: TLX-MODULE-PLANT-AROMA-0001
module_name: badh2_2ap_aroma_module
display_name: BADH2 / 2-acetyl-1-pyrroline aroma module

module_category: aroma
kingdom_scope: plant

core_genes:
  - symbol: BADH2
    full_name: betaine aldehyde dehydrogenase 2
    aliases:
      - OsBADH2
      - fgr
      - fragrance gene
    expected_role: primary_candidate

supporting_genes:
  - symbol: BADH1
    expected_role: paralog_context

pathway_keywords:
  - 2-acetyl-1-pyrroline
  - aroma
  - fragrance
  - aldehyde dehydrogenase

annotation_queries:
  gene_symbols:
    - BADH2
    - BADH1
  keywords:
    - betaine aldehyde dehydrogenase
    - 2-acetyl-1-pyrroline
    - fragrance

context_rules:
  include_if:
    taxon:
      - Oryza
      - Poaceae
    organ:
      - grain
      - seed

causal_status: known_major_candidate_in_rice
evidence_level: causal

phenosieve_compatibility:
  export_ready: true
  suggested_output_name: badh2_2ap_aroma.phenosieve.yaml
```

---

## Evidence levels

TraitLexicon entries should carry explicit evidence levels.

Suggested controlled vocabulary:

| Evidence level | Meaning |
|---|---|
| **causal** | Direct functional evidence exists |
| **strong_association** | Strong genetic or phenotype association |
| **pathway_supported** | Pathway is clearly associated with the phenotype |
| **orthology_inferred** | Candidate inferred from homologs or orthologs |
| **expression_supported** | Candidate supported by transcriptomic evidence |
| **morphology_inferred** | Candidate inferred from developmental or morphological analogy |
| **exploratory** | Hypothesis-generating only |

This prevents overclaiming and is especially important for unusual or non-model traits.

---

## Legacy seed materials

TraitLexicon will reuse earlier AI-assisted trait-list documents as **legacy seed material**, especially for the first-pass coverage of plants, algae, and fungi.

However, these legacy materials should **not** be copied verbatim into the public repository.

Instead, they should be:

1. re-curated
2. rewritten in standardized TraitLexicon format
3. evidence-graded
4. revised with source-backed biological interpretation
5. exported as modular YAML definitions

This is especially important because the legacy files originated during a prior GSI-era work context.

---

## Planned v0.1 seed modules

### Plants
- BADH2 / 2-acetyl-1-pyrroline aroma module
- Anthocyanin pigmentation core module
- Carotenoid pigmentation core module
- HKT/SOS salt tolerance module
- DREB/RD29A drought response module
- Lignin biosynthesis / wood density module
- Cuticle wax biosynthesis module
- Root architecture / auxin transport module
- Floral surface / Rafflesia wart exploratory morphology module

### Algae
- Chlorophyll / carotenoid / phycobilin pigment module
- Lipid biosynthesis / biofuel module
- Carbon fixation / carbonic anhydrase module
- Heavy metal detoxification / phytochelatin module

### Fungi
- PKS/NRPS secondary metabolite module
- Industrial enzyme production module
- Fermentation / ADH-PDC module
- Biocontrol / chitinase module
- Remediation / laccase-detoxification module

---

## Roadmap

### v0.1 — Seed concept and curated skeleton
- define README and project identity
- define trait-entry format
- define module-definition format
- create first seed YAML examples
- establish plants/algae/fungi directory structure

### v0.2 — Curation framework
- add controlled vocabularies
- add curation guidelines
- add evidence-level documentation
- add legacy-seed conversion rules
- add JSON schemas

### v0.3 — First resolver prototype
- add basic phrase-to-module resolver
- support optional context fields:
  - taxon
  - tissue
  - organ
  - developmental stage
  - phenotype context

Example future usage:

```bash
traitlexicon resolve "red color" --taxon Arabidopsis --organ flower
```

### v0.4 — PhenoSieve handoff
- export TraitLexicon module definitions into PhenoSieve-compatible module files
- test full TraitLexicon → PhenoSieve workflow

### v0.5 — Cross-kingdom seed expansion
- expand algae trait coverage
- expand fungi trait coverage
- refine plant trait granularity
- improve context-aware ambiguity handling

### v1.0 — Stable curated release
- stable schema
- versioned module library
- documented curation standards
- example workflows
- citation and manuscript-friendly structure

---

## Author

**Adhityo Wicaksono**

TraitLexicon is being developed as part of a broader bioinformatics and comparative genomics toolkit vision linking trait interpretation, module curation, and downstream candidate sequence extraction.

---

## AI declaration

This repository concept, structure, and initial documentation were developed with assistance from **ChatGPT (OpenAI)** as an AI-supported writing, structuring, and brainstorming tool.

The human author is responsible for:
- project direction
- biological judgment
- curation decisions
- verification of scientific content
- repository maintenance
- final interpretation and public release

AI assistance should be understood as a support tool for drafting and ideation, not as a substitute for expert biological validation.

---

## Status

Early-stage concept and curated data-framework initialization.

TraitLexicon is currently intended as a structured upstream trait-to-module dictionary for **plants, algae, and fungi**, with downstream compatibility for tools such as **PhenoSieve**.
