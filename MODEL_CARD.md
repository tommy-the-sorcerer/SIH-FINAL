# Model Card: FALCON-AI Baseline Crop Health Diagnostic Model

**Model Identifier:** `Models/PlantDiseaseDetection.pt`  
**Model Family:** Ultralytics YOLOv8 Deep Detection Architecture  
**Release Date:** 2026-09-09 (Frozen Baseline)  
**Governance Protocol:** Immutable Baseline Lock (Zero Premature Overwrite Rule)  
**Client / Ministry:** Government of Maharashtra (Maharashtra State Innovation Society / Department of Agriculture)  

---

## 1. Model Overview

| Characteristic | Specification |
| :--- | :--- |
| **Architecture** | YOLOv8 Convolutional Feature Backbone with Decoupled Anchor-Free Detection Head |
| **Model File Size** | 457,175,703 bytes (436.0 MB) |
| **Class Cardinality** | 116 classes across 12 crop families |
| **Input Tensor Format** | Normalized RGB $[1 \times 3 \times 640 \times 640]$ float32 |
| **Host Runtime Target** | Intel Core Multi-Core CPU (14 Physical / 20 Logical Threads), 24 GB RAM |
| **Software Framework** | PyTorch 2.14.0+cpu, Ultralytics 8.1+ |
| **Load Time** | 0.257 seconds |
| **Runtime Memory Delta** | 585.7 MB RAM |
| **CPU Inference Latency** | Cold: 1,026.5 ms · Steady-State: ~590.2 ms per specimen |

---

## 2. Intended Use & Application Boundaries

### 2.1. Primary Intended Uses
- Handheld smartphone scouting by Maharashtra smallholder farmers in Marathi, Hindi, and English.
- Agricultural Extension Officer triage and Taluka-level outbreak surveillance.
- Static Raspberry Pi / Village Kiosk leaf diagnostic scanning stations.

### 2.2. Out-of-Scope & Prohibited Applications
- **NO DRONES:** This model is calibrated for close-range foliar photography ($15\text{ cm} - 60\text{ cm}$). It must NEVER be deployed on aerial drone platforms.
- **Autonomous Pesticide Spraying:** The neural network is strictly barred from approving pesticides. All chemical prescriptions are evaluated deterministically via CIBRC/ICAR gazettes.
- **Single-Model Outbreak Declaration:** A single inference detection can never trigger a regional quarantine without field confirmation.

---

## 3. Baseline Performance Metrics

*Audited reference baseline metrics on historical benchmark holdout:*

| Metric | Measured Baseline Value | Evaluation Notes |
| :--- | :---: | :--- |
| **mAP@0.50** | **69.89%** | Primary evaluation metric for model promotion gate |
| **mAP@0.50-0.95** | **68.56%** | High-iou bounding localization across foliar lesions |
| **Mean Precision** | **63.50%** | Minimizes false positive alarms on healthy foliage |
| **Mean Recall** | **68.20%** | Detects active lesions and chewing pests |
| **Golden Test Set Latency** | **~590 ms** | Real-time performance on standard non-GPU laptops |

---

## 4. Multi-Tiered Safety Gating Hierarchy

```
Camera Specimen -> [OpenCV Quality Guard] (Rejects blur / darkness)
       │
       ▼
[YOLOv8 Inference] (Extracts confidence & bounding boxes)
       │
 ┌─────┴─────────────────────────────────────────────┐
 ▼                                                   ▼
Confidence >= 70%                             50% <= Conf < 65%
(Crop-Compatible)                                    │
       │                                             ▼
       │                              [Doubt Doctor™ Interactive Gate]
       │                                     │
       │                      ┌──────────────┴──────────────┐
       │                      ▼                             ▼
       │                Farmer: YES                   Farmer: NO
       │           (Confidence Boosted)          (Escalate to Officer)
       ▼                      │                             │
[CIBRC Deterministic Safety Engine] <───────────────────────┘
       │
       ├─> Banned Ingredient? ──> STRICTLY PROHIBITED
       ├─> Lalya Reddening?   ──> CHEMICAL VETO (MgSO4 + DAP)
       ├─> Beneficial Insect? ──> PREDATOR CONSERVATION VETO
       └─> CIBRC Approved?    ──> Validated Dosage & Waiting Days
```

---

## 5. Model Promotion & Rollback Protocol

- **Baseline Immutability:** `Models/PlantDiseaseDetection.pt` is permanent and protected against in-place overwriting.
- **Promotion Threshold:** Any newly trained candidate model must achieve $\text{mAP@0.50} > 69.89\%$ on the exact 141-image Golden Test Set without regressions on Maharashtra priority crops.
- **Rollback Guarantee:** The baseline model file remains on disk at all times. If a promoted candidate encounters production edge-case degradation, rollback requires a single configuration pointer swap in `pipeline.py`.
