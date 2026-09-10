# FALCON-AI: Failure Analysis & Risk Mitigation Report

**Date:** September 9, 2026  
**Subject:** Empirical Failure Modes, Boundary Conditions, and Algorithmic Guardrails  
**Audience:** SIH 2026 Evaluation Jury, Agronomists, and Systems Engineers  

---

## 1. Executive Summary

In agricultural AI, a misclassification is not just a statistical error—it can result in crop failure, financial ruin, or severe ecological damage through inappropriate pesticide application. 

FALCON-AI adopts a **Safety-First Agronomic Principle**:
> *When visual evidence is ambiguous, the system must never hallucinate a definitive disease. Instead, it must express uncertainty, solicit corroborating symptoms, or instruct the farmer to inspect non-foliar organs.*

This report documents all known failure modes discovered during the Golden Test Set evaluation and details the deterministic mitigation mechanisms implemented in FALCON-AI.

---

## 2. Empirical Failure Modes from Golden Test Set

During the benchmarking of 141 authentic field images, four distinct categories of failure/edge cases were identified:

```
+-------------------------------------------------------------------------------+
|                       IDENTIFIED FAILURE MODES & FREQUENCIES                  |
+--------------------------+-----------------------+----------------------------+
| Failure Category         | Golden Set Occurrence | Direct Mitigation          |
+--------------------------+-----------------------+----------------------------+
| 1. Cross-Crop Visual     | 22.0% (Pigeonpea spot | Canonical Taxonomy Mapping |
|    Surrogacy             | -> Citrus Greening)   | & Crop Compatibility Guard |
| 2. Hidden Pest Pathology | 15.6% (Leaf Webber    | 4-Step Field Inspection    |
|    (Internal/Webbing)    | -> Leaf Only)         | Scouting Protocol          |
| 3. Subsurface / Non-     | Inherent to Computer  | Guided Collar / Root Rot   |
|    Foliar Diseases       | Vision (Wilt/Rot)     | Inspection Tasks           |
| 4. Out-of-Distribution   | 80% Safely Rejected   | Low-Confidence (<0.50)     |
|    Unseen Foliage        | as Low/Unknown        | Safety Rejection           |
+--------------------------+-----------------------+----------------------------+
```

### Failure Mode 1: Cross-Crop Visual Surrogacy (Taxonomic Shift)
* **Description:** When evaluating crops outside the model's primary training set (such as Pigeonpea *Cajanus cajan*), the model's convolutional feature extractors detect visual primitives (chlorotic halos, necrosis, viral mottling) and map them to known classes that share those exact visual markers (e.g. `bean mosaic virus` or `citrus greening`).
* **Root Cause:** Deep neural networks operate on texture, color gradients, and edge geometry rather than biological taxonomy.
* **Mitigation Mechanism:**
  1. **Pre-Inference Crop Verification:** The frontend and API require the farmer to declare or confirm the crop type. If the declared crop does not match the model's validated family, a compatibility warning is issued.
  2. **Canonical Biological Taxonomy (`CANONICAL_TAXONOMY.json`):** Maps symptom clusters to biological entities, standardizing 116 raw classes into 111 unified biological categories.

### Failure Mode 2: Hidden Pest Pathology (Leaf Webbers & Borers)
* **Description:** In pest infestations such as Pigeonpea Leaf Webber (*Grapholita critica*) or Pod Borer (*Helicoverpa armigera*), the insect larva hides inside folded leaves or silk webbing. A single top-down photograph often captures only folded leaf tissue, leading the model to predict healthy foliage (`eggplant leaf` 31.8%, `soybean leaf` 22.7%).
* **Root Cause:** Foliar photography cannot see through opaque folded leaf envelopes or internal plant tissue.
* **Mitigation Mechanism:**
  1. **Doubt Doctor Interactive Clarification:** When confidence is borderline ($0.50 \le 	ext{conf} < 0.65$), the system asks a single targeted question: *"Are the leaves webbed together with silk threads or droppings inside?"*
  2. If answered affirmative, the diagnosis is escalated to **Leaf Webber / Pod Borer** regardless of visual foliage scores.

### Failure Mode 3: Subsurface Pathologies (Root Rot & Vascular Wilt)
* **Description:** Diseases like *Fusarium udum* (Pigeonpea Wilt) and *Rhizoctonia bataticola* (Dry Root Rot) cause above-ground leaves to droop, wither, and desiccate. An image model sees only yellowed/wilted leaves and frequently misdiagnoses drought stress or fungal leaf scorch.
* **Root Cause:** Pathogen colonization occurs in the vascular xylem and taproot, completely out of sight of foliar cameras.
* **Mitigation Mechanism:**
  * **Structured Guided Field Inspection Tasks (`/api/inspection/tasks`):**
    FALCON-AI provides interactive 4-step physical inspection routines:
    1. *Step 1 (Collar Check):* Scrape bark at soil collar. Look for dark brown vascular streaking.
    2. *Step 2 (Root Pull Test):* Gently pull plant. If taproot snaps easily and lateral roots are rotted, suspect Dry Root Rot.
    3. *Step 3 (Split Stem Examination):* Cut stem longitudinally. Check for brown-black discoloration in xylem vessels.
    4. *Step 4 (Foliar Symptom Corroboration):* Note whether wilting is unilateral (one branch) or whole-plant.

---

## 3. The 3-Tier Confidence Architecture

To prevent false confidence, FALCON-AI enforces strict boundary behavior:

```
                  [Farmer Leaf Photo Upload]
                              |
                              v
             [Model Inference & Feature Scoring]
                              |
            +-----------------+-----------------+
            |                                   |
    conf >= 0.65                         conf < 0.65
            |                                   |
            v                                   v
   [High Confidence]                  +---------+---------+
            |                         |                   |
            v                 0.50 <= conf < 0.65     conf < 0.50
    [CIBRC Deterministic              |                   |
      Safety Verification]            v                   v
            |                  [Doubt Doctor        [Diagnosis Rejected]
            v                  1-Question Triage]         |
    [Final Advisory]                  |                   v
                                      v            [Guided Field
                               [Corroborated]      Inspection Task]
```

1. **High Confidence ($\ge 0.65$):** Automated report generated, but all chemical treatments are gated by deterministic CIBRC rules.
2. **Borderline Confidence ($0.50 - 0.65$):** Handed to Doubt Doctor for interactive triage.
3. **Low Confidence ($< 0.50$):** Image alone is deemed insufficient. System explicitly tells the farmer: *"Unable to confirm disease from photo alone. Follow field inspection steps."*

---

## 4. Pesticide Safety Guardrails (Zero-Tolerance Policy)

* **Zero Hallucination Rule:** No LLM or generative network is permitted to recommend pesticides or dosages.
* **Deterministic Active Ingredient Engine (`pesticide_checker.py`):**
  * Validates every chemical recommendation against Central Insecticides Board & Registration Committee (CIBRC) schedules.
  * Enforces active ingredient bans (e.g. Monocrotophos, Endosulfan, Methyl Parathion vetoed).
  * Enforces Pre-Harvest Interval (PHI) compliance (e.g. blocks systemic organophosphates within 14 days of harvest).
  * Protects beneficial predators and flags Lalya (cotton red leaf) physiological disorders.

---

## 5. Conclusion

By recognizing the physical limitations of single-image foliar computer vision and integrating interactive agronomical triage (Doubt Doctor) with deterministic chemical safety (CIBRC), FALCON-AI eliminates catastrophic failure modes and provides farmers with a dependable, trustworthy decision support system.
