# SIH 26131 COMPLIANCE AUDIT — FALCON-AI (RoboticDrones)

**Audit date:** September 8, 2026
**Audit type:** Read-only inspection & compliance audit (no project files modified)
**Audited repository:** `RoboticDrones/` (FALCON-AI Crop Health Diagnosis)

---

## 1. Executive Verdict

**Status:** 🟡 **PARTIAL MATCH** (borderline 🔴 — one pillar genuinely works, eleven do not)
**Overall Score:** **23.5 / 100**

**One-paragraph explanation:**
FALCON-AI is a working, honest single-feature MVP: real image-based crop disease screening using a genuine ~97-class YOLO detection model, with an OpenCV quality guardrail, damage visualization, a caution-first advisory, per-farmer history in SQLite, and a Google Translate widget. It is **not** an integrated crop-health decision-support system. Of the 12 SIH capabilities, only **1 (disease detection) is genuinely implemented**, **4 are partial** (advisory, safe-guidance-by-omission, multilingual, follow-up history), and **7 are entirely absent** (pest detection, weather, risk forecasting, GIS, IPM, expert validation, feedback/learning). The name, team page, and SIH footer are real; the surrounding "intelligence" is not there yet.

---

## 2. What the Current Project Actually Does

FALCON-AI is a **single-page crop-image screening app**:

1. Farmer enters name + 10-digit phone (stored in `localStorage`, no real authentication).
2. Farmer uploads a leaf photo (gallery or camera — camera uses bleeding-edge Chrome-only APIs: `navigator.mediaDevices.getUserMedia`, `canvas.toBlob`, `URL.createObjectURL`).
3. Optionally types in 3 sensor readings (soil moisture / temperature / humidity) — **manually**, or via "Demo sensor presets" buttons.
4. `POST /predict` → `pipeline.process_and_predict()`:
   - OpenCV guardrail (`validate_specimen_framing`): rejects cartoons/flat graphics via HSV green/autumn masks, Laplacian texture variance, Canny edge clutter.
   - Real YOLO inference (`Models/PlantDiseaseDetection.pt`, 436 MB, ~97 classes across ~30 crops, confirmed by extracting class strings from the checkpoint: Cassava, Corn, Tomato, apple, banana, bean, cherry, coffee, cucumber, grape, peach, potato, rice, strawberry, zucchini…).
   - Confidence threshold 0.70; below it → `Uncertain` ("Possible X") with no treatment advice.
   - `_analyse_leaf_surface`: HSV-based leaf mask + brown/pale damage mask → `damage_percent`, lesion `markers`, base64 `overlay` image.
   - `_make_recommendation`: rule-based, template text keyed only on `damage_percent` and `soil_moisture`.
5. Result rendered in a themed result card; per-farmer history via `GET /history?phone=`; CSV export client-side.
6. Everything persisted to a single SQLite table `diagnoses` (only 3 real test rows exist — from 2026-09-07, with confidences 28–40%, all below the current 0.70 threshold, i.e. written by an earlier code version).

There is **no pest pipeline, no weather service, no risk engine, no map, no expert role, no feedback loop, no retraining integration, no notifications, no drone/IoT components** — the "RoboticDrones" folder name notwithstanding.

---

## 3. Architecture

```
Farmer (browser, single page)
   │  multipart POST /predict (file + name + phone + optional manual sensor values)
   ▼
FastAPI (main.py) — 3 routes: GET /, POST /predict, GET /history
   │
   ▼
pipeline.py
   ├─ OpenCV guardrail (validate_specimen_framing)
   ├─ YOLO inference (MODEL = YOLO("Models/PlantDiseaseDetection.pt"), conf=0.15, 640×640)
   ├─ Leaf damage analysis (HSV masks, markers, base64 overlay)
   └─ Rule-based recommendation templates (_make_recommendation)
   │
   ▼
storage.py ──► SQLite falcon_ai.db (single table: diagnoses)
   │
   ▼
Response JSON ──► app.js (displayResults) ──► result card + history + CSV export
```

**External calls:** Google Fonts CDN, FontAwesome CDN, Google Translate widget (`translate.google.com/translate_a/element.js`). **No weather/GIS/translation/expert APIs exist.**

**Stack:**
- **Frontend:** vanilla HTML/CSS/JS (no framework), Jinja2 template `templates/index.html`, `static/js/app.js`, `static/css/style.css`
- **Backend:** Python + FastAPI (`main.py`)
- **Database:** SQLite (`falcon_ai.db`, table `diagnoses`)
- **AI/ML:** Ultralytics YOLO 8.4.117 + Torch 2.13 + OpenCV + NumPy (`pipeline.py`, `Models/PlantDiseaseDetection.pt`)
- **Training:** standalone script `train_regularized.py` (disconnected, Colab path)
- **Auth:** none (localStorage name + phone)
- **Deployment:** none (no requirements.txt, README, Dockerfile, .env, tests, CI)

---

## 4. Requirement Compliance Matrix

| Requirement | Status | Evidence | Missing / Problem |
|---|---|---|---|
| Disease Detection | ✅ **PASS** | `pipeline.py::process_and_predict`, `MODEL = YOLO(...)`, `Models/PlantDiseaseDetection.pt` (real 97-class checkpoint), `POST /predict`, DB rows prove real inference | Disease-vs-healthy is a **keyword heuristic** (`_is_disease_label`, `DISEASE_TERMS`), not a model decision; real-world confidences (28–40%) mostly fall under the 0.70 threshold → "Uncertain"; no crop selection; heavy 436 MB model |
| Pest Detection | ❌ **FAIL** | Only class string `"Corn Insects Damages"` in the checkpoint; `_is_disease_label` treats it as *disease*; no object detection, traps, counts, trends, or alerts | Entire pest pillar absent |
| Weather | ❌ **FAIL** | No weather API/config/location/forecast anywhere; "temperature/humidity" are manual form fields; UI even labels them "Demo sensor presets" | Weather never affects any risk/diagnosis; only soil-moisture<35 gates a recommendation text |
| Risk Forecasting | ❌ **FAIL** | No risk score, no LOW/MED/HIGH, no probability; only `confidence` (model certainty) and `damage_percent` (image heuristic) | Risk engine absent |
| GIS Hotspots | ❌ **FAIL** | No lat/long, GPS, maps, district/taluka, or hotspot logic anywhere in code | Absent |
| Advisory | 🟡 **PARTIAL** | `_make_recommendation` returns action/dosage/status/reason; UI renders them | 3–4 static templates, not disease-specific, not severity-specific, no prevention/treatment detail |
| IPM | ❌ **FAIL** | No cultural/biological/mechanical/chemical strategies; only "isolate & verify with agronomist" | Absent |
| Safe Guidance | 🟡 **PARTIAL** | Deliberately refuses pesticide doses ("Use only the product label dose after field confirmation") — safe by omission | No dosage, application, precautions, or crop-specific guidance |
| Multilingual | 🟡 **PARTIAL** | Real Google Translate widget, 6 languages (en, te, kn, ta, ml, hi), `switchLanguageViaApi` sets `goog-te-combo` + fires `change` | Third-party client widget, hidden container, fragile programmatic switching, no backend i18n, needs internet |
| Expert Validation | ❌ **FAIL** | "Uncertain" status only tells the farmer to seek local confirmation; nothing routes to an expert or stores a review | Absent |
| Follow-up | 🟡 **PARTIAL** | `diagnoses` table + `GET /history?phone=` + CSV export show past observations per phone | No images stored, no progression/treatment history, no before/after, no recovery tracking |
| Feedback/Learning | ❌ **FAIL** | No feedback/ground-truth collection; `train_regularized.py` is a standalone Colab script hardcoded to `/content/dataset/data.yaml` with no link to app data | No retraining/eval pipeline wired to the system |

---

## 5. Code Evidence (PASS/PARTIAL features)

### Disease detection (PASS)
- `RoboticDrones/main.py` → `app = FastAPI(...)`; `POST /predict` reads `UploadFile`, calls `process_and_predict`, `save_diagnosis`.
- `RoboticDrones/pipeline.py` → `MODEL = YOLO(str(MODEL_PATH))` (line 8); `MODEL(img_resized, conf=0.15)` (line 211); `CONFIDENCE_THRESHOLD = 0.70` (line 209); `results.boxes`, `top_box.conf`, `top_box.cls`, `MODEL.names` (lines 213–219); `validate_specimen_framing`; `_analyse_leaf_surface`; `_is_disease_label` + `DISEASE_TERMS`.
- `RoboticDrones/Models/PlantDiseaseDetection.pt` → 436 MB torch archive; class strings extracted from `archive/data.pkl` confirm ~97 labels (e.g., `Tomato early blight`, `Grape downy mildew`, `Corn Insects Damages`, `Cassava Bacterial Blight`, `peach leaf curl`).
- `RoboticDrones/storage.py` → `CREATE TABLE diagnoses(...)`; `save_diagnosis`; `get_diagnoses(phone)`.
- `RoboticDrones/templates/index.html` + `static/js/app.js` → `fetch("/predict", {method:"POST", body:formData})` (line 368); `displayResults(data)` renders status/disease/confidence/markers/overlay/recommendation.
- **Proof of real inference:** `falcon_ai.db` contains 3 genuine rows ("Grape Downy Mildew" 39.78%, "Possible Tomato Early Blight" 28.95% — written by an earlier code version with a lower threshold).

### Advisory / Safe guidance (PARTIAL)
- `RoboticDrones/pipeline.py::_make_recommendation` (lines ~118–160): `action`, `dosage`, `sensor_status`, `reason`, `sensor_values`; moisture<35 → "Check irrigation before spraying"; damage<2% → "Continue monitoring; no treatment indicated"; else → "Isolate the plant and verify … with an agronomist".

### Multilingual (PARTIAL)
- `RoboticDrones/templates/index.html` lines ~36–47 (Google Translate init, `includedLanguages: 'en,te,kn,ta,ml,hi'`); `static/js/app.js::switchLanguageViaApi` + `LANG_MAP`.

### Follow-up history (PARTIAL)
- `GET /history` (`main.py`); `app.js::renderPredictionHistory`, `exportPredictionHistory` (CSV).

### Training script (exists, disconnected)
- `RoboticDrones/train_regularized.py`: YOLOv8m, epochs=100, patience=10, weight_decay=0.001, dropout=0.2, label_smoothing=0.1, mosaic/mixup/erasing; hardcoded `data="/content/dataset/data.yaml"` (Google Colab path).

---

## 6. Fake / Mock / Placeholder Detection

Only **verified** findings:

- ✅ **No fake predictions, no hardcoded disease results, no fake weather, no fake coordinates, no fake confidence** — the core inference is real. This project is *not* a mock of the features it has.
- ⚠️ `static/js/app.js::applySensorPreset` + `templates/index.html` "Demo sensor presets" → the only "sensor" inputs are **manual demo values**; there is no IoT/telemetry. Labeled "Demo" in the UI itself.
- ⚠️ `train_regularized.py` → training pipeline is a **disconnected placeholder** (Colab path, no dataset, never invoked by the app).
- ⚠️ `templates/index.html` Google Translate widget is hidden (`display:none`) and driven by a synthetic `change` event — fragile, may silently not translate.
- ⚠️ `app.js::openCameraModal` uses non-standard `navigator.mediaDevices.getUserMedia` / `canvas.toBlob` / `URL.createObjectURL` — works only on recent Chrome; fails elsewhere.
- ⚠️ No `requirements.txt`, no README, no `.env`, no Dockerfile, no tests, no CI — nothing to run from a fresh checkout without manual dependency reconstruction.

---

## 7. End-to-End Workflow Test

| # | Step | Status | Evidence |
|---|---|---|---|
| 1 | Farmer logs in | 🟡 PARTIAL | `submitFarmerRegistration` — localStorage only, no server session |
| 2 | Farmer selects crop | ❌ FAIL | No crop field anywhere |
| 3 | Farmer provides location | ❌ FAIL | No location fields |
| 4 | Uploads crop image | ✅ PASS | `handleSelectedImage` → multipart |
| 5 | Backend receives image | ✅ PASS | `POST /predict`, `UploadFile` |
| 6 | AI analyzes image | ✅ PASS | Real YOLO inference |
| 7 | Disease/pest detected | 🟡 PARTIAL | Disease: real; pest: one class mislabeled as disease |
| 8 | Confidence calculated | ✅ PASS | `top_box.conf` → % |
| 9 | Weather retrieved | ❌ FAIL | Manual optional inputs only |
| 10 | Risk calculated | ❌ FAIL | No risk concept |
| 11 | Location mapped | ❌ FAIL | No geo data |
| 12 | Recommendation generated | 🟡 PARTIAL | Static templates |
| 13 | Low-confidence → expert | ❌ FAIL | Status text only |
| 14 | Farmer receives advisory | ✅ PASS | `displayResults` |
| 15 | Follow-up observation | 🟡 PARTIAL | History list only, no follow-up flow |
| 16 | System stores outcome | 🟡 PARTIAL | Stores diagnosis; stores no outcome/feedback |

---

## 8. SIH Gap Analysis

### 🔴 Critical (core promise of 26131, entirely absent)
- Pest detection
- Weather integration
- Risk / early-warning engine
- Geospatial hotspot mapping
- Expert validation (human-in-the-loop)
- Feedback / learning loop

### 🟠 Major
- IPM (no management strategies)
- Advisory not diagnosis-specific
- No real auth / roles
- No deployment / requirements / demo packaging
- No follow-up workflow (history only)
- No sample demo images in repo

### 🟡 Minor
- Multilingual widget fragility
- Chrome-only camera
- No logging / configuration
- Heuristic healthy-vs-disease labeling
- Heavy model loaded at import
- Broken venv (base interpreter path missing)
- No tests

---

## 9. Minimum Changes Required

*Not implemented — listed for planning only.*

1. **Weather:** add Open-Meteo/IMD API call keyed on farmer location; feed temp/humidity/rainfall into a risk rule engine.
2. **Risk engine:** rule-based or ML score (crop × disease × weather × damage × location) → LOW/MED/HIGH with explanation.
3. **Pest detection:** add a pest YOLO model (or trap/IoT ingest) + severity/trend logic.
4. **GIS:** collect lat/long (browser geolocation or village picker), store per diagnosis, render hotspot markers (Leaflet/MapLibre) with density/risk heat.
5. **Expert module:** role-based auth (officer), review queue for `Uncertain`/low-confidence cases, correction stored as ground truth.
6. **Feedback/learning:** capture field-confirmed outcomes; export labeled dataset; wire a retraining job (reuse `train_regularized.py` with a real dataset path).
7. **Advisory upgrade:** disease-specific, severity-specific IPM + safe-use content (dosage, precautions, PHI).
8. **Ops:** `requirements.txt`, README, `.env` config, Dockerfile, tests, sample images, working camera fallback.

---

## 10. Final SIH Judge Perspective

- **Innovation:** The OpenCV "cartoon/Pikachu filter" guardrail and the caution-first, no-pesticide-until-confirmed advisory are genuinely thoughtful. Nothing else is novel.
- **Technical implementation:** Competent, small, and honest — but a 3-route FastAPI app with one model and one table cannot carry a 12-pillar problem statement.
- **Problem alignment:** ~8% of the problem statement. It screens leaf photos; it does not manage crop health.
- **Completeness / Demo readiness:** Not demo-ready as a full SIH solution. With internet + a rebuilt environment + a good leaf photo, the disease demo *will* work — but most photos will return "Uncertain" (all 3 real test rows were 28–40% confidence, below the 0.70 threshold), and judges will immediately probe weather, map, expert, and pest flows that do not exist.
- **Real-world usefulness:** Genuinely useful as a first-level farmer screening tool; insufficient as a decision-support system.

**Final one-sentence answer:**
> **"Does this project genuinely implement SIH 26131?" — No. It genuinely implements one of the twelve required capabilities (image-based disease detection) and nothing else; as a complete SIH 26131 solution it is currently a PARTIAL MATCH at best, ~23.5/100.**

---

## Appendix: Score Breakdown (out of 100)

| Requirement | Weight | Score | Weighted |
|---|---|---|---|
| Disease detection | 15 | 13 | 13.0 |
| Pest detection | 10 | 0 | 0.0 |
| Weather integration | 10 | 0 | 0.0 |
| Risk forecasting / early warning | 15 | 0 | 0.0 |
| GIS hotspot mapping | 10 | 0 | 0.0 |
| Farmer advisory | 10 | 3 | 3.0 |
| Integrated management | 5 | 0 | 0.0 |
| Safe treatment guidance | 5 | 2 | 2.0 |
| Multilingual support | 5 | 2 | 2.0 |
| Expert validation | 5 | 0 | 0.0 |
| Follow-up monitoring | 5 | 2.5 | 2.5 |
| Feedback/learning | 5 | 0 | 0.0 |
| **Total** | **100** | | **22.5 → 23.5** (disease detection 13 + advisory 3 + safe guidance 2 + multilingual 2 + follow-up 2.5 + 1.0 bonus for genuine end-to-end image pipeline integration) |

*Scoring notes: Disease detection scores 13/15 (real model + real threshold + visualization, minus crop selection, heuristic healthy/disease labeling, and low real-world confidence). Advisory 3/10 (templates exist but are generic). Safe guidance 2/5 (safe-by-omission only). Multilingual 2/5 (real widget, fragile). Follow-up 2.5/5 (history only, no progression). No credit for unbuilt pillars. Score intentionally not inflated.*