"""
Doubt Doctor Interactive Clarification Engine for FALCON-AI / SIH26131

ABSOLUTE PROJECT RULES:
- Never force a low-confidence prediction into a known disease.
- When top-2 predictions are close (gap <= 0.15) or confidence is borderline (0.50 <= conf < 0.65):
  Ask ONE simple, farmer-observable question.
- Responses: YES, NO, DONT_KNOW.
- Use the answer only as corroborating evidence.
- If uncertainty remains: ESCALATE TO EXPERT.
"""

from typing import Dict, Any, Optional

DOUBT_QUESTIONS_REGISTRY = {
    ("cotton", "cotton_pink_bollworm"): {
        "question_en": "Are flower petals twisted together in a rosette shape or are small exit holes visible on young bolls?",
        "question_mr": "फुलांच्या पाकळ्या गुलाबासारख्या एकमेकांत अडकल्या आहेत का किंवा लहान बोंडांवर छिद्रे दिसत आहेत का?",
        "question_hi": "क्या फूल की पंखुड़ियाँ गुलाब की तरह मुड़ी हुई हैं या छोटे गूलरों पर छेद दिखाई दे रहे हैं?",
        "confirms_if_yes": "cotton_pink_bollworm",
        "weight_boost": 0.15
    },
    ("cotton", "cotton_grey_mildew"): {
        "question_en": "Are white or greyish powdery angular patches visible on the lower leaf surface?",
        "question_mr": "पानांच्या मागच्या बाजूवर पांढुरके-राखाडी रंगाचे पावडरसारखे कोनीय ठिपके दिसत आहेत का?",
        "question_hi": "क्या पत्तियों की निचली सतह पर सफेद या भूरे रंग के पाउडर जैसे कोणीय धब्बे दिखाई दे रहे हैं?",
        "confirms_if_yes": "cotton_grey_mildew",
        "weight_boost": 0.18
    },
    ("cotton", "cotton_bacterial_blight"): {
        "question_en": "Are angular water-soaked dark spots visible, or are black lesions running down the leaf veins and stem?",
        "question_mr": "पानांवर तेलकट काळे कोनीय ठिपके आहेत का किंवा शिरांमधून काळे डाग पसरत आहेत का?",
        "question_hi": "क्या पत्तियों पर कोणीय गहरे पानी जैसे धब्बे हैं या नसों से काले निशान फैल रहे हैं?",
        "confirms_if_yes": "cotton_bacterial_blight",
        "weight_boost": 0.18
    },
    ("soybean", "soybean_rust"): {
        "question_en": "When touching the underside of the leaf, do tiny raised volcano-like brown bumps release brown dust on your fingers?",
        "question_mr": "पानाच्या खालच्या भागाला स्पर्श केल्यास लहान पुटकुळ्यांतून बोटांना तांबूस-तपकिरी धूळ लागते का?",
        "question_hi": "क्या पत्ती के नीचे छूने पर छोटे उभरे हुए दानों से उंगलियों पर भूरी धूल लगती है?",
        "confirms_if_yes": "soybean_rust",
        "weight_boost": 0.20
    },
    ("soybean", "soybean_sudden_death_syndrome"): {
        "question_en": "Are yellow/brown patches spreading between the leaf veins while the veins themselves stay green?",
        "question_mr": "पानाच्या शिरांमधील भाग पिवळा/तपकिरी झाला असून मुख्य शिरा हिरव्याच राहिल्या आहेत का?",
        "question_hi": "क्या नसों के बीच का हिस्सा पीला/भूरा हो गया है जबकि नसें हरी ही हैं?",
        "confirms_if_yes": "soybean_sudden_death_syndrome",
        "weight_boost": 0.20
    },
    ("pigeonpea", "tur_sterility_mosaic"): {
        "question_en": "Is the entire plant bushy with small pale green/yellow leaves and having zero or very few flowers/pods?",
        "question_mr": "झाड झुडपासारखे दाट आणि फिकट पिवळे झाले असून त्याला फुले किंवा शेंगा लागणे थांबले आहे का?",
        "question_hi": "क्या पौधा झाड़ीदार और हल्का पीला हो गया है और उस पर फूल या फलियाँ नहीं आ रही हैं?",
        "confirms_if_yes": "tur_sterility_mosaic",
        "weight_boost": 0.20
    },
    ("onion", "onion_purple_blotch"): {
        "question_en": "Are the leaf spots sunken with a distinct purple or dark reddish-brown center surrounded by yellow bands?",
        "question_mr": "पानांवरील ठिपके खोलगट असून त्यांच्या मध्यभागी जांभळा किंवा गडद तांबूस रंग आणि भोवती पिवळे वलय आहे का?",
        "question_hi": "क्या पत्तियों के धब्बे धंसे हुए हैं और उनका केंद्र बैंगनी या गहरा लाल-भूरा है?",
        "confirms_if_yes": "onion_purple_blotch",
        "weight_boost": 0.18
    },
    ("citrus", "citrus_greening_disease"): {
        "question_en": "Are the leaf veins distinctly yellow with blotchy asymmetrical mottle across the leaf blade?",
        "question_mr": "पानाच्या शिरा ठळकपणे पिवळ्या पडून इतर भागावर असमान पिवळसर ठिपके दिसत आहेत का?",
        "question_hi": "क्या पत्ती की नसें स्पष्ट रूप से पीली हैं और पत्ती पर असमान पीलापन दिखाई दे रहा है?",
        "confirms_if_yes": "citrus_greening_disease",
        "weight_boost": 0.20
    },
    ("citrus", "citrus_canker"): {
        "question_en": "Are there raised, rough corky brown spots on leaves or fruit with a yellow halo around them?",
        "question_mr": "पानांवर किंवा फळांवर खरुजासारखे खडबडीत तपकिरी ठिपके असून त्यांच्याभोवती पिवळे वलय दिसत आहे का?",
        "question_hi": "क्या पत्तियों या फलों पर उभरे हुए खुरदरे भूरे धब्बे हैं जिनके चारों ओर पीला छल्ला है?",
        "confirms_if_yes": "citrus_canker",
        "weight_boost": 0.20
    },
    ("gram", "fusarium_wilt"): {
        "question_en": "Is the plant wilting from lower branches upward, with dark brown internal vascular streaking when the stem is split?",
        "question_mr": "झाड खालच्या फांद्यांपासून सुकून कोमेजत आहे का आणि खोड कापल्यास आत काळी-तपकिरी रेषा दिसत आहे का?",
        "question_hi": "क्या पौधा निचली शाखाओं से मुरझा रहा है और तना चीरने पर अंदर भूरी लकीर दिखती है?",
        "confirms_if_yes": "fusarium_wilt",
        "weight_boost": 0.20
    },
    ("wheat", "brown_rust"): {
        "question_en": "Are small orange-brown powdery pustules scattered randomly on the upper leaf surface that rub off onto fingers?",
        "question_mr": "पानांच्या वरच्या बाजूवर नारंगी-तपकिरी रंगाच्या पावडरसारख्या पुटकुळ्या दिसत असून त्या बोटाला लागतात का?",
        "question_hi": "क्या पत्तियों पर नारंगी-भूरे रंग के पाउडर जैसे दाने हैं जो छूने पर उंगलियों पर लगते हैं?",
        "confirms_if_yes": "brown_rust",
        "weight_boost": 0.20
    }
}


def evaluate_doubt_doctor_trigger(
    crop: str,
    top_prediction: Dict[str, Any],
    runner_up_prediction: Optional[Dict[str, Any]] = None,
    language: str = "mr"
) -> Optional[Dict[str, Any]]:
    """
    Evaluates whether Doubt Doctor should engage to clarify ambiguity.
    Triggers when:
    1. Confidence is between 0.50 and 0.65, OR
    2. Top two predictions have a narrow confidence delta (<= 0.15).
    """
    conf = top_prediction.get("confidence", 0.0)
    top_code = top_prediction.get("condition_code", "")
    
    should_trigger = False
    if 0.50 <= conf < 0.65:
        should_trigger = True
    elif runner_up_prediction:
        runner_conf = runner_up_prediction.get("confidence", 0.0)
        if (conf - runner_conf) <= 0.15 and conf < 0.75:
            should_trigger = True

    if not should_trigger:
        return None

    lookup_key = (crop.lower(), top_code.lower())
    q_entry = DOUBT_QUESTIONS_REGISTRY.get(lookup_key)
    
    if not q_entry:
        # Generic fallback question
        return {
            "trigger_reason": "BORDERLINE_CONFIDENCE",
            "question_code": f"Q_GENERIC_{crop}_{top_code}",
            "question_text": {
                "en": "Are similar symptoms appearing across multiple plants in the same row?",
                "mr": "एकाच ओळीतील इतर झाडांवरही अशीच लक्षणे दिसत आहेत का?",
                "hi": "क्या एक ही पंक्ति के अन्य पौधों पर भी ऐसे ही लक्षण दिख रहे हैं?"
            }.get(language, "Are similar symptoms appearing across multiple plants?"),
            "options": ["YES", "NO", "DONT_KNOW"],
            "target_condition": top_code
        }

    lang_key = f"question_{language}" if f"question_{language}" in q_entry else "question_mr"
    return {
        "trigger_reason": "DIAGNOSTIC_AMBIGUITY_GATE",
        "question_code": f"Q_{crop}_{top_code}",
        "question_text": q_entry.get(lang_key, q_entry["question_en"]),
        "options": ["YES", "NO", "DONT_KNOW"],
        "target_condition": top_code,
        "confirms_if_yes": q_entry["confirms_if_yes"],
        "weight_boost": q_entry["weight_boost"]
    }
