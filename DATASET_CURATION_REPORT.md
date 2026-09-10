# FALCON-AI: Dataset Curation Audit Report — Novel Pigeonpea (PPLD)

**Dataset:** Novel Pigeonpea Leaf Dataset (`PPLD.zip`)  
**DOI:** 10.17632/bd553pdtny.1  
**Audit Timestamp:** 2026-09-09  
**Audit Tool:** `datasets/scripts/leakage_and_quality_guard.py`  

---

## 1. Summary Statistics

- **Total Specimen Images Analyzed:** 973
- **Readable & Structurally Valid:** 973 (100.0%)
- **Corrupt / Truncated / Zero-Byte:** 0
- **Exact Cryptographic Duplicates (SHA256):** 58
- **Resolution Uniformity:** 100% normalized at 256x256 px RGB JPEG
- **Class Breakdown:**
  - **Healthy**: 196 specimens
  - **Leaf_Spot**: 336 specimens
  - **Leaf_webber**: 149 specimens
  - **Sterilic_mosaic**: 292 specimens

---

## 2. Integrity Certification

- **Archive Integrity:** Verified via ZIP CRC32 and SHA256 checksums.
- **Image Header Integrity:** Verified via PIL binary verification and OpenCV matrix decode.
- **Agronomic Verification:** Corresponds to 4 biological conditions in pigeonpea:
  1. *Sterilic_mosaic*: Sterility mosaic virus (bushy stunting, small pale leaflets)
  2. *Leaf_Spot*: Cercospora leaf spot (circular necrotic foliar lesions)
  3. *Leaf_webber*: Grapholita critica caterpillar webbing
  4. *Healthy*: Clean negative control foliage
