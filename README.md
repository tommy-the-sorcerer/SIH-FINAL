# FALCON-AI | Farmer-First Crop Disease & Pest Management Platform
### Smart India Hackathon 2026 (SIH 2026) — Problem Statement SIH26131

> **Title:** "Early detection and management of crop diseases and pest infestations"  
> **Organization:** Government of Maharashtra  
> **Department:** Maharashtra State Innovation Society, Department of Skills, Employment, Entrepreneurship and Innovation  
> **Category:** Software | **Theme:** Agriculture, FoodTech & Rural Development  
> **Platform Type:** 100% Ground-Level Scouting, Smartphone & Edge Kiosk (Zero Drone Dependence)

---

## 🌾 Overview & Problem Statement Alignment

FALCON-AI is an intelligent, farmer-first crop disease and pest management platform engineered specifically for Maharashtra's agro-climatic zones and smallholder farming communities. 

Built strictly for **ground-level field scouting via smartphone cameras, rural community kiosks, and digital pest traps**, the platform completely eliminates aerial drone dependencies. It addresses the core failure modes of computer vision in agriculture through an ensemble of deep learning, deterministic chemical safety verification, and interactive agronomic triage:

1. **Pre-Inference OpenCV Quality Guard:** Intercepts out-of-focus, over-exposed, dark, or non-foliar uploads before inference to prevent garbage-in-garbage-out errors.
2. **Deterministic Baseline Vision Engine:** Powered by a 116-class YOLOv8 deep neural detector (`Models/PlantDiseaseDetection.pt`, 436.00 MB), delivering **591.90 ms median latency (p50)** on standard CPU hardware.
3. **Sealed Golden Test Set (141 Authentic Images):** Empirically validated against genuine field specimens from the Mendeley Novel Pigeonpea Leaf Dataset (SHA256 `ddbcf410...`) with zero synthetic images.
4. **Interactive Doubt Doctor:** Solicits a single targeted physical symptom observation when model confidence is borderline ($0.50 \le \text{conf} < 0.65$), eliminating ambiguity before taking action.
5. **Guided Field Inspection Tasks:** For subsurface and non-foliar pathologies (e.g. *Fusarium* Wilt, Dry Root Rot, Stem Borers), guides farmers through a 4-step physical inspection protocol (collar scrape, root pull, stem split).
6. **Deterministic CIBRC Pesticide Safety Engine:** All chemical recommendations are strictly validated against Central Insecticides Board & Registration Committee (CIBRC) schedules. Prohibits banned chemicals (Monocrotophos, Endosulfan) and protects natural predator insects.
7. **Live Open-Meteo Meteorological Telemetry:** Ingests live micro-climate parameters (temperature, relative humidity, wind speed) with resilient offline fallback.
8. **Transparent Rule-Based Risk Engine:** Generates explainable 0–100 risk indices (Low, Moderate, High, Critical) accounting for pathogen spread physics.
9. **Geospatial 15 km Early Warning Radius:** Alerts neighboring farms within 15 km of newly confirmed pest or disease clusters using Haversine indexing.
10. **Native Trilingual Support:** Full Marathi (`mr`), Hindi (`hi`), and English (`en`) localization tailored for Maharashtra farmers.

---

## 🏛️ System Architecture

```
                       Farmer / Field Scout (Smartphone / Edge Kiosk)
                                             │
                                             ▼
                             ┌───────────────────────────────┐
                             │   Responsive Web & PWA App    │
                             │ - Multilingual (mr, hi, en)   │
                             │ - OpenCV Quality Guardrail    │
                             │ - Doubt Doctor Triage Card    │
                             │ - Guided Physical Inspection  │
                             │ - CIBRC Safety Verifier       │
                             └───────────────┬───────────────┘
                                             │ HTTP REST / JSON
                                             ▼
                             ┌───────────────────────────────┐
                             │    FastAPI Modular Backend    │
                             │ - Auth & RBAC (Farmer/Expert) │
                             │ - Outbreak Radius Alerting    │
                             │ - Canonical Biology Taxonomy  │
                             └───────┬───────────────┬───────┘
                                     │               │
         ┌───────────────────────────┴───┐           └───────────────────────────┐
         ▼                               ▼                                       ▼
┌──────────────────────────┐    ┌──────────────────────────┐    ┌───────────────────────────────┐
│     AI Vision Engine     │    │  Deterministic Safeties  │    │        Data Persistence       │
│ - YOLOv8 (116 Classes)   │    │ - CIBRC Safety Verifier  │    │ - SQLite in WAL Mode          │
│ - Sub-second CPU Infer   │    │ - Doubt Doctor Triage    │    │ - Audit Logs & Verified Cases │
│ - 3-Tier Confidence Gate │    │ - 4-Step Inspection Tasks│    │ - GIS Outbreak Clusters       │
│ - Sealed Golden Holdout  │    │ - Open-Meteo Weather API │    │ - Farmer Profiles & Farms     │
└──────────────────────────┘    └──────────────────────────┘    └───────────────────────────────┘
```

---

## 📂 Project Directory Structure

```
SIH-FINAL-main/
│
├── 📂 app/                                # Modular Application Package
│   ├── main.py                            # FastAPI app, route handlers, error handlers
│   ├── core/                              # Foundational Infrastructure
│   │   ├── config.py                      # App settings, paths & security parameters
│   │   ├── storage.py                     # SQLite DB persistence, sessions, RBAC
│   │   ├── taxonomy.py                    # 116-class crop taxonomy, IPM advisory
│   │   └── i18n.py                        # Multilingual localization (mr, hi, en)
│   └── services/                          # Domain & Business Logic Services
│       ├── pipeline.py                    # Vision pipeline & YOLOv8 inference
│       ├── doubt_doctor.py                # Active triage engine for borderline confidence
│       ├── inspection_engine.py           # Guided 4-step physical inspection protocol
│       ├── pesticide_checker.py           # CIBRC pesticide compliance & ban verifier
│       ├── risk_engine.py                 # Multi-factor spread risk scoring
│       ├── weather_service.py             # Open-Meteo weather telemetry & cache
│       └── spread_alerts.py               # Geospatial 15 km outbreak proximity engine
│
├── 📂 docs/                               # Categorized Documentation Hub
│   ├── README.md                          # Documentation directory index
│   ├── compliance/                        # Hackathon compliance & audit records
│   │   ├── SIH26131_COMPLIANCE_AUDIT_FALCON_AI.md
│   │   ├── SIH26131_EXECUTIVE_SUMMARY.md
│   │   ├── PROJECT_AUDIT_MASTER.md
│   │   └── PROJECT_STATUS.md
│   ├── datasets/                          # Dataset forensic reports & provenance
│   │   ├── DATASET_ACQUISITION_REPORT.md
│   │   ├── DATASET_AUDIT_REPORT.md
│   │   ├── DATASET_CURATION_REPORT.md
│   │   ├── DATASET_EXPANSION_PLAN.md
│   │   ├── DATASET_PROVENANCE.md
│   │   ├── DATA_LEAKAGE_REPORT.md
│   │   ├── GOLDEN_TEST_SET_REPORT.md
│   │   └── MAHARASHTRA_CROP_COVERAGE_REPORT.md
│   ├── model/                             # Model card and evaluation metrics
│   │   └── MODEL_CARD.md
│   └── deployment/                        # Production deployment runbook
│       └── DEPLOYMENT.md
│
├── 📂 reports/                            # Automated Benchmark & Empirical Reports
│   ├── BASELINE_MODEL_REPORT.md
│   ├── MODEL_BENCHMARK_REPORT.md
│   ├── FINAL_AI_VALIDATION_REPORT.md
│   ├── FINAL_SYSTEM_VALIDATION.md
│   ├── FAILURE_ANALYSIS_REPORT.md
│   ├── MODEL_PROMOTION_DECISION.md
│   ├── SIH_COMPLIANCE_REPORT.md
│   └── EXECUTION_STATUS.md
│
├── 📂 scripts/                            # Operational & Training Scripts
│   ├── audit_bug_check.py                 # DOM and event handler verification
│   └── train_regularized.py               # Anti-overfitting YOLOv8 fine-tuning script
│
├── 📂 datasets/                           # Data Governance, Golden Tests & Manifests
│   ├── CANONICAL_TAXONOMY.json
│   ├── CLASS_MAPPING.json
│   ├── golden_test/                       # 141 authentic holdout field images
│   ├── incoming/                          # Ingestion directory
│   ├── manifests/                         # Split manifests and registries
│   ├── quarantine/                        # Out-of-focus or poor quality uploads
│   ├── rejected/                          # Non-foliar or corrupted uploads
│   ├── reports/                           # Curation audit logs
│   └── scripts/                           # Data processing utilities
│
├── 📂 Models/                             # Deep Learning Checkpoints
│   └── PlantDiseaseDetection.pt           # 116-class YOLOv8 model weights (Git LFS)
│
├── 📂 static/                             # Frontend Static Assets
│   ├── css/style.css                      # UI themes & responsive styling
│   ├── js/app.js                          # SPA frontend logic & camera module
│   ├── images/                            # Icons and graphics
│   └── uploads/                           # Uploaded specimen storage
│
├── 📂 templates/                          # Template Engine Views
│   └── index.html                         # Farmer-first dashboard SPA
│
├── 📂 tests/                              # Automated Test Suites
│   ├── conftest.py                        # Path injection configuration
│   ├── test_api_endpoints.py
│   ├── test_backend_hardening.py
│   ├── test_falcon_core_endpoints.py
│   ├── test_full_suite.py
│   ├── test_phase2_integration.py
│   ├── test_sih_suite.py
│   └── verify_prod_fixes.py
│
└── 🚀 Root Level (Entrypoints & Deployments)
    ├── main.py                            # Production entrypoint (`uvicorn main:app`)
    ├── README.md                          # Primary platform documentation
    ├── falcon_ai.db                       # SQLite database (WAL mode)
    ├── Dockerfile                         # Production container definition
    ├── docker-compose.yml                 # Service configuration
    ├── requirements.txt                   # Dependency definitions
    └── .env.example                       # Environment template
```

---

## 🔑 Demo Personas & Credentials

For evaluators and hackathon judges, instant 1-click logins are provided on the Login Modal:

| Role | Name | Phone Number | Password | Portal View |
|:---|:---|:---|:---|:---|
| **Farmer** | Ramesh Kumar Patil (Niphad, Nashik) | `8008742279` | `farmer123` | Farmer Ingestion, Doubt Doctor & Inspection |
| **Agricultural Expert** | Dr. Suresh Patil (MPKV Rahuri) | `9822012345` | `expert123` | Expert Agronomic Review Desk |
| **Agriculture Officer** | Sunil Deshmukh (Dept. of Agri) | `9423012345` | `admin123` | GIS Outbreak Hotspots & Proximity Alerts |

---

## ⚡ Empirical Baseline Benchmark Results

Tested on `datasets/golden_test/` (141 real field holdout images):

* **Model File:** `Models/PlantDiseaseDetection.pt` (436.00 MB)
* **Classes:** 116 Horticultural & Field Crop Conditions
* **Load Time:** 0.271 seconds
* **RAM Delta:** 576.2 MB
* **Median Latency (p50):** **591.90 ms**
* **90th Percentile (p90):** **645.30 ms**
* **95th Percentile (p95):** **684.00 ms**
* **Steady-State Latency:** **597.90 ms**
* **Throughput:** 1.65 images / second (CPU multi-threaded)
* **Confidence Gate:** 22.0% High, 17.7% Borderline (Doubt Doctor), 60.3% Low/Rejection

---

## 🚀 Quick Start Instructions

### Prerequisites
* Python 3.10, 3.11, or 3.12 (Python 3.11 recommended)
* Git

### 1. Setup Virtual Environment
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Automated Test Suite (28 Tests)
```bash
# Run verified test suites
python tests/test_api_endpoints.py
python tests/test_backend_hardening.py
python tests/test_phase2_integration.py
python tests/test_sih_suite.py
python tests/test_falcon_core_endpoints.py
```

### 4. Launch the Application Server
```bash
# Start server using uvicorn or python main.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# or
python main.py
```
Open your browser at: **`http://localhost:8000`**

### 5. Docker Deployment
```bash
# Build and run via Docker
docker build -t falcon-ai .
docker run -p 8000:8000 falcon-ai

# Or with Docker Compose
docker-compose up -d
```
See [DEPLOYMENT.md](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/docs/deployment/DEPLOYMENT.md) for full containerization details.

---

## 📋 Technical Documentation & Compliance Reports

* [**Documentation Hub & Index**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/docs/README.md) — Directory of all technical reports and guides.
* [**Final AI Validation Report**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/reports/FINAL_AI_VALIDATION_REPORT.md) — Master AI system audit & jury report.
* [**Model Benchmark Report**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/reports/MODEL_BENCHMARK_REPORT.md) — Latency percentiles & Golden Test Set metrics.
* [**Model Promotion Decision**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/reports/MODEL_PROMOTION_DECISION.md) — Ratified baseline retention decision.
* [**Failure Analysis Report**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/reports/FAILURE_ANALYSIS_REPORT.md) — Failure mode analysis & triage mitigations.
* [**Dataset Curation Report**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/docs/datasets/DATASET_CURATION_REPORT.md) — Mendeley PPLD data provenance & duplicate isolation.
* [**SIH Compliance Report**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/reports/SIH_COMPLIANCE_REPORT.md) — Item-by-item verification against SIH26131.
* [**Model Card**](file:///c:/Users/imman/OneDrive/Pictures/SIH-FINAL-main/SIH-FINAL-main/docs/model/MODEL_CARD.md) — Model architecture and constraints.
