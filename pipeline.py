import cv2
import numpy as np
from ultralytics import YOLO
import base64
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "Models" / "PlantDiseaseDetection.pt"
MODEL = YOLO(str(MODEL_PATH))


def validate_specimen_framing(img_cv2):
    """
    OpenCV Guardrail:
    Filters cartoons (like Pikachu) and flat graphics while allowing real foliage.
    """
    h, w, _ = img_cv2.shape
    total_pixels = h * w
    hsv = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HSV)

    # --- 1. COLOR DOMINANCE CHECK ---
    lower_green = np.array([25, 30, 25])
    upper_green = np.array([90, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.count_nonzero(mask_green) / total_pixels
    green_contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_green_ratio = max((cv2.contourArea(contour) for contour in green_contours), default=0) / total_pixels

    lower_autumn = np.array([10, 30, 20])
    upper_autumn = np.array([24, 255, 255])
    mask_autumn = cv2.inRange(hsv, lower_autumn, upper_autumn)
    autumn_ratio = np.count_nonzero(mask_autumn) / total_pixels

    # THE PIKACHU FILTER: High yellow/orange, but virtually no green.
    if green_ratio < 0.02 and autumn_ratio > 0.15:
        return False, "Invalid Specimen: Image lacks green foliage (Possible cartoon or non-plant object)."

    if (green_ratio + autumn_ratio) < 0.04:
        return False, "Invalid Specimen: No recognizable plant foliage detected."

    if largest_green_ratio < 0.03:
        return False, "Invalid Specimen: Plant foliage is too small or fragmented in the frame."

    # --- 2. TEXTURE COMPLEXITY CHECK ---
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if laplacian_var < 25.0:
        return False, "Invalid Specimen: Image lacks organic plant texture."

    # --- 3. CLUTTER CHECK ---
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = np.count_nonzero(edges) / total_pixels
    if edge_ratio > 0.50:
        return False, "Invalid Specimen: Background is extremely cluttered."

    return True, "Valid"


def format_class_name(raw_name: str) -> str:
    """Formats raw class labels into clean, human-readable strings."""
    return raw_name.replace("___", " - ").replace("__", " - ").replace("_", " ").title()


def _encode_image(img_cv2):
    success, encoded = cv2.imencode(".jpg", img_cv2, [cv2.IMWRITE_JPEG_QUALITY, 88])
    if not success:
        return None
    return "data:image/jpeg;base64," + base64.b64encode(encoded).decode("ascii")


def _analyse_leaf_surface(img_cv2, box):
    """Estimate leaf and visibly damaged area inside the best detected leaf box."""
    height, width = img_cv2.shape[:2]
    x1, y1, x2, y2 = [int(value) for value in box]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width, x2), min(height, y2)
    crop = img_cv2[y1:y2, x1:x2]
    if crop.size == 0:
        return {"leaf_area_percent": 0.0, "damage_percent": 0.0, "markers": [], "overlay": None}

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    # Green, yellow and brown pixels form a practical field-photo leaf mask.
    leaf_mask = cv2.inRange(hsv, np.array([15, 25, 20]), np.array([100, 255, 255]))
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    leaf_pixels = leaf_mask > 0

    # Brown/yellow discoloration and very low-value tissue are visual indicators,
    # not a laboratory diagnosis. Keep the estimate constrained to the leaf.
    brown = cv2.inRange(hsv, np.array([5, 35, 20]), np.array([28, 255, 220])) > 0
    pale_or_dark = ((hsv[:, :, 1] < 55) & (hsv[:, :, 2] < 165)) | (hsv[:, :, 2] < 45)
    damage_mask = (brown | pale_or_dark) & leaf_pixels
    damage_mask = cv2.morphologyEx(damage_mask.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    markers = []
    contours, _ = cv2.findContours(damage_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    overlay = img_cv2.copy()
    overlay_crop = crop.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 220, 255), 2)
    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        area = cv2.contourArea(contour)
        if area < max(12, crop.shape[0] * crop.shape[1] * 0.001):
            continue
        marker_x, marker_y, marker_w, marker_h = cv2.boundingRect(contour)
        marker = {"x": x1 + marker_x, "y": y1 + marker_y, "width": marker_w, "height": marker_h}
        markers.append(marker)
        cv2.rectangle(overlay, (marker["x"], marker["y"]),
                      (marker["x"] + marker["width"], marker["y"] + marker["height"]), (0, 60, 255), 2)

    leaf_count = int(np.count_nonzero(leaf_pixels))
    damage_count = int(np.count_nonzero(damage_mask))
    overlay_crop[damage_mask.astype(bool)] = (0, 80, 255)
    overlay[y1:y2, x1:x2] = cv2.addWeighted(overlay_crop, 0.72, crop, 0.28, 0)
    blended = cv2.addWeighted(overlay, 0.72, img_cv2, 0.28, 0)
    return {
        "leaf_area_percent": round(leaf_count / (crop.shape[0] * crop.shape[1]) * 100, 2),
        "damage_percent": round(damage_count / max(leaf_count, 1) * 100, 2),
        "markers": markers[:20],
        "overlay": _encode_image(blended)
    }


def _make_recommendation(disease_name, damage_percent, soil_moisture=None, temperature=None, humidity=None):
    def parse_sensor(value):
        try:
            return None if value in (None, "") else float(value)
        except (TypeError, ValueError):
            return None

    moisture = parse_sensor(soil_moisture)
    temp = parse_sensor(temperature)
    air_humidity = parse_sensor(humidity)
    sensor_status = "Sensor data not connected"
    if moisture is not None:
        sensor_status = "Adequate moisture" if moisture >= 35 else "Possible dehydration"
        if moisture < 35:
            return {
                "action": "Check irrigation before spraying",
                "dosage": "No pesticide recommendation until hydration is verified",
                "sensor_status": sensor_status,
                "reason": "Low soil moisture can cause stress symptoms that resemble disease.",
                "sensor_values": {"soil_moisture": moisture, "temperature": temp, "humidity": air_humidity}
            }
    if damage_percent < 2:
        action = "Continue monitoring; no treatment indicated"
        dosage = "No fertilizer or pesticide dose recommended"
    else:
        action = f"Isolate the plant and verify {format_class_name(disease_name)} with an agronomist"
        dosage = "Use only the product label dose after field confirmation"
    return {
        "action": action,
        "dosage": dosage,
        "sensor_status": sensor_status,
        "reason": "Image guidance is an early warning, not a substitute for a local agronomy diagnosis.",
        "sensor_values": {"soil_moisture": moisture, "temperature": temp, "humidity": air_humidity}
    }


def _invalid_result(disease_name, message):
    return {
        "status": "Unidentified",
        "disease_name": disease_name,
        "confidence": 0.0,
        "message": message,
        "is_valid_crop": False,
        "leaf_area_percent": 0.0,
        "damage_percent": 0.0,
        "markers": [],
        "overlay": None,
        "recommendation": {
            "action": "Choose a clear supported crop image and try again",
            "dosage": "No fertilizer or pesticide recommendation available",
            "sensor_status": "Not applicable",
            "reason": "The image was not confidently recognized as a supported PlantVillage leaf or disease class."
        }
    }


DISEASE_TERMS = (
    "rust", "blight", "spot", "mildew", "wilt", "mosaic", "canker",
    "scorch", "rot", "curl", "virus", "anthracnose", "smut", "insect",
    "pest", "disease", "discoloration", "yellowing"
)


def _is_disease_label(raw_name):
    label = raw_name.lower()
    return any(term in label for term in DISEASE_TERMS)


def process_and_predict(image_bytes: bytes, soil_moisture=None, temperature=None, humidity=None):
    if not image_bytes or len(image_bytes) > 15 * 1024 * 1024:
        return _invalid_result("Invalid Upload", "Upload a non-empty image smaller than 15 MB.")

    nparr = np.frombuffer(image_bytes, np.uint8)
    img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_cv2 is None:
        return _invalid_result("Invalid File Format", "The uploaded file could not be read as an image.")

    is_valid, reject_reason = validate_specimen_framing(img_cv2)
    if not is_valid:
        return _invalid_result("Out of Distribution / Improper Framing", reject_reason)

    # Keep low-confidence predictions visible as uncertainty instead of calling
    # them healthy. The checkpoint contains leaf and disease classes.
    img_resized = cv2.resize(img_cv2, (640, 640))
    # Only present a disease as identified when the checkpoint clears the
    # confidence standard used for the internal demonstration.
    CONFIDENCE_THRESHOLD = 0.70

    results = MODEL(img_resized, conf=0.15, verbose=False)[0]

    if hasattr(results, 'boxes') and results.boxes is not None and len(results.boxes) > 0:
        boxes = sorted(results.boxes, key=lambda b: float(b.conf[0]), reverse=True)
        top_box = boxes[0]
        confidence = float(top_box.conf[0])

        class_id = int(top_box.cls[0])
        raw_name = MODEL.names[class_id]
        formatted_name = format_class_name(raw_name)
        surface = _analyse_leaf_surface(img_resized, top_box.xyxy[0].tolist())
        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "status": "Uncertain",
                "disease_name": f"Possible {formatted_name}",
                "confidence": round(confidence * 100, 2),
                "message": (f"The model's best match was {formatted_name}, but confidence is below the safe diagnosis threshold. "
                            "Do not apply treatment based on this result; use a clearer image or seek local confirmation."),
                "is_valid_crop": True,
                **surface,
                "recommendation": {
                    "action": "Retake the image or request local agronomy confirmation",
                    "dosage": "No fertilizer or pesticide recommendation for an uncertain result",
                    "sensor_status": "Sensor readings do not resolve the image uncertainty",
                    "reason": "The model is not sufficiently confident to distinguish similar disease symptoms."
                }
            }

        recommendation = _make_recommendation(raw_name, surface["damage_percent"], soil_moisture, temperature, humidity)
        is_disease = _is_disease_label(raw_name) and "healthy" not in raw_name.lower()
        return {
            "status": "Identified" if is_disease else "Healthy",
            "disease_name": formatted_name if is_disease else f"{formatted_name} - no disease class detected",
            "confidence": round(confidence * 100, 2),
            "message": (f"Possible {formatted_name} detected. Review the marked regions and confirm locally."
                        if is_disease else f"{formatted_name} detected. No disease class was identified in this image."),
            "is_valid_crop": True,
            **surface,
            "recommendation": recommendation
        }

    return _invalid_result(
        "Foreign or unidentified image",
        "The model did not recognize a supported PlantVillage leaf or disease class in this image."
    )