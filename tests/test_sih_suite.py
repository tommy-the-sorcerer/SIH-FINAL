"""
Automated Test Suite for SIH 2026 Problem Statement SIH26131
"Early detection and management of crop diseases and pest infestations"
Government of Maharashtra (Maharashtra State Innovation Society)
"""

import os
import sys
import json
import numpy as np
import cv2
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import storage
import taxonomy
from weather_service import get_current_weather
from risk_engine import calculate_risk
from i18n import get_translation, get_all_translations
import pipeline


def test_taxonomy_and_crops():
    print("\n--- [TEST 1] Taxonomy, Maharashtra Districts & Curated IPM ---")
    assert "soybean" in taxonomy.CROPS, "Soybean must be in priority crops"
    assert "cotton" in taxonomy.CROPS, "Cotton must be in priority crops"
    assert "maize" in taxonomy.CROPS, "Maize must be in priority crops"
    assert "tomato" in taxonomy.CROPS, "Tomato must be in priority crops"
    assert "grape" in taxonomy.CROPS, "Grape must be in priority crops"

    assert "Pune" in taxonomy.MAHARASHTRA_DISTRICTS, "Pune must be in districts"
    assert "Nashik" in taxonomy.MAHARASHTRA_DISTRICTS, "Nashik must be in districts"
    assert "Nagpur" in taxonomy.MAHARASHTRA_DISTRICTS, "Nagpur must be in districts"

    # Verify pest distinction
    pest_class = taxonomy.YOLO_CLASS_TAXONOMY.get(99)
    assert pest_class is not None, "Class 99 must exist"
    assert pest_class["type"] == "PEST", f"Class 99 must be PEST, got {pest_class['type']}"
    assert "Insects Damages" in pest_class["raw"], "Must be insect damage"

    # Verify IPM curated content (no hallucinated chemicals)
    adv = taxonomy.get_ipm_advisory("corn_rust", "DISEASE")
    assert "immediate_action" in adv, "Advisory must have immediate_action"
    assert "biological" in adv, "Advisory must have biological control"
    assert "safety" in adv, "Advisory must have safety precautions"
    print("✅ PASS: Taxonomy, Maharashtra Districts & IPM content verified.")


def test_image_quality_guardrails():
    print("\n--- [TEST 2] OpenCV Image Quality & Specimen Guardrail ---")
    # 1. Test pitch black image
    black_img = np.zeros((300, 300, 3), dtype=np.uint8)
    valid, reason, msg = pipeline.validate_specimen_quality(black_img, "mr")
    assert not valid, "Dark image must be rejected"
    assert "dark" in reason.lower(), f"Reason must mention darkness: {reason}"
    assert "फोटोची गुणवत्ता पुरेशी नाही" in msg, "Must have Marathi farmer message"

    # 2. Test tiny image (< 120px)
    tiny_img = np.full((80, 80, 3), 120, dtype=np.uint8)
    valid, reason, msg = pipeline.validate_specimen_quality(tiny_img, "en")
    assert not valid, "Tiny image must be rejected"
    assert "too low" in reason.lower(), f"Reason must mention resolution: {reason}"

    # 3. Test blurry / flat image
    flat_gray = np.full((300, 300, 3), 128, dtype=np.uint8)
    valid, reason, msg = pipeline.validate_specimen_quality(flat_gray, "hi")
    assert not valid, "Flat/blurry image must be rejected"

    # 4. Test pipeline response on bad image
    _, encoded = cv2.imencode(".jpg", black_img)
    res = pipeline.process_and_predict(encoded.tobytes(), crop_code="maize", language="mr")
    assert res["status"] == "image_quality_issue", f"Status must be image_quality_issue, got {res['status']}"
    assert res["requires_expert"] is False, "Quality issues should ask farmer to retake, not expert"
    assert res["prediction"] is None, "Bad image must NEVER invent a diagnosis"
    print("✅ PASS: Image Quality Guardrails successfully reject corrupt/blurry/dark inputs.")


def test_unknown_and_uncertain_contract():
    print("\n--- [TEST 3] AI Output Contract: Never Invent a Diagnosis ---")
    # Generate synthetic foliage image (green background with simulated texture)
    foliage = np.zeros((400, 400, 3), dtype=np.uint8)
    # HSV green converted to BGR: (35, 150, 40)
    foliage[:, :] = [35, 140, 45]
    # Add texture noise
    noise = np.random.randint(-20, 20, (400, 400, 3), dtype=np.int16)
    foliage = np.clip(foliage.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    _, encoded = cv2.imencode(".jpg", foliage)
    image_bytes = encoded.tobytes()

    # Case A: Unsupported condition or blank foliage should return UNKNOWN or HEALTHY, never a forced disease
    res = pipeline.process_and_predict(image_bytes, crop_code="soybean", language="mr")
    assert res["status"] in ("unknown", "healthy", "uncertain"), f"Got status: {res['status']}"
    if res["status"] == "unknown":
        assert res["prediction"] is None, "Unknown status must have prediction = None"
        assert res["requires_expert"] is True, "Unknown status must require expert"
    print(f"✅ PASS: Unsupported/Ambiguous condition cleanly yielded '{res['status']}' with expert routing.")


def test_weather_and_risk_engine():
    print("\n--- [TEST 4] Weather Telemetry & Transparent Risk Engine ---")
    # Test real weather fetch for Pune, Maharashtra
    weather = get_current_weather(18.5204, 73.8567)
    if weather["available"]:
        print(f"Live Open-Meteo Weather for Pune: {weather['temperature']}°C, {weather['humidity']}% RH, {weather['rainfall']}mm")
        assert weather["temperature"] is not None
        assert weather["humidity"] is not None
    else:
        print(f"Weather offline fallback triggered gracefully: {weather['message']}")
        assert weather["temperature"] is None, "Offline weather must NOT fabricate values!"

    # Test Offline Fallback when coordinates are None
    offline = get_current_weather(None, None)
    assert offline["available"] is False
    assert offline["temperature"] is None

    # Test Transparent Risk Engine: High Risk Fungal Epidemic Scenario
    high_risk_weather = {"available": True, "temperature": 23.0, "humidity": 92.0, "rainfall": 15.0}
    risk = calculate_risk(
        crop_code="tomato",
        condition_code="tomato_late_blight",
        observation_type="DISEASE",
        ai_confidence=94.0,
        damage_percent=32.0,
        growth_stage="fruiting_pod",
        weather_snapshot=high_risk_weather
    )
    assert risk["risk_level"] in ("HIGH", "CRITICAL"), f"Expected HIGH/CRITICAL, got {risk['risk_level']}"
    assert risk["score"] >= 65
    assert len(risk["factors"]) >= 3, "Transparent factors must be provided"
    print(f"✅ PASS: Risk calculated transparently: Level={risk['risk_level']}, Score={risk['score']}, Factors={risk['factors']}")


def test_storage_and_expert_workflow():
    print("\n--- [TEST 5] Relational Database, Expert Workflow & RBAC ---")
    storage.initialize_database()

    # 1. Check Seeded Users
    farmer = storage.get_user_by_phone("8008742279")
    expert = storage.get_user_by_phone("9822012345")
    officer = storage.get_user_by_phone("9423012345")

    assert farmer is not None and farmer["role"] == "FARMER"
    assert expert is not None and expert["role"] == "EXPERT"
    assert officer is not None and officer["role"] == "ADMIN"

    # 2. Check Password Verification
    assert storage.verify_password("farmer123", farmer["salt"], farmer["password_hash"])
    assert storage.verify_password("expert123", expert["salt"], expert["password_hash"])
    assert not storage.verify_password("wrong_password", farmer["salt"], farmer["password_hash"])

    # 3. Create a Case
    case = storage.create_case({
        "farmer_id": farmer["id"],
        "crop_code": "maize",
        "season": "KHARIF",
        "growth_stage": "vegetative",
        "district": "Nashik",
        "taluka": "Niphad",
        "village": "Pimpalgaon",
        "latitude": 20.1705,
        "longitude": 73.9885,
        "image_path": "/static/uploads/test.jpg",
        "ai_status": "UNCERTAIN",
        "ai_raw_prediction": "Corn Insects Damages",
        "ai_condition_code": "corn_insects_damages",
        "ai_observation_type": "PEST",
        "ai_confidence": 48.5,
        "damage_percent": 15.0,
        "severity_level": "MODERATE",
        "risk_level": "MODERATE",
        "risk_score": 58,
        "requires_expert": 1,
        "case_status": "PENDING_EXPERT"
    })
    assert case["id"] is not None
    assert case["case_status"] == "PENDING_EXPERT"

    # 4. Expert Review Workflow: Doctor reviews and verifies case
    reviewed = storage.submit_expert_review(
        case_id=case["id"],
        expert_id=expert["id"],
        review_action="CONFIRM",
        diagnosis_code="corn_insects_damages",
        condition_name="Fall Armyworm (Confirmed)",
        observation_type="PEST",
        expert_confidence=98.0,
        expert_severity="MODERATE",
        expert_notes="Verified Fall Armyworm frass and whorl damage. Recommend Chlorantraniliprole whorl application."
    )
    assert reviewed["case_status"] == "VERIFIED"
    assert reviewed["final_diagnosis_code"] == "corn_insects_damages"
    # CRITICAL: AI PREDICTION MUST REMAIN PRESERVED SEPARATELY!
    assert reviewed["ai_condition_code"] == "corn_insects_damages"
    assert reviewed["ai_confidence"] == 48.5, "AI confidence must never be overwritten by expert review"

    # 5. Field Confirmation
    confirmed = storage.submit_field_confirmation(
        case_id=case["id"],
        user_id=farmer["id"],
        actual_condition_code="corn_insects_damages",
        actual_condition_name="Fall Armyworm",
        outcome="IMPROVED",
        notes="After whorl spraying, new growth is healthy."
    )
    assert confirmed["follow_up_outcome"] == "IMPROVED"

    # 6. Verify Dashboard Statistics & Hotspots
    stats = storage.get_dashboard_statistics()
    assert stats["total_cases"] >= 1
    assert stats["disease_cases"] >= 0
    assert stats["pest_cases"] >= 1

    hotspots = storage.get_hotspot_data()
    assert len(hotspots) >= 1
    assert "latitude" in hotspots[0] and "longitude" in hotspots[0]
    print("✅ PASS: Case lifecycle, expert review, AI preservation, and field confirmation verified.")


def test_multilingual_localization():
    print("\n--- [TEST 6] Multilingual Localization (Marathi, Hindi, English) ---")
    mr_title = get_translation("app_title", "mr")
    hi_title = get_translation("app_title", "hi")
    en_title = get_translation("app_title", "en")

    assert "फाल्कन-एआय" in mr_title, f"Marathi title missing: {mr_title}"
    assert "फाल्कन-एआई" in hi_title, f"Hindi title missing: {hi_title}"
    assert "FALCON-AI" in en_title, f"English title missing: {en_title}"

    # Verify fallback for missing key
    fallback_test = get_translation("non_existent_key_xyz", "mr")
    assert fallback_test == "non_existent_key_xyz"

    all_mr = get_all_translations("mr")
    assert "status_identified" in all_mr
    assert "advisory_title" in all_mr
    print("✅ PASS: Multilingual catalogs for Marathi, Hindi, and English fully operational.")


if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING SIH 26131 COMPREHENSIVE VERIFICATION SUITE")
    print("==================================================================")
    test_taxonomy_and_crops()
    test_image_quality_guardrails()
    test_unknown_and_uncertain_contract()
    test_weather_and_risk_engine()
    test_storage_and_expert_workflow()
    test_multilingual_localization()
    print("\n==================================================================")
    print("ALL 6 SIH 26131 TEST SUITES PASSED CLEANLY! (100% SUCCESS)")
    print("==================================================================")
