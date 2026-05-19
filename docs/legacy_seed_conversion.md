# TraitLexicon Legacy Seed Conversion Guide

TraitLexicon may use older AI-assisted trait-list documents as **legacy seed material**.

These legacy files can help identify useful trait categories, candidate genes, pathway keywords, and practical applications for plants, algae, and fungi.

However, legacy materials should **not** be copied directly into the public repository.

Instead, they should be re-curated into new TraitLexicon entries with standardized wording, evidence levels, context rules, and PhenoSieve-compatible module definitions.

---

## 1. Purpose of this document

This guide explains how to convert older trait-list material into TraitLexicon YAML files.

The goal is to transform broad diagnostic-style trait tables into structured, reusable, scientifically cautious entries.

The conversion path is:

```text
legacy trait table
        ↓
curation review
        ↓
trait entry YAML
        ↓
module definition YAML
        ↓
PhenoSieve-compatible candidate module
```

TraitLexicon should preserve the useful biological ideas from legacy material while improving:

- structure
- evidence grading
- terminology
- biological caution
- downstream compatibility
- ownership clarity
- literature-readiness

---

## 2. Legacy seed material policy

Legacy seed materials may be used as **conceptual seeds only**.

They should not be treated as final curated evidence.

Recommended metadata for converted entries:

```yaml
legacy_source:
  source_type: internal_legacy_seed_catalog
  reused_as: conceptual_seed_only
  verbatim_text_reused: false
  requires_independent_verification: true
```

Recommended curation block:

```yaml
curation:
  status: seed_recurated_from_legacy_catalog
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

---

## 3. Why not copy legacy text directly?

Do not copy legacy wording directly because:

1. the original documents may have been created in an institutional work context
2. the phrasing may be too broad or client-service oriented
3. some gene names may be placeholders or overly generic
4. evidence levels were not defined in the old format
5. context rules were not explicit
6. TraitLexicon needs a stricter public-facing structure
7. downstream tools such as PhenoSieve need machine-readable fields

The safer approach is:

```text
reuse the idea
rewrite the description
verify the biology
assign evidence level
convert to YAML
```

---

## 4. What can be reused?

The following elements may be useful as seed information:

| Legacy element | TraitLexicon conversion |
|---|---|
| trait category | `trait_category` |
| trait name | `canonical_name` and `input_phrases` |
| scientific terms | `biological_process`, `pathway_keywords` |
| genes | `core_genes`, `supporting_genes`, `annotation_queries` |
| description | rewritten `description`, `context_note`, or `warnings` |
| application | `trait_application` or `use_case` |
| organism group | `kingdom_scope` |

The following should be rewritten or rechecked:

| Legacy element | Required action |
|---|---|
| broad claims | rewrite cautiously |
| placeholder genes | flag for review |
| medical/pharmaceutical claims | verify carefully |
| industrial applications | convert into biological modules |
| gene lists without evidence | mark as literature verification needed |

---

## 5. Conversion workflow

Use this workflow for each legacy trait.

### Step 1 — Identify the trait phrase

Ask:

> What would a human user search for?

Examples:

```text
salt tolerance
fragrant rice
red color
algal biofuel production
fungal enzyme production
heavy metal remediation
antibiotic production
```

This becomes the basis for the trait entry.

---

### Step 2 — Identify the biological module

Ask:

> What gene/pathway module should this trait phrase point to?

Examples:

| Trait phrase | Candidate module |
|---|---|
| salt tolerance | HKT/SOS ion homeostasis module |
| fragrant rice | BADH2 / 2-acetyl-1-pyrroline aroma module |
| red color | anthocyanin/carotenoid/betalain/chlorophyll-loss modules |
| algal biofuel production | ACC/DGAT lipid biosynthesis module |
| fungal enzyme production | cellulase/amylase/protease module |
| antibiotic production | PKS/NRPS secondary metabolite module |

---

### Step 3 — Decide whether the trait is precise or ambiguous

Some traits map cleanly to a module.

Example:

```text
fragrant rice → BADH2 / 2-acetyl-1-pyrroline module
```

Other traits are ambiguous.

Example:

```text
red color → anthocyanin OR carotenoid OR betalain OR chlorophyll-loss context
```

For ambiguous traits, include multiple candidate modules with `use_when` conditions.

---

### Step 4 — Assign kingdom scope

Every converted entry must specify:

```yaml
kingdom_scope: plant
```

or:

```yaml
kingdom_scope: algae
```

or:

```yaml
kingdom_scope: fungi
```

Do not assume that a trait has the same molecular basis across plants, algae, and fungi.

---

### Step 5 — Assign evidence level

Use one of the controlled evidence levels:

```text
causal
strong_association
pathway_supported
orthology_inferred
expression_supported
morphology_inferred
exploratory
```

Default recommendation for legacy material:

```yaml
evidence_level: pathway_supported
```

for known pathways, or:

```yaml
evidence_level: exploratory
```

when uncertainty is high.

---

### Step 6 — Add curation metadata

Every converted legacy entry should include:

```yaml
curation:
  status: seed_recurated_from_legacy_catalog
  version: 0.1.0
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

This makes the early status transparent.

---

### Step 7 — Add warnings

Warnings are useful when:

- the trait is ambiguous
- the module is context-dependent
- genes are placeholders
- the pathway is broad
- the entry is industrial/application-oriented
- organism-specific evidence is missing

Example:

```yaml
warnings:
  - This module represents a candidate pathway-level search space, not a validated causal explanation for all taxa.
  - Literature verification is required before using this entry for publication-level interpretation.
```

---

## 6. Conversion template: trait entry

Use this template when converting a legacy trait phrase into a TraitLexicon trait entry.

```yaml
trait_id: TLX-TRAIT-<KINGDOM>-<CATEGORY>-0001
canonical_name: ""
trait_category: ""
kingdom_scope: ""

input_phrases:
  - ""

recommended_context:
  taxon: []
  organ: []
  tissue: []
  developmental_stage: []
  trait_application: []

candidate_modules:
  - module_id: TLX-MODULE-<KINGDOM>-<CATEGORY>-0001
    module_name: ""
    confidence: ""
    relationship: ""

warnings:
  - ""

phenosieve_export:
  recommended_module_file: ""

legacy_source:
  source_type: internal_legacy_seed_catalog
  reused_as: conceptual_seed_only
  verbatim_text_reused: false
  requires_independent_verification: true

curation:
  status: seed_recurated_from_legacy_catalog
  version: 0.1.0
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

---

## 7. Conversion template: module definition

Use this template when converting a biological candidate module.

```yaml
module_id: TLX-MODULE-<KINGDOM>-<CATEGORY>-0001
module_name: ""
display_name: ""

module_category: ""
kingdom_scope: ""

description: ""

core_genes:
  - symbol: ""
    full_name: ""
    aliases: []
    expected_role: ""

supporting_genes: []

pathway_keywords: []

annotation_queries:
  gene_symbols: []
  keywords: []
  domains: []

context_rules:
  include_if: {}
  caution_if: {}

evidence_level: ""
causal_status: ""

warnings:
  - ""

phenosieve_compatibility:
  export_ready: false
  reason: requires_literature_verification
  suggested_output_name: ""

legacy_source:
  source_type: internal_legacy_seed_catalog
  reused_as: conceptual_seed_only
  verbatim_text_reused: false
  requires_independent_verification: true

curation:
  status: seed_recurated_from_legacy_catalog
  version: 0.1.0
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

---

## 8. Example conversion: plant salt tolerance

### Legacy-style idea

```text
Salt tolerance, sodium ion transport, HKT1, SOS1
```

### Trait entry

```yaml
trait_id: TLX-TRAIT-PLANT-STRESS-0001
canonical_name: salt tolerance
trait_category: stress_tolerance
kingdom_scope: plant

input_phrases:
  - salt tolerance
  - salinity tolerance
  - sodium stress tolerance
  - salt stress response

recommended_context:
  taxon:
    - plants
  stress_condition:
    - salinity
    - sodium stress

candidate_modules:
  - module_id: TLX-MODULE-PLANT-STRESS-0001
    module_name: hkt_sos_ion_homeostasis_module
    confidence: high
    relationship: primary_candidate_module

warnings:
  - Salt tolerance is polygenic and context-dependent.
  - This module focuses on sodium ion homeostasis and does not cover all salt-stress mechanisms.

phenosieve_export:
  recommended_module_file: data/modules/plants/stress_tolerance/hkt_sos_ion_homeostasis.yaml

legacy_source:
  source_type: internal_legacy_seed_catalog
  reused_as: conceptual_seed_only
  verbatim_text_reused: false
  requires_independent_verification: true

curation:
  status: seed_recurated_from_legacy_catalog
  version: 0.1.0
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

---

## 9. Example conversion: algal biofuel production

### Legacy-style idea

```text
Biofuel production, lipid biosynthesis, ACC, DGAT
```

### Trait entry

```yaml
trait_id: TLX-TRAIT-ALGAE-BIOFUEL-0001
canonical_name: algal biofuel lipid production
trait_category: biofuel
kingdom_scope: algae

input_phrases:
  - algal biofuel
  - lipid-rich algae
  - algal oil production
  - triacylglycerol accumulation

recommended_context:
  trait_application:
    - biofuel
    - bioenergy
  cellular_process:
    - lipid accumulation
    - triacylglycerol biosynthesis

candidate_modules:
  - module_id: TLX-MODULE-ALGAE-BIOFUEL-0001
    module_name: acc_dgat_lipid_biosynthesis_module
    confidence: medium
    relationship: pathway_level_candidate_module

warnings:
  - Biofuel potential depends on lipid accumulation, biomass productivity, cultivation condition, and extraction feasibility.
  - This module should not be interpreted as sufficient to predict industrial biofuel performance.

phenosieve_export:
  recommended_module_file: data/modules/algae/biofuel/acc_dgat_lipid_biosynthesis.yaml

legacy_source:
  source_type: internal_legacy_seed_catalog
  reused_as: conceptual_seed_only
  verbatim_text_reused: false
  requires_independent_verification: true

curation:
  status: seed_recurated_from_legacy_catalog
  version: 0.1.0
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

---

## 10. Example conversion: fungal secondary metabolites

### Legacy-style idea

```text
Antibiotic production, secondary metabolism, PKS, NRPS
```

### Trait entry

```yaml
trait_id: TLX-TRAIT-FUNGI-SECMET-0001
canonical_name: fungal secondary metabolite production
trait_category: secondary_metabolites
kingdom_scope: fungi

input_phrases:
  - fungal antibiotic production
  - fungal secondary metabolites
  - fungal bioactive compounds
  - fungal polyketides
  - fungal nonribosomal peptides

recommended_context:
  trait_application:
    - pharmaceutical discovery
    - antimicrobial discovery
    - natural product biosynthesis

candidate_modules:
  - module_id: TLX-MODULE-FUNGI-SECMET-0001
    module_name: pks_nrps_secondary_metabolite_module
    confidence: medium
    relationship: pathway_level_candidate_module

warnings:
  - PKS/NRPS gene presence suggests biosynthetic potential, not guaranteed metabolite production.
  - Culture condition, gene cluster regulation, and genome mining context are important.

phenosieve_export:
  recommended_module_file: data/modules/fungi/secondary_metabolites/pks_nrps_secondary_metabolite.yaml

legacy_source:
  source_type: internal_legacy_seed_catalog
  reused_as: conceptual_seed_only
  verbatim_text_reused: false
  requires_independent_verification: true

curation:
  status: seed_recurated_from_legacy_catalog
  version: 0.1.0
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

---

## 11. Placeholder-gene warning system

Some legacy catalogs may contain gene names that are too generic or likely placeholders.

Examples:

```text
PRT1
VITB
MINR
HYD1
COLL
FOB
Protein 1
Mineral Transporter
Hydratase 1
```

These should not be used as confident module anchors without verification.

Recommended action:

```yaml
curation:
  caution: placeholder_gene_names_detected
  needs_literature_verification: true
```

If a placeholder-like gene cannot be resolved, remove it from `core_genes` and move it into a note:

```yaml
curation_notes:
  - Legacy catalog included a broad gene label, but it was not retained as a core gene because the identity was ambiguous.
```

---

## 12. Industrial application conversion rules

Many legacy categories are application-oriented.

TraitLexicon should convert them into biological mechanisms.

| Legacy application | Convert into |
|---|---|
| cosmetics and personal care | antioxidant, pigment, polysaccharide, hydration-related compound modules |
| food supplements | nutrient biosynthesis or storage compound modules |
| aquaculture feed | protein, lipid, amino acid, pigment, or digestibility modules |
| bioremediation | metal transport, detoxification, degradation enzyme modules |
| biofuel | lipid biosynthesis, carbohydrate metabolism, biomass accumulation modules |
| pharmaceuticals | secondary metabolite, bioactive compound, or biosynthetic gene cluster modules |

Avoid using the commercial application as if it were a molecular trait.

---

## 13. Conversion priority levels

Use these levels to decide what to convert first.

### Priority 1 — strong anchors

Convert first.

Examples:

- BADH2 aroma
- HKT/SOS salt tolerance
- DREB/RD29A drought response
- CHS/DFR/ANS anthocyanin pigmentation
- PSY/PDS/ZDS carotenoid pigmentation
- ACC/DGAT lipid biosynthesis
- MT/PCS/GST heavy metal detoxification
- PKS/NRPS secondary metabolites
- ADH/PDC fermentation

### Priority 2 — useful but broad

Convert after Priority 1.

Examples:

- root architecture
- cuticle thickness
- lignin/wood density
- carbon fixation
- antioxidant production
- mycorrhizal symbiosis
- biocontrol

### Priority 3 — vague or high-risk

Convert only after review.

Examples:

- cosmetics
- anti-aging
- biocompatibility
- drug delivery
- nutritional enhancement
- broad pharmaceutical potential
- generic protein/vitamin/mineral traits

---

## 14. Recommended batch workflow

For each batch of converted YAML files:

1. choose 5–10 traits only
2. convert trait entries
3. convert module definitions
4. mark all as seed or literature-verification-needed
5. validate YAML syntax
6. run schema validation when available
7. add a seed batch index file
8. commit the batch

Recommended commit message:

```bash
git commit -m "data: add recurated legacy seed batch 01"
```

---

## 15. Seed batch index format

Each conversion batch should have an index file.

Example:

```yaml
batch_id: TLX-SEED-BATCH-0001
batch_name: initial_plant_algae_fungi_seed_modules
version: 0.1.0

source:
  source_type: internal_legacy_seed_catalog
  organisms:
    - plants
    - algae
    - fungi
  verbatim_text_reused: false

converted_entries:
  trait_entries:
    - data/traits/plants/aroma/fragrant_rice.yaml
    - data/traits/algae/biofuel/algal_biofuel_lipid_production.yaml
    - data/traits/fungi/secondary_metabolites/fungal_secondary_metabolite_production.yaml

  module_definitions:
    - data/modules/plants/aroma/badh2_2ap_aroma.yaml
    - data/modules/algae/biofuel/acc_dgat_lipid_biosynthesis.yaml
    - data/modules/fungi/secondary_metabolites/pks_nrps_secondary_metabolite.yaml

curation:
  status: seed_recurated_from_legacy_catalog
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

Recommended location:

```text
data/seed_batches/seed_batch_0001.yaml
```

---

## 16. Review checklist

Before accepting a converted legacy entry, check:

- [ ] Has the old text been rewritten?
- [ ] Is `legacy_source.verbatim_text_reused` set to `false`?
- [ ] Is the kingdom scope clear?
- [ ] Is the trait phrase biologically meaningful?
- [ ] Is the module mechanistic rather than merely commercial?
- [ ] Are placeholder genes removed or flagged?
- [ ] Is evidence level assigned conservatively?
- [ ] Is literature verification marked?
- [ ] Is PhenoSieve compatibility stated?
- [ ] Are warnings included for ambiguous traits?
- [ ] Is the YAML valid?

---

## 17. Summary

Legacy seed material is valuable, but only as a starting point.

The goal is not to preserve old tables.

The goal is to transform them into a cleaner, safer, and more useful framework:

```text
legacy trait idea
        ↓
re-curated module definition
        ↓
evidence-graded YAML
        ↓
PhenoSieve-compatible candidate search space
```

TraitLexicon should grow slowly, with conservative evidence labels and clear curation history.
