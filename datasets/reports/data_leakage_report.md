# Data Leakage & Contamination Prevention Report
**Phase:** 4B Forensic Curation  

---

## 1. Train / Validation / Test Contamination Risks
1. **The PlantDoc Web-Scraping Leakage Risk:**
   - PlantDoc scraped multiple crops of identical photos from web search engines.
   - If an un-deduplicated random split is used, identical leaves with different crops appear in both Train and Validation sets.
   - **Mitigation:** Enforce Perceptual Hashing (pHash with Hamming distance threshold $\le 4$) to purge near-duplicate crops across splits before Phase 4C retraining.

2. **The Farm-Level Partitioning Mandate:**
   - Datasets like Novel Pigeonpea were collected on Hittinahalli Campus.
   - Images taken from the same plant branch must **never** be divided across train and test partitions.
   - **Mitigation:** When Phase 4C train/val/test partitions are compiled, partition at the plant/sequence level, allocating 70% Train, 15% Validation, and 15% Holdout.

## 2. Golden Test Set Status
- **Current Status:** **"Golden field test set not yet available."**
- In strict adherence to Phase 4B rules, **no synthetic or fake test images have been fabricated**.
- A dedicated 2,500-image holdout partition spanning Maharashtra agro-climatic conditions will be assembled and locked in Phase 4C prior to model retraining.
