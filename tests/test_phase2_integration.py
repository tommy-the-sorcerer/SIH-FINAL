"""
Phase 2 End-to-End Integration Verification Suite
Tests all 10 views, static assets, APIs, and prediction lifecycle.
"""

import sys
import io
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_phase2_full_integration():
    print("==================================================================")
    print("PHASE 2 INTEGRATION VERIFICATION: FRONTEND & BACKEND")
    print("==================================================================")

    # 1. Check HTML Views
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    expected_views = [
        "view-dashboard",
        "view-diagnose",
        "view-fields",
        "view-alerts",
        "view-weather",
        "view-hotspots",
        "view-advisory",
        "view-sensors",
        "view-expert",
        "view-officer"
    ]
    for v in expected_views:
        assert f'id="{v}"' in html, f"Missing view panel #{v}"
    print(f"[DOM] All {len(expected_views)} view panels exist.")

    # Check SIH Functional Widgets in DOM
    assert 'cibrc-verifier-widget' in html, "Missing CIBRC pesticide verifier widget"
    assert 'res-doubt-doctor-box' in html, "Missing Doubt Doctor clarification box"
    assert 'inspection-modal' in html, "Missing guided field inspection modal"
    print("[DOM] CIBRC Verifier, Doubt Doctor, and Inspection Modal present in DOM.")

    # 2. Check Static Assets
    for asset in ["/static/css/style.css", "/static/js/app.js", "/static/images/falcon-logo.svg"]:
        r = client.get(asset)
        assert r.status_code == 200, f"Asset {asset} returned {r.status_code}"
    print("[ASSETS] style.css, app.js, and falcon-logo.svg loaded successfully.")

    # 3. Test Dashboard Stats
    r = client.get("/api/dashboard/stats")
    assert r.status_code == 200
    stats = r.json()
    assert "total_cases" in stats
    assert "disease_cases" in stats
    assert "pest_cases" in stats
    assert "high_risk_cases" in stats
    assert "recent_alerts" in stats
    assert "crop_distribution" in stats
    assert "district_distribution" in stats
    print(f"[API] /api/dashboard/stats: Total cases={stats['total_cases']}, Alerts count={len(stats.get('recent_alerts', []))}")

    # 4. Test Farms API (My Fields)
    r = client.get("/api/farms")
    assert r.status_code == 200
    farms_data = r.json()
    farms = farms_data.get("farms", [])
    assert len(farms) > 0, "No farms returned"
    print(f"[API] /api/farms: {len(farms)} farms returned. First farm: {farms[0]['farm_name']}, crop: {farms[0]['primary_crop']}")

    r = client.get("/api/farms?user_id=1")
    assert r.status_code == 200
    farmer_farms = r.json().get("farms", [])
    assert len(farmer_farms) > 0, "No farmer farms returned for user_id=1"
    print(f"[API] /api/farms?user_id=1: {len(farmer_farms)} farms returned.")

    # 5. Test Weather API (Pune and Nashik)
    r = client.get("/api/weather/current?district=Nashik")
    assert r.status_code == 200
    w = r.json()
    assert "temperature" in w
    assert "humidity" in w
    assert "wind_speed" in w
    print(f"[API] /api/weather/current?district=Nashik: {w['temperature']}°C, {w['humidity']}% RH")

    # 6. Test Advisory API
    r = client.get("/api/advisory/corn_fall_armyworm")
    assert r.status_code == 200
    adv = r.json()
    assert adv["status"] == "success"
    assert "advisory" in adv
    assert "cultural" in adv["advisory"]
    assert "biological" in adv["advisory"]
    assert "chemical" in adv["advisory"]
    print(f"[API] /api/advisory/corn_fall_armyworm: status={adv['status']}, chemical recommendations={len(adv['advisory']['chemical'])}")

    # 7. Test Hotspots API
    r = client.get("/api/dashboard/hotspots")
    assert r.status_code == 200
    hotspots_data = r.json()
    hotspots = hotspots_data.get("hotspots", [])
    assert len(hotspots) > 0
    print(f"[API] /api/dashboard/hotspots: {len(hotspots)} GIS markers returned.")

    # 8. Test Cases API (for history / expert / alerts)
    r = client.get("/api/cases?limit=5")
    assert r.status_code == 200
    cases_data = r.json()
    cases = cases_data.get("cases", [])
    assert len(cases) > 0
    print(f"[API] /api/cases: {len(cases)} cases returned.")

    # 9. Test i18n API
    for lang in ["en", "mr", "hi"]:
        r = client.get(f"/api/i18n/{lang}")
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 20
    print("[API] /api/i18n/ catalogs for Marathi, Hindi, and English verified.")

    # 10. Test Real /predict endpoint with a valid JPEG image
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"file": ("test_leaf.jpg", buf, "image/jpeg")}
    data = {
        "crop_code": "corn",
        "growth_stage": "vegetative",
        "district": "Nashik",
        "taluka": "Niphad",
        "farmer_name": "Ramesh Kumar Patil",
        "farmer_phone": "9876543210"
    }
    r = client.post("/predict", files=files, data=data)
    assert r.status_code == 200
    pred = r.json()
    risk_info = pred.get("risk") or {}
    print(f"[API] /predict: Status={pred['status']}, Condition={pred['condition_name']}, Confidence={pred['confidence']}, Risk={risk_info.get('risk_level')}")
    assert "status" in pred
    assert "risk" in pred
    assert "advisory" in pred

    print("==================================================================")
    print("ALL INTEGRATION CHECKS COMPLETED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    test_phase2_full_integration()
