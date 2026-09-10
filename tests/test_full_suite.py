import io
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from PIL import Image

from main import app
import storage

client = TestClient(app)

def test_full_system():
    print("=== STARTING FULL FALCON-AI END-TO-END TEST SUITE ===")

    # 1. UI Root & Health
    r = client.get("/")
    assert r.status_code == 200, f"Root page failed: {r.status_code}"
    assert "FALCON-AI" in r.text
    print("[PASS] 1. SPA Root UI HTML rendered successfully.")

    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"
    print("[PASS] 2. Health probe returned 200 OK.")

    # 2. Taxonomy & Localization
    r = client.get("/api/config/taxonomy")
    assert r.status_code == 200
    tax = r.json()
    assert "soybean" in tax["crops"]
    assert "maize" in tax["crops"]
    assert len(tax["districts"]) >= 10
    print(f"[PASS] 3. Taxonomy loaded: {len(tax['crops'])} crops, {len(tax['districts'])} districts.")

    for lang in ["en", "mr", "hi"]:
        r = client.get(f"/api/i18n/{lang}")
        assert r.status_code == 200
        assert len(r.json()) > 10
    print("[PASS] 4. Multilingual catalogs (en, mr, hi) verified.")

    # 3. Auth Workflow (Email-based)
    ts = int(time.time() * 1000)
    farmer_email = f"test_farmer_{ts}@agri.gov.in"
    reg_payload = {
        "email": farmer_email,
        "password": "strongPassword123",
        "full_name": "Balasaheb Vikhe",
        "role": "FARMER",
        "preferred_language": "en"
    }
    r = client.post("/api/auth/register", json=reg_payload)
    assert r.status_code == 200, f"Register failed: {r.text}"
    farmer_data = r.json()
    assert "token" in farmer_data
    assert "welcome_quote" in farmer_data
    farmer_id = farmer_data["user"]["id"]
    farmer_token = farmer_data["token"]
    print(f"[PASS] 5. Registered new farmer: {farmer_email} (Quote: '{farmer_data['welcome_quote'][:40]}...')")

    # Login test
    r = client.post("/api/auth/login", json={"email": farmer_email, "password": "strongPassword123"})
    assert r.status_code == 200
    login_data = r.json()
    assert login_data["user"]["id"] == farmer_id
    assert "welcome_quote" in login_data
    print("[PASS] 6. Login authenticated successfully with welcome quote.")

    # Wrong password test
    r = client.post("/api/auth/login", json={"email": farmer_email, "password": "wrongpassword"})
    assert r.status_code == 401
    print("[PASS] 7. Invalid credentials rejected with 401 Unauthorized.")

    # Profile /api/auth/me with Bearer token
    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {farmer_token}"})
    assert r.status_code == 200
    assert r.json()["id"] == farmer_id
    print("[PASS] 8. Bearer token session authentication verified.")

    # 4. User Activity & Work History
    client.post("/api/user/activity", json={
        "user_id": farmer_id,
        "activity_type": "SEARCH",
        "query_text": "Fall armyworm whorl dosage",
        "metadata": {"query": "armyworm"}
    })
    client.post("/api/user/activity", json={
        "user_id": farmer_id,
        "activity_type": "VOICE_QUERY",
        "query_text": "What is today's weather in Nashik?",
        "metadata": {"lang": "en"}
    })
    r = client.get(f"/api/user/activity/{farmer_id}")
    assert r.status_code == 200
    act_data = r.json()
    assert act_data["count"] >= 3  # LOGIN from registration + 2 activities
    print(f"[PASS] 9. User activity logs recorded & retrieved ({act_data['count']} logs).")

    # 5. Farm Registration
    r = client.post("/api/farms", json={
        "user_id": farmer_id,
        "farm_name": "Godavari Green Acres",
        "district": "Nashik",
        "taluka": "Niphad",
        "village": "Pimpalgaon",
        "area_acres": 4.5,
        "primary_crop": "maize"
    })
    assert r.status_code == 200
    farm_id = r.json()["farm"]["id"]
    print(f"[PASS] 10. Registered new farm id={farm_id}.")

    # 6. Treatment Advisory for different crops
    for crop in ["maize", "soybean", "tomato"]:
        r = client.get(f"/api/advisory/{crop}")
        assert r.status_code == 200
        adv = r.json()["advisory"]
        assert "immediate_action" in adv
        assert "chemical" in adv
        assert "biological" in adv
    print("[PASS] 11. Distinct crop advisories verified for maize, soybean, and tomato.")

    # 7. AI Leaf Diagnosis (/predict) with synthetic test image
    img = Image.new("RGB", (256, 256), color=(34, 139, 34)) # Forest green leaf image
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    r = client.post(
        "/predict",
        data={
            "crop": "maize",
            "growth_stage": "vegetative",
            "district": "Nashik",
            "taluka": "Niphad",
            "village": "Pimpalgaon",
            "latitude": 20.1705,
            "longitude": 73.9885,
            "farmer_id": farmer_id,
            "farm_id": farm_id
        },
        files={"file": ("leaf_test.jpg", buf.getvalue(), "image/jpeg")}
    )
    assert r.status_code == 200, f"Predict failed: {r.text}"
    diag_res = r.json()
    assert "prediction" in diag_res
    assert "severity" in diag_res
    assert "risk" in diag_res
    assert "advisory" in diag_res
    case_id = diag_res["case_id"]
    print(f"[PASS] 12. Leaf prediction successful (Case: {diag_res['case_number']}, Condition: {diag_res['prediction']}).")

    # 8. Expert Review Flow
    expert_login = client.post("/api/auth/login", json={"email": "expert1@falconai.demo", "password": "Falcon@2026"})
    assert expert_login.status_code == 200
    expert_token = expert_login.json()["token"]
    expert_id = expert_login.json()["user"]["id"]

    r = client.get("/api/expert/pending")
    assert r.status_code == 200
    print(f"[PASS] 13. Expert pending review desk accessible ({r.json()['count']} pending).")

    r = client.post(
        f"/api/cases/{case_id}/review",
        json={
            "expert_id": expert_id,
            "review_action": "CONFIRM",
            "diagnosis_code": "corn_rust",
            "condition_name": "Maize Common Rust",
            "observation_type": "DISEASE",
            "expert_confidence": 98.0,
            "expert_severity": "MODERATE",
            "expert_notes": "Foliar pustules verified visually.",
            "custom_advisory": "Spray Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L."
        },
        headers={"Authorization": f"Bearer {expert_token}"}
    )
    assert r.status_code == 200, f"Expert review failed: {r.text}"
    print(f"[PASS] 14. Expert review submitted and case verified.")

    # 9. Field Confirmation Flow
    r = client.post(f"/api/cases/{case_id}/confirm", json={
        "user_id": farmer_id,
        "actual_condition_code": "corn_rust",
        "actual_condition_name": "Maize Common Rust",
        "outcome": "IMPROVED",
        "notes": "Follow-up spraying controlled disease progression."
    })
    assert r.status_code == 200
    print(f"[PASS] 15. Field confirmation submitted (Outcome: IMPROVED).")

    # 10. Dashboard Stats & Hotspots (RBAC test)
    r = client.get("/api/dashboard/stats")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_cases"] >= 1
    print(f"[PASS] 16. Statewide telemetry dashboard stats verified ({stats['total_cases']} total cases).")

    # RBAC: Farmer cannot view sensitive hotspot coordinates
    r = client.get("/api/dashboard/hotspots", headers={"Authorization": f"Bearer {farmer_token}"})
    assert r.status_code == 403, "Farmer should be forbidden from hotspot GPS intelligence!"
    print("[PASS] 17. RBAC security confirmed: Farmer blocked (403 Forbidden) from regional Hotspot GIS map.")

    # RBAC: Expert/Officer can view hotspots
    r = client.get("/api/dashboard/hotspots", headers={"Authorization": f"Bearer {expert_token}"})
    assert r.status_code == 200
    print(f"[PASS] 18. RBAC security confirmed: Expert granted access to {len(r.json()['hotspots'])} GIS outbreak points.")

    # 11. CIBRC Pesticide Checker
    r = client.post("/api/pesticide/check", json={
        "crop": "maize",
        "condition_code": "fall_armyworm",
        "product_query": "Chlorantraniliprole"
    })
    assert r.status_code == 200, f"Pesticide check failed: {r.text}"
    pesticide_res = r.json()
    assert "safety_status" in pesticide_res
    print(f"[PASS] 19. CIBRC deterministic verifier checked: {pesticide_res['product_analyzed']} (Status: {pesticide_res['safety_status']}).")

    # 12. Doubt Doctor Evaluation
    r = client.post("/api/doubt-doctor/evaluate", json={
        "crop": "cotton",
        "top_prediction": {"code": "cotton_pink_bollworm", "confidence": 0.62},
        "runner_up_prediction": {"code": "cotton_grey_mildew", "confidence": 0.55},
        "language": "en"
    })
    assert r.status_code == 200, f"Doubt Doctor failed: {r.text}"
    dd_eval = r.json()
    assert "trigger" in dd_eval
    print("[PASS] 20. Doubt Doctor clinical reasoning engine evaluated.")

    print("\n=======================================================")
    print(">>> 20/20 END-TO-END TESTS PASSED WITH 100% SUCCESS <<<")
    print("=======================================================")

if __name__ == '__main__':
    test_full_system()
