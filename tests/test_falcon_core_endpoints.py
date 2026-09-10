"""
Automated Test Suite for FALCON-AI Core SIH Endpoints
Tests:
- Deterministic Pesticide Safety Verification (/api/pesticide-check)
- Doubt Doctor Clarification Engine (/api/doubt-doctor/evaluate, /api/doubt-doctor/answer)
- Guided Field Inspection Tasks (/api/inspection/tasks)
- Geospatial Proximity & Spread Alerts (/api/alerts/spread)
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_pesticide_safety_approved():
    print("--- Testing Pesticide Safety: Approved Chemical ---")
    resp = client.post(
        "/api/pesticide-check",
        json={
            "crop": "cotton",
            "condition_code": "cotton_pink_bollworm",
            "product_query": "Coragen"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["safety_status"] == "COMPATIBLE"
    assert "Chlorantraniliprole" in data["matched_active_ingredient"]
    assert data["waiting_period_days"] == 21
    print("  OK: Coragen correctly identified as COMPATIBLE with 21 day waiting period.")


def test_pesticide_safety_banned_substance():
    print("--- Testing Pesticide Safety: Banned Substance Veto ---")
    resp = client.post(
        "/api/pesticide-check",
        json={
            "crop": "cotton",
            "condition_code": "cotton_pink_bollworm",
            "product_query": "Monocrotophos 36% SL"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["safety_status"] == "INCOMPATIBLE"
    assert "PROHIBITED" in data["verdict"]
    print("  OK: Monocrotophos strictly vetoed as PROHIBITED.")


def test_pesticide_safety_abiotic_lalya_veto():
    print("--- Testing Pesticide Safety: Abiotic Lalya Veto ---")
    resp = client.post(
        "/api/pesticide-check",
        json={
            "crop": "cotton",
            "condition_code": "cotton_leaf_reddening_lalya",
            "product_query": "Chlorpyrifos"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["safety_status"] == "INCOMPATIBLE"
    assert "CHEMICAL PESTICIDE VETOED" in data["verdict"]
    assert "Magnesium Sulphate" in data["reason"]
    print("  OK: Chemical spray on Lalya vetoed, directed to MgSO4 + DAP foliar spray.")


def test_pesticide_safety_beneficial_predator_veto():
    print("--- Testing Pesticide Safety: Beneficial Predator Veto ---")
    resp = client.post(
        "/api/pesticide-check",
        json={
            "crop": "cotton",
            "condition_code": "beneficial_lady_beetle",
            "product_query": "Cypermethrin"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["safety_status"] == "INCOMPATIBLE"
    assert "PREDATOR CONSERVATION VETO" in data["verdict"]
    print("  OK: Insecticide on Lady Beetle vetoed under predator conservation policy.")


def test_pesticide_safety_unverified_product():
    print("--- Testing Pesticide Safety: Unverified Product Escalation ---")
    resp = client.post(
        "/api/pesticide-check",
        json={
            "crop": "cotton",
            "condition_code": "cotton_pink_bollworm",
            "product_query": "SuperMagicPlantTonic9000"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["safety_status"] == "EXPERT_REQUIRED"
    assert data["requires_expert"] is True
    print("  OK: Unverified tonic routed to EXPERT_REQUIRED.")


def test_doubt_doctor_trigger_borderline():
    print("--- Testing Doubt Doctor: Borderline Confidence Trigger ---")
    resp = client.post(
        "/api/doubt-doctor/evaluate",
        json={
            "crop": "cotton",
            "top_prediction": {
                "condition_code": "cotton_pink_bollworm",
                "confidence": 0.58
            },
            "language": "mr"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["trigger"] is True
    assert "doubt_doctor" in data
    assert "गुलाबासारख्या" in data["doubt_doctor"]["question_text"]
    print("  OK: Doubt Doctor triggered for borderline 58% confidence with Marathi prompt.")


def test_doubt_doctor_trigger_high_confidence():
    print("--- Testing Doubt Doctor: High Confidence Bypass ---")
    resp = client.post(
        "/api/doubt-doctor/evaluate",
        json={
            "crop": "cotton",
            "top_prediction": {
                "condition_code": "cotton_pink_bollworm",
                "confidence": 0.92
            }
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["trigger"] is False
    assert data["doubt_doctor"] is None
    print("  OK: High confidence 92% bypasses Doubt Doctor.")


def test_doubt_doctor_answer_flow():
    print("--- Testing Doubt Doctor: Observation Response Corroboration ---")
    resp_yes = client.post(
        "/api/doubt-doctor/answer",
        json={
            "target_condition": "cotton_pink_bollworm",
            "original_confidence": 58.0,
            "answer": "YES",
            "confirms_if_yes": "cotton_pink_bollworm",
            "weight_boost": 15.0
        }
    )
    assert resp_yes.status_code == 200
    data_yes = resp_yes.json()
    assert data_yes["status"] == "CORROBORATED"
    assert data_yes["adjusted_confidence"] == 73.0
    assert data_yes["requires_expert"] is False

    resp_no = client.post(
        "/api/doubt-doctor/answer",
        json={
            "target_condition": "cotton_pink_bollworm",
            "original_confidence": 58.0,
            "answer": "NO"
        }
    )
    assert resp_no.status_code == 200
    data_no = resp_no.json()
    assert data_no["status"] == "SYMPTOM_CONTRADICTION"
    assert data_no["requires_expert"] is True
    print("  OK: YES corroborates confidence to 73%; NO flags contradiction and escalates.")


def test_inspection_tasks_wilt():
    print("--- Testing Inspection Tasks: Wilt Protocol ---")
    resp = client.get("/api/inspection/tasks?symptom_context=wilt&language=mr")
    assert resp.status_code == 200
    data = resp.json()["inspection_task"]
    assert data["task_type"] == "ROOT_AND_VASCULAR_INSPECTION"
    assert len(data["steps"]) >= 3
    assert data["status"] == "PENDING_FARMER_OBSERVATION"
    print("  OK: Wilt generated root & vascular inspection task.")


def test_inspection_tasks_stem_borer():
    print("--- Testing Inspection Tasks: Stem Borer Protocol ---")
    resp = client.get("/api/inspection/tasks?symptom_context=stem_borer&language=en")
    assert resp.status_code == 200
    data = resp.json()["inspection_task"]
    assert data["task_type"] == "WHORL_AND_STEM_INSPECTION"
    assert any("deadheart" in s.lower() or "whorl" in s.lower() for s in data["steps"])
    print("  OK: Stem borer generated whorl & deadheart inspection task.")


def test_spread_alerts_calculation():
    print("--- Testing Spread Alerts: Haversine Proximity Calculation ---")
    resp = client.get("/api/alerts/spread?case_id=1&radius_km=100.0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["case_id"] == 1
    assert "alerts" in data
    print(f"  OK: Spread alerts returned {data['alerts_generated']} alert notifications.")


if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING FALCON-AI CORE SIH FUNCTIONAL MODULES TEST SUITE")
    print("==================================================================")
    test_pesticide_safety_approved()
    test_pesticide_safety_banned_substance()
    test_pesticide_safety_abiotic_lalya_veto()
    test_pesticide_safety_beneficial_predator_veto()
    test_pesticide_safety_unverified_product()
    test_doubt_doctor_trigger_borderline()
    test_doubt_doctor_trigger_high_confidence()
    test_doubt_doctor_answer_flow()
    test_inspection_tasks_wilt()
    test_inspection_tasks_stem_borer()
    test_spread_alerts_calculation()
    print("==================================================================")
    print("ALL 11 FALCON-AI CORE SIH UNIT TESTS PASSED 100%!")
    print("==================================================================")
