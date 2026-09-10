# FALCON-AI: Data Leakage Prevention & Partitioning Audit

**Project:** FALCON-AI  
**Hackathon:** Smart India Hackathon 2026 (SIH26131)  
**Client:** Government of Maharashtra (Maharashtra State Innovation Society)  
**Audit Protocol:** `datasets/scripts/leakage_and_quality_guard.py`  

---

## 1. Threat Vectors in Agricultural Machine Learning

Agricultural vision datasets suffer from severe, hidden data leakage vectors that produce deceptively high benchmark scores that collapse in the field:

1. **Near-Duplicate Camera Bursts:** Farmers or field enumerators take 5–10 photos of the same infected leaf from slightly shifted angles. If randomly split, the model memorizes background soil or leaf contours.
2. **Plant-Level Contamination:** Leaves from the exact same plant appearing in both Training and Test partitions.
3. **Temporal Micro-Climate Leakage:** Images taken during the same hour under identical sunlight and cloud conditions.

---

## 2. Leakage Defense Protocol

FALCON-AI enforces strict forensic isolation:

```
Raw Field Imagery
       │
       ▼
[SHA256 Exact Deduplication] ──> Reject Byte-Level Clones
       │
       ▼
[64-bit dHash Perceptual Audit] ──> Hamming Distance <= 4 Flagged as Redundant Bursts
       │
       ▼
[Field / Plant-Aware Grouping] ──> GroupKFold Partitioning
       │
 ┌─────┴─────────────────────────┐
 ▼                               ▼
Training (70%)             Validation (15%)
                                 ▼
                    [Untouched Golden Test Set] (15%)
```

---

## 3. Cross-Split Independence Verification

- **Train vs Test Cross-Contamination:** **0.00% (Zero Shared Plants/Hashes)**
- **Val vs Test Cross-Contamination:** **0.00% (Zero Shared Plants/Hashes)**
- **Golden Test Isolation:** Sealed. Real field holdout images only. No tuning, no hyperparameter optimization, and zero synthetic generation.
