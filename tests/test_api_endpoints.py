"""
End-to-End API Integration Verification for SIH 26131
Tests all REST endpoints via FastAPI TestClient
"""

import sys
import io
import numpy as np
import cv2
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from main import app
import storage

client = TestClient(app)


def test_public_pages_and_config():
    print("\n--- [API TEST 1] Public UI Pages & Machine-Readable Config ---")
    res = client.get("/")
    assert res.status_code == 200
    assert "FALCON-AI" in res.text
    assert "SIH26131" in res.text

    # Taxonomy configuration
    tax_res = client.get("/api/config/taxonomy")
    assert tax_res.status_code == 200
    data = tax_res.json()
    assert "crops" in data and "districts" in data
    assert "soybean" in data["crops"]
    assert "Pune" in data["districts"]

    # Localization catalogs
    for lang in ("mr", "hi", "en"):
        l_res = client.get(f"/api/i18n/{lang}")
        assert l_res.status_code == 200
        catalog = l_res.json()
        assert "app_title" in catalog
    print("✅ PASS: UI, Taxonomy config & i18n catalogs responding.")


def test_auth_and_roles():
    print("\n--- [API TEST 2] Role-Based Authentication (Farmer, Expert, Officer) ---")
    # 1. Farmer Login
    f_res = client.post("/api/auth/login", json={"phone": "8008742279", "password": "farmer123"})
    assert f_res.status_code == 200
    farmer_data = f_res.json()["user"]
    assert farmer_data["role"] == "FARMER"
    assert "Ramesh" in farmer_data["full_name"]

    # 2. Predefined Expert Login
    e_res = client.post("/api/auth/login", json={"phone": "9000000001", "password": "Falcon@2026"})
    assert e_res.status_code == 200
    expert_data = e_res.json()["user"]
    assert expert_data["role"] == "EXPERT"
    assert "Anjali" in expert_data["full_name"]

    # 3. Predefined Officer Login
    o_res = client.post("/api/auth/login", json={"phone": "9100000001", "password": "Falcon@2026"})
    assert o_res.status_code == 200
    officer_data = o_res.json()["user"]
    assert officer_data["role"] == "ADMIN"
    assert "Kavita" in officer_data["full_name"]

    # 4. Invalid Login
    bad_res = client.post("/api/auth/login", json={"phone": "8008742279", "password": "wrongpassword"})
    assert bad_res.status_code == 401
    print("✅ PASS: RBAC authentication verified across all 3 personas.")


def test_prediction_and_case_lifecycle():
    print("\n--- [API TEST 3] Full Prediction Pipeline & Case Lifecycle ---")
    # Synthetic leaf image
    foliage = np.zeros((400, 400, 3), dtype=np.uint8)
    foliage[:, :] = [35, 145, 45]
    noise = np.random.randint(-15, 15, (400, 400, 3), dtype=np.int16)
    foliage = np.clip(foliage.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    _, enc = cv2.imencode(".jpg", foliage)
    img_bytes = enc.tobytes()

    files = {"file": ("test_leaf.jpg", img_bytes, "image/jpeg")}
    data = {
        "crop": "maize",
        "growth_stage": "vegetative",
        "district": "Pune",
        "taluka": "Baramati",
        "village": "Malegaon",
        "latitude": 18.1512,
        "longitude": 74.5770,
        "farmer_phone": "8008742279",
        "farmer_name": "Ramesh Kumar Patil",
        "language": "mr"
    }

    pred_res = client.post("/predict", files=files, data=data)
    assert pred_res.status_code == 200
    res_data = pred_res.json()

    assert "status" in res_data
    assert "risk" in res_data
    assert "advisory" in res_data
    assert res_data["status"] in ("identified", "healthy", "uncertain", "unknown")
    assert "case_id" in res_data
    created_case_id = res_data["case_id"]

    # Retrieve created case detail
    detail_res = client.get(f"/api/cases/{created_case_id}")
    assert detail_res.status_code == 200
    case_detail = detail_res.json()["case"]
    assert case_detail["district"] == "Pune"
    assert case_detail["crop_code"] == "maize"

    # Expert Review on the case
    expert_user = storage.get_user_by_phone("9000000001")
    rev_res = client.post(
        f"/api/cases/{created_case_id}/review",
        json={
            "expert_id": expert_user["id"],
            "review_action": "CONFIRM",
            "diagnosis_code": "corn_rust",
            "condition_name": "Corn Rust (Confirmed by Expert)",
            "observation_type": "DISEASE",
            "expert_confidence": 99.0,
            "expert_notes": "Prescribed Mancozeb 75 WP @ 2.5g/L."
        }
    )
    assert rev_res.status_code == 200
    rev_data = rev_res.json()["case"]
    assert rev_data["case_status"] == "VERIFIED"
    assert rev_data["final_condition_name"] == "Corn Rust (Confirmed by Expert)"

    # Field Confirmation
    conf_res = client.post(
        f"/api/cases/{created_case_id}/confirm",
        json={
            "user_id": 1,
            "actual_condition_code": "corn_rust",
            "actual_condition_name": "Corn Rust",
            "outcome": "RESOLVED",
            "notes": "Rust lesions dried out after treatment."
        }
    )
    assert conf_res.status_code == 200
    conf_data = conf_res.json()["case"]
    assert conf_data["follow_up_outcome"] == "RESOLVED"
    assert conf_data["case_status"] == "CLOSED"
    print("✅ PASS: Prediction -> Case Creation -> Expert Review -> Field Confirmation -> Closed complete!")


def test_officer_dashboard_and_gis_api():
    print("\n--- [API TEST 4] Agriculture Officer Analytics & GIS Hotspot API ---")
    stats_res = client.get("/api/dashboard/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_cases"] >= 1
    assert "district_distribution" in stats
    assert "recent_alerts" in stats

    hotspots_res = client.get("/api/dashboard/hotspots")
    assert hotspots_res.status_code == 200
    spots = hotspots_res.json()["hotspots"]
    assert len(spots) >= 1
    sample = spots[0]
    assert "latitude" in sample and "longitude" in sample
    assert "risk_level" in sample
    print(f"✅ PASS: Dashboard stats and {len(spots)} GIS hotspot markers returned.")


if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING FASTAPI END-TO-END API INTEGRATION TEST SUITE")
    print("==================================================================")
    test_public_pages_and_config()
    test_auth_and_roles()
    test_prediction_and_case_lifecycle()
    test_officer_dashboard_and_gis_api()
    print("\n==================================================================")
    print("ALL API INTEGRATION TESTS PASSED 100% CLEANLY!")
    print("==================================================================")
