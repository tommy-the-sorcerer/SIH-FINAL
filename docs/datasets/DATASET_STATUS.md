# FALCON-AI: Dataset Acquisition & Verification Status

**Problem Statement SIH26131:** Early detection and management of crop diseases and pest infestations  
**Client / Ministry:** Government of Maharashtra (Maharashtra State Innovation Society / Dept. of Agriculture)  
**Audit Timestamp:** 2026-09-09T13:35:00+05:30  
**Absolute Rule:** ZERO FABRICATION. Every file listed corresponds to authentic, verifiable research datasets.  

---

## 1. Dataset Status Register

| Dataset Name | Source / DOI | Crop | Modality & Classes | Actual Files / Size | Status | Verification Detail |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Novel Pigeonpea (PPLD)** | Mendeley Data / `10.17632/bd553pdtny.1` | Pigeonpea (तूर) | Classification (4 classes: SMD, Cercospora, Leaf Webber, Healthy) | 1,000 JPGs · 12,354,713 B | **INGESTING (86%)** | Resumable download active. CRC32 / SHA256 verified. |
| **Cotton-Pune Tabular** | Mendeley Data / `10.17632/533j2mzd4s.1` | Cotton (कापूस) | Agronomic Symptoms & Treatments (12 conditions) | 82 rows · 14,770 B | **CURATED FOR IPM** | Accepted for IPM rules; rejected for vision (0 images). |
| **CottonPest-BD** | Mendeley Data / `10.17632/wkjg6srrk8.2` | Cotton (कापूस) | Object Detection (4 pests + 3 beneficial predators) | 1,625 images · 224,597,620 B | **QUARANTINED** | Beneficial predators segregated to prevent insecticide sprays. |
| **Soybean-MH Multi-Class** | Mendeley Data / `10.17632/6fhphxg297.2` | Soybean (सोयाबीन) | Classification (Rust, SDS, Blight, Cercospora, Healthy) | 4,500 images · 2.03 GB | **QUEUED** | DataCite metadata verified; awaiting S3 allocation. |
| **Onion Leaf Disease** | Mendeley Data / `10.17632/7nxxn4gj5s.1` | Onion (कांदा) | Classification (Purple Blotch, Stemphylium, Healthy) | RAR Archive · 16,346,221 B | **FORMAT GATED** | Requires unrar binary in container; queued for unpacking. |
| **Baseline Multiclass Benchmark** | Baseline Production Model | 12 Crops | 116 Classes (YOLO detection & classification) | 436.0 MB frozen weights | **FROZEN IN PRODUCTION** | Benchmark mAP@0.50 = 69.89%. Untouched immutable reference. |

---

## 2. Integrity & Forensic Screening Verification

Every incoming dataset passes through `datasets/scripts/leakage_and_quality_guard.py` with 9 automated gates:
1. **Cryptographic SHA256 & CRC32 Verification:** Guarantees bit-for-bit file integrity.
2. **Exact Byte Duplicate Elimination:** SHA256 hash sets eliminate redundant image instances.
3. **Perceptual Near-Duplicate Elimination:** 64-bit difference hash (dHash) with Hamming distance threshold $\le 4$ removes near-identical bursts.
4. **Image Decodability & Header Verification:** PIL and OpenCV verify matrix integrity; rejects truncated or zero-byte files.
5. **Blank & Non-Plant Detection:** Vegetation color variance check flags blank backgrounds.
6. **Group-Aware Partitioning:** Plant-level and sequence-level grouping prevents same-plant leakage across Train, Val, and Golden Test.
7. **Beneficial Predator Quarantining:** Coccinellids, Chrysopids, and Syrphids quarantined to prevent pesticide recommendations.
