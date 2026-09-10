# FALCON-AI: Novel Pigeonpea Bounding-Box Annotation Plan
**SIH 26131 — Early Detection and Management of Crop Diseases and Pest Infestations**  
**Government of Maharashtra | Department of Skills, Employment, Entrepreneurship and Innovation**  
**Dataset:** Novel Pigeonpea Leaf Dataset (`10.17632/bd553pdtny.1`)  
**Status:** REQUIRED BEFORE PHASE 4C TRAINING | STRICT ZERO-FABRICATION MANDATE  

---

## 1. Executive Summary & Audit Finding

During the Phase 4B/4C forensic audit, the Novel Pigeonpea Leaf Dataset (authored by Dr. G.G. Rajput and Vanita Doddamani, Vijayapur, Karnataka) was examined. The dataset comprises 1,000 field images (256x256 px JPG) organized across 4 classification folders.

> [!CRITICAL]
> **Audit Finding:** **0 bounding box annotations exist.**  
> The current active model (`Models/PlantDiseaseDetection.pt`) is an **object detection model (YOLO)** requiring normalized spatial coordinates `(class_id, x_center, y_center, width, height)`. Feeding image-level classifications into a bounding-box detection pipeline without spatial localization degrades mAP and causes hallucinated bounding boxes.
> 
> **Zero-Fabrication Policy:** We **STRICTLY REFUSE** to programmatically fabricate synthetic bounding boxes (e.g. naive whole-image boxes `[0.5, 0.5, 1.0, 1.0]` or unverified heuristic blob contours). True agrarian diagnostic reliability demands verified human-in-the-loop expert annotations.

---

## 2. Target Annotation Format

Every image will be paired with a standard YOLO text annotation file with matching basename:
- Image: `<basename>.jpg`
- Annotation: `<basename>.txt`

### Format Specification:
```text
<class_id> <x_center> <y_center> <width> <height>
```
- All coordinate values are normalized floats between `0.000000` and `1.000000`, rounded to 6 decimal digits.
- Formulas:
  $$x_{	ext{center}} = rac{x_{\min} + x_{\max}}{2 	imes W}$$
  $$y_{	ext{center}} = rac{y_{\min} + y_{\max}}{2 	imes H}$$
  $$w = rac{x_{\max} - x_{\min}}{W}$$
  $$h = rac{y_{\max} - y_{\min}}{H}$$
  where $W = 256$, $H = 256$.

---

## 3. Class Mapping & Canonical Ontology

All classes map directly to the FALCON-AI Canonical Registry ([`datasets/manifests/CANONICAL_LABELS_REGISTRY.json`](file:///c:/Users/lenovo/Desktop/RoboticDrones/RoboticDrones/datasets/manifests/CANONICAL_LABELS_REGISTRY.json)):

| Proposed YOLO Class ID | Source Folder Name | Canonical Label | Taxonomy Category | Agronomic Entity | Total Source Images | Annotation Target |
| :---: | :--- | :--- | :---: | :--- | :---: | :--- |
| **0** | `Cercospora Leaf Spot` | `tur_cercospora_leaf_spot` | Disease | *Cercospora cajani* (Fungal) | 336 | Discrete brown necrotic spots with dark rings |
| **1** | `Sterilic Mosaic` | `tur_sterility_mosaic` | Disease | Pigeonpea Sterility Mosaic Virus (PPSMV) | 292 | Chlorotic leaf mottle / yellow mosaic lamina patches |
| **2** | `Leaf Webber` | `tur_leaf_webber_damage` | Damage / Pest | *Grapholita critica* (Entomological) | 146 | Silk webbing folds, skeletonized leaf lamina |
| **3 / None** | `Healthy` | `tur_healthy_leaf` | Healthy | Vigorous uninfected pigeonpea leaf | 196 | Empty `.txt` file (negative background frame) |

> [!NOTE]
> For class `Healthy`, standard YOLO best practice is to maintain an empty 0-byte `.txt` file to train the model against background false positives. For dual multi-task verification, annotators will also generate a secondary polygon mask of the healthy leaflet.

---

## 4. Rigorous Agronomic Annotation Guidelines

### A. Cercospora Leaf Spot (*Cercospora cajani*)
1. **Isolated Lesions:** Draw tight bounding boxes around individual circular or sub-circular brown spots. Do not include excessive healthy green margin (> 2 pixels margin).
2. **Confluent Lesion Clusters:** When multiple fungal lesions coalesce into a contiguous necrotic blight patch, annotate the entire merged lesion as a single cluster bounding box.
3. **Petioles and Veins:** If lesions extend onto secondary veins, include the affected vein tissue within the box.

### B. Sterility Mosaic Disease (PPSMV)
1. **Nature of Pathology:** Sterility mosaic is a viral, systemic infection transmitted by the eriophyid mite (*Aceria cajani*). It exhibits diffuse, irregular yellow-green chlorotic mottling rather than distinct punctate spots.
2. **Bounding Scope:** Annotators must draw bounding boxes around each affected **leaflet** or distinct **chlorotic mosaic sector**. Do not bound the whole frame if surrounding leaflets are unaffected.
3. **Differentiating Nutrient Chlorosis:** If chlorosis is uniform across the entire lamina without mosaic mottling (indicative of nitrogen/iron deficiency), tag image as `FLAG_ABIOTIC_CHLOROSIS` for pathologist review.

### C. Leaf Webber (*Grapholita critica*)
1. **Nature of Damage:** Larvae web leaves together with silken threads, feeding internally on chlorophyll.
2. **Bounding Scope:** Bounding boxes must tightly encapsulate:
   - The webbed silk shelter.
   - The folded or curled leaf margins held by silk.
   - Visible frass (excrement) and skeletonized leaf patches.
3. **Larval Sightings:** If the actual caterpillar larva is visible outside the web, draw a distinct bounding box with label `tur_leaf_webber_damage`.

---

## 5. Tooling Recommendation & Setup

| Tool | Deployment | Strengths for FALCON-AI | Recommendation Level |
| :--- | :--- | :--- | :---: |
| **CVAT (Computer Vision Annotation Tool)** | Self-hosted Docker or CVAT.ai | Full YOLO 1.1 export, multi-user role separation, SAM semi-auto bounding | **PRIMARY (RECOMMENDED)** |
| **Label Studio** | Self-hosted Python / Open Source | Native REST API integration with FALCON-AI backend | **SECONDARY** |
| **Roboflow** | Cloud Hosted | Automated dataset health, split distribution checks | **ACCEPTABLE CLOUD** |

### Recommended CVAT Configuration:
- Project: `FALCON_AI_PIGEONPEA_PHASE4C`
- Task Classes:
  - `tur_cercospora_leaf_spot` (Color: `#FF5722` Orange-Red)
  - `tur_sterility_mosaic` (Color: `#FFEB3B` Amber-Yellow)
  - `tur_leaf_webber_damage` (Color: `#9C27B0` Purple)
  - `tur_healthy_leaf` (Color: `#4CAF50` Green)

---

## 6. Quality Control & Reviewer Protocol

### A. Inter-Annotator Agreement (IAA)
- **Validation Sample:** A randomly selected 20% validation split (200 images: 67 Cercospora, 58 Mosaic, 29 Webber, 46 Healthy) is annotated independently by two certified annotators.
- **Metric:** Intersection-over-Union (IoU) of bounding boxes:
  $$	ext{IoU}(A, B) = rac{	ext{Area}(A \cap B)}{	ext{Area}(A \cup B)}$$
- **Approval Thresholds:**
  - $	ext{IoU} \ge 0.70$ and identical class: **AUTO-APPROVED**.
  - $0.50 \le 	ext{IoU} < 0.70$: **FLAGGED FOR REVIEW** (Reviewer trims coordinates).
  - $	ext{IoU} < 0.50$ or class disagreement: **REJECTED** (Referred to Senior Plant Pathologist).

### B. Pathological Reviewer Qualifications
- Reviewers must possess accredited agronomic qualifications (M.Sc. or Ph.D. in Plant Pathology or Agricultural Entomology) from accredited institutions:
  - Vasantrao Naik Marathwada Krishi Vidyapeeth (VNMKV), Parbhani
  - Mahatma Phule Krishi Vidyapeeth (MPKV), Rahuri
  - Dr. Panjabrao Deshmukh Krishi Vidyapeeth (PDKV), Akola
  - ICAR-Indian Institute of Pulses Research (IIPR), Kanpur / Regional Station

### C. Ambiguous Image Handling
- Images with severe blur, sensor noise, or low illumination where symptoms cannot be diagnosed with > 90% human certainty will be tagged `QUARANTINED_AMBIGUOUS` and permanently excluded from the training split.
- Source images remain 100% read-only and immutable.
