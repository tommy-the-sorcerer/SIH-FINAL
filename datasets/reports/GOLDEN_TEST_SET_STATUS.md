# FALCON-AI: Golden Field Test Set Status & Specification
**SIH 26131 — Early Detection and Management of Crop Diseases and Pest Infestations**  
**Government of Maharashtra | Department of Skills, Employment, Entrepreneurship and Innovation**  
**Timestamp:** 2026-09-09T11:38:00+05:30  
**Phase:** 4C Preparation  

---

## 1. Current Physical Status

```text
STATUS = NOT AVAILABLE
```

### Physical Audit Verification:
- Directory Inspected: `datasets/golden_test/`
- Image Files Found: **0**
- Annotation Files Found: **0**
- Synthetic / Placeholders Present: **0**

> [!IMPORTANT]
> **STRICT ZERO-FABRICATION POLICY**  
> In strict conformance with SIH 26131 ethical data governance:
> 1. **Zero Fake Images:** No synthetic, GAN-generated, or diffusion-generated images have been placed into `datasets/golden_test/`.
> 2. **Zero Contamination:** Candidate training images from incoming datasets have **NOT** been copied into `golden_test/` to artificially fabricate a 2,500-image count.
> 3. **Statistical Independence:** Copying training candidates into the evaluation set constitutes catastrophic data leakage, destroying the model's out-of-distribution evaluation integrity.

---

## 2. Acquisition Specification for Future Golden Test Set

To serve as a genuine gold-standard benchmark for the Government of Maharashtra, the 2,500-image Golden Test Set must be acquired according to the following strict agronomic protocol:

### A. Agro-Climatic Zone Stratification (2,500 Images Total)

| Maharashtra Agricultural Region | Target Districts | Primary Focus Pathologies & Pests | Target Image Count |
| :--- | :--- | :--- | :---: |
| **Vidarbha Cotton & Soybean Belt** | Yavatmal, Amravati, Akola, Wardha | Cotton Pink Bollworm damage, Grey Mildew, Lalya (Leaf reddening), Soybean Rust, Anthracnose | **750** |
| **Marathwada Dryland & Pulses Hub** | Chhatrapati Sambhajinagar, Jalna, Latur, Beed | Pigeonpea (Tur) Sterility Mosaic, Cercospora Leaf Spot, Cotton Sucking Pests (Jassids/Thrips) | **600** |
| **Western Maharashtra Cash Crop Zone** | Sangli, Kolhapur, Solapur, Pune | Soybean Sudden Death Syndrome, Bacterial Pustule, Onion Purple Blotch, Sugarcane Rust | **550** |
| **Khandesh Agro-Corridor** | Jalgaon, Dhule, Nandurbar | Cotton Mirid Bugs, Spodoptera caterpillar, Banana Sigatoka leaf spot | **350** |
| **Konkan Coastal & Horticultural Zone** | Ratnagiri, Sindhudurg, Raigad | Rice Blast, Brown Spot, Mango Anthracnose & Leaf Hopper | **250** |

---

### B. Sensor, Capture & Environmental Diversity Mandates
1. **Multi-Hardware Sensors:** Images must be collected using at least 5 different smartphone models widely used by Maharashtra farmers (e.g., Xiaomi Redmi, Realme, Samsung Galaxy M-series, Vivo, OnePlus) spanning budget (8 MP) to mid-range (64 MP) sensors.
2. **Illumination Regimes:**
   - Harsh direct midday sun (> 70,000 lux) with high-contrast leaf shadows: 35%
   - Early morning / overcast diffuse light (10,000–30,000 lux): 45%
   - Golden hour / twilight low-angle light (< 10,000 lux): 20%
3. **Foliar Perspectives:**
   - Adaxial (upper leaf surface) close-ups: 40%
   - Abaxial (lower leaf surface showing rust pustules, mite colonies, sucking pest clusters): 35%
   - Whole-plant canopy perspective (capturing systemic wilt, stunting, mosaic pattern): 25%

---

### C. University Pathologist Ground-Truth Protocol
1. **Diagnostic Verification:** Every image must be independently diagnosed by at least two senior plant pathologists from Maharashtra State Agricultural Universities (SAUs):
   - Vasantrao Naik Marathwada Krishi Vidyapeeth (VNMKV), Parbhani
   - Mahatma Phule Krishi Vidyapeeth (MPKV), Rahuri
   - Dr. Panjabrao Deshmukh Krishi Vidyapeeth (PDKV), Akola
2. **Diagnostic Certainty:** Only cases with $\ge 95\%$ pathological certainty (verified visually or supported by university lab microscopy/culture) may enter the Golden Test Set.
3. **Exclusion Criteria:** Images with ambiguous dual-pathology overlap without consensus, extreme motion blur, or digital compression artifacts will be discarded.

---

### D. Cryptographic Isolation & Governance
1. **Immutable Checksums:** Upon collection, all 2,500 images will have their SHA256 hashes recorded in `datasets/manifests/golden_test_manifest.json` and committed to git.
2. **Strict Air-Gap:** The Golden Test Set will remain strictly air-gapped from any model training loop, hyperparameter tuning search, or data augmentation pipeline.
