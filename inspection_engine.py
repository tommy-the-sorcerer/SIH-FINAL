"""
Inspection Task Engine for FALCON-AI / SIH26131

ABSOLUTE PROJECT RULE:
- For diseases/pests not reliably diagnosable from a photo (e.g. Wilt, Root Rot, Stem Borer):
  NEVER force a foliar diagnosis.
- Generate structured field inspection tasks.
"""

from typing import Dict, Any, List

INSPECTION_TASKS_DATABASE = {
    "cotton_wilt_or_root_rot": {
        "task_type": "ROOT_AND_VASCULAR_INSPECTION",
        "title_en": "Cotton Root & Vascular Browning Inspection",
        "title_mr": "कापूस मुळांची व खोडाची अंतर्गत तपासणी",
        "title_hi": "कपास की जड़ और तने की आंतरिक जांच",
        "steps_en": [
            "Carefully uproot one wilting plant from moist soil.",
            "Inspect the tap root for blackened decay or nematode galls.",
            "Split the lower stem vertically with a clean blade.",
            "Check if inner vascular tissues show dark brown discoloration (indicates Fusarium/Verticillium wilt)."
        ],
        "steps_mr": [
            "वाळत असलेल्या एका रोपाला मुळासह हलक्या हाताने उपटा.",
            "मुख्य मुळावर काळे कुजणे किंवा गाठी आहेत का ते तपासा.",
            "खालचे खोड स्वच्छ पात्याने उभे चिरा.",
            "खोडाच्या आतील नळ्यांचा भाग तपकिरी/काळा पडला आहे का ते पहा (फ्युझारियम मर रोगाचे लक्षण)."
        ],
        "steps_hi": [
            "मुरझा रहे एक पौधे को जड़ सहित सावधानीपूर्वक उखाड़ें।",
            "मुख्य जड़ पर काला सड़न या गांठें देखें।",
            "निचले तने को साफ चाकू से सीधा चीरें।",
            "जांचें कि तने के अंदर भूरा रंग तो नहीं आ गया (उकठा/मुरझान रोग का लक्षण)।"
        ],
        "follow_up_action": "Upload photo of split stem for laboratory confirmation."
    },
    "subsurface_stem_borer": {
        "task_type": "WHORL_AND_STEM_INSPECTION",
        "title_en": "Stem Borer / Whorl Deadheart Inspection",
        "title_mr": "खोडकिडा व पोंगा मर तपासणी",
        "title_hi": "तना छेदक एवं मृत गोभ (डेडहार्ट) निरीक्षण",
        "steps_en": [
            "Gently pull the central drying shoot / leaf whorl.",
            "If it pulls out easily and smells rotten, look for borer entry holes at the base.",
            "Check for granular sawdust-like frass near leaf axils."
        ],
        "steps_mr": [
            "वाळलेला मधला पोंगा हळूच वर ओढा.",
            "जर पोंगा सहज बाहेर आला आणि कुजका वास आला, तर खोडाच्या तळाशी छिद्र तपासा.",
            "पानांच्या बेचक्यात लाकडाच्या भुशासारखी विष्ठा (frass) आहे का ते पहा."
        ],
        "steps_hi": [
            "सूख रहे बीच के गोभ को धीरे से खींचे।",
            "यदि यह आसानी से निकल जाए और सड़ांध आए, तो तने के निचले हिस्से पर छेद देखें।",
            "पत्तियों के जोड़ों के पास बुरादे जैसा मल देखें।"
        ],
        "follow_up_action": "Install pheromone traps or apply bio-pesticide granules."
    }
}


def generate_inspection_task(symptom_context: str, language: str = "mr") -> Dict[str, Any]:
    """Generates structured guided inspection tasks for subsurface/ambiguous pathologies."""
    clean_ctx = symptom_context.lower()
    
    key = "cotton_wilt_or_root_rot" if any(w in clean_ctx for w in ["wilt", "root", "decay", "droop"]) else "subsurface_stem_borer"
    task_spec = INSPECTION_TASKS_DATABASE[key]
    
    title_key = f"title_{language}" if f"title_{language}" in task_spec else "title_mr"
    steps_key = f"steps_{language}" if f"steps_{language}" in task_spec else "steps_mr"
    
    return {
        "task_type": task_spec["task_type"],
        "title": task_spec.get(title_key, task_spec["title_en"]),
        "steps": task_spec.get(steps_key, task_spec["steps_en"]),
        "follow_up_action": task_spec["follow_up_action"],
        "status": "PENDING_FARMER_OBSERVATION"
    }
