# FALCON-AI: Maharashtra Crop & Agro-Climatic Coverage Report

**Problem Statement SIH26131:** Early detection and management of crop diseases and pest infestations  
**Client / Ministry:** Government of Maharashtra (Maharashtra State Innovation Society / Dept. of Agriculture)  
**Publication Date:** 2026-09-09  

---

## 1. Agro-Climatic Zones & Cropping Distribution in Maharashtra

Maharashtra's agriculture is divided into 9 distinct agro-climatic zones, from the high-rainfall Konkan coastal strip to the drought-prone rainshadow Ghats, Vidarbha black cotton soils, and Khandesh river valleys. FALCON-AI provides explicit algorithmic and taxonomic coverage for the state's economic lifelines:

| Crop | Agro-Climatic Region in Maharashtra | Key Pathologies / Pests Covered in FALCON-AI | Diagnostic Modality |
| :--- | :--- | :--- | :--- |
| **Cotton (कापूस)** | Vidarbha (Yavatmal, Wardha), Marathwada, Khandesh | Pink Bollworm (*Pectinophora gossypiella*), Bacterial Blight (*Xanthomonas*), Grey Mildew (*Ramularia*), Leaf Reddening (*Lalya* - Abiotic) | Visual YOLO + CIBRC + Abiotic Veto |
| **Soybean (सोयाबीन)** | Vidarbha (Amravati, Nagpur), Marathwada (Latur, Nanded) | Soybean Rust (*Phakopsora pachyrhizi*), Sudden Death Syndrome (*Fusarium*), Bacterial Blight (*Pseudomonas*) | Visual YOLO + Doubt Doctor + CIBRC |
| **Tur / Pigeonpea (तूर)** | Marathwada, Vidarbha (Akola, Buldhana) | Sterility Mosaic Virus (SMD - vector mite), Cercospora Leaf Spot, Leaf Webber (*Grapholita*) | Visual Classification + Doubt Doctor |
| **Onion (कांदा)** | Nashik (Niphad, Kalwan), Pune, Ahmednagar | Purple Blotch (*Alternaria porri*), Stemphylium Blight, Thrips (*Thrips tabaci*) | Visual YOLO + Weather Risk Fusion |
| **Maize (मका)** | Nashik, Pune (Baramati), Ahmednagar, Solapur | Fall Armyworm (*Spodoptera frugiperda*), Northern Leaf Blight (*Exserohilum*), Common Rust | Visual YOLO + Pheromone Guidance |
| **Tomato (टोमॅटो)** | Nashik, Pune (Junnar), Sangli | Late Blight (*Phytophthora*), Early Blight (*Alternaria*), Tomato Yellow Leaf Curl Virus (TYLCV) | Visual YOLO + Humidity Spore Window |
| **Grape (द्राक्षे)** | Nashik (Pimpalgaon, Dindori), Sangli (Tasgaon) | Downy Mildew (*Plasmopara viticola*), Powdery Mildew (*Uncinula*), Anthracnose | Visual YOLO + Microclimate Spore Gating |
| **Citrus / Orange (संत्रा)** | Vidarbha (Nagpur, Katol, Amravati) | Citrus Canker (*Xanthomonas*), Citrus Greening / Huanglongbing, Black Spot | Visual YOLO + Sanitation Tasks |
| **Sugarcane (ऊस)** | Western Maharashtra (Kolhapur, Satara, Ahmednagar) | Red Rot (*Colletotrichum*), Grassy Shoot, Woolly Aphid (*Ceratovacuna*) | Field Inspection Protocols + Lab Escalation |

---

## 2. Priority Agronomic Interventions for Maharashtra

### 2.1. Cotton Leaf Reddening (*Lalya*)
- **Nature:** Abiotic / Physiological stress induced by low night temperatures, magnesium deficiency, and waterlogging.
- **Historic Problem in Maharashtra:** Farmers frequently panic-spray expensive chemical fungicides, wasting ₹1,500–₹2,500 per acre with zero disease resolution.
- **FALCON-AI Action:** Explicit veto on chemical pesticides. Directs farmers to spray 1% Magnesium Sulphate ($10\text{ g/L}$) + 2% DAP ($20\text{ g/L}$) at 15-day intervals.

### 2.2. Beneficial Biocontrol Predator Protection
- **Nature:** Cotton and pigeonpea fields host natural biocontrol agents:
  1. *Coccinella septempunctata* (Seven-spotted Lady Beetle)
  2. *Chrysoperla carnea* (Green Lacewing)
  3. *Syrphus ribesii* (Hoverfly larvae)
- **FALCON-AI Action:** Classifies predators as `BENEFICIAL_PREDATOR` and triggers an automatic `PREDATOR CONSERVATION VETO` if a farmer attempts chemical application against them.

### 2.3. Fall Armyworm (*Spodoptera frugiperda*) in Maize
- **Nature:** Invasive polyphagous pest ravaging maize whorls in Nashik and Ahmednagar.
- **FALCON-AI Action:** Detects characteristic pinhole and "window pane" feeding symptoms, checks vegetative stage susceptibility, advises whorl application of *Chlorantraniliprole 18.5% SC* @ $0.4\text{ ml/L}$ or release of *Trichogramma pretiosum* @ 50,000/acre.
