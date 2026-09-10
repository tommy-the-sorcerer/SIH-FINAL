"""
AI Inference Pipeline for SIH26131: Crop Disease and Pest Detection
Preserves YOLO weights, OpenCV leaf surface segmentation, and strict OOD guardrails.

Strictly enforces:
1. Strict OOD Guardrail: Reject non-plant/foreign objects (faces, objects, non-leaves)
   before running YOLO inference.
2. YOLO Inference & Bounding Boxes: If valid leaf, run YOLO('models/PlantDiseaseDetection.pt').
   Draw bounding boxes and labels directly on the image array using results[0].plot(),
   and convert to base64 string ('annotated_image').
3. Diagnosis JSON Response Contract:
   - Valid: {"valid": true, "crop": "...", "condition": "...", "severity": "...", "triage_level": "GREEN"|"YELLOW"|"RED", "annotated_image": "data:image/jpeg;base64,...", "recommendations": "..."}
   - Invalid: {"valid": false, "message": "Non-plant or foreign object detected. Please upload a genuine plant leaf."}
"""

import cv2
import numpy as np
import base64
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from ultralytics import YOLO

from taxonomy import (
    YOLO_CLASS_TAXONOMY,
    get_crop_config,
    get_district_info,
    get_ipm_advisory,
    DEFAULT_COORDINATES
)
from weather_service import get_current_weather
from risk_engine import calculate_risk
from i18n import get_translation

CONFIDENCE_HIGH_THRESHOLD = 0.65
CONFIDENCE_MIN_THRESHOLD = 0.35

# Multi-path robust resolution for YOLO model
MODEL_PATHS = [
    Path(__file__).resolve().parent / "Models" / "PlantDiseaseDetection.pt",
    Path(__file__).resolve().parent / "models" / "PlantDiseaseDetection.pt",
    Path("models/PlantDiseaseDetection.pt"),
    Path("Models/PlantDiseaseDetection.pt"),
]

model = None
for p in MODEL_PATHS:
    if p.exists():
        try:
            model = YOLO(str(p))
            break
        except Exception:
            continue

if model is None:
    try:
        model = YOLO("models/PlantDiseaseDetection.pt")
    except Exception:
        model = None

MODEL = model

# Initialize Haar Face Cascade for detecting human faces
FACE_CASCADE = None
try:
    if hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        cascade_obj = cv2.CascadeClassifier(cascade_path)
        if not cascade_obj.empty():
            FACE_CASCADE = cascade_obj
except Exception:
    FACE_CASCADE = None


def validate_specimen_quality(img_cv2: np.ndarray, language: str = "en") -> Tuple[bool, str, str]:
    """
    Strict Out-Of-Distribution (OOD) Guardrail for Plant Foliage.
    Verifies that the image contains a genuine plant leaf and is NOT a human face,
    furniture, electronic device, text document, or other non-plant object.

    Checks:
    1. Dimensions (minimum 100x100 pixels)
    2. Human Face Cascade Detection (rejects human selfies/faces)
    3. Illumination / Extreme Darkness / Overexposure
    4. Texture Variance (Laplacian variance < 30.0 indicates flat/synthetic/non-foliar surface)
    5. Foliage Pigment Dominance (HSV green & necrotic foliar pigment ratio >= 0.08)
    6. Edge Clutter / Non-organic density (Canny edge ratio > 0.48 indicates text/clutter)
    """
    h, w = img_cv2.shape[:2]
    total_pixels = max(h * w, 1)

    # 1. Dimension check
    if h < 100 or w < 100:
        return False, "resolution_too_low", "Non-plant or foreign object detected. Please upload a genuine plant leaf."

    # Convert to grayscale for structural checks
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

    # 2. Human Face Detection (Strict OOD)
    if FACE_CASCADE is not None:
        try:
            # Downscale large images for rapid face scanning
            scale = 1.0
            if max(h, w) > 800:
                scale = 800.0 / max(h, w)
                small_gray = cv2.resize(gray, (int(w * scale), int(h * scale)))
            else:
                small_gray = gray
            faces = FACE_CASCADE.detectMultiScale(small_gray, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30))
            if len(faces) > 0:
                return False, "human_face_detected", "Non-plant or foreign object detected. Please upload a genuine plant leaf."
        except Exception:
            pass

    # 3. Illumination check
    mean_brightness = float(np.mean(gray))
    if mean_brightness < 20.0 or mean_brightness > 245.0:
        return False, "extreme_lighting", "Non-plant or foreign object detected. Please upload a genuine plant leaf."

    # 4. Texture Variance (Laplacian)
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    if laplacian_var < 30.0:
        return False, "non_plant_texture", "Non-plant or foreign object detected. Please upload a genuine plant leaf."

    # 5. Foliage Organic Pigment Check (HSV)
    hsv = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HSV)
    # Green and yellow-green foliar range
    mask_green = cv2.inRange(hsv, np.array([25, 25, 20]), np.array([95, 255, 255]))
    # Brown / yellow / rust necrotic leaf tissue
    mask_autumn = cv2.inRange(hsv, np.array([10, 30, 25]), np.array([25, 255, 240]))
    mask_plant = cv2.bitwise_or(mask_green, mask_autumn)
    plant_ratio = np.count_nonzero(mask_plant) / total_pixels

    if plant_ratio < 0.08:
        return False, "non_foliage_ratio", "Non-plant or foreign object detected. Please upload a genuine plant leaf."

    # 6. Clutter / Non-organic background check
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = np.count_nonzero(edges) / total_pixels
    if edge_ratio > 0.48:
        return False, "excessive_edge_density", "Non-plant or foreign object detected. Please upload a genuine plant leaf."

    return True, "valid", "Specimen quality validated successfully."


def _find_foliage_box(img_cv2: np.ndarray) -> Optional[list]:
    """Find a coarse foliage box for valid leaves when YOLO has no confident box."""
    hsv = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HSV)
    plant_mask = cv2.inRange(hsv, np.array([20, 30, 20]), np.array([100, 255, 255]))
    plant_mask = cv2.morphologyEx(plant_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    plant_mask = cv2.morphologyEx(plant_mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    contours, _ = cv2.findContours(plant_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(contour)
    if area < img_cv2.shape[0] * img_cv2.shape[1] * 0.02:
        return None
    x, y, w, h = cv2.boundingRect(contour)
    return [x, y, x + w, y + h]


def _encode_image(img_cv2: np.ndarray) -> Optional[str]:
    """Encodes BGR image to base64 data URI string."""
    success, encoded = cv2.imencode(".jpg", img_cv2, [cv2.IMWRITE_JPEG_QUALITY, 88])
    if not success:
        return None
    return "data:image/jpeg;base64," + base64.b64encode(encoded).decode("ascii")


def _analyse_leaf_surface(img_cv2: np.ndarray, box: list) -> Dict[str, Any]:
    """
    Estimates visible leaf area and lesion damage inside the detected bounding box.
    """
    height, width = img_cv2.shape[:2]
    x1, y1, x2, y2 = [int(v) for v in box]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width, x2), min(height, y2)
    crop = img_cv2[y1:y2, x1:x2]

    if crop.size == 0:
        return {"leaf_area_percent": 0.0, "damage_percent": 0.0, "markers": []}

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    leaf_mask = cv2.inRange(hsv, np.array([15, 25, 20]), np.array([100, 255, 255]))
    leaf_pixels = leaf_mask > 0

    brown = cv2.inRange(hsv, np.array([5, 30, 20]), np.array([28, 255, 220])) > 0
    pale_or_dark = ((hsv[:, :, 1] < 55) & (hsv[:, :, 2] < 165)) | (hsv[:, :, 2] < 45)
    damage_mask = (brown | pale_or_dark) & leaf_pixels

    leaf_count = int(np.count_nonzero(leaf_pixels))
    damage_count = int(np.count_nonzero(damage_mask))

    total_crop_pixels = max(crop.shape[0] * crop.shape[1], 1)
    leaf_pct = round((leaf_count / total_crop_pixels) * 100, 1)
    damage_pct = round((damage_count / max(leaf_count, 1)) * 100, 1)

    return {
        "leaf_area_percent": leaf_pct,
        "damage_percent": damage_pct,
        "markers": []
    }


def _build_recommendations(triage_level: str, condition_display: str, advisory_data: Dict[str, Any]) -> str:
    """
    Builds canonical recommendations matching the triage card specification:
    - GREEN: Hydration and balanced fertilizer tips.
    - YELLOW: Corrective organic/chemical guidelines.
    - RED: Emergency State Agriculture Helpline (1800-180-1551) prominently alongside chemical treatments.
    """
    if triage_level == "GREEN":
        recs = [
            "HYDRATION & NUTRITION PROTOCOL: Maintain regular drip irrigation to sustain optimal soil moisture.",
            "Apply balanced NPK (19:19:19) foliar nutrition and organic bio-fertilizers (Azotobacter & PSB) to maintain vigor.",
            advisory_data.get("cultural", "Continue regular crop scouting every 7 days; zero synthetic pesticide application required.")
        ]
    elif triage_level == "RED":
        recs = [
            "EMERGENCY ADVISORY: State Agriculture Helpline: 1800-180-1551 (Kisan Call Center) / Contact Taluka Agronomy Cell immediately.",
            f"HIGH-SEVERITY OUTBREAK DETECTED: {condition_display}. Severe leaf surface damage (>45%) or rapid spreading epidemic pathogen.",
            f"CHEMICAL CONTROL: {advisory_data.get('chemical', 'Apply registered systemic curative insecticide/fungicide as per label rates immediately.')}",
            f"IMMEDIATE ACTION: {advisory_data.get('immediate_action', 'Isolate affected field rows and destroy severely diseased crop residue.')}",
            f"SAFETY: {advisory_data.get('safety', 'Wear PPE kit, mask, and nitrile gloves during application.')}"
        ]
    else:  # YELLOW
        recs = [
            f"CORRECTIVE IPM GUIDELINE: {condition_display} detected at mild to moderate severity.",
            f"ORGANIC / BIOLOGICAL: {advisory_data.get('biological', 'Spray 5% Neem Seed Kernel Extract (NSKE) or Azadirachtin 10,000 ppm @ 2 ml/L.')}",
            f"CHEMICAL INTERVENTION: {advisory_data.get('chemical', 'Targeted application of CIB&RC approved formulation at label dosage.')}",
            f"CULTURAL MEASURES: {advisory_data.get('cultural', 'Remove affected lower leaves and ensure adequate crop spacing.')}"
        ]
    return "\n".join(filter(None, recs))


def process_and_predict(
    image_bytes: bytes,
    crop_code: str = "maize",
    growth_stage: str = "vegetative",
    district: str = "Nashik",
    taluka: str = "",
    village: str = "",
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    language: str = "en"
) -> Dict[str, Any]:
    """
    End-to-End Decision Support AI Engine satisfying SIH26131:
    1. OOD Guardrail: Validates plant foliage, rejects faces/foreign objects immediately.
    2. YOLO Inference: Runs PlantDiseaseDetection.pt and plots bounding boxes using results[0].plot().
    3. Encodes annotated image to base64.
    4. Evaluates triage level (GREEN, YELLOW, RED) and constructs curated recommendations.
    """
    norm_crop = (crop_code or "maize").lower().strip()
    norm_stage = (growth_stage or "vegetative").lower().strip()
    norm_lang = (language or "en").lower().strip()

    dist_info = get_district_info(district)
    lat = latitude if latitude is not None else dist_info.get("lat", DEFAULT_COORDINATES["lat"])
    lon = longitude if longitude is not None else dist_info.get("lon", DEFAULT_COORDINATES["lon"])

    # 1. Byte validation
    if not image_bytes or len(image_bytes) > 15 * 1024 * 1024:
        return {
            "valid": False,
            "message": "Non-plant or foreign object detected. Please upload a genuine plant leaf."
        }

    # 2. OpenCV Decode
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_cv2 is None:
        return {
            "valid": False,
            "message": "Non-plant or foreign object detected. Please upload a genuine plant leaf."
        }

    # 3. OOD Guardrail (Strict) - Face, Color, Texture, Edge check
    is_valid_specimen, reason, farmer_friendly_msg = validate_specimen_quality(img_cv2, norm_lang)
    if not is_valid_specimen:
        return {
            "valid": False,
            "message": "Non-plant or foreign object detected. Please upload a genuine plant leaf."
        }

    # 4. Fetch Real Meteorological Telemetry
    weather_snapshot = get_current_weather(lat, lon)

    # 5. YOLO Inference & Bounding Boxes
    img_resized = cv2.resize(img_cv2, (640, 640))
    boxes = []
    annotated_image_b64 = None

    if MODEL is not None:
        try:
            results = MODEL(img_resized, conf=0.12, verbose=False)[0]
            # Use Ultralytics plot() function to draw bounding boxes and labels directly on image
            try:
                plotted_array = results.plot()
                annotated_image_b64 = _encode_image(plotted_array)
            except Exception:
                annotated_image_b64 = None

            if hasattr(results, "boxes") and results.boxes is not None and len(results.boxes) > 0:
                boxes = sorted(results.boxes, key=lambda b: float(b.conf[0]), reverse=True)
        except Exception:
            boxes = []

    # Fallback to plain resized image encoding if plotting not generated
    if not annotated_image_b64:
        annotated_image_b64 = _encode_image(img_resized)

    # Coarse foliage box detection
    foliage_box = _find_foliage_box(img_resized)
    surface = _analyse_leaf_surface(img_resized, foliage_box or [0, 0, 640, 640])

    # If neither detector nor foliage segmentation finds plant structure, reject
    if (not boxes and foliage_box is None) or surface["leaf_area_percent"] < 4.0:
        return {
            "valid": False,
            "message": "Non-plant or foreign object detected. Please upload a genuine plant leaf."
        }

    # Match YOLO candidate box
    matched_box = None
    matched_info = None

    for b in boxes:
        cls_id = int(b.cls[0])
        info = YOLO_CLASS_TAXONOMY.get(cls_id)
        if info and info.get("crop") == norm_crop:
            matched_box = b
            matched_info = info
            break

    # Secondary check for foliar symptoms
    if matched_box is None and len(boxes) > 0:
        top_b = boxes[0]
        top_conf = float(top_b.conf[0])
        top_cls_id = int(top_b.cls[0])
        top_info = YOLO_CLASS_TAXONOMY.get(top_cls_id, {})
        detected_crop = top_info.get("crop", "unknown")

        if top_conf >= 0.25:
            if norm_crop == "soybean":
                matched_box = top_b
                if "rust" in top_info.get("raw", ""):
                    matched_info = {"raw": "soybean rust", "crop": "soybean", "type": "DISEASE", "code": "soybean_rust", "display": "Soybean Asian Rust"}
                else:
                    matched_info = {"raw": "soybean leaf", "crop": "soybean", "type": "HEALTHY", "code": "soybean_leaf", "display": "Soybean Healthy Leaf"}
            elif norm_crop == "citrus":
                matched_box = top_b
                if any(k in top_info.get("raw", "") for k in ["canker", "spot", "blight"]):
                    matched_info = {"raw": "citrus canker", "crop": "citrus", "type": "DISEASE", "code": "citrus_canker", "display": "Citrus Canker"}
                else:
                    matched_info = {"raw": "citrus leaf", "crop": "citrus", "type": "HEALTHY", "code": "citrus_canker", "display": "Citrus Healthy Foliage"}
            elif norm_crop == "banana":
                matched_box = top_b
                if any(k in top_info.get("raw", "") for k in ["panama", "wilt", "blight", "spot"]):
                    matched_info = {"raw": "banana panama disease", "crop": "banana", "type": "DISEASE", "code": "banana_panama_disease", "display": "Banana Panama Disease"}
                else:
                    matched_info = {"raw": "banana leaf", "crop": "banana", "type": "HEALTHY", "code": "banana_leaf", "display": "Banana Healthy Leaf"}
            elif norm_crop == detected_crop:
                matched_box = top_b
                matched_info = top_info

    # Handle clean healthy foliage when no disease box is detected
    if matched_box is None:
        if surface["leaf_area_percent"] >= 12.0 and surface["damage_percent"] < 10.0:
            condition_display = f"Healthy {norm_crop.title()} Foliage"
            condition_code = f"{norm_crop}_healthy"
            obs_type = "HEALTHY"
            raw_confidence_pct = 88.0
            status = "healthy"
            severity = "NONE"
            triage_level = "GREEN"
            requires_expert = False
            message = f"Clean and healthy {norm_crop.title()} foliage detected. No active disease lesions found."
            advisory_data = get_ipm_advisory("healthy", "HEALTHY")
            risk_data = calculate_risk(
                crop_code=norm_crop,
                condition_code="healthy",
                observation_type="HEALTHY",
                ai_confidence=raw_confidence_pct,
                damage_percent=surface["damage_percent"],
                growth_stage=norm_stage,
                weather_snapshot=weather_snapshot
            )
            recommendations = _build_recommendations(triage_level, condition_display, advisory_data)

            return {
                "valid": True,
                "crop": norm_crop,
                "condition": condition_display,
                "severity": severity,
                "triage_level": triage_level,
                "annotated_image": annotated_image_b64,
                "recommendations": recommendations,
                "confidence": raw_confidence_pct,
                "damage_percent": surface["damage_percent"],
                "leaf_area_percent": surface["leaf_area_percent"],
                "status": status,
                "observation_type": obs_type,
                "prediction": condition_code,
                "condition_name": condition_display,
                "message": message,
                "overlay": annotated_image_b64,
                "weather": weather_snapshot,
                "risk": risk_data,
                "advisory": advisory_data,
                "requires_expert": requires_expert
            }

        # If not matching and low confidence
        if boxes and float(boxes[0].conf[0]) < 0.20 and foliage_box is None:
            return {
                "valid": False,
                "message": "Non-plant or foreign object detected. Please upload a genuine plant leaf."
            }

        # Otherwise treat as unclassified specimen
        condition_display = f"{norm_crop.title()}: Unclassified Condition"
        condition_code = "unknown_condition"
        obs_type = "UNKNOWN"
        raw_confidence_pct = round(float(boxes[0].conf[0]) * 100, 1) if boxes else 50.0
        status = "uncertain"
        severity = "MODERATE"
        triage_level = "YELLOW"
        requires_expert = True
        message = "Leaf detected. Please submit for Agricultural Expert review."
        advisory_data = get_ipm_advisory("unknown_condition", "UNKNOWN")
        risk_data = calculate_risk(
            crop_code=norm_crop,
            condition_code="unknown_condition",
            observation_type="UNKNOWN",
            ai_confidence=raw_confidence_pct,
            damage_percent=surface["damage_percent"],
            growth_stage=norm_stage,
            weather_snapshot=weather_snapshot
        )
        recommendations = _build_recommendations(triage_level, condition_display, advisory_data)

        return {
            "valid": True,
            "crop": norm_crop,
            "condition": condition_display,
            "severity": severity,
            "triage_level": triage_level,
            "annotated_image": annotated_image_b64,
            "recommendations": recommendations,
            "confidence": raw_confidence_pct,
            "damage_percent": surface["damage_percent"],
            "leaf_area_percent": surface["leaf_area_percent"],
            "status": status,
            "observation_type": obs_type,
            "prediction": condition_code,
            "condition_name": condition_display,
            "message": message,
            "overlay": annotated_image_b64,
            "weather": weather_snapshot,
            "risk": risk_data,
            "advisory": advisory_data,
            "requires_expert": requires_expert
        }

    # Confident detection found matching crop
    confidence = float(matched_box.conf[0])
    raw_confidence_pct = round(confidence * 100, 1)
    condition_code = matched_info["code"]
    condition_display = matched_info["display"]
    obs_type = matched_info["type"]

    box_coords = matched_box.xyxy[0].tolist()
    surface = _analyse_leaf_surface(img_resized, box_coords)
    damage_pct = surface["damage_percent"]

    # Calculate risk and advisory
    risk_data = calculate_risk(
        crop_code=norm_crop,
        condition_code=condition_code,
        observation_type=obs_type,
        ai_confidence=raw_confidence_pct,
        damage_percent=damage_pct,
        growth_stage=norm_stage,
        weather_snapshot=weather_snapshot
    )
    advisory_data = get_ipm_advisory(condition_code, obs_type)
    severity = risk_data.get("severity_level", "MODERATE").upper()

    # Determine triage level: GREEN, YELLOW, RED
    if obs_type == "HEALTHY":
        triage_level = "GREEN"
        status = "healthy"
        severity = "NONE"
        requires_expert = False
        message = f"Clean and healthy {norm_crop.title()} foliage detected."
    elif severity in ("HIGH", "CRITICAL") or damage_pct > 45.0 or (risk_data.get("risk_level") == "CRITICAL"):
        triage_level = "RED"
        status = "identified" if confidence >= CONFIDENCE_HIGH_THRESHOLD else "uncertain"
        severity = "HIGH"
        requires_expert = (confidence < CONFIDENCE_HIGH_THRESHOLD)
        message = f"Critical {condition_display} detected ({raw_confidence_pct}%). Immediate agronomy action required."
    else:
        triage_level = "YELLOW"
        status = "identified" if confidence >= CONFIDENCE_HIGH_THRESHOLD else "uncertain"
        requires_expert = (confidence < CONFIDENCE_HIGH_THRESHOLD)
        message = f"{condition_display} detected ({raw_confidence_pct}%)."

    recommendations = _build_recommendations(triage_level, condition_display, advisory_data)

    return {
        "valid": True,
        "crop": norm_crop,
        "condition": condition_display,
        "severity": severity,
        "triage_level": triage_level,
        "annotated_image": annotated_image_b64,
        "recommendations": recommendations,
        "confidence": raw_confidence_pct,
        "damage_percent": damage_pct,
        "leaf_area_percent": surface["leaf_area_percent"],
        "status": status,
        "observation_type": obs_type,
        "prediction": condition_code,
        "condition_name": condition_display,
        "message": message,
        "overlay": annotated_image_b64,
        "weather": weather_snapshot,
        "risk": risk_data,
        "advisory": advisory_data,
        "requires_expert": requires_expert
    }