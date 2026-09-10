# FALCON-AI: Maharashtra AI Dataset Expansion & Training Plan
**SIH 26131 — Early Detection & Management of Crop Diseases and Pest Infestations**  
**Government of Maharashtra | Department of Skills, Employment, Entrepreneurship and Innovation**  
**Phase:** 4A (Planning, Taxonomy & Dataset Architecture — Strictly Non-Destructive)  
**Status:** Approved for Architectural Review  

---

## 1. Executive Summary

FALCON-AI is an operational, AI-assisted decision-support platform engineered for the Government of Maharashtra under Problem Statement SIH 26131. The platform's mission is early detection and management of crop diseases and pest infestations across Maharashtra's distinct agro-climatic zones, utilizing mobile camera uploads from farmers, extension workers, and agricultural officers—**strictly without reliance on aerial drones or synthetic hallucinations**.

A comprehensive forensic audit of the current production model ([`Models/PlantDiseaseDetection.pt`](file:///c:/Users/lenovo/Desktop/RoboticDrones/RoboticDrones/Models/PlantDiseaseDetection.pt), 116 YOLO classes, mAP@0.50 of 69.89%) revealed a critical geographic and biological mismatch:
1. **Critical Agronomic Voids:** The model contains **zero classes** for Maharashtra's #1 cash crop (Cotton, >42 lakh ha), zero classes for major pulse staples (Tur/Pigeon Pea >12 lakh ha, Gram/Chickpea >25 lakh ha), zero classes for Onion (>5.5 lakh ha), and zero classes for Wheat (>10 lakh ha). For Soybean (>46 lakh ha), only a single healthy leaf class exists—all diseases and pests are missing.
2. **Extreme Disease vs. Pest Asymmetry:** Out of 116 output classes, **82 are foliar diseases (70.7%)**, **33 are healthy leaf classes (28.4%)**, and **only 1 single class represents pest damage (`[99] Corn Insects Damages`, 0.86%)**. Zero insect body detection classes exist in the model.
3. **Redundant Duplicate Classes:** Five duplicate biological concepts exist across distinct output indices (e.g., `corn rust` [0] vs `Corn rust leaf` [109]), diluting probability mass and causing artificial `UNCERTAIN` predictions.

### Core Objective of Phase 4A:
To design a rigorous, scientifically grounded, Maharashtra-centric dataset expansion and training architecture that systematically bridges these gaps. 

> [!IMPORTANT]
> **Planning Constraints (Strict Non-Destructive Policy):**
> - **No code changes:** Production files (`main.py`, `pipeline.py`, `taxonomy.py`, `storage.py`, `risk_engine.py`, frontend) remain unmodified.
> - **No model tampering:** `Models/PlantDiseaseDetection.pt` is preserved intact as the active baseline.
> - **No premature downloads or training:** No datasets are downloaded, scraped, or trained in Phase 4A.
> - **Safety first:** Existing defensive routing (`UNKNOWN`/`UNCERTAIN` escalation to human experts) remains the primary safeguard for unsupported crops.

---

## 2. Current Model Baseline & Technical Constraints

The current model checkpoint serves as our performance, size, and latency benchmark:

| Metric / Parameter | Baseline Value | Implication for Future Models |
| :--- | :--- | :--- |
| **Model Checkpoint** | `Models/PlantDiseaseDetection.pt` | Current active model in production. |
| **File Size** | **436.0 MB** | High memory footprint; future models should aim for equivalent or smaller size (e.g., YOLO11m/YOLO11s). |
| **Architecture** | `ultralytics.nn.tasks.DetectionModel` (YOLO11x) | Anchor-free PyTorch detection network with 116 output heads. |
| **Precision (`val/P`)** | **63.54%** | Baseline true-positive rate across existing classes. |
| **Recall (`val/R`)** | **68.20%** | Baseline lesion recovery rate. |
| **mAP@0.50** | **69.89%** | Primary detection accuracy benchmark at 0.5 IoU. |
| **mAP@0.50–0.95** | **68.56%** | Multi-threshold localization benchmark. |
| **Total Classes** | **116** | 89 from PlantDoc, 5 from Cassava, 16 from Corn, 6 from Tomato. |
| **Pest Representation** | **1 class (0.86%)** | Must be expanded via dedicated pest damage and trap datasets. |
| **Duplicate Classes** | **5 pairs (10 classes)** | Must be harmonized into 5 canonical concepts before next training. |
| **Supported MH Crops** | **Maize, Tomato, Grape, Citrus, Rice** | 5 of 11 configured crops have meaningful disease representation. |
| **Unsupported MH Crops**| **Cotton, Soybean, Tur, Gram, Onion, Wheat** | 6 of 11 configured crops currently lack disease/pest representation. |

---

## 3. Maharashtra Crop Priority Matrix

The 11 priority crops configured in [`taxonomy.py`](file:///c:/Users/lenovo/Desktop/RoboticDrones/RoboticDrones/taxonomy.py) represent >85% of Maharashtra's cultivated acreage and agrarian economic value. Below is the rigorous priority evaluation:

| Crop Name & Local Name | Current Classes in Model | Current Status | Critical Required Diseases | Critical Required Pests | Priority | Agronomic & Economic Rationale | Image-Based Detection Feasibility | Expert Review Requirement |
| :--- | :---: | :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **Soybean**<br>*(सोयाबीन)* | 1 *(Healthy only)* | 🔴 5% | Soybean Rust (*Phakopsora pachyrhizi*), Bacterial Pustule (*Xanthomonas axonopodis*), Yellow Mosaic Virus (YMV), Charcoal Rot (*Macrophomina phaseolina*) | Stem Fly (*Melanagromyza sojae* damage), Girdle Beetle (*Obereopsis brevis* ring), Tobacco Caterpillar (*Spodoptera litura* skeletonization), Semilooper | **CRITICAL** | >46 Lakh Hectares. Maharashtra's primary kharif oilseed (Vidarbha & Marathwada). Rust epidemics (e.g. Sangli, Kolhapur) cause up to 80% yield loss in 14 days. | **Yes** for foliar lesions & feeding patterns; **Partial** for internal stem fly (wilting shoot). | Mandatory for wilt/root rot; conditional for rust. |
| **Cotton**<br>*(कापूस)* | 0 | 🔴 0% | Bacterial Blight / Angular Leaf Spot (*Xanthomonas citri*), Grey Mildew / Dahiya (*Ramularia areola*), Alternaria Leaf Spot, Root Rot | Pink Bollworm (*Pectinophora gossypiella* - rosette flower & entrance hole), Whitefly (*Bemisia tabaci*), Jassids / Leafhopper (*Amrasca biguttula* burn), Thrips | **CRITICAL** | >42 Lakh Hectares. Primary cash crop ("White Gold"). Pink Bollworm resistance to Bt cotton is Maharashtra's foremost agrarian crisis (Vidarbha, Marathwada, Khandesh). | **Yes** for foliar lesions, rosette flowers, hopper burn, and pheromone trap scans; **Partial** for tiny nymphs. | Mandatory for Pink Bollworm ETL & root rots. |
| **Tur / Pigeon Pea**<br>*(तूर)* | 0 | 🔴 0% | Fusarium Wilt (*Fusarium udum*), Sterility Mosaic Disease (SMD), Phytophthora Stem Blight | Gram Pod Borer (*Helicoverpa armigera* pod damage), Pod Fly (*Melanagromyza obtusa*), Plume Moth | **HIGH** | >12 Lakh Hectares. Key protein pulse, heavily intercropped with cotton/soybean. SMD ("green plague") causes complete sterility. | **Yes** for Sterility Mosaic (mosaic/chlorosis/bushiness), stem blight lesions, and pod bore holes. | Mandatory for vascular wilt. |
| **Gram / Chickpea**<br>*(हरभरा)* | 0 | 🔴 0% | Fusarium Wilt (*Fusarium oxysporum* f. sp. *ciceri*), Dry Root Rot (*Rhizoctonia bataticola*), Ascochyta Blight, Collar Rot | Chickpea Pod Borer (*Helicoverpa armigera* larva on foliage/pods, defoliation) | **HIGH** | >25 Lakh Hectares. Leading post-monsoon Rabi pulse in Marathwada & Western Maharashtra. Wilt causes sudden patch-drying. | **Yes** for Ascochyta foliar lesions and *Helicoverpa* larvae/feeding; **Partial** for vascular wilt. | Mandatory for root rot / wilt. |
| **Onion**<br>*(कांदा)* | 0 | 🔴 0% | Purple Blotch (*Alternaria porri*), Stemphylium Leaf Blight, Downy Mildew, Basal Rot (*Fusarium*), Colletotrichum / Twister Disease | Onion Thrips (*Thrips tabaci* - silvering / white flecking damage) | **HIGH** | >5.5 Lakh Hectares. Maharashtra produces ~35–40% of India's onion supply (Nashik, Pune, Ahmednagar). Purple blotch wipes out foliage in wet weather. | **Yes** for purple blotch concentric lesions, Stemphylium, and thrips silvering damage. | Mandatory for basal bulb rot; conditional for purple blotch. |
| **Wheat**<br>*(गहू)* | 0 | 🔴 0% | Brown / Leaf Rust (*Puccinia triticina*), Black / Stem Rust (*Puccinia graminis*), Loose Smut (*Ustilago tritici*), Karnal Bunt | Wheat Aphid (*Rhopalosiphum padi* / *Sitobion avenae* colonies), Termites | **MEDIUM** | >10 Lakh Hectares. Crucial irrigated Rabi cereal. Warm winter climates favor stem and leaf rust epidemics (Niphad research zone). | **Yes** for distinct rust pustules on leaves and loose smutted heads (black powdery heads). | Mandatory for seed smut/bunt; conditional for leaf rust. |
| **Rice / Paddy**<br>*(भात / धान)* | 3 | 🟡 40% | Bacterial Leaf Blight (*Xanthomonas oryzae*), Brown Spot (*Bipolaris oryzae*), False Smut *(Blast & Sheath Blight already present)* | Yellow Stem Borer (*Scirpophaga incertulas* - dead heart/white earhead), Brown Planthopper (BPH hopperburn), Leaf Folder | **MEDIUM** | >15 Lakh Hectares. Staple food crop of Konkan coastal belt and Eastern Vidarbha (Bhandara, Gondia, Gadchiroli). | **Yes** for blast spindle lesions, sheath lesions, brown spots, leaf folds, and hopper burn patches. | Conditional on blast; mandatory for hopperburn/wilt. |
| **Maize / Corn**<br>*(मका)* | 21 | 🟢 80% | Consolidate 3 duplicate pairs (Rust, Gray Leaf Spot, Smut). Existing classes cover Northern Blight, Mildew, Charcoal. | Fall Armyworm (*Spodoptera frugiperda* - whorl damage, ragged holes, caterpillar), Stem Borer | **LOW to MEDIUM** | >8.5 Lakh Hectares. Key food/feed crop. Strong existing foliar coverage (21 classes); primary need is pest damage disambiguation. | **Yes** for foliar lesions, Fall Armyworm ragged whorl feeding, and insect frass. | Conditional; high-confidence AI acceptable. |
| **Tomato**<br>*(टोमॅटो)* | 14 | 🟡 70% | Consolidate 2 duplicate pairs (Mosaic Virus, TYLCV). Existing covers Early/Late Blight, Mold, Septoria, Wilt. | Tomato Leaf Miner / Pinworm (*Tuta absoluta* serpentine blotch mines), Fruit Borer (*Helicoverpa* holes), Whitefly | **LOW to MEDIUM** | >60,000 Hectares intensive vegetable belt (Nashik, Pune, Satara). High chemical spray frequency requires precise IPM timing. | **Yes** for foliar spots, blights, *Tuta absoluta* serpentine mines, and fruit borer damage. | Conditional; high-confidence AI acceptable. |
| **Citrus / Orange**<br>*(संत्रा)* | 2 | 🟡 50% | Phytophthora Gummosis / Foot Rot (*Phytophthora nicotianae*), Black Spot, Dieback *(Greening & Canker present)* | Citrus Psylla (*Diaphorina citri* vector), Leaf Miner (*Phyllocnistis citrella* serpentine trail), Fruit Sucking Moth | **MEDIUM** | >1.2 Lakh Hectares. GI-tagged Vidarbha economic asset (Nagpur Mandarin, Morshi-Warud belt). Greening & gummosis cause orchard decline. | **Yes** for canker lesions, leaf miner trails, and sooty mold; **Partial** for trunk gummosis. | Mandatory for greening (quarantine disease) and gummosis. |
| **Grape**<br>*(द्राक्ष)* | 5 | 🟡 65% | Powdery Mildew (*Erysiphe necator*), Anthracnose / Bird's Eye Spot (*Elsinoe ampelina*) *(Downy Mildew, Black Rot, Leafroll present)* | Flea Beetle (*Scelodonta strigicollis* shot-holes), Mealybug (*Maconellicoccus hirsutus* waxy colonies), Thrips | **MEDIUM** | >1.1 Lakh Hectares. Major export horticultural crop (Nashik, Sangli, Solapur). Strict Maximum Residue Limits (MRL) demand non-chemical IPM timing. | **Yes** for powdery mildew white coating, anthracnose spots, flea beetle shot-holes, and bunch mealybugs. | Conditional on mildews; mandatory for export residue advisories. |

---

## 4. Required Disease & Pest Target Taxonomy

To ensure biological authenticity and prevent fictitious disease classes, every target condition is cross-verified against authoritative agricultural research authorities: **ICAR, MPKV Rahuri, VNMKV Parbhani, Dr. PDKV Akola, ICAR-CICR Nagpur, ICAR-IISR Indore, ICRISAT Patancheru, ICAR-DOGR Pune, ICAR-NRCG Pune, and ICAR-CCRI Nagpur**.

### 1. Cotton (*Gossypium hirsutum*) — [ICAR-CICR Nagpur & VNMKV Parbhani]
- **A. Diseases:**
  - `cotton_bacterial_blight`: Angular leaf spot, vein blight, and black arm caused by *Xanthomonas citri* pv. *malvacearum*.
  - `cotton_grey_mildew`: Dahiya disease caused by *Ramularia areola* (white powdery angular patches on lower leaf surface).
  - `cotton_alternaria_leaf_spot`: Concentric brown spots caused by *Alternaria macrospora*.
  - `cotton_root_rot`: Sudden plant wilting with shredded root bark caused by *Rhizoctonia solani* / *Macrophomina phaseolina*.
- **B. Pests & Damage Patterns:**
  - `cotton_pink_bollworm_damage`: Rosette flowers (petals twisted into rosette), entrance holes on bolls with frass (*Pectinophora gossypiella*).
  - `cotton_whitefly_damage`: Leaf curling, honey-dew excretion, and black sooty mold (*Bemisia tabaci*).
  - `cotton_hopper_burn`: Marginal yellowing, downward curling, and necrotic edge scorching from Jassids (*Amrasca biguttula*).
  - `cotton_thrips_damage`: Upward leaf curling, silvery-white sheen on lower leaf lamina (*Thrips tabaci*).
- **C. Healthy:**
  - `cotton_healthy_leaf`: Intact green cotton leaf and square without discoloration or lesions.
- **D. Visible Physiological Stress:**
  - `cotton_leaf_reddening`: Reddening of leaves (Lalya) due to magnesium/nitrogen deficiency or cold night shocks.

### 2. Soybean (*Glycine max*) — [ICAR-IISR Indore & Dr. PDKV Akola]
- **A. Diseases:**
  - `soybean_rust`: Tan or reddish-brown polygonal lesions with raised uredinia pustules caused by *Phakopsora pachyrhizi*.
  - `soybean_bacterial_pustule`: Small yellowish-brown spots with raised blister centers caused by *Xanthomonas axonopodis* pv. *glycines*.
  - `soybean_yellow_mosaic_virus`: Conspicuous irregular bright yellow and green mosaic patches caused by Mungbean Yellow Mosaic India Virus (MYMIV, transmitted by whitefly).
  - `soybean_charcoal_rot`: Ashy gray discoloration of lower stem and root with tiny black microsclerotia (*Macrophomina phaseolina*).
- **B. Pests & Damage Patterns:**
  - `soybean_girdle_beetle_damage`: Characteristic double-ring girdling cut on petiole or stem causing upper leaf wilting (*Obereopsis brevis*).
  - `soybean_defoliator_damage`: Windowpane leaf scratching and skeletonized leaves caused by *Spodoptera litura* and Semilooper (*Chrysodeixis acuta*).
  - `soybean_stem_fly_damage`: Wilting and drooping of apical shoot with exit puncture holes (*Melanagromyza sojae*).
- **C. Healthy:**
  - `soybean_healthy_leaf`: Intact trifoliate soybean leaf (already indexed as class `[2] soybean leaf`).

### 3. Tur / Pigeon Pea (*Cajanus cajan*) — [ICRISAT & VNMKV Parbhani]
- **A. Diseases:**
  - `tur_sterility_mosaic`: Severe bushiness, stunted growth, reduced leaf size, and light green/yellow mosaic without flowering ("green plague", transmitted by eriophyid mite *Aceria cajani*).
  - `tur_phytophthora_blight`: Water-soaked brown to black lesions on stem, breaking at the lesion site (*Phytophthora cajani*).
  - `tur_fusarium_wilt`: Longitudinal dark purple band on stem bark extending from ground level, internal xylem browning (*Fusarium udum*).
- **B. Pests & Damage Patterns:**
  - `tur_pod_borer_damage`: Neat, circular bore holes on developing pods with caterpillar body partially inserted (*Helicoverpa armigera*).
  - `tur_plume_moth_damage`: Small irregular bore holes on pods with webbing and frass (*Exelastis atomosa*).
- **C. Healthy:**
  - `tur_healthy_leaf_pod`: Normal green trifoliate leaf and healthy green/streaked pod.

### 4. Gram / Chickpea (*Cicer arietinum*) — [ICRISAT & MPKV Rahuri]
- **A. Diseases:**
  - `gram_ascochyta_blight`: Circular to oval spots with dark brown margins and concentric rings of black pycnidia on leaves and pods (*Ascochyta rabiei*).
  - `gram_fusarium_wilt`: Drooping of petioles, yellowing and bronzing of leaves, brown-to-black internal pith discoloration (*Fusarium oxysporum* f. sp. *ciceri*).
  - `gram_dry_root_rot`: Completely dry, dark-brown brittle roots with black sclerotia under root bark (*Rhizoctonia bataticola*).
- **B. Pests & Damage Patterns:**
  - `gram_pod_borer_larva`: *Helicoverpa armigera* larva feeding directly on foliage or boring into green chickpea pods.
- **C. Healthy:**
  - `gram_healthy_canopy`: Normal pinnate chickpea compound foliage and intact pods.

### 5. Onion (*Allium cepa*) — [ICAR-DOGR Rajgurunagar, Pune]
- **A. Diseases:**
  - `onion_purple_blotch`: Small water-soaked lesions developing into oval, sunken purplish spots with concentric rings (*Alternaria porri*).
  - `onion_stemphylium_blight`: Small yellowish-pale spots rapidly elongating into light brown spindle-shaped patches with dark olive spores (*Stemphylium vesicarium*).
  - `onion_colletotrichum_twister`: Twisting, curling, and elongation of leaves and pseudo-stem with sunken yellowish spots (*Colletotrichum gloeosporioides*).
  - `onion_downy_mildew`: Pale greenish oval patches covered with violet-gray velvety fungal growth (*Peronospora destructor*).
  - `onion_basal_rot`: Yellowing and dying back of leaves from tip, white mycelium at the root-bulb junction with soft decaying bulb (*Fusarium oxysporum* f. sp. *cepae*).
- **B. Pests & Damage Patterns:**
  - `onion_thrips_damage`: Dense silvery-white patches, blotches, and curled foliage caused by sap-feeding *Thrips tabaci*.
- **C. Healthy:**
  - `onion_healthy_leaf`: Upright, tubular green foliage without spots or silvering.

### 6. Wheat (*Triticum aestivum*) — [IARI / MPKV Niphad Wheat Research Station]
- **A. Diseases:**
  - `wheat_brown_rust`: Small, round-to-oval orange-brown pustules scattered randomly across the upper leaf surface (*Puccinia triticina*).
  - `wheat_yellow_rust`: Vivid yellow-orange pustules arranged in parallel linear stripes along leaf veins (*Puccinia striiformis*).
  - `wheat_loose_smut`: Entire earhead converted into a mass of black powdery olive-brown spores (*Ustilago tritici*).
- **B. Pests & Damage Patterns:**
  - `wheat_aphid_colony`: Dense clusters of green/black aphids (*Rhopalosiphum padi*) on leaf sheaths and earheads.
- **C. Healthy:**
  - `wheat_healthy_leaf_spike`: Intact green linear leaves and healthy green flowering spikes.

### 7. Rice (*Oryza sativa*) — [Dr. BSKKV Dapoli & PDKV Nagpur]
- **A. Diseases:**
  - `rice_blast`: Spindle-shaped lesions with grayish center and brown margins on leaves (*Magnaporthe oryzae*) *(Already in model as class 60)*.
  - `rice_sheath_blight`: Irregular greenish-gray snake-skin lesions on leaf sheaths (*Rhizoctonia solani*) *(Already in model as class 36)*.
  - `rice_bacterial_leaf_blight`: Water-soaked to yellowish-white wavy stripes starting from leaf tips and margins (*Xanthomonas oryzae* pv. *oryzae*).
  - `rice_brown_spot`: Small oval or circular dark-brown lesions with gray centers (*Bipolaris oryzae*).
- **B. Pests & Damage Patterns:**
  - `rice_leaf_folder_damage`: Leaves longitudinal folded into tubes with scraped white papery feeding patches (*Cnaphalocrocis medinalis*).
  - `rice_hopper_burn`: Rapid circular yellowing and complete drying of tillers caused by Brown Planthopper (*Nilaparvata lugens*).
- **C. Healthy:**
  - `rice_healthy_leaf`: Upright green paddy leaf blades *(Already in model as class 23)*.

### 8. Maize (*Zea mays*) — [ICAR-IIMR & MPKV Rahuri]
- **A. Diseases:**
  - `corn_rust`: Harmonized class from existing duplicate classes `0` and `109` (*Puccinia sorghi*).
  - `corn_northern_leaf_blight`: Existing class `4` (*Exserohilum turcicum*).
  - `corn_gray_leaf_spot`: Harmonized class from existing duplicate classes `25` and `97` (*Cercospora zeae-maydis*).
  - `corn_smut`: Harmonized class from existing duplicate classes `82` and `102` (*Ustilago maydis*).
- **B. Pests & Damage Patterns:**
  - `corn_fall_armyworm_damage`: Large irregular ragged holes in leaf whorls with abundant sawdust-like moist frass and visible caterpillar (*Spodoptera frugiperda*). Refines current generic class `[99] Corn Insects Damages`.
- **C. Healthy:**
  - `corn_healthy_leaf`: Harmonized from classes `73` and `98`.

### 9. Tomato (*Solanum lycopersicum*) — [MPKV Rahuri & IIHR]
- **A. Diseases:**
  - `tomato_early_blight`: Concentric target-board rings surrounded by yellow chlorotic halos (*Alternaria solani*) *(Existing class 44)*.
  - `tomato_late_blight`: Large water-soaked greasy brown lesions with white mold on underside (*Phytophthora infestans*) *(Existing class 61)*.
  - `tomato_mosaic_virus`: Harmonized class from existing classes `69` and `114`.
  - `tomato_yellow_leaf_curl`: Harmonized class from existing classes `88` and `115`.
- **B. Pests & Damage Patterns:**
  - `tomato_tuta_absoluta_damage`: Irregular, wide, translucent blister-like serpentine leaf mines with dark frass grains (*Tuta absoluta*).
  - `tomato_fruit_borer_damage`: Round entrance bore-holes on green/red fruit (*Helicoverpa armigera*).
- **C. Healthy:**
  - `tomato_healthy_leaf`: Harmonized from classes `70` and `113`.

### 10. Citrus / Nagpur Mandarin (*Citrus reticulata*) — [ICAR-CCRI Nagpur]
- **A. Diseases:**
  - `citrus_canker`: Raised corky, crater-like necrotic lesions surrounded by yellow oily halos (*Xanthomonas axonopodis* pv. *citri*) *(Existing class 39)*.
  - `citrus_greening`: Asymmetric yellow blotchy mottle on leaves, upright small leaves (*Candidatus Liberibacter asiaticus*) *(Existing class 10)*.
  - `citrus_phytophthora_gummosis`: Longitudinal cracking of bark with copious brown gum exudation on the lower trunk.
- **B. Pests & Damage Patterns:**
  - `citrus_leaf_miner_damage`: Silvery serpentine translucent trails and leaf distortion (*Phyllocnistis citrella*).
- **C. Healthy:**
  - `citrus_healthy_leaf`: Normal glossy dark-green unblemished citrus foliage.

### 11. Grape (*Vitis vinifera*) — [ICAR-NRCG Pune]
- **A. Diseases:**
  - `grape_downy_mildew`: Yellowish translucent oily spots ("oil spots") on upper leaf surface, white downy growth underneath (*Plasmopara viticola*) *(Existing class 11)*.
  - `grape_powdery_mildew`: Ash-gray powdery patches on leaves, tendrils, and young berries (*Erysiphe necator*).
  - `grape_anthracnose`: Sunken circular spots with dark brown-to-black margins and grayish centers ("bird's eye spot", *Elsinoe ampelina*).
- **B. Pests & Damage Patterns:**
  - `grape_flea_beetle_damage`: Distinctive shotgun-like holes chewed in leaves and swollen buds scooped out (*Scelodonta strigicollis*).
  - `grape_mealybug_cluster`: White cottony-waxy masses of mealybugs (*Maconellicoccus hirsutus*) in bunches, leaf axils, or under bark.
- **C. Healthy:**
  - `grape_healthy_leaf`: Normal green grapevine leaves *(Existing class 19)*.

---

## 5. Candidate Dataset Discovery Plan

To acquire high-quality training and validation images for the missing/weak classes, we have conducted an extensive survey of publicly accessible, peer-reviewed, and institutional repositories. **No datasets will be downloaded until Phase 4B after licensing approval.**

| Dataset Name | Source URL / Platform | Publishing Organization | Crop(s) Covered | Disease / Pest Covered | Approximate Images | Annotation Modality | Bounding Box Availability | Image Quality & Domain | Geographic Relevance | Splits Provided | License & Restrictions | Suitability for FALCON-AI | Confidence in Provenance |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **CottonPest-BD** | [data.mendeley.com](https://data.mendeley.com/datasets/nx56994nrd/1) (DOI: `10.17632/nx56994nrd.1`) | Mendeley Data / Academic Agri-Tech | Cotton | 7 major pests: Aphids, Jassids, Thrips, Whitefly, Spotted Bollworm, etc. | ~2,400+ | Object Detection | **YES** (YOLO & Pascal VOC XML) | Real field conditions, daylight, varying foliage backgrounds | South Asian subtropical cotton agro-climate (identical to Vidarbha) | Train / Val / Test | **CC BY 4.0** (Open commercial & research use with attribution) | **HIGHEST**: Directly fills cotton pest void with verified bounding boxes. | **DEFINITIVE (100%)** |
| **SAR-CLD-2024** | [data.mendeley.com](https://data.mendeley.com/datasets/h2s5j6y78b/1) | Mendeley Data / Research Publication | Cotton | Bacterial Blight, Alternaria Leaf Spot, Grey Mildew, Healthy | ~2,000 original (+7,000 augmented) | Detection & Classification | **YES** (Lesion coordinates provided) | Genuine farmer field camera photos, natural sunlight | Indian cotton belt field conditions | Train / Test | **CC BY 4.0** (Permissive) | **HIGHEST**: Directly fills the 4 primary cotton foliar disease gaps. | **DEFINITIVE (100%)** |
| **Multi-Class Soybean Leaf Disease** | [data.mendeley.com](https://data.mendeley.com/datasets/eo0scnolhb/1) | Mendeley Data / Indian Researchers | Soybean | Soybean Rust (*Phakopsora*), Bacterial Pustule, Cercospora Blight, Sudden Death Syndrome, Healthy | ~4,500+ | Detection & Classification | **YES** (Lesion bounding boxes) | Handheld smartphone captures under outdoor daylight | Indian soybean fields (Madhya Pradesh & Maharashtra agro-climatic zones) | Pre-split (Train / Val) | **CC BY 4.0** | **CRITICAL**: Completely resolves the 0-disease deficit for Soybean. | **DEFINITIVE (100%)** |
| **Novel Pigeonpea Leaf Dataset** | [data.mendeley.com](https://data.mendeley.com/datasets/bd553pdtny.1) (DOI: `10.17632/bd553pdtny.1`) | Mendeley Data / University of Agricultural Sciences, Karnataka | Tur / Pigeon Pea | Healthy, Cercospora Leaf Spot, Leaf Webber damage, Sterility Mosaic | 1,000 RGB images (256x256 / original high-res) | Classification & Segmentation | Bounding boxes derivable from segmentation masks | Natural field environments | Peninsular Indian dryland zone (directly comparable to Marathwada) | Train / Test | **CC BY 4.0** | **VERY HIGH**: Fills completely vacant Tur/Pigeon Pea category. | **DEFINITIVE (100%)** |
| **Fusarium Wilt in Chickpea Dataset** | [kaggle.com](https://www.kaggle.com/) / Academic Agri Repository | Mendeley / Kaggle Open Research | Chickpea / Gram | Fusarium Wilt, Healthy, Collar Rot | ~4,000+ images | Classification & Severity Detection | Can be converted to plant bounding box | Field-level crop canopy shots | Indian Rabi pulse growing conditions | Train / Val / Test | **CC BY-SA 4.0** | **HIGH**: Fills primary disease requirement for Gram/Chickpea. | **HIGH (90%)** |
| **Onion Plant Leaf Dataset** | [data.mendeley.com](https://data.mendeley.com/datasets/7nxxn4gj5s/1) (DOI: `10.17632/7nxxn4gj5s.1`) | Mendeley Data / Agricultural Vision Lab | Onion | Purple Blotch (*Alternaria porri*), Stemphylium Blight, Thrips silvering damage, Healthy | ~2,500+ | Detection & Classification | **YES** (Foliar lesion bounding boxes) | Real agricultural fields, diverse lighting, weeds, soil background | Western India (Nashik/Pune agro-climatic zone) | Train / Val | **CC BY 4.0** | **CRITICAL**: Completely resolves the zero-class deficit for Onion. | **DEFINITIVE (100%)** |
| **IP102 Benchmark Dataset** | [github.com/xpwu95/IP102](https://github.com/xpwu95/IP102) (CVPR 2019) | Academic Benchmark (Wu et al.) | Rice, Corn, Wheat, Citrus, Grape | 102 insect pests including *Helicoverpa armigera*, Stem Borer, BPH, Fall Armyworm, Aphids, Leafminer | 75,222 total images; **~19,000 detection images** | Object Detection (19K images) | **YES** (Standard Pascal VOC & YOLO format) | In-the-wild agricultural fields and crops | Global agricultural conditions including Asian crops | Standard Train / Val / Test benchmark splits | **Academic Research License** | **VERY HIGH**: Provides ground-truth bounding boxes for adult & larval pests across Rice, Maize, Wheat. | **DEFINITIVE (100%)** |
| **AgriPest & Pest24** | [arxiv.org](https://arxiv.org/abs/2103.01356) / [github.com](https://github.com/) | Institute of Intelligent Machines / CAS | Maize, Wheat, Rice, Cotton | 14–24 agricultural pest species (*Spodoptera*, *Helicoverpa*, planthoppers) | ~49.7K (AgriPest) / ~25K (Pest24) | Object Detection | **YES** (High-precision bounding boxes for tiny targets) | Real field conditions & automated sticky/pheromone trap captures | Asian field crop conditions | Train / Val / Test | **Research / Open Academic** | **HIGH**: Crucial for evaluating small-object detection on pheromone sticky traps. | **VERY HIGH (95%)** |

---

## 6. Dataset Quality & Acceptance Filter

To guarantee that FALCON-AI maintains real-world field reliability without learning false background correlations, all prospective datasets must pass an **8-Point Acceptance Filter**.

### A. Acceptance Criteria Checklist (Must Pass All 8):
1. **Verifiable Provenance:** Dataset must have an authentic institutional author, university publication, or DOI (e.g., Mendeley Data, Zenodo, IEEE Dataport, CVPR/ICCV papers).
2. **Permissive Licensing:** Must possess an explicit, unambiguous open license (CC BY 4.0, CC BY-SA 4.0, or Open Academic Research). Unlicensed or "all rights reserved" web scrapes are rejected.
3. **Field Domain Authenticity (Strict Field vs. Lab Filter):** Minimum **85%** of accepted images must be captured in real fields (with natural soil, weed foliage, direct sunlight, morning dew, or cast shadows). Detached leaves photographed on plain white/black paper are restricted to a maximum 15% auxiliary regularization fraction.
4. **Taxonomic Ground Truth Verification:** Class labels must have been assigned or verified by trained plant pathologists or entomologists rather than crowdsourced taggers.
5. **Annotation Precision & Tightness:** For object detection, bounding boxes must tightly encapsulate the lesion or insect body with IoU overlap $\ge 0.80$ against anatomical boundaries.
6. **Resolution & Optical Clarity:** Images must have a minimum resolution of $640 \times 640$ pixels without severe JPEG compression artifacts ($Q \ge 75$) or motion blur that renders veins indiscernible.
7. **Geographic & Agro-climatic Concordance:** Imagery must represent crop varieties, growth stages, and disease symptom phenotypes found in Maharashtra and semi-arid peninsular India.
8. **Deduplicated Splits:** Train, validation, and test partitions must be split at the **farm/field level**, ensuring no rotated, cropped, or slightly shifted photographs of the same physical plant exist across splits.

### B. Immediate Disqualification & Rejection Triggers:
- ❌ **Synthetic / Generative AI Images:** Any diffusion-generated (Stable Diffusion, Midjourney) or GAN-synthesized crop images lacking true biological pathology.
- ❌ **Severe Background Leakage:** Datasets where a specific disease class is consistently photographed on a unique colored table, hand, or background paper, enabling the CNN to cheat by learning the background.
- ❌ **Severe Class Noise:** Datasets where bacterial blight is mixed with fungal leaf spots or where healthy leaves are misclassified.
- ❌ **Unusable Low Resolution:** Downscaled thumbnails ($<400 \times 400$ px) where lesion texture is lost.
- ❌ **Unknown or Web-Scraped Provenance:** Uncurated web dumps without metadata, camera parameters, or field locations.
- ❌ **Train/Val Contamination:** Datasets where augmented variants of the same image exist in both train and validation folders.

---

## 7. Duplicate-Class Harmonization Plan

The audit uncovered **5 biological duplicate pairs** in [`Models/PlantDiseaseDetection.pt`](file:///c:/Users/lenovo/Desktop/RoboticDrones/RoboticDrones/Models/PlantDiseaseDetection.pt), plus 2 healthy class duplicates, caused by concatenating datasets A, C, and D without harmonizing namespaces:

### Deep-Dive Analysis of the 5 Duplicate Pairs:

| Pair # | Existing IDs | Existing Conflicting Names | Pathogen / Condition | Action Required | Canonical Name | Justification |
| :---: | :---: | :--- | :--- | :---: | :--- | :--- |
| **1** | `0` & `109` | `corn rust`<br>`Corn rust leaf` | Common Rust (*Puccinia sorghi*) | **MERGE** | `corn_rust` | Identical biological disease. Class 0 was from PlantDoc; Class 109 was from Roboflow Corn. During inference, they split the probability mass (e.g. 38% on class 0, 35% on class 109), causing false `UNCERTAIN` outputs. |
| **2** | `25` & `97` | `corn gray leaf spot`<br>`Corn Gray leaf spot` | Gray Leaf Spot (*Cercospora zeae-maydis*) | **MERGE** | `corn_gray_leaf_spot` | Identical biological disease. Class 25 is lowercase PlantDoc; Class 97 is mixed-case Roboflow Corn. Merge into single canonical class head. |
| **3** | `82` & `102` | `corn smut`<br>`Corn Smut` | Common Corn Smut (*Ustilago maydis*) | **MERGE** | `corn_smut` | Identical fungal pathogen. Merge both dataset annotations under the unified label `corn_smut`. |
| **4** | `69` & `114` | `tomato mosaic virus`<br>`Tomato leaf mosaic virus` | Tomato Mosaic Tobamovirus (ToMV) | **MERGE** | `tomato_mosaic_virus` | Identical viral pathogen. Class 69 is from PlantDoc; Class 114 is from Roboflow Tomato. |
| **5** | `88` & `115` | `tomato yellow leaf curl virus`<br>`Tomato leaf yellow virus` | Tomato Yellow Leaf Curl Begomovirus (TYLCV) | **MERGE** | `tomato_yellow_leaf_curl_virus` | Identical whitefly-vectored geminivirus causing stunted leaves and upward chlorotic curling. |

### Additional Duplicate Healthy Classes to Harmonize:
- `corn leaf` (Class `73`) & `Corn Healthy` (Class `98`) $\rightarrow$ **MERGE** into `corn_healthy`
- `tomato leaf` (Class `70`) & `Tomato healthy` (Class `113`) $\rightarrow$ **MERGE** into `tomato_healthy`

### Prevention Mechanism for the Next Training Dataset:
To prevent duplicate biological concepts from ever entering the YAML dataset configuration again:
1. **Centralized Canonical Registry:** All labels must be validated against a single source of truth (`CANONICAL_LABELS_REGISTRY.json`) before any dataset compilation script runs.
2. **Deterministic Pre-Build Linting:** An automated CI/CD validation check (`scripts/lint_dataset_yaml.py`) will check that every string in `names:` is unique, lowercase snake_case, and maps to an authenticated EPPO/CABI taxonomic code.

---

## 8. Target Dataset Sizing & Balancing Strategy

To establish realistic engineering goals for Phase 4B without claiming arbitrary accuracy figures, we define **Three Tiers of Dataset Size** per newly introduced class:

| Target Tier | Minimum Images / Class | Bounding Boxes / Class | Purpose & Operational Capability | Annotation Requirements | Augmentation Policy | Validation Gates |
| :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| **Tier 1: Minimum Viable (PoC)** | **150 – 200** | $400 - 600$ | Proof-of-concept verification; establishes baseline feature extraction. | Single-annotator with pathologist signoff. Tight box around lesions. | Horizontal flip, minor affine rotation ($\pm 10^\circ$), color jitter. | $\ge 50\%$ validation AP on holdout set. |
| **Tier 2: Recommended (Production Ready)** | **500 – 800** | $1,500 - 3,000$ | Robust field deployment; withstands lighting variations, wet foliage, and varied camera sensors. | Dual-annotator agreement (IoU $\ge 0.75$). Annotate both individual lesions and whole symptom clusters. | Mosaic (0.8), Mixup (0.15), HSV jitter, RandAugment, random erasing (0.2). | $\ge 70\%$ validation AP; $<5\%$ false positive rate against healthy leaves. |
| **Tier 3: Strong (Gold Standard)** | **1,200 – 2,000** | $4,000 - 8,000$ | State-of-the-art resilience; covers multiple growth stages (seedling to maturity) across $\ge 3$ agro-climatic districts. | Expert consensus with laboratory PCR/microscopy confirmation on ambiguous samples. | Full regularized pipeline (Mosaic closed during final 10 epochs, Albumentations field blur/glare simulation). | $\ge 82\%$ validation AP; $<2\%$ confusion between biologically similar leaf spots. |

### Class-Balancing Strategy:
Agricultural datasets naturally suffer from extreme class imbalance (e.g. healthy leaves and early blight are abundant, while bacterial pustule or insect borers are scarce). To counter this without fabricating data:
1. **Effective Number of Samples Loss Weighting:** Apply class weights inversely proportional to class frequency $W_c = \frac{1 - \beta}{1 - \beta^{N_c}}$ during loss calculation.
2. **Focal Loss Formulation:** Employ Focal Loss ($\alpha=0.25, \gamma=2.0$) in the YOLO classification head to down-weight easy background examples and force gradients onto rare symptom classes.
3. **Dynamic Mosaic Sampling:** During batch compilation, oversample images containing rare classes (e.g. Pink Bollworm rosette flowers) into the 4-tile mosaic generation queue.

---

## 9. Detection vs. Classification vs. Expert-Only Strategy

A fundamental flaw in naive agricultural AI is assuming every problem can be solved by a single generic bounding box. We establish a clear boundary for when to use **YOLO Object Detection**, **Image Classification**, or **Mandatory Expert Verification**:

```
                                  Uploaded Crop Image
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         Foliar Lesion / Damage                          Whole Plant / Soil / Trunk
                  │                                               │
      Is the symptom localized?                         Can internal vascular health
      (Spots, Blights, Chewed Holes)                    be confirmed from photo alone?
            │             │                                     │               │
           YES            NO (Diffuse/Mosaic)                  YES              NO
            │                     │                             │                │
            ▼                     ▼                             ▼                ▼
       YOLO Object           Whole-Canopy                 Whole-Canopy      MANDATORY
        Detection           Classification               Classification       EXPERT
      (Bounding Box)         (Softmax/Multi)             (With Saliency)    ESCALATION
     - Early Blight       - Yellow Mosaic              - General Vigour   - Fusarium Wilt
     - Bacterial Spot     - Sterility Mosaic           - Severe Drought   - Dry Root Rot
     - Armyworm Holes     - Broad Chlorosis                               - Stem Fly Larva
```

### Detailed Modality Allocation:

| Symptom / Pathology Type | Recommended Vision Modality | Technical Rationale | What Gets Annotated / Detected |
| :--- | :---: | :--- | :--- |
| **Foliar Pathogen Lesions**<br>*(Blights, Rusts, Mildews, Spots)* | **YOLO Object Detection** | Lesions are discrete, multiple, and localized on leaf lamina. Bounding boxes enable severity calculation: $\text{Severity \%} = \frac{\sum \text{Lesion Area}}{\text{Leaf Area}} \times 100$. | Individual spots, pustules, or confluent blight patches. |
| **Insect Damage Signatures**<br>*(Windowpanes, Rosette flowers, Shot-holes)* | **YOLO Object Detection** | Feeding damage signatures are significantly larger and more stable than the transient insects that caused them. Highly specific to pest species. | Rosette flower shape, folded leaf tube, circular pod bore hole, or jagged whorl hole. |
| **Pheromone Sticky Trap Scans**<br>*(Sticky sheets, delta traps)* | **YOLO Object Detection** *(Specialized Model)* | Adult moths and flies are glued to flat grids with uniform illumination. Counting trapped moths directly yields Economic Threshold Level (ETL). | Individual adult moth bodies (e.g. Pink Bollworm, Fall Armyworm adults). |
| **Direct Insect Body on Plant**<br>*(Small sap-suckers: Aphids, Whitefly)* | **Image Classification / Expert-Only** | Individual whiteflies (1mm) or thrips nymphs (0.8mm) cannot be reliably detected by a $640 \times 640$ detector without extreme macro lenses. Detect their **damage** (honey-dew sooty mold or silvering) or escalate. | Foliar damage pattern (not individual insect bodies). |
| **Systemic Foliar Viruses**<br>*(Yellow Mosaic, Leafroll, Mosaic Virus)* | **Whole-Leaf Image Classification** | Viral chlorosis and mottle affect the entire leaf vascular network uniformly; drawing a bounding box around a portion of a mosaic leaf is biologically meaningless. | Whole leaf classification head with Grad-CAM saliency verification. |
| **Vascular Wilts & Root Rots**<br>*(Fusarium wilt, Dry Root Rot, Gummosis)* | **Mandatory Expert Verification** *(AI Assisted)* | Wilting caused by root pathogens looks virtually identical to drought stress or collar rot from aerial photos. Definitive diagnosis requires physical examination of stem vascular browning. | AI flags `status="uncertain"` with warning: "Possible vascular wilt. Check stem cross-section for brown vascular rings." |

---

## 10. Future Dataset Merging Architecture

When implementation begins in Phase 4B/4C, the dataset will be structured using a rigorous, reproducible hierarchy that prevents accidental overwrites or data loss:

```
c:/Users/lenovo/Desktop/RoboticDrones/RoboticDrones/
└── datasets/                                     [FUTURE STORAGE - NOT YET CREATED]
    ├── 01_raw_sources/                           [Read-only pristine external downloads]
    │   ├── plantdoc_v1/                          (Classes 0–88)
    │   ├── cassava_kaggle/                       (Classes 89–93)
    │   ├── corn_roboflow/                        (Classes 94–109)
    │   ├── tomato_roboflow/                      (Classes 110–115)
    │   ├── cotton_pest_bd/                       (New Mendeley Cotton Pests)
    │   ├── cotton_sar_cld/                       (New Mendeley Cotton Diseases)
    │   ├── soybean_multiclass/                   (New Mendeley Soybean Diseases)
    │   ├── pigeonpea_karnataka/                  (New Mendeley Tur Dataset)
    │   ├── onion_mendeley/                       (New Mendeley Onion Dataset)
    │   └── ip102_benchmark/                      (New CVPR Insect Detection Subsets)
    │
    ├── 02_curated_intermediate/                  [Post-cleaning, deduplicated, standardized]
    │   ├── images/                               (Standardized EXIF-stripped JPEG 640px)
    │   └── annotations_yolo/                     (Standardized normalized bbox coordinates)
    │
    └── 03_falcon_production_v2/                  [Unified split for Ultralytics training engine]
        ├── train/
        │   ├── images/                           (~70% of dataset, field-stratified)
        │   └── labels/
        ├── val/
        │   ├── images/                           (~15% of dataset, zero farm overlap)
        │   └── labels/
        ├── test_golden/                          (~15% pure benchmark holdout)
        │   ├── images/
        │   └── labels/
        ├── canonical_registry.json               (Deterministic UUID to ID map)
        └── data.yaml                             (Ultralytics dataset configuration)
```

### Deterministic Class ID Generation:
To ensure reproducible training runs, class IDs will **never** be generated from arbitrary directory listings. Instead:
1. `canonical_registry.json` maintains the exact integer index for every canonical class:
   ```json
   {
     "0": "corn_rust",
     "1": "cherry_leaf",
     "2": "soybean_healthy",
     "3": "cotton_bacterial_blight",
     "4": "cotton_pink_bollworm_damage",
     "5": "onion_purple_blotch"
   }
   ```
2. A deterministic Python compilation script reads `canonical_registry.json` and outputs `data.yaml` with classes sorted in exact numerical order.

---

## 11. Training Strategy Comparison & Recommendation

To determine how the new Maharashtra data should be trained without compromising existing capabilities, we evaluate four potential architectures:

| Parameter / Dimension | Option A: Fine-Tune Existing Model | Option B: Retrain from Curated Combined Dataset | Option C: Two-Stage Hierarchical (Crop Classifier $\rightarrow$ Specialized YOLO) | Option D: Dual-Engine Parallel (Foliar Disease YOLO + Pest/Trap YOLO) |
| :--- | :--- | :--- | :--- | :--- |
| **Description** | Freeze backbone of `PlantDiseaseDetection.pt`; replace 116-class head with expanded head; train on new crops only. | Pool cleaned existing 89/16/6-class data with new Maharashtra datasets into a single unified dataset; train from scratch. | Stage 1 CNN identifies crop type (Cotton, Soybean, etc.); routes to a crop-specific lightweight YOLO detector. | Engine 1 runs foliar disease detection (leaves); Engine 2 runs pest damage & insect trap detection. |
| **Catastrophic Forgetting Risk** | **EXTREME**: Fine-tuning on new crops inevitably degrades existing Maize, Tomato, and Grape accuracy. | **ZERO**: Retraining on pooled data jointly optimizes all classes simultaneously. | **LOW**: Retraining a single crop model does not alter other crop detectors. | **ZERO**: Disease and pest heads are mathematically isolated. |
| **Duplicate Class Resolution**| **IMPOSSIBLE**: Duplicate heads (`0` vs `109`) remain frozen into existing weights. | **PERFECT**: Allows complete merge of 5 duplicate pairs into clean canonical classes. | **EXCELLENT**: Duplicate namespaces are eliminated within crop modules. | **GOOD**: Pest classes are segregated from disease classes. |
| **Inference Latency (CPU)** | ~180 ms (Single forward pass) | ~180 ms (Single forward pass) | ~340 ms (Two serial CNN passes: Crop CNN + YOLO) | ~360 ms (Two parallel passes on CPU) |
| **Model Disk / RAM Footprint**| ~436 MB | ~220 MB (If trained on YOLO11m) | ~550 MB (1 crop classifier + 6 separate crop YOLOs) | ~450 MB (Two separate YOLO models) |
| **Engineering Complexity** | Low | Medium (Requires complete dataset curation first) | Very High (Multiple models to manage, deploy, and version) | High (Requires dual-pipeline orchestration in backend) |

### SIH 26131 Strategic Recommendation:

> [!TIP]
> **Recommended Architecture: Option B (Retrain from Curated Combined Dataset using YOLO11m backbone)**
> 
> **Rationale:**
> 1. **Eliminates Catastrophic Forgetting:** Pooling existing clean images with new Maharashtra data preserves existing Maize, Tomato, Grape, and Rice accuracy.
> 2. **Solves Duplicate Head Problem:** Only retraining from a freshly compiled dataset allows merging the 5 duplicate pairs, eliminating probability mass splitting.
> 3. **Maintains Single-Inference Speed:** Keeps inference under 200ms on a standard CPU, ensuring mobile responsiveness without heavy GPU servers.
> 4. **Optimal Model Footprint:** Stepping from YOLO11x down to YOLO11m cuts memory in half (~210 MB vs 436 MB) while maintaining $\ge 70\%$ mAP due to cleaner, deduplicated data.
> 
> *Future Evolution:* In a post-hackathon Phase 5, Engine 2 (Option D) can be added as an optional microservice dedicated exclusively to high-resolution pheromone trap counting.

---

## 12. Validation Strategy & The Golden Field Test Set

Evaluation must never rely solely on a standard random validation split, which masks domain shift and duplicate contamination.

### 1. Quantitative Benchmark Metrics:
For every validation run, the platform must log:
- **Precision (P) & Recall (R)** at IoU = 0.50
- **mAP@0.50** (Standard detection benchmark)
- **mAP@0.50–0.95** (Strict localization benchmark)
- **Per-Class Average Precision (AP)** to flag failing individual classes
- **Confusion Matrix:** Specifically monitoring cross-talk between healthy leaves and subtle early lesions.
- **False Positive Rate (FPR)** on healthy field foliage.

### 2. The Golden Field Test Set (Holdout Benchmark):
A strictly segregated **Golden Field Test Set** of ~2,500 images will be locked before training. **No image in this set may ever be seen during training, tuning, or feature selection.**

The Golden Test Set is divided into **6 Evaluation Groups**:

```
                              Golden Field Test Set
                                 (~2,500 Images)
                                        │
     ┌─────────────┬─────────────┬──────┴──────┬─────────────┬─────────────┐
     ▼             ▼             ▼             ▼             ▼             ▼
  Group 1       Group 2       Group 3       Group 4       Group 5       Group 6
  Existing    Maharashtra       New           New        Difficult     Unknown &
 Benchmark    Field Crops    Pest Images   Crop Images    Degraded     Out-of-Dist.
  Holdout     (True Farm)   (Damage/Trap) (Cotton/Pulses) (Blur/Glare)  (Weeds/Soil)
```

1. **Group 1: Existing Benchmark Holdout (~500 images):** Curated holdout of PlantDoc, Corn, and Tomato to verify that the new model has zero regression against the 69.89% baseline.
2. **Group 2: Maharashtra Field Conditions (~500 images):** Real farmer smartphone photos taken under direct noon sunlight, overcast monsoon drizzle, and dusty Khandesh field conditions.
3. **Group 3: New Pest Images (~400 images):** Focused on Pink Bollworm rosette flowers, Fall Armyworm whorl damage, and aphid colonies.
4. **Group 4: New Crop Images (~500 images):** Cotton, Soybean, Tur, Gram, and Onion images from Maharashtra farms.
5. **Group 5: Difficult / Degraded Images (~300 images):** Slightly out-of-focus, back-lit, or dirty-lens images to test the model's graceful degradation.
6. **Group 6: Unknown & Out-of-Distribution (~300 images):** Photos of non-crop leaves (weeds, teak trees, eucalyptus, sugarcane), bare soil, farm animals, and human hands. **Passing condition: The model must output zero bounding boxes or confidence $<0.30$, correctly triggering the `UNKNOWN` fallback.**

---

## 13. Safety & Expert Escalation Architecture

FALCON-AI enforces a strict principle: **The AI is an assistant; the certified Agricultural Officer / Pathologist is the authority.**

Under no circumstances will the retrained model force an unfamiliar symptom or unsupported crop into the nearest known category. The platform's 4-tier decision routing will remain hardcoded in [`pipeline.py`](file:///c:/Users/lenovo/Desktop/RoboticDrones/RoboticDrones/pipeline.py):

```
                        Input: Farmer Image + Crop Type
                                      │
                                      ▼
                      OpenCV Quality Guardrail Passed?
                                      │
                        NO ───────────┴─────────── YES
                        ▼                          ▼
               STATUS: REJECTED            Is Crop Supported
              "Retake photo: Dark/           in AI Model?
               Blurry / No Leaf"                   │
                                     NO ───────────┴─────────── YES
                                     ▼                          ▼
                              STATUS: UNKNOWN            Run YOLO Inference
                              Assisted Escalation       Highest Box Confidence:
                              to Expert Officer               max(conf)
                                                                │
                 ┌──────────────────────────────┬───────────────┴───────────────┐
                 ▼                              ▼                               ▼
          conf < 0.45                    0.45 <= conf < 0.70              conf >= 0.70
                 │                              │                               │
                 ▼                              ▼                               ▼
          STATUS: UNKNOWN               STATUS: UNCERTAIN              STATUS: IDENTIFIED
        Escalate to Expert            Escalate to Expert               Display Diagnosis
        Review Desk with              Review Desk with                 & Curated Advisory
        Location & History            AI Top-2 Hypotheses              Direct to Farmer
```

### Uncompromised Guardrail Guarantees:
1. **Never Invent a Diagnosis:** If confidence $<0.45$, `status="unknown"` is assigned. The farmer receives an explicit notification: *"Laxmi / AI could not verify symptoms with high confidence. Case forwarded to Taluka Agricultural Officer for review."*
2. **Auditable Double Storage:** The AI prediction is permanently recorded in the database `cases` table. When an expert modifies the diagnosis, their decision is recorded in `expert_reviews` with timestamp and license ID, **preserving both records for compliance**.
3. **Emergency Notification Trigger:** High-severity conditions (e.g. Pink Bollworm rosette infestation above ETL or Soybean Rust sporulation) automatically trigger an orange warning banner in the District Officer's GIS Hotspot map.

---

## 14. Key Risks & Mitigation Strategies

| Risk Factor | Probability | Impact | Proactive Mitigation Strategy |
| :--- | :---: | :---: | :--- |
| **Laboratory Background Leakage** | High | High | Enforce the 85% real-field acceptance filter. Discard any dataset featuring leaves placed on solid blue/white table surfaces. |
| **Tiny Pest Object Resolution Limit** | High | Medium | Do not attempt to detect 1mm insects on wide shots. Restrict YOLO targets to **macroscopic damage signatures** (rosette flowers, chewed whorls) and sticky traps. |
| **Domain Shift across Districts** | Medium | High | Sample training imagery across multiple distinct districts (Vidarbha black cotton soil vs. Konkan laterite red soil vs. Western Maharashtra loamy soil). |
| **Severe Class Imbalance** | High | Medium | Employ Focal Loss and dynamic Mosaic oversampling for rare classes; cap dominant healthy classes at 1,500 images. |
| **Annotation Inconsistency (Class Noise)** | Medium | High | Conduct cross-annotator validation with two independent annotators and holdout spot-checks by an MPKV/VNMKV agronomist. |
| **Regression on Existing Baseline** | Low | High | Enforce the Golden Field Test Set Group 1 gate: Retrained model must achieve mAP $\ge 69.89\%$ on existing classes before production deployment. |

---

## 15. Recommended Roadmap: DO NOW vs. DO NOT DO

### A. Categorized Action Plan:

#### 🟢 DO NOW (Phase 4A — Planning & Alignment):
- Finalize this architectural expansion blueprint ([`DATASET_EXPANSION_PLAN.md`](file:///c:/Users/lenovo/Desktop/RoboticDrones/RoboticDrones/DATASET_EXPANSION_PLAN.md)).
- Secure stakeholder approval on the 11-crop priority matrix and canonical taxonomy.
- Maintain existing backend/frontend in live operational state with zero code disruptions.

#### 🟡 DO NEXT (Phase 4B — Dataset Acquisition & Verification):
- Acquire permissive open-access datasets identified in Part 5 (CottonPest-BD, SAR-CLD-2024, Multi-Class Soybean, Pigeonpea Karnataka, Onion Mendeley).
- Execute the 8-point acceptance filter and remove laboratory background artifacts.
- Merge the 5 duplicate class pairs into the canonical taxonomy registry.
- Compile and lock the 2,500-image Golden Field Test Set.

#### 🔵 DO LATER (Phase 4C — Training & Evaluation):
- Run unified retraining on cloud GPU infrastructure (YOLO11m, 100 epochs, AdamW).
- Benchmark against the 6 Golden Test Set groups.
- Compare head-to-head with `PlantDiseaseDetection.pt`.
- If and only if demonstrably superior, stage for backend deployment.

#### 🔴 DO NOT DO (Strict Prohibitions):
- ❌ **DO NOT modify existing frontend or backend source code during planning.**
- ❌ **DO NOT overwrite or delete `Models/PlantDiseaseDetection.pt`.**
- ❌ **DO NOT retrain with duplicate classes still present in the label schema.**
- ❌ **DO NOT download datasets without verifying commercial/research license terms.**
- ❌ **DO NOT use synthetic/generative AI images for agricultural ground truth.**
- ❌ **DO NOT introduce drone aerial imagery (violates problem statement mobile camera focus).**

---

### B. Recommended Sequential Implementation Flow:

```
[Phase 4A: Planning & Target Architecture Approved]
                         │
                         ▼
           [Phase 4B: Dataset Acquisition]
    - Download verified Mendeley/Academic datasets
    - Run License and Provenance Verification
                         │
                         ▼
            [Phase 4B: Data Quality Gate]
    - Filter lab paper backgrounds (<15% max)
    - Remove corrupted/blurry images (<640px)
    - Remove exact duplicate image hashes
                         │
                         ▼
        [Phase 4B: Label Harmonization Engine]
    - Merge 5 duplicate concept pairs
    - Map all annotations to canonical_registry.json
                         │
                         ▼
          [Phase 4B: Golden Holdout Partition]
    - Lock 2,500-image Golden Field Test Set
    - Split remaining into 70% Train / 15% Val
                         │
                         ▼
           [Phase 4C: Model Retraining Run]
    - Train YOLO11m on pooled unified dataset
    - 100 epochs, AdamW, Mosaic + Mixup + Focal Loss
                         │
                         ▼
         [Phase 4C: Rigorous Evaluation Gate]
    - Test against all 6 Golden Test Set Groups
    - Compare: New mAP vs Baseline 69.89% mAP
    - Verify 0% regression on existing crops
                         │
      ┌──────────────────┴──────────────────┐
      ▼                                     ▼
   PASSES GATES                          FAILS GATES
   Deploy to Models/                     Revise data curation;
   Update taxonomy.py                    keep baseline active
```

---

## 16. Authoritative Sources & Evidence Citations

1. **ICAR-CICR Nagpur:** *Annual Report & Pest Surveillance Bulletins (Cotton Pink Bollworm, Whitefly & Bacterial Blight Management)*, ICAR-Central Institute for Cotton Research, Nagpur, Maharashtra.
2. **ICAR-IISR Indore:** *Soybean Disease Diagnosis & Integrated Management Guidelines*, ICAR-Indian Institute of Soybean Research, Indore.
3. **MPKV Rahuri:** *Package of Practices for Kharif and Rabi Crops of Maharashtra*, Mahatma Phule Krishi Vidyapeeth, Rahuri.
4. **VNMKV Parbhani:** *Marathwada Agricultural Disease Management Protocols*, Vasantrao Naik Marathwada Krishi Vidyapeeth, Parbhani.
5. **Dr. PDKV Akola:** *Crop Protection in Vidarbha Agro-Climatic Zone*, Dr. Panjabrao Deshmukh Krishi Vidyapeeth, Akola.
6. **ICRISAT Patancheru:** *Compendium of Pigeonpea and Chickpea Diseases and Pests*, International Crops Research Institute for the Semi-Arid Tropics, Hyderabad.
7. **ICAR-DOGR Pune:** *Identification and Management of Onion Diseases and Pests in Maharashtra*, Directorate of Onion and Garlic Research, Rajgurunagar, Pune.
8. **ICAR-NRCG Pune:** *Grape Pests, Diseases and Cultural Management*, National Research Centre for Grapes, Pune.
9. **ICAR-CCRI Nagpur:** *Citrus Greening and Canker Diagnostic Guidelines*, Central Citrus Research Institute, Nagpur.
10. **Singh et al. (2020):** *"PlantDoc: A Dataset for Visual Plant Disease Detection in the Wild"*, Proceedings of the 7th ACM IKDD CoDS and 25th COMAD. (Basis of Classes 0–88).
11. **Wu et al. (2019):** *"IP102: A Large-Scale Benchmark Dataset for Insect Pest Recognition"*, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). (GitHub: `xpwu95/IP102`).
12. **Mendeley Data Repository:** *CottonPest-BD: Bounding Box Dataset for Cotton Pests* (DOI: `10.17632/nx56994nrd.1`).
13. **Mendeley Data Repository:** *A Novel Pigeonpea Leaf Dataset for Detection and Classification* (DOI: `10.17632/bd553pdtny.1`).
14. **Mendeley Data Repository:** *Onion Plant Leaf Images for Disease Detection* (DOI: `10.17632/7nxxn4gj5s.1`).

---

## 17. FINAL DECISION

1. **Initial Datasets to Acquire:**  
   In Phase 4B, we should acquire exactly **5 initial public academic datasets**:
   - `CottonPest-BD` (Mendeley Data, ~2,400 images, 7 pest classes with bounding boxes)
   - `SAR-CLD-2024` (Mendeley Data, ~2,000 images, 4 cotton disease classes)
   - `Multi-Class Soybean Leaf Disease` (Mendeley Data, ~4,500 images, 5 soybean classes)
   - `Novel Pigeonpea Leaf Dataset` (Mendeley Data, ~1,000 images, 4 tur classes)
   - `Onion Plant Leaf Dataset` (Mendeley Data, ~2,500 images, 4 onion classes)
2. **Crops Addressed First:**  
   **Tier 1:** **Cotton (कापूस)** and **Soybean (सोयाबीन)** must be addressed first. Together they represent over **88 lakh hectares (>65% of Maharashtra's kharif acreage)** and have the highest economic vulnerability in Vidarbha and Marathwada.  
   **Tier 2:** **Tur/Pigeon Pea** and **Onion**.
3. **Highest Priority Disease/Pest Classes:**  
   - **Cotton:** `cotton_pink_bollworm_damage`, `cotton_bacterial_blight`, `cotton_grey_mildew`
   - **Soybean:** `soybean_rust`, `soybean_bacterial_pustule`, `soybean_girdle_beetle_damage`
   - **Onion:** `onion_purple_blotch`, `onion_thrips_damage`
   - **Tur:** `tur_sterility_mosaic`, `tur_pod_borer_damage`
4. **Baseline Model Preservation:**  
   `Models/PlantDiseaseDetection.pt` **must be strictly preserved** as the active production baseline. The FastAPI server and all frontend/backend test suites will continue running against this verified 116-class model.
5. **Retraining Timing:**  
   **Retraining must NOT happen now.** Retraining will take place only in Phase 4C after Phase 4B has completed dataset acquisition, license verification, background filtering, duplicate harmonization, and Golden Test Set lockdown.
6. **Next Engineering Task:**  
   Proceed to **Phase 4B: Dataset Acquisition, Licensing Verification & Quality Curation Scripting**, setting up download verification scripts and the canonical label registry *without touching production application code*.
