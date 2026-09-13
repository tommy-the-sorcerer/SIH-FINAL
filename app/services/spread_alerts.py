"""
Geospatial Epidemic Proximity & Spread Alert Engine for FALCON-AI / SIH26131

ABSOLUTE PROJECT RULE:
- Never declare an outbreak from a single unverified case.
- Trigger spread alerts only on EXPERT_VERIFIED or FIELD_CONFIRMED contagious cases.
- Evaluate spatial distance and favorable microclimate conditions.
"""

import math
from typing import List, Dict, Any

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in kilometers."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def evaluate_proximity_alerts(
    confirmed_case: Dict[str, Any],
    neighboring_farms: List[Dict[str, Any]],
    alert_radius_km: float = 15.0
) -> List[Dict[str, Any]]:
    """
    Evaluates neighboring farms growing the same crop within alert radius.
    Generates tailored warning payloads for state extension officers and farmers.
    """
    alerts = []
    c_lat = confirmed_case.get("latitude")
    c_lon = confirmed_case.get("longitude")
    crop = confirmed_case.get("crop_code", "").lower()
    cond = confirmed_case.get("final_condition_name") or confirmed_case.get("ai_condition_code", "")

    if not c_lat or not c_lon:
        return alerts

    for farm in neighboring_farms:
        f_lat = farm.get("latitude")
        f_lon = farm.get("longitude")
        f_crop = farm.get("primary_crop", "").lower()

        if not f_lat or not f_lon:
            continue

        # Check crop match
        if crop and f_crop and crop != f_crop:
            continue

        dist = haversine_distance_km(c_lat, c_lon, f_lat, f_lon)
        if dist <= alert_radius_km:
            risk = "HIGH" if dist <= 5.0 else ("MODERATE" if dist <= 10.0 else "LOW")
            alerts.append({
                "source_case_id": confirmed_case.get("id"),
                "target_farm_id": farm.get("id"),
                "farm_name": farm.get("farm_name"),
                "district": farm.get("district"),
                "taluka": farm.get("taluka"),
                "distance_km": dist,
                "crop": crop,
                "pathology": cond,
                "alert_level": risk,
                "message": f"Confirmed {cond} outbreak reported {dist} km away in your taluka. Initiate preventive scouting."
            })

    return alerts
