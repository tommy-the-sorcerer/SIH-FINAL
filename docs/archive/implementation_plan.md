# FALCON-AI SIH Final Enhancement Plan

Comprehensive architecture and implementation plan addressing all 14 review feedback points for SIH26131 (Government of Maharashtra - Maharashtra State Innovation Society).

## User Review Required

> [!IMPORTANT]
> **Model Classes & Crop Coverage**:
> The existing `PlantDiseaseDetection.pt` YOLOv8 model contains **116 classes** covering major crops (Corn/Maize, Tomato, Potato, Rice, Grape, Citrus, Soybean, Cucumber, Bean, Apple, Garlic, Banana, etc.).
> We will align the crops prominently displayed in the farmer interface and diagnosis pipeline with **Maharashtra's primary agro-climatic crops** supported by the model:
> 1. Soybean (सोयाबीन)
> 2. Cotton / Cash Crops (कापूस)
> 3. Maize / Corn (मका)
> 4. Tomato (टोमॅटो)
> 5. Rice / Paddy (भात)
> 6. Grape (द्राक्ष)
> 7. Citrus / Sweet Lime / Orange (संत्रा / मोसंबी)
> 8. Potato (बटाटा)
> 9. Garlic / Onion (लसूण / कांदा)
> 10. Banana (केळी)
>
> We will ensure the AI pipeline detects leaves from these crops with precise bounding-box detection, crop-level validation, and reliable fallback handling when a leaf shows healthy tissue or unlisted symptoms.

> [!IMPORTANT]
> **Role-Based Access Control (RBAC) & GPS / Hotspot Restriction**:
> - **Farmer Role**: Access restricted to their own farm profile, diagnosis engine, their personal cases history, treatment advisory, and local weather. **Hotspot GIS map & district GPS intelligence are strictly hidden and blocked via backend authentication** for Farmers.
> - **Expert Role**: Access to cases submitted in their assigned district/division, review desk with triage & prescription verification.
> - **Agriculture Officer Role (Admin)**: Full district-wide epidemic surveillance, live GIS Hotspot Map with pest clustering, predictive spread simulation, and official advisory broadcasts.

> [!IMPORTANT]
> **Speech-to-Speech / Voice AI Assistant**:
> We will integrate a client-side Web Speech API + voice synthesis agent ("कृषी सखा / Krishi Mitra") that supports Marathi, Hindi, and English voice input and audio response, allowing hands-free interaction for farmers directly in the browser!

---

## Proposed Changes

### 1. Maharashtra Government Official Branding & UI Cleanup
- Incorporate official Government of Maharashtra Emblem / Logo ("महाराष्ट्र शासन" Rajmudra) and Maharashtra State Innovation Society / Department of Agriculture branding into the header, sidebar, login modals, and report exports.
- Remove all dummy/draft placeholder text, confusing debug messages, and extraneous draft states. Clean up all card headers and footers for a polished SIH presentation.

### 2. Crop Growth Stage Made Optional
- Make crop growth stage dropdown optional in the UI (or pre-select default "vegetative / auto-inferred").
- Update FastAPI `/api/diagnose` route and `pipeline.py` so `growth_stage` defaults to `auto` or `vegetative` if omitted by the farmer, removing manual friction.

### 3. Crop Selection & Model Pipeline Optimization
- Update `taxonomy.py` and `pipeline.py` to map the 116 YOLO classes from `PlantDiseaseDetection.pt` directly to Maharashtra priority crops (Soybean, Maize, Tomato, Rice, Grape, Citrus, Potato, Garlic, Cucumber, Banana).
- Refine confidence thresholding and crop-aware gating so the model accurately detects diseases for selected Maharashtra crops.

### 4. Comprehensive Treatment & Medicine Advisory
- Expand `taxonomy.py` and `advisory` engine with detailed, actionable recommendations:
  - **Immediate Action** (Pruning, isolation, soil moisture adjustment)
  - **Categorized Inputs / Medicines**:
    - Organic / Bio-control (Trichoderma viride, Pseudomonas fluorescens, Neem oil 1500ppm)
    - Chemical Treatment (CIBRC approved fungicide/insecticide, technical active ingredient, exact dosage e.g. 2ml/L, waiting/PHI period)
  - **Safety & Precaution**: PPE guidance, spraying time (avoid hot midday), environmental precautions (pollinators/bees).
  - **Monitoring & Escalation**: When to call the Taluka Agriculture Officer or KVK specialist.

### 5. Farmer Onboarding & Enhanced Registration
- Upgrade registration and farmer profile modal to capture:
  - Farmer Full Name, Phone Number, Alternate Contact
  - District, Taluka, Village, Pin Code
  - Farm Size (acres), Irrigation Type (Drip, Sprinkler, Rainfed)
  - Major Crops Cultivated
- Store in `users` and `farms` SQLite tables.

### 6. Strict Role-Based Authentication & Navigation Separation
- Provide clear Persona switchers and dedicated login modals for:
  1. 🧑‍🌾 **Farmer** (Ramesh Patil - Nashik)
  2. 🔬 **Agricultural Expert** (Dr. Sunita Deshmukh - MPKV Rahuri / Nashik Zone)
  3. 🏛️ **Agriculture Officer** (Shri. Anand Rao Kulkarni - District Agriculture Office)
- Enforce backend role guard in FastAPI endpoints (`/api/cases/officer-summary`, `/api/hotspots`, `/api/cases/pending-review`). If a Farmer token attempts to access officer GIS endpoints, return `403 Forbidden`.
- In the frontend sidebar and router (`app.js` and `index.html`), dynamically hide **Hotspot Map**, **Smart Traps**, **Expert Desk**, and **Officer Dashboard** when logged in as a Farmer.

### 7. Restricted Map & GPS Access
- Hotspot Map and GPS coordinate layer rendered **only** for `EXPERT` and `ADMIN` (Officer) roles.
- Farmer view only shows their own village/farm general weather and localized advisory, preventing panic or unauthorized access to regional disease cluster coordinate data.

### 8. Consistent Multilingual Support (Marathi, Hindi, English)
- Expand `i18n.py` to cover 100% of UI strings, medicine names, instructions, and error messages.
- Fix any hardcoded strings in `index.html` and `app.js` to ensure when "मराठी" is selected, the entire interface displays consistent Devanagari Marathi without mixing English or Hindi words.
- Smooth instant language switching with persistence in `localStorage`.

### 9. Voice-to-Voice AI Agent ("कृषी सखा / Krishi Mitra")
- Integrate an interactive Voice Assistant widget into the UI:
  - Mic button with speech recognition (Web Speech API `webkitSpeechRecognition`) supporting Marathi (`mr-IN`), Hindi (`hi-IN`), and English (`en-IN`).
  - Natural Language query processor for farming questions (crop disease symptoms, medicine dosage, weather advice, government schemes).
  - Speech synthesis (`speechSynthesis.speak`) to respond back in clear voice in the farmer's selected language.

### 10. Continuous Live Weather Telemetry
- Enhance `weather_service.py` to continuously fetch real-time Open-Meteo weather for the farmer's selected Maharashtra district/taluka with auto-refresh every 10 minutes.
- Real-time weather parameters (temperature, humidity, rain forecast, wind) dynamically feed into the disease risk scoring engine (`risk_engine.py`).

---

## Verification Plan

### Automated Verification
- Verify Python backend syntax and start FastAPI server without errors.
- Run test diagnosis via Python script with sample crop images and check inference output against `PlantDiseaseDetection.pt`.
- Verify role-based authorization: test endpoints with Farmer token vs Officer token.
- Verify `i18n` dictionary integrity across all 3 languages.

### Manual Verification
- Open Web application in browser and test:
  - Maharashtra Government logo and clean header.
  - Role-based login and navigation filtering (Farmer vs Expert vs Officer).
  - Crop diagnosis without mandatory growth stage selection.
  - Voice assistant speech input and audio speech output in Marathi/English.
  - Multilingual switching between English, Marathi, and Hindi.
  - Hotspot Map access blocked for Farmers and available for Officers.
