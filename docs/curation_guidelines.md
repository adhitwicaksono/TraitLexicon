# TraitLexicon Curation Guidelines

TraitLexicon is a curated, context-aware trait-to-module dictionary for plants, algae, and fungi.

Its purpose is to translate human-readable biological trait phrases into standardized candidate gene/pathway module definitions that can later be used by downstream tools such as PhenoSieve.

TraitLexicon does **not** extract sequences directly. It defines the biological meaning of a trait phrase.

---

## 1. Core curation principle

Every TraitLexicon entry should answer one main question:

> When a user says this trait phrase, what biological module or modules should we reasonably examine?

A good entry should connect:

```text
trait phrase
+ biological context
+ candidate genes/pathways
+ evidence level
+ uncertainty notes
+ PhenoSieve-compatible module definition
```

TraitLexicon should avoid simple one-trait-one-gene assumptions unless the biological evidence strongly supports that simplification.

---

## 2. Trait entry vs module definition

TraitLexicon separates **trait entries** from **module definitions**.

### 2.1 Trait entry

A trait entry represents a human-readable phrase or group of synonymous phrases.

Examples:

- fragrant rice
- red color
- yellow color
- drought tolerance
- heavy metal remediation
- antibiotic production
- Rafflesia warts

A trait entry should point to one or more candidate modules.

### 2.2 Module definition

A module definition represents the biological candidate gene/pathway set associated with the trait.

Examples:

- BADH2 / 2-acetyl-1-pyrroline aroma module
- anthocyanin pigmentation module
- carotenoid pigmentation module
- HKT/SOS salt tolerance module
- PKS/NRPS fungal secondary metabolite module
- algal lipid biosynthesis biofuel module

A module definition should be structured enough to support downstream extraction by PhenoSieve.

---

## 3. Recommended file placement

Trait entries should be stored under:

```text
data/traits/<kingdom>/<category>/<trait_name>.yaml
```

Module definitions should be stored under:

```text
data/modules/<kingdom>/<category>/<module_name>.yaml
```

Examples:

```text
data/traits/plants/aroma/fragrant_rice.yaml
data/modules/plants/aroma/badh2_2ap_aroma.yaml

data/traits/algae/biofuel/algal_biofuel_lipid_production.yaml
data/modules/algae/biofuel/acc_dgat_lipid_biosynthesis.yaml

data/traits/fungi/secondary_metabolites/fungal_antibiotic_production.yaml
data/modules/fungi/secondary_metabolites/pks_nrps_secondary_metabolite.yaml
```

---

## 4. Curation status labels

Each entry should include a curation status.

Recommended values:

| Status | Meaning |
|---|---|
| `seed` | First-pass entry, manually drafted |
| `seed_recurated_from_legacy_catalog` | Rewritten from older seed material |
| `needs_literature_verification` | Biologically plausible, but references still needed |
| `literature_supported` | Supported by curated literature |
| `reviewed` | Checked for formatting, evidence, and biological logic |
| `deprecated` | Kept for history but no longer recommended |

For v0.1, most entries should be marked as:

```yaml
curation:
  status: seed_recurated_from_legacy_catalog
  needs_literature_verification: true
```

This keeps the project honest during early development.

---

## 5. Evidence levels

Every module should include an evidence level.

Recommended controlled vocabulary:

| Evidence level | Meaning |
|---|---|
| `causal` | Direct functional evidence supports the gene/module as causal for the trait |
| `strong_association` | Strong genetic, QTL, GWAS, or phenotype association exists |
| `pathway_supported` | Pathway is clearly associated with the trait, but causality may be distributed |
| `orthology_inferred` | Candidate inferred from homologs or orthologs in related taxa |
| `expression_supported` | Candidate supported by expression or omics evidence |
| `morphology_inferred` | Candidate inferred from developmental or morphological analogy |
| `exploratory` | Hypothesis-generating only |

Examples:

```yaml
evidence_level: causal
```

for BADH2-associated rice aroma.

```yaml
evidence_level: pathway_supported
```

for anthocyanin pigmentation modules.

```yaml
evidence_level: exploratory
```

for Rafflesia wart candidate morphology modules.

---

## 6. Handling ambiguous traits

Many trait phrases are biologically ambiguous.

TraitLexicon should preserve ambiguity instead of forcing a single answer.

### Example: red color

Do **not** encode:

```text
red color = anthocyanin
```

Instead, encode context-aware possibilities:

| Context | Candidate module |
|---|---|
| red flower, red leaf, red stem | anthocyanin module |
| red tomato-like fruit | carotenoid/chromoplast module |
| red beetroot-like tissue | betalain module |
| red/yellow senescent tissue | chlorophyll-loss/unmasking module |

A good ambiguous trait entry should include:

```yaml
candidate_modules:
  - module_name: anthocyanin_core_module
    use_when:
      organ:
        - flower
        - leaf
        - stem
  - module_name: carotenoid_core_module
    use_when:
      organ:
        - fruit
      phenotype_context:
        - chromoplast-rich tissue
```

---

## 7. Handling broad industrial traits

Some legacy traits are industrial or application-oriented rather than strict biological phenotypes.

Examples:

- biofuel production
- biocontrol
- cosmetics and personal care
- nutraceutical potential
- heavy metal remediation
- enzyme production

These should be converted into biological modules by identifying the molecular process behind the application.

Examples:

| Application phrase | TraitLexicon biological module |
|---|---|
| algal biofuel production | lipid biosynthesis / TAG accumulation module |
| fungal enzyme production | cellulase/amylase/protease industrial enzyme module |
| heavy metal remediation | metallothionein/phytochelatin/GST detoxification module |
| fungal biocontrol | chitinase / mycoparasitism / pathogen-antagonism module |

Avoid treating the industrial application itself as the gene module.

---

## 8. Handling legacy seed material

TraitLexicon may use older AI-assisted trait-list documents as seed material.

However, legacy material should not be copied verbatim into the public repository.

Instead, each legacy trait should be:

1. re-read
2. rewritten in new wording
3. converted into TraitLexicon YAML structure
4. assigned an evidence level
5. assigned a curation status
6. checked for vague or placeholder gene names
7. marked for literature verification

Recommended metadata:

```yaml
legacy_source:
  source_type: internal_legacy_seed_catalog
  reused_as: conceptual_seed_only
  verbatim_text_reused: false
```

This protects the project from institutional ambiguity and improves scientific quality.

---

## 9. Avoiding placeholder genes

Some older trait catalogs may contain broad or placeholder-like gene labels.

Examples that need extra review:

- generic names such as `PRT1`, `VITB`, `MINR`, `HYD1`, `COLL`, or similar labels without clear organism-specific meaning
- overly generic labels such as `Protein 1`, `Mineral Transporter`, or `Hydratase 1`
- genes borrowed from unrelated organisms without context
- pathway labels written as if they were exact genes

These should not be used as high-confidence module anchors unless verified.

Recommended handling:

```yaml
curation:
  status: seed_recurated_from_legacy_catalog
  needs_literature_verification: true
  caution: placeholder_gene_names_detected
```

Prefer stronger anchors such as:

- BADH2
- HKT1
- SOS1/SOS2/SOS3
- DREB
- CBF
- CHS/DFR/ANS
- PSY/PDS/ZDS
- PAL/C4H/CHS
- PKS/NRPS
- ACC/DGAT
- MT/PCS/GST
- ADH/PDC
- cellulase/amylase/protease genes, when organism context is clear

---

## 10. Recommended YAML fields for trait entries

A trait entry should include:

```yaml
trait_id: TLX-TRAIT-PLANT-AROMA-0001
canonical_name: fragrant rice
trait_category: aroma
kingdom_scope: plant

input_phrases:
  - fragrant rice
  - aromatic rice
  - rice aroma

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

warnings:
  - Aroma traits outside rice may involve different volatile pathways.

phenosieve_export:
  recommended_module_file: data/modules/plants/aroma/badh2_2ap_aroma.yaml

curation:
  status: seed
  version: 0.1.0
  needs_literature_verification: true
```

---

## 11. Recommended YAML fields for module definitions

A module definition should include:

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
    expected_role: primary_candidate

supporting_genes:
  - symbol: BADH1
    expected_role: paralog_context

pathway_keywords:
  - 2-acetyl-1-pyrroline
  - aroma
  - aldehyde dehydrogenase

annotation_queries:
  gene_symbols:
    - BADH2
    - BADH1
  keywords:
    - betaine aldehyde dehydrogenase
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

curation:
  status: seed
  version: 0.1.0
  needs_literature_verification: true
```

---

## 12. PhenoSieve compatibility rules

A module is considered PhenoSieve-compatible when it contains enough information for sequence extraction or annotation search.

Minimum useful fields:

```yaml
core_genes:
annotation_queries:
pathway_keywords:
phenosieve_compatibility:
```

A module should not be marked as export-ready if it only contains a vague description without gene symbols, pathway terms, domain terms, or annotation keywords.

Recommended values:

```yaml
phenosieve_compatibility:
  export_ready: false
  reason: requires_literature_verification
```

or:

```yaml
phenosieve_compatibility:
  export_ready: true
  suggested_output_name: module_name.phenosieve.yaml
```

---

## 13. Cross-kingdom curation rules

TraitLexicon currently covers three broad organism groups:

- plants
- algae
- fungi

Do not assume that a trait has the same molecular basis across kingdoms.

Examples:

| Trait phrase | Plant interpretation | Algae interpretation | Fungi interpretation |
|---|---|---|---|
| pigment production | anthocyanin/carotenoid/chlorophyll | chlorophyll/carotenoid/phycobilin | melanins/carotenoids/secondary metabolites |
| stress tolerance | ABA, DREB, HKT/SOS, ROS detoxification | salinity/light/temperature response, carbon concentration | heat shock, osmotic regulation, cell wall adaptation |
| bioactive compounds | phenylpropanoids, alkaloids, terpenes | PUFA, pigments, antioxidants | PKS/NRPS metabolites, antibiotics |

Always specify `kingdom_scope`.

---

## 14. Naming conventions

### Trait IDs

Recommended format:

```text
TLX-TRAIT-<KINGDOM>-<CATEGORY>-<NUMBER>
```

Example:

```text
TLX-TRAIT-PLANT-AROMA-0001
```

### Module IDs

Recommended format:

```text
TLX-MODULE-<KINGDOM>-<CATEGORY>-<NUMBER>
```

Example:

```text
TLX-MODULE-PLANT-AROMA-0001
```

### File names

Use lowercase snake case.

Examples:

```text
fragrant_rice.yaml
badh2_2ap_aroma.yaml
algal_lipid_biofuel.yaml
fungal_pks_nrps_secondary_metabolites.yaml
```

---

## 15. What should not be included

Do not include:

- unsupported claims of causality
- unverified gene lists copied from broad AI-generated material
- vague industrial claims without molecular interpretation
- disease/medical claims without strong evidence
- organism-specific genes applied broadly without context
- sequence extraction outputs
- FASTA files
- orthogroup tables
- BLAST results

Those belong elsewhere, especially in PhenoSieve or downstream analysis projects.

---

## 16. Minimum checklist before adding a new entry

Before adding a new TraitLexicon entry, check:

- [ ] Is this a trait entry or a module definition?
- [ ] Is the kingdom scope clear?
- [ ] Is the trait phrase precise or ambiguous?
- [ ] Are candidate modules listed?
- [ ] Are evidence levels assigned?
- [ ] Are context rules included?
- [ ] Are vague or placeholder genes flagged?
- [ ] Is literature verification needed?
- [ ] Is PhenoSieve compatibility stated?
- [ ] Is the text newly written rather than copied from legacy material?

---

## 17. Development priority

For early versions, prioritize entries that are:

1. biologically well anchored
2. easy to explain
3. useful for downstream extraction
4. relevant to plants, algae, or fungi
5. suitable for PhenoSieve handoff

Good v0.1 targets:

- BADH2 rice aroma
- anthocyanin pigmentation
- carotenoid pigmentation
- HKT/SOS salt tolerance
- DREB/RD29A drought response
- algal ACC/DGAT lipid biosynthesis
- algal MT/PCS/GST remediation
- fungal PKS/NRPS secondary metabolism
- fungal cellulase/amylase/protease enzyme production
- fungal ADH/PDC fermentation

Exploratory entries such as Rafflesia warts are welcome, but must be clearly labeled as exploratory.

---

## 18. Scientific responsibility

TraitLexicon is a curation framework, not an oracle.

It should help researchers organize candidate biological modules, but it should not replace:

- literature review
- expert judgment
- organism-specific validation
- experimental evidence
- careful comparative genomics

All modules should be treated as candidate search spaces unless strong causal evidence is available.

---

## 19. AI-assisted curation policy

AI tools may be used for:

- brainstorming candidate modules
- restructuring legacy notes
- drafting YAML templates
- summarizing possible pathways
- generating first-pass documentation

However, AI-generated content must be manually reviewed.

The human curator is responsible for:

- accepting or rejecting candidate genes
- checking biological plausibility
- adding references
- assigning evidence levels
- avoiding overclaiming
- maintaining public repository quality

Recommended note for AI-assisted entries:

```yaml
curation:
  ai_assisted: true
  human_review_required: true
```

---

## 20. Summary

TraitLexicon should be curated slowly and carefully.

The goal is not to create the largest possible trait list.

The goal is to create a trustworthy bridge:

```text
human trait language
        ↓
curated biological module
        ↓
PhenoSieve-compatible candidate search space
```

A small number of well-curated entries is better than a large number of vague ones.
