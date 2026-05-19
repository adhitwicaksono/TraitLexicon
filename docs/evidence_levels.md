# TraitLexicon Evidence Levels

TraitLexicon entries must distinguish between well-supported biological relationships and exploratory candidate modules.

This document defines the recommended evidence-level vocabulary for TraitLexicon trait entries and module definitions.

The goal is to prevent overclaiming.

A module should be treated as a **candidate biological search space** unless strong causal evidence is available.

---

## 1. Why evidence levels matter

TraitLexicon translates human-readable trait phrases into candidate gene/pathway modules.

However, not all trait-to-module mappings have the same strength.

For example:

| Trait phrase | Candidate module | Evidence strength |
|---|---|---|
| fragrant rice | BADH2 / 2-acetyl-1-pyrroline module | high / causal in rice context |
| red flower | anthocyanin module | pathway-supported |
| salt tolerance | HKT/SOS ion homeostasis module | strong association / pathway-supported |
| algal biofuel production | lipid biosynthesis / TAG accumulation module | pathway-supported |
| fungal antibiotic production | PKS/NRPS secondary metabolite module | pathway-supported |
| Rafflesia warts | epidermal patterning / cuticle / cell wall module | exploratory |

Evidence levels help users understand whether a module is:

- known to be causal
- strongly associated
- pathway-supported
- inferred by homology
- inferred from expression
- inferred from morphology
- exploratory

---

## 2. Controlled vocabulary

Use one of the following values for `evidence_level`:

```yaml
evidence_level: causal
```

Allowed values:

```text
causal
strong_association
pathway_supported
orthology_inferred
expression_supported
morphology_inferred
exploratory
```

Avoid inventing new evidence-level labels unless the schema is updated.

---

## 3. Evidence-level definitions

### 3.1 `causal`

Use `causal` when direct functional evidence supports that a gene, allele, mutation, pathway component, or module has a causal role in the trait.

Typical evidence may include:

- mutant phenotype
- transgenic complementation
- gene knockout or knockdown
- CRISPR/Cas functional test
- validated causal allele
- biochemical validation linked to phenotype
- replicated functional study in the relevant organism or close context

Example:

```yaml
evidence_level: causal
causal_status: known_major_candidate_in_rice
```

Appropriate for:

```text
BADH2-associated fragrant rice aroma
```

when the context is rice grain aroma and 2-acetyl-1-pyrroline accumulation.

Caution:

Do not mark a gene as causal across all taxa just because it is causal in one organism.

---

### 3.2 `strong_association`

Use `strong_association` when a gene or module is repeatedly associated with a trait, but direct causality may not be fully established in the current context.

Typical evidence may include:

- QTL mapping
- GWAS association
- marker-trait association
- repeated breeding association
- strong comparative evidence
- association supported by multiple studies

Example:

```yaml
evidence_level: strong_association
causal_status: associated_candidate
```

Appropriate for:

```text
candidate loci repeatedly associated with drought tolerance, grain quality, pigmentation intensity, or disease resistance
```

Caution:

Strong association does not always imply causality.

---

### 3.3 `pathway_supported`

Use `pathway_supported` when the candidate module belongs to a known biological pathway that plausibly produces or influences the trait.

This is useful for pathway-level traits where many genes contribute collectively.

Typical evidence may include:

- known biosynthetic pathway
- known metabolic class
- established biological process
- pathway-level experimental support
- known role of pathway in the phenotype class

Example:

```yaml
evidence_level: pathway_supported
causal_status: pathway_level_candidate
```

Appropriate for:

```text
anthocyanin pigmentation
carotenoid pigmentation
lignin biosynthesis and wood density
algal lipid biosynthesis and biofuel potential
fungal PKS/NRPS secondary metabolite production
```

Caution:

This level supports a module as a useful search space, not necessarily as a precise causal answer.

---

### 3.4 `orthology_inferred`

Use `orthology_inferred` when a candidate is inferred from similarity to genes or modules in another organism.

Typical evidence may include:

- orthologous gene relationship
- reciprocal best hit
- OrthoFinder/orthogroup support
- conserved domain architecture
- phylogenetic placement
- conserved pathway membership

Example:

```yaml
evidence_level: orthology_inferred
causal_status: inferred_from_related_taxa
```

Appropriate for:

```text
candidate salt-tolerance genes in a non-model plant inferred from Arabidopsis or rice homologs
candidate fungal enzyme genes inferred from known enzyme families
candidate algal carbon-fixation genes inferred from related algal models
```

Caution:

Orthology does not guarantee identical function, especially across distant taxa or duplicated gene families.

---

### 3.5 `expression_supported`

Use `expression_supported` when transcriptomic, proteomic, or other omics data supports the involvement of a candidate gene/module.

Typical evidence may include:

- differential expression
- tissue-specific expression
- stage-specific expression
- stress-induced expression
- co-expression with known pathway genes
- proteomic/metabolomic correlation

Example:

```yaml
evidence_level: expression_supported
causal_status: omics_supported_candidate
```

Appropriate for:

```text
genes upregulated in pigmented tissue
stress-response modules induced under salinity or drought
floral surface genes enriched in Rafflesia wart-like tissue
```

Caution:

Expression evidence supports involvement, but not necessarily causality.

---

### 3.6 `morphology_inferred`

Use `morphology_inferred` when a module is inferred from developmental, anatomical, or morphological analogy.

Typical evidence may include:

- similarity to known developmental processes
- anatomical reasoning
- tissue patterning analogy
- organ surface structure analogy
- developmental biology logic

Example:

```yaml
evidence_level: morphology_inferred
causal_status: morphology_based_candidate
```

Appropriate for:

```text
Rafflesia wart candidate modules
floral surface patterning modules
cuticle/cell-wall remodeling candidates inferred from visible surface morphology
```

Caution:

This is weaker than expression-supported or pathway-supported evidence unless backed by experimental data.

---

### 3.7 `exploratory`

Use `exploratory` when the module is hypothesis-generating only.

Typical situations:

- little or no direct evidence
- unusual non-model organism trait
- conceptual module built for first-pass exploration
- candidate list assembled from analogy
- trait phrase is vague or novel
- legacy seed entry has not yet been verified

Example:

```yaml
evidence_level: exploratory
causal_status: hypothesis_generating_candidate
```

Appropriate for:

```text
Rafflesia warts
poorly characterized non-model traits
broad industrial application traits before detailed curation
legacy seed entries requiring verification
```

Caution:

Exploratory modules should never be described as validated.

---

## 4. Evidence level vs curation status

`evidence_level` and `curation.status` are related but different.

### Evidence level

Describes the biological strength of the trait-to-module relationship.

Example:

```yaml
evidence_level: pathway_supported
```

### Curation status

Describes the repository-development status of the entry.

Example:

```yaml
curation:
  status: seed_recurated_from_legacy_catalog
  needs_literature_verification: true
```

A module can be biologically strong but still need formatting or reference verification.

Example:

```yaml
evidence_level: causal
curation:
  status: seed
  needs_literature_verification: true
```

This means:

> The biological relationship is likely strong, but this repository entry still needs references and review.

---

## 5. Recommended `causal_status` values

Use `causal_status` to add more nuance beyond the main evidence level.

Suggested values:

```text
known_causal_gene
known_major_candidate
known_major_candidate_in_specific_taxon
pathway_level_candidate
associated_candidate
orthology_based_candidate
omics_supported_candidate
morphology_based_candidate
hypothesis_generating_candidate
unknown
```

Example:

```yaml
evidence_level: causal
causal_status: known_major_candidate_in_specific_taxon
```

Example:

```yaml
evidence_level: exploratory
causal_status: hypothesis_generating_candidate
```

---

## 6. Confidence labels for trait entries

Trait entries may contain multiple candidate modules.

Each candidate module inside a trait entry should include a `confidence` field.

Recommended values:

```text
high
medium
low
exploratory
context_dependent
```

Example:

```yaml
candidate_modules:
  - module_id: TLX-MODULE-PLANT-PIGMENT-0001
    module_name: anthocyanin_core_module
    confidence: high
    use_when:
      organ:
        - flower
        - leaf
        - stem

  - module_id: TLX-MODULE-PLANT-PIGMENT-0002
    module_name: carotenoid_core_module
    confidence: medium
    use_when:
      organ:
        - fruit
      phenotype_context:
        - chromoplast-rich tissue
```

---

## 7. Recommended mapping between evidence and confidence

Evidence level and confidence are not identical, but they should be consistent.

| Evidence level | Typical confidence |
|---|---|
| `causal` | high |
| `strong_association` | high or medium |
| `pathway_supported` | high or medium |
| `orthology_inferred` | medium |
| `expression_supported` | medium |
| `morphology_inferred` | low or exploratory |
| `exploratory` | exploratory |

Use `context_dependent` when confidence depends strongly on organism, tissue, developmental stage, or phenotype interpretation.

---

## 8. Examples

### 8.1 BADH2 rice aroma

```yaml
module_name: badh2_2ap_aroma_module
kingdom_scope: plant
evidence_level: causal
causal_status: known_major_candidate_in_specific_taxon

context_rules:
  include_if:
    taxon:
      - Oryza
    organ:
      - grain
      - seed

warnings:
  - This module is high-confidence for rice grain aroma, but aroma traits in other plants may involve different volatile pathways.
```

---

### 8.2 Anthocyanin pigmentation

```yaml
module_name: anthocyanin_core_module
kingdom_scope: plant
evidence_level: pathway_supported
causal_status: pathway_level_candidate

context_rules:
  include_if:
    phenotype:
      - red pigmentation
      - purple pigmentation
      - blue pigmentation
    organ:
      - flower
      - leaf
      - stem
      - fruit skin

warnings:
  - Red pigmentation can also involve carotenoids, betalains, or chlorophyll-loss context.
```

---

### 8.3 Algal lipid biofuel module

```yaml
module_name: acc_dgat_lipid_biosynthesis_module
kingdom_scope: algae
evidence_level: pathway_supported
causal_status: pathway_level_candidate

context_rules:
  include_if:
    trait_application:
      - biofuel
      - lipid accumulation
      - triacylglycerol production

warnings:
  - Biofuel potential is an applied trait and should be interpreted through lipid metabolism, biomass productivity, and cultivation context.
```

---

### 8.4 Fungal PKS/NRPS secondary metabolite module

```yaml
module_name: pks_nrps_secondary_metabolite_module
kingdom_scope: fungi
evidence_level: pathway_supported
causal_status: pathway_level_candidate

context_rules:
  include_if:
    trait_application:
      - antibiotic production
      - secondary metabolite production
      - bioactive compound discovery

warnings:
  - PKS/NRPS presence suggests biosynthetic potential, not guaranteed metabolite production under all culture conditions.
```

---

### 8.5 Rafflesia warts

```yaml
module_name: rafflesia_floral_surface_morphology_module
kingdom_scope: plant
evidence_level: exploratory
causal_status: hypothesis_generating_candidate

candidate_submodules:
  - epidermal_patterning
  - cuticle_development
  - cell_wall_remodeling
  - floral_surface_development

warnings:
  - This is an exploratory candidate module.
  - Spatial transcriptomics or tissue-specific expression data would be needed for stronger support.
```

---

## 9. When to downgrade evidence level

Downgrade evidence level when:

- the organism is very distant from the original evidence source
- gene family duplication makes orthology unclear
- the trait phrase is broad or ambiguous
- the gene name is generic or placeholder-like
- evidence is based only on pathway intuition
- no references have been checked
- the entry came from legacy AI-assisted material

Example:

```yaml
evidence_level: exploratory
curation:
  needs_literature_verification: true
```

is safer than overclaiming.

---

## 10. When to upgrade evidence level

Upgrade evidence level only after adding support such as:

- reference-backed functional evidence
- curated pathway source
- experimentally validated gene function
- strong orthology and phylogenetic support
- transcriptomic support in the target organism
- QTL/GWAS or association evidence
- biochemical or metabolite evidence

Recommended metadata after upgrading:

```yaml
curation:
  status: literature_supported
  references_added: true
  reviewed_by_human: true
```

---

## 11. Literature verification field

All early entries should include:

```yaml
curation:
  needs_literature_verification: true
```

Once references are added:

```yaml
curation:
  needs_literature_verification: false
  references_added: true
```

Recommended reference structure:

```yaml
references:
  - citation_key: author_year_shorttitle
    title: ""
    authors: ""
    year: ""
    doi: ""
    note: ""
```

---

## 12. Evidence-level checklist

Before assigning an evidence level, ask:

- Is this gene/module experimentally validated for this trait?
- Is the evidence from the same species or a related species?
- Is this a single-gene trait or a pathway-level trait?
- Is the trait phrase ambiguous?
- Is this inferred from orthology?
- Is this inferred from expression?
- Is this inferred from morphology?
- Does this come from legacy seed material?
- Could another pathway explain the same phenotype?

When uncertain, choose the more conservative evidence level.

---

## 13. Recommended default for v0.1

For early seed entries derived from legacy catalogs, use conservative defaults:

```yaml
curation:
  status: seed_recurated_from_legacy_catalog
  needs_literature_verification: true
  ai_assisted: true
  human_review_required: true
```

Suggested evidence defaults:

| Entry type | Recommended initial evidence level |
|---|---|
| Known gene-trait example | `causal` or `strong_association`, with verification needed |
| Known pathway-trait example | `pathway_supported` |
| Orthology-only candidate | `orthology_inferred` |
| Expression-only candidate | `expression_supported` |
| Morphology analogy | `morphology_inferred` |
| Unusual or poorly characterized trait | `exploratory` |
| Legacy uncertain entry | `exploratory` |

---

## 14. Summary

TraitLexicon should be biologically useful but scientifically cautious.

A good evidence label tells users:

```text
How much should I trust this trait-to-module mapping?
```

The safest principle:

> Underclaim first, upgrade later.

A small set of conservative, well-documented modules is better than a large set of overconfident mappings.
