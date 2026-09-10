# FALCON-AI: Multi-Class Soybean (MH) Bounding-Box Annotation Plan
**SIH 26131 — Early Detection and Management of Crop Diseases and Pest Infestations**  
**Government of Maharashtra | Department of Skills, Employment, Entrepreneurship and Innovation**  
**Dataset:** Multi-Class Soybean Leaf Disease Dataset (`10.17632/6fhphxg297.2`)  
**Status:** REQUIRED BEFORE PHASE 4C TRAINING | STRICT ZERO-FABRICATION MANDATE  

---

## 1. Executive Summary & Physical Inspection Audit

During the Phase 4B/4C physical filesystem audit, candidate dataset `10.17632/6fhphxg297.2` (authored by Thorwat, Magdum, Jadhav, Sutar, Oswal, Maharashtra Agricultural Research Group) was audited.

### Forensic Findings:
- **Physical Availability:** Archive file (`6fhphxg297-2.zip`, 2.03 GB) is currently cataloged via verified DataCite S3 metadata (`9527630a...`), but was held from automated ingestion due to Mendeley's Cloudflare anti-bot challenge.
- **Total Claimed Images:** 4,500 natural field images captured in the Sangli/Kolhapur/Western Maharashtra soybean belt.
- **Source Format:** Whole-image folder-level classification.
- **Existing Annotations:** **0 bounding boxes exist in the source dataset.**
- **Bounding Box Policy:** **Strict Zero-Fabrication.** Automated pseudo-bounding or rectangular heuristics are strictly forbidden. Field-grade pathological ground-truth requires human-in-the-loop expert annotation.

---

## 2. Dataset Characteristics & Class Distribution

| Class Index | Source Class Name | Canonical Target Label | Estimated Count | Visual Pathology Characteristics |
| :---: | :--- | :--- | :---: | :--- |
| **0** | `Bacterial Blight` | `soybean_bacterial_pustule` | ~900 | Angular, water-soaked lesions turning brown/black with conspicuous translucent yellow chlorotic halos. |
| **1** | `Cercospora Leaf Blight` | `soybean_cercospora_leaf_blight` | ~900 | Diffuse reddish-purple to bronze upper-canopy discoloration; affected leaves take on a distinct leathery/cupped texture. |
| **2** | `Sudden Death Syndrome` | `soybean_sudden_death_syndrome` | ~950 | Punctate interveinal chlorotic spots expanding into coalescing interveinal necrosis while the midrib and primary veins remain green. |
| **3** | `Soybean Rust` | `soybean_rust` | ~950 | Polygonal tan to dark brown lesions on lower leaf surfaces with raised, volcano-shaped eruptive pustules (*uredinia*). |
| **4** | `Healthy` | `soybean_healthy_leaf` | ~800 | Uninfected, fully expanded green trifoliate soybean leaves. |

---

## 3. Target Annotation Format

Every image will be paired with an isolated YOLO text file (`.txt`) with normalized floating-point coordinates:
```text
<class_id> <x_center> <y_center> <width> <height>
```
- Coordinates normalized between `0.000000` and `1.000000`, rounded to 6 decimal places.
- Image resolution: Native high-resolution field imagery (~3000 x 2000 pixels) must be preserved during annotation to retain micro-lesion detail. Downsampling to 640x640 will occur solely at model training time.

---

## 4. Rigorous Pathology Annotation Guidelines

### A. Soybean Rust (*Phakopsora pachyrhizi*) — The Micro-Pustule Challenge
1. **Pustule Colony Bounding:** A single soybean leaflet infected with Asian Soybean Rust may contain thousands of microscopic pustules (0.1–0.3 mm). Individual bounding is visually and computationally impractical.
2. **Annotation Directive:** Annotators must delineate **colony clusters** — bounding contiguous groups of active rust pustules.
3. **Abaxial Surface Focus:** Annotators must confirm lesions exhibit eruptive abaxial pustules rather than flat superficial spots (to distinguish from Brown Spot / *Septoria glycines*).

### B. Sudden Death Syndrome / SDS (*Fusarium virguliforme*)
1. **Interveinal Necrosis Delineation:** Draw bounding boxes around the symptomatic interveinal necrotic strips.
2. **Preserving Green Vein Contrast:** Ensure bounding boxes capture the contrast between dead interveinal tissue and the viable green veins, as this differential pattern is the hallmark visual diagnostic signature of SDS.

### C. Bacterial Blight (*Pseudomonas savastanoi* pv. *glycinea*)
1. **Angular Lesion Bounding:** Annotate the distinctive vein-bounded angular brown spots.
2. **Halo Inclusion:** The characteristic bright yellow-green chlorotic halo must be encompassed inside the bounding box.
3. **Tear / Ragged Hole Handling:** In advanced infections, dead centers drop out, leaving ragged shot-holes. Annotators must bound the entire ragged lesion including the border margin.

### D. Healthy Leaves
- Paired with an empty 0-byte `.txt` file for negative-class model training to suppress false positive alerts on healthy canopies.

---

## 5. Tooling, Roles & Quality Control

### A. Recommended Tooling
- **Primary Tool:** **CVAT (Computer Vision Annotation Tool)** v2.x with Docker deployment.
- **Project Structure:** 5 tasks partitioned by pathogen class to enable specialized annotator focus.

### B. Dual-Annotator Cross-Validation
- 20% of the dataset (900 images: 180 per class) will be assigned concurrently to two independent certified annotators.
- **Intersection-over-Union (IoU) Threshold:**
  - $	ext{IoU} \ge 0.70$ with concordant class label: **APPROVED**.
  - $0.50 \le 	ext{IoU} < 0.70$: Sent to Senior Pathologist for boundary trim.
  - $	ext{IoU} < 0.50$ or class disagreement: Rejected for multi-expert review.

### C. Reviewer Credentials
- Reviewers must be certified agronomists or plant pathologists from:
  - ICAR-Indian Institute of Soybean Research (IISR), Indore
  - Mahatma Phule Krishi Vidyapeeth (MPKV), Rahuri (Department of Plant Pathology)
  - Vasantrao Naik Marathwada Krishi Vidyapeeth (VNMKV), Parbhani
