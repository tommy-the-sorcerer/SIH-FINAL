"""
Transparent, Multi-Factor Rule-Based Agro-climatic Risk Engine
Complies with SIH26131:
- Transparent factor breakdown
- Never claims scientifically unvalidated epidemiological perfection
- Incorporates pathogen severity, damage %, micro-climate, and phenological stage
"""

from typing import Dict, Any, List, Optional


# Highly destructive pathogens with epidemic potential
HIGH_IMPACT_PATHOGENS = {
    "tomato_late_blight", "corn_rust", "rice_blast", "grape_downy_mildew",
    "corn_insects_damages", "soybean_rust", "rice_sheath_blight"
}

# Moderate foliar conditions
MODERATE_IMPACT_PATHOGENS = {
    "tomato_early_blight", "corn_northern_leaf_blight", "citrus_canker",
    "grape_black_rot", "tomato_bacterial_leaf_spot", "cucumber_angular_spot"
}


def calculate_risk(
    crop_code: str,
    condition_code: Optional[str],
    observation_type: str,
    ai_confidence: float,
    damage_percent: float,
    growth_stage: str,
    weather_snapshot: Optional[Dict[str, Any]] = None,
    recent_local_outbreak: bool = False
) -> Dict[str, Any]:
    """
    Computes a transparent risk score (0-100) and risk level:
    LOW, MODERATE, HIGH, CRITICAL, alongside human-readable contributing factors.
    """
    damage_percent = max(0.0, min(100.0, float(damage_percent if damage_percent is not None else 0.0)))
    ai_confidence = max(0.0, min(100.0, float(ai_confidence if ai_confidence is not None else 0.0)))

    factors: List[str] = []
    score = 0

    # 1. Healthy baseline
    if observation_type == "HEALTHY":
        return {
            "risk_level": "LOW",
            "score": 10,
            "factors": ["Crop foliage identified as healthy", "Routine monitoring recommended"],
            "severity_level": "NONE",
            "disclaimer": "Rule-based decision support assessment based on visible image evidence."
        }

    # 2. Unknown or Uncertain diagnosis
    if observation_type == "UNKNOWN" or not condition_code or ai_confidence < 45.0:
        score += 35
        factors.append("Diagnostic uncertainty: Unverified condition requires precautionary agronomic verification")

    # 3. Pathogen Hazard Factor
    if condition_code in HIGH_IMPACT_PATHOGENS:
        score += 35
        factors.append(f"High-impact pathogen/pest detected: {condition_code.replace('_', ' ').title()}")
    elif condition_code in MODERATE_IMPACT_PATHOGENS:
        score += 20
        factors.append(f"Moderate foliar condition identified: {condition_code.replace('_', ' ').title()}")
    elif observation_type == "PEST":
        score += 30
        factors.append("Insect pest infestation presents rapid defoliation threat")
    elif observation_type == "DISEASE":
        score += 18
        factors.append("Foliar disease symptoms confirmed on crop foliage")

    # 4. Visible Foliage Damage Factor
    if damage_percent >= 30.0:
        score += 25
        factors.append(f"High visible lesion damage ({damage_percent}% of leaf area affected)")
        severity_level = "CRITICAL" if score >= 75 else "HIGH"
    elif damage_percent >= 15.0:
        score += 16
        factors.append(f"Moderate visible lesion damage ({damage_percent}% of leaf area affected)")
        severity_level = "MODERATE"
    elif damage_percent >= 4.0:
        score += 8
        factors.append(f"Early stage foliar lesion damage ({damage_percent}% of leaf area affected)")
        severity_level = "LOW"
    else:
        score += 3
        severity_level = "LOW"

    # 5. Crop Growth Stage Susceptibility
    stage_key = (growth_stage or "").lower()
    if stage_key in ("flowering", "fruiting_pod"):
        score += 15
        factors.append("Critical reproductive/fruiting stage: high economic yield sensitivity to stress")
    elif stage_key == "seedling":
        score += 10
        factors.append("Seedling stage: high vulnerability to stand loss")
    elif stage_key == "vegetative":
        score += 5
        factors.append("Vegetative canopy development phase")
    elif stage_key == "maturity":
        score += 2
        factors.append("Crop nearing harvest maturity")

    # 6. Micro-climate & Weather Conduciveness (ONLY when real weather is available)
    if weather_snapshot and weather_snapshot.get("available"):
        temp = weather_snapshot.get("temperature")
        humidity = weather_snapshot.get("humidity")
        rainfall = weather_snapshot.get("rainfall")

        # Fungal explosion conditions: High humidity (>80%) + moderate temperatures (18-28C)
        if observation_type == "DISEASE" and humidity is not None and humidity >= 80.0:
            score += 15
            factors.append(f"High relative humidity ({humidity}%) creates active fungal spore germination conditions")
            if temp is not None and 18.0 <= temp <= 29.0:
                score += 5
                factors.append(f"Ambient temperature ({temp}°C) falls within prime disease propagation range")

        # Pest flight & multiplication: Dry, warm conditions (>30C, RH < 65%)
        if observation_type == "PEST" and temp is not None and temp >= 30.0:
            score += 12
            factors.append(f"Elevated temperatures ({temp}°C) accelerate insect reproductive cycles and feeding rate")

        # Recent precipitation
        if rainfall is not None and rainfall > 2.0:
            score += 8
            factors.append(f"Recent rainfall ({rainfall} mm) promotes rain-splash dispersal and leaf surface wetness")

    # 7. Local Outbreak Context
    if recent_local_outbreak:
        score += 12
        factors.append("Recent elevated outbreak incidence reported in same district/taluka")

    # Final normalization & Classification
    score = min(100, max(5, score))

    if score >= 80:
        risk_level = "CRITICAL"
    elif score >= 60:
        risk_level = "HIGH"
    elif score >= 35:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"

    return {
        "risk_level": risk_level,
        "score": score,
        "factors": factors,
        "severity_level": severity_level,
        "disclaimer": "Rule-based decision support assessment. Consult your local Taluka Agriculture Officer before major chemical intervention."
    }
