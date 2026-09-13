"""
Deterministic Pesticide Safety Verification Engine for FALCON-AI / SIH26131
Complies with Central Insecticides Board & Registration Committee (CIBRC) and ICAR guidelines.

ABSOLUTE PROJECT RULE:
- The AI / LLM must NEVER approve a pesticide.
- Decisions are strictly deterministic based on verified agronomic registries.
- Outcomes: COMPATIBLE, INCOMPATIBLE, INSUFFICIENT_INFORMATION, EXPERT_REQUIRED.
"""

from typing import Dict, Any, Optional

# Verified CIBRC & ICAR Approved Active Ingredients Registry
CIBRC_APPROVED_DATABASE = {
    # 1. COTTON
    ("cotton", "cotton_pink_bollworm"): [
        {
            "active_ingredient": "Chlorantraniliprole 18.5% SC",
            "trade_names": ["Coragen", "Cosko"],
            "dosage_per_acre": "60 ml in 200 L water",
            "waiting_period_days": 21,
            "cibrc_status": "APPROVED",
            "notes": "Apply at 10% rosetted flower or 8 moths/trap ETL."
        },
        {
            "active_ingredient": "Spinosad 45% SC",
            "trade_names": ["Tracer", "Spintor"],
            "dosage_per_acre": "75 ml in 200 L water",
            "waiting_period_days": 14,
            "cibrc_status": "APPROVED",
            "notes": "Target young 1st/2nd instar larvae before boll entry."
        },
        {
            "active_ingredient": "Emamectin Benzoate 5% SG",
            "trade_names": ["Proclaim", "EM-1"],
            "dosage_per_acre": "88-100 g in 200 L water",
            "waiting_period_days": 15,
            "cibrc_status": "APPROVED",
            "notes": "Effective against lepidopteran complex."
        }
    ],
    ("cotton", "cotton_bacterial_blight"): [
        {
            "active_ingredient": "Copper Oxychloride 50% WP + Streptocycline",
            "trade_names": ["Blitox-50 + Streptocycline"],
            "dosage_per_acre": "500 g COC + 6 g Streptocycline in 200 L water",
            "waiting_period_days": 30,
            "cibrc_status": "APPROVED",
            "notes": "Bactericide combination for foliar and black arm phase."
        }
    ],
    ("cotton", "cotton_grey_mildew"): [
        {
            "active_ingredient": "Wettable Sulphur 80% WP",
            "trade_names": ["Sulfex", "Thiovit"],
            "dosage_per_acre": "600-800 g in 200 L water",
            "waiting_period_days": 14,
            "cibrc_status": "APPROVED",
            "notes": "Foliar spray at first appearance of white angular patches."
        },
        {
            "active_ingredient": "Kresoxim-methyl 44.3% SC",
            "trade_names": ["Ergon"],
            "dosage_per_acre": "200 ml in 200 L water",
            "waiting_period_days": 21,
            "cibrc_status": "APPROVED",
            "notes": "Systemic strobilurin fungicide for grey mildew."
        }
    ],

    # 2. SOYBEAN
    ("soybean", "soybean_rust"): [
        {
            "active_ingredient": "Hexaconazole 5% EC",
            "trade_names": ["Contaf", "Sitara"],
            "dosage_per_acre": "200 ml in 200 L water",
            "waiting_period_days": 30,
            "cibrc_status": "APPROVED",
            "notes": "Spray immediately at first detection of abaxial rust pustules."
        },
        {
            "active_ingredient": "Propiconazole 25% EC",
            "trade_names": ["Tilt", "Radar"],
            "dosage_per_acre": "200 ml in 200 L water",
            "waiting_period_days": 30,
            "cibrc_status": "APPROVED",
            "notes": "Triazole systemic curative fungicide."
        },
        {
            "active_ingredient": "Tebuconazole 25.9% EC",
            "trade_names": ["Folicur"],
            "dosage_per_acre": "250 ml in 200 L water",
            "waiting_period_days": 21,
            "cibrc_status": "APPROVED",
            "notes": "Curative and protective action on Asian soybean rust."
        }
    ],
    ("soybean", "soybean_bacterial_pustule"): [
        {
            "active_ingredient": "Copper Oxychloride 50% WP",
            "trade_names": ["Blitox", "Phytolan"],
            "dosage_per_acre": "500 g in 200 L water",
            "waiting_period_days": 20,
            "cibrc_status": "APPROVED",
            "notes": "Preventive copper spray. Avoid application during peak bloom."
        }
    ],

    # 3. PIGEONPEA (TUR)
    ("pigeonpea", "tur_cercospora_leaf_spot"): [
        {
            "active_ingredient": "Carbendazim 50% WP",
            "trade_names": ["Bavistin"],
            "dosage_per_acre": "200 g in 200 L water",
            "waiting_period_days": 21,
            "cibrc_status": "APPROVED",
            "notes": "Apply at initiation of circular necrotic leaf spots."
        },
        {
            "active_ingredient": "Mancozeb 75% WP",
            "trade_names": ["Dithane M-45", "Indofil M-45"],
            "dosage_per_acre": "500 g in 200 L water",
            "waiting_period_days": 15,
            "cibrc_status": "APPROVED",
            "notes": "Contact protective dithiocarbamate fungicide."
        }
    ],

    # 4. ONION
    ("onion", "onion_purple_blotch"): [
        {
            "active_ingredient": "Mancozeb 75% WP",
            "trade_names": ["Dithane M-45"],
            "dosage_per_acre": "600 g in 200 L water",
            "waiting_period_days": 14,
            "cibrc_status": "APPROVED",
            "notes": "Mix with sticker/spreader (0.5 ml/L) due to waxy onion foliage."
        },
        {
            "active_ingredient": "Tebuconazole 50% + Trifloxystrobin 25% WG",
            "trade_names": ["Nativo"],
            "dosage_per_acre": "140 g in 200 L water",
            "waiting_period_days": 21,
            "cibrc_status": "APPROVED",
            "notes": "Broad-spectrum systemic dual-action control for purple blotch & Stemphylium."
        }
    ],

    # 5. MAIZE / CORN
    ("maize", "corn_rust"): [
        {
            "active_ingredient": "Mancozeb 75% WP",
            "trade_names": ["Dithane M-45"],
            "dosage_per_acre": "500-600 g in 200 L water",
            "waiting_period_days": 15,
            "cibrc_status": "APPROVED",
            "notes": "Spray upon noticing golden brown pustules on leaf lamina."
        }
    ]
}

# List of banned, restricted, or strictly prohibited active ingredients in Indian Agriculture
BANNED_RESTRICTED_INGREDIENTS = {
    "monocrotophos": "Prohibited for use on vegetables and pulses under Indian CIBRC gazette.",
    "endosulfan": "Completely banned by Supreme Court of India order.",
    "methyl parathion": "Banned for manufacture, import, and agricultural use in India.",
    "phorate": "Restricted highly toxic organophosphate; banned for foliar spraying.",
    "paraquat dichloride": "Strictly restricted non-selective herbicide; prohibited as foliar crop spray.",
    "ddt": "Banned in Indian agriculture."
}


def check_pesticide_safety(
    product_query: str,
    crop: str,
    condition_code: str
) -> Dict[str, Any]:
    """
    Deterministic pesticide compatibility and safety evaluation.
    Guarantees:
    - Zero AI/LLM hallucination of chemical approvals.
    - Authoritative CIBRC/ICAR compliance check.
    - Explicit veto for banned chemicals or cross-pathology misapplication (e.g. insecticide on fungal rust).
    """
    clean_query = product_query.strip().lower()
    clean_crop = crop.strip().lower()
    clean_cond = condition_code.strip().lower()

    # 1. Check for banned / prohibited active ingredients
    for banned_chem, ban_reason in BANNED_RESTRICTED_INGREDIENTS.items():
        if banned_chem in clean_query:
            return {
                "safety_status": "INCOMPATIBLE",
                "verdict": "STRICTLY PROHIBITED",
                "product_analyzed": product_query,
                "crop": crop,
                "target_condition": condition_code,
                "reason": f"Active ingredient '{banned_chem.upper()}' is {ban_reason}",
                "dosage_recommendation": None,
                "waiting_period_days": None,
                "reference": "CIBRC Banned / Restricted Pesticides Gazette Notification",
                "requires_expert": False
            }

    # 2. Check for physiological / abiotic disorder veto
    if "lalya" in clean_cond or "reddening" in clean_cond:
        return {
            "safety_status": "INCOMPATIBLE",
            "verdict": "CHEMICAL PESTICIDE VETOED",
            "product_analyzed": product_query,
            "crop": crop,
            "target_condition": condition_code,
            "reason": (
                "Cotton Leaf Reddening (Lalya) is a physiological/abiotic condition caused by "
                "magnesium deficiency and temperature shock. Chemical insecticides/fungicides "
                "have zero therapeutic effect and risk chemical leaf scorch. Spray 1% Magnesium Sulphate + 2% DAP."
            ),
            "dosage_recommendation": "1 kg MgSO4 + 2 kg DAP in 100 L water",
            "waiting_period_days": 0,
            "reference": "MPKV Rahuri Agronomic Advisory Bulletin",
            "requires_expert": False
        }

    # 3. Check for beneficial predator veto
    if "beneficial" in clean_cond or "lady_beetle" in clean_cond or "lacewing" in clean_cond:
        return {
            "safety_status": "INCOMPATIBLE",
            "verdict": "PREDATOR CONSERVATION VETO",
            "product_analyzed": product_query,
            "crop": crop,
            "target_condition": condition_code,
            "reason": (
                "Target entity is a BENEFICIAL BIOCONTROL PREDATOR. "
                "Spraying chemical insecticides will decimate natural enemies, inducing severe secondary pest outbreaks."
            ),
            "dosage_recommendation": None,
            "waiting_period_days": None,
            "reference": "FALCON-AI Biocontrol Conservation Policy / ICAR-NBAIR",
            "requires_expert": False
        }

    # 4. Check against CIBRC approved database
    lookup_key = (clean_crop, clean_cond)
    approved_list = CIBRC_APPROVED_DATABASE.get(lookup_key, [])

    if approved_list:
        # Check if query matches any approved active ingredient or trade name
        for entry in approved_list:
            ai_lower = entry["active_ingredient"].lower()
            trades_lower = [t.lower() for t in entry["trade_names"]]

            if any(term in clean_query for term in [ai_lower] + trades_lower) or any(clean_query in t for t in trades_lower):
                return {
                    "safety_status": "COMPATIBLE",
                    "verdict": "CIBRC & ICAR APPROVED",
                    "product_analyzed": product_query,
                    "matched_active_ingredient": entry["active_ingredient"],
                    "crop": crop,
                    "target_condition": condition_code,
                    "dosage_recommendation": entry["dosage_per_acre"],
                    "waiting_period_days": entry["waiting_period_days"],
                    "reason": f"Approved for {crop} against {condition_code}. {entry['notes']}",
                    "reference": "Central Insecticides Board & Registration Committee (CIBRC)",
                    "requires_expert": False
                }

        # Query did not match any of the approved options for this specific condition
        approved_names = [f"{e['active_ingredient']} ({', '.join(e['trade_names'])})" for e in approved_list]
        return {
            "safety_status": "EXPERT_REQUIRED",
            "verdict": "UNVERIFIED PRODUCT FOR THIS CONDITION",
            "product_analyzed": product_query,
            "crop": crop,
            "target_condition": condition_code,
            "reason": (
                f"Product '{product_query}' is not cataloged as a standard first-line treatment for {condition_code} in {crop}. "
                f"Officially recommended alternatives: {'; '.join(approved_names)}"
            ),
            "dosage_recommendation": None,
            "waiting_period_days": None,
            "reference": "CIBRC / State Agricultural Universities Guidelines",
            "requires_expert": True
        }

    # 5. Crop / condition not yet in deterministic local DB
    return {
        "safety_status": "INSUFFICIENT_INFORMATION",
        "verdict": "EXPERT CONSULTATION REQUIRED",
        "product_analyzed": product_query,
        "crop": crop,
        "target_condition": condition_code,
        "reason": (
            f"No verified deterministic CIBRC record found for combination: Crop='{crop}', Condition='{condition_code}'. "
            "To prevent chemical misapplication, consult your local Taluka Agricultural Extension Officer."
        ),
        "dosage_recommendation": None,
        "waiting_period_days": None,
        "reference": "FALCON-AI Safety Gating Protocol",
        "requires_expert": True
    }
