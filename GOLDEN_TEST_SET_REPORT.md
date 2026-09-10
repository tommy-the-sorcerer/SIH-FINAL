# FALCON-AI: Golden Test Set Verification Report

**Project:** FALCON-AI (SIH 2026 Problem Statement SIH26131)  
**Client / Ministry:** Government of Maharashtra (Maharashtra State Innovation Society)  
**Integrity Status:** **SEALED & READY (100% REAL IMAGES · ZERO SYNTHETIC)**  
**Audit Timestamp:** 2026-09-09  

---

## 1. Composition Summary

The Golden Test Set contains **141 real, untouched holdout images** strictly isolated from all training and validation sets:

| Crop | Class / Condition | Image Count | Resolution | Provenance |
| :--- | :--- | :---: | :---: | :--- |
| **Pigeonpea (तूर)** | Sterility Mosaic Disease (SMD) | 35 | 256x256 px | Doddamani & Rajput (2024), Vijayapur |
| **Pigeonpea (तूर)** | Cercospora Leaf Spot | 50 | 256x256 px | Doddamani & Rajput (2024), Vijayapur |
| **Pigeonpea (तूर)** | Leaf Webber (*Grapholita*) | 22 | 256x256 px | Doddamani & Rajput (2024), Vijayapur |
| **Pigeonpea (तूर)** | Healthy Canopy | 29 | 256x256 px | Doddamani & Rajput (2024), Vijayapur |
| **Maize (मका)** | Fall Armyworm | 1 | Real Field Specimen | Maharashtra Field Enumeration |
| **Tomato (टोमॅटो)** | Late Blight | 1 | Real Field Specimen | Maharashtra Field Enumeration |
| **Cotton (कापूस)** | Bacterial Blight | 1 | Real Field Specimen | Maharashtra Field Enumeration |
| **Multi-Crop** | Healthy Control | 1 | Real Field Specimen | Maharashtra Field Enumeration |
| **Out-of-Distribution** | Non-Plant / Ambiguous | 1 | Real Field Specimen | Negative Control Baseline |
| **TOTAL** | **All Evaluated Classes** | **141** | Real Imagery | **100% Real · Zero Synthetic** |

---

## 2. Leakage Protection Verification

- **Exact Duplicate Check:** 0 duplicates with training data.
- **Perceptual dHash Audit:** Hamming distance >= 4 against all training entries.
- **Sealing Rule:** This test set is immutable. No hyperparameters or weights are tuned against it.
