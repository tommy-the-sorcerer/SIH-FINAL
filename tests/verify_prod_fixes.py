import urllib.request
import json
import cv2
import numpy as np

def run_tests():
    print("--- 1. Testing Root HTML & DOM IDs ---")
    html = urllib.request.urlopen("http://127.0.0.1:8000/").read().decode("utf-8")
    assert 'id="globalSearchInput"' in html, "globalSearchInput missing in HTML"
    assert 'id="quick-action-modal"' in html, "quick-action-modal missing in HTML"
    assert 'id="nav-item-alerts"' in html, "nav-item-alerts missing in HTML"
    assert 'rbac-officer-expert' in html, "rbac-officer-expert class missing in HTML"
    assert 'id="auth-role-group"' in html, "auth-role-group missing in HTML"
    assert 'id="header-btn-signout"' in html, "header-btn-signout missing in HTML"
    assert 'id="persona-gateway-card"' in html, "persona-gateway-card missing in HTML"
    print("[PASS] Root HTML DOM elements verified!")

    print("\n--- 2. Testing Taxonomy Config API ---")
    tax_res = urllib.request.urlopen("http://127.0.0.1:8000/api/config/taxonomy").read().decode("utf-8")
    tax = json.loads(tax_res)
    assert "cotton" in tax["crops"]
    assert "maize" in tax["crops"]
    assert "soybean" in tax["crops"]
    print("[PASS] Taxonomy configuration verified!")

    print("\n--- 3. Testing Escalation API ---")
    escalate_payload = {
        "case_id": "TEST-ESC-999",
        "timestamp": "10:00 AM, Today",
        "crop": "MAIZE",
        "disease": "Fall Armyworm",
        "severity": "HIGH",
        "image_url": "/static/images/image.jpeg",
        "location": "Nashik, Maharashtra",
        "farmer_name": "Test Farmer",
        "latitude": 20.0,
        "longitude": 73.8,
        "damage_percent": 50.0
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/escalate",
        data=json.dumps(escalate_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    esc_res = urllib.request.urlopen(req).read().decode("utf-8")
    esc_data = json.loads(esc_res)
    assert esc_data["status"] == "success"
    print("[PASS] Escalation API verified!")

    print("\n--- 4. Testing Weather Telemetry API ---")
    weather_res = urllib.request.urlopen("http://127.0.0.1:8000/api/weather/current?lat=20.0&lon=73.8").read().decode("utf-8")
    wdata = json.loads(weather_res)
    assert "temperature" in wdata
    print(f"[PASS] Weather telemetry verified! (Temperature: {wdata.get('temperature')} C)")

    print("\n--- 5. Testing Diagnosis API with OOD Specimen Guardrail ---")
    # Synthetic flat white image (non-plant object)
    flat_img = np.full((300, 300, 3), 255, dtype=np.uint8)
    _, encoded = cv2.imencode(".jpg", flat_img)
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="specimen.jpg"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + encoded.tobytes() + (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="crop_code"\r\n\r\nmaize\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="growth_stage"\r\n\r\nvegetative\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="district"\r\n\r\nNashik\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="language"\r\n\r\nen\r\n'
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    diag_req = urllib.request.Request(
        "http://127.0.0.1:8000/predict",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    diag_res = urllib.request.urlopen(diag_req).read().decode("utf-8")
    diag_data = json.loads(diag_res)
    print("Diagnosis response for flat non-plant object:", diag_data.get("status"), "| Message:", diag_data.get("message"))
    assert diag_data.get("valid") is False or diag_data.get("status") in ["image_quality_issue", "invalid_specimen"]
    print("[PASS] Non-plant / OOD rejection verified!")

    print("\n==================================================")
    print("ALL VERIFICATION CHECKS PASSED WITH 100% INTEGRITY!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
