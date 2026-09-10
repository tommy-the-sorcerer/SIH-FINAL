# Forensic Duplicate Detection & Quarantine Report
**Phase:** 4B Forensic Curation  
**Status:** Audit Completed  

---

## 1. Intraset Duplication Analysis
- **Cotton Plant Disease (Pune):** Contains 1 CSV file (`Data.csv`). Zero image files exist. Zero image duplicate risk.
- **Novel Pigeonpea (Vijayapur):** 1,000 distinct photographs taken at varied angles under field conditions. MD5 hash verification reveals zero exact binary duplicates across classes.

## 2. Cross-Dataset Biological Duplicate Concepts
Forensic cross-referencing against the baseline 116-class model (`PlantDiseaseDetection.pt`) identified 5 duplicate concept pairs that must be merged in `CANONICAL_LABELS_REGISTRY.json`:
1. `corn rust` (Class 0) <--> `Corn rust leaf` (Class 109) -> Action: MERGE into `corn_rust`
2. `corn gray leaf spot` (Class 25) <--> `Corn Gray leaf spot` (Class 97) -> Action: MERGE into `corn_gray_leaf_spot`
3. `corn smut` (Class 82) <--> `Corn Smut` (Class 102) -> Action: MERGE into `corn_smut`
4. `tomato mosaic virus` (Class 69) <--> `Tomato leaf mosaic virus` (Class 114) -> Action: MERGE into `tomato_mosaic_virus`
5. `tomato yellow leaf curl virus` (Class 88) <--> `Tomato leaf yellow virus` (Class 115) -> Action: MERGE into `tomato_yellow_leaf_curl_virus`

## 3. Quarantine Actions
- **CottonPest-BD Quarantined Classes:**
  - `Lady Beetle` (438 images)
  - `Green Lacewings` (300 images)
  - `Hoverfly` (108 images)
  - **Reason for Quarantine:** These are beneficial predators. Training them under a generic "cotton pest" label would train the model to recommend pesticides against farmer-friendly biological control organisms.
