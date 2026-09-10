"""
Centralized Multilingual Localization Service for SIH26131
Supports Marathi (mr), Hindi (hi), and English (en).
Maharashtra-first terminology with stable internal code translation.
"""

from typing import Dict, Any, Optional

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # Navigation & Brand
        "app_title": "FALCON-AI | Crop Health Decision Support Platform",
        "service_subtitle": "Maharashtra State Innovation Society · SIH26131",
        "nav_farmer_portal": "Farmer Portal",
        "nav_expert_desk": "Expert Review Desk",
        "nav_officer_dashboard": "Agriculture Officer Dashboard",
        "nav_login": "Login / Register",
        "nav_logout": "Logout",
        "language_select": "Language",

        # Hero & Upload
        "hero_eyebrow": "EARLY DETECTION & INTEGRATED CROP HEALTH MANAGEMENT",
        "hero_title": "Protect your crops with AI diagnosis and expert guidance",
        "hero_desc": "Upload a field photograph of your affected crop. Get instant AI detection, micro-climate risk assessment, and verified agricultural officer advisories.",
        "start_assessment": "Start Crop Health Diagnosis",
        "upload_subtext": "Capture a photo with your mobile camera or choose a leaf picture from device.",
        "btn_open_camera": "Open Camera",
        "btn_upload_pc": "Upload Image",
        "drop_zone_text": "Drop crop photo here or browse files",
        "drop_zone_sub": "JPG, JPEG, PNG, or WEBP (up to 15 MB)",
        "step1_select_crop": "1. Select Crop",
        "step2_select_location": "2. Farm & Location",
        "step3_select_stage": "3. Crop Growth Stage",
        "step4_upload_image": "4. Upload Leaf Photo",
        "btn_run_diagnosis": "Run AI Diagnosis & Risk Assessment",
        "btn_analyzing": "Analyzing Image & Weather...",

        # Quality & Errors
        "quality_issue_title": "Image Quality Issue",
        "quality_issue_msg": "The image quality is not sufficient for reliable analysis. Please upload a clearer image showing the affected part of the crop.",
        "invalid_file": "Invalid or corrupt file. Please select a valid image.",

        # Statuses
        "status_identified": "Identified",
        "status_healthy": "Healthy Foliage",
        "status_uncertain": "Uncertain (Expert Review Required)",
        "status_unknown": "Unknown / Unclassified Condition",
        "status_image_quality_issue": "Image Quality Issue",
        "status_pending_expert": "Awaiting Agricultural Expert Review",
        "status_verified": "Expert Verified Diagnosis",
        "status_lab_referral": "Referred for Laboratory Confirmation",
        "status_follow_up": "Follow-up Required",
        "status_closed": "Case Resolved & Closed",

        # Taxonomy & Roles
        "type_disease": "Crop Disease (Pathogen)",
        "type_pest": "Insect Pest Infestation",
        "type_healthy": "Healthy Crop",
        "type_unknown": "Unclassified Symptom",

        # Severity & Risk
        "severity_none": "None",
        "severity_low": "Low",
        "severity_moderate": "Moderate",
        "severity_high": "High",
        "severity_critical": "Critical",
        "severity_not_assessed": "Not Assessed",
        "risk_low": "Low Risk",
        "risk_moderate": "Moderate Risk",
        "risk_high": "High Risk",
        "risk_critical": "Critical Epidemic Risk",
        "risk_factors_title": "Contributing Risk Factors",
        "confidence_label": "AI Confidence",
        "severity_label": "Foliage Severity",
        "damage_area_label": "Estimated Visible Damage",
        "leaf_area_label": "Leaf Coverage",
        "weather_context_title": "Local Micro-Climate Context",
        "weather_temp": "Temperature",
        "weather_humidity": "Relative Humidity",
        "weather_rain": "Precipitation",
        "weather_source": "Source",
        "weather_unavailable": "Live weather telemetry unavailable for this coordinate",

        # Advisory Sections
        "advisory_title": "Integrated Pest Management (IPM) Advisory",
        "immediate_action_title": "Immediate Action",
        "monitoring_title": "Field Monitoring",
        "cultural_title": "Cultural & Preventive Measures",
        "biological_title": "Biological Control",
        "chemical_title": "Safe Chemical Guidance",
        "safety_title": "Farmer Safety & Legal Precautions",
        "referral_alert_title": "When to Contact Officer / KVK",
        "follow_up_alert": "Recommended follow-up observation in {days} days",

        # Follow up & Confirmation
        "followup_title": "Follow-up Observation & Field Outcome",
        "outcome_improved": "Condition Improved",
        "outcome_unchanged": "Condition Unchanged",
        "outcome_worsened": "Condition Worsened",
        "outcome_resolved": "Condition Completely Resolved",
        "btn_submit_followup": "Upload Follow-up Image",
        "btn_confirm_outcome": "Confirm Field Outcome",

        # Expert Desk
        "expert_desk_title": "Agricultural Expert & Doctor Review Portal",
        "pending_cases_count": "Cases Pending Review",
        "btn_confirm_ai": "Confirm AI Diagnosis",
        "btn_correct_ai": "Correct Diagnosis",
        "btn_refer_lab": "Refer to Laboratory",
        "btn_request_image": "Request Clearer Photo",
        "expert_notes_placeholder": "Add agronomic notes, chemical prescription, or cultural guidance...",

        # Officer Dashboard & GIS
        "dashboard_title": "Maharashtra Agriculture Officer GIS Intelligence",
        "total_observations": "Total Field Cases",
        "disease_cases": "Disease Outbreaks",
        "pest_cases": "Pest Infestations",
        "high_risk_alerts": "High Risk Alerts",
        "hotspot_map_title": "Geospatial Outbreak Hotspots (Maharashtra)",
        "district_distribution_title": "Top District Outbreaks",

        # Footer
        "footer_text": "FALCON-AI · SIH 2026 Problem Statement SIH26131 · Dept. of Skills, Employment, Entrepreneurship & Innovation, Government of Maharashtra",

        # Reference Navigation & Dashboard
        "sidebar_subtitle": "AI for Healthy Crops · Prosperous Maharashtra",
        "nav_dashboard": "Dashboard",
        "nav_diagnose": "Diagnose Crop",
        "nav_fields": "My Fields",
        "nav_alerts": "Pest Alerts",
        "nav_weather": "Weather & Risk",
        "nav_hotspots": "Hotspot Map",
        "nav_advisory": "Treatment Advisory",
        "nav_reports": "Reports & Insights",
        "nav_expert_connect": "Expert Connect",
        "nav_knowledge": "Knowledge Hub",
        "nav_sensors": "Smart Traps & Sensors",
        "search_placeholder": "Search crops, diseases, advisories...",
        "hero_headline": "Healthy Crops, Brighter Tomorrows",
        "hero_supporting": "AI • Farmers • Sustainable Agriculture",
        "hero_quote": "Nirogi Sheti, Samruddh Maharashtra",
        "kpi_fields": "My Fields",
        "kpi_main_crop": "Main Crop",
        "kpi_crop_health": "Crop Health",
        "kpi_current_weather": "Current Weather",
        "recent_diagnosis_title": "Recent Diagnosis",
        "risk_forecast_title": "7-Day Disease Risk Forecast",
        "upcoming_alerts_title": "Upcoming Alerts",
        "btn_get_advisory": "Get Treatment Advisory",
        "btn_save_result": "Save Result",
        "btn_track_case": "Track Case",
        "btn_upload_another": "Upload Another Image",
        "unknown_state_title": "Unable to confidently identify this crop condition.",
        "unknown_state_desc": "Your case has been submitted to an agricultural expert for review.",
        "sensor_dashboard_title": "Smart Traps & Field Sensors",
        "sensor_dashboard_subtitle": "Live data from devices deployed in your fields.",
        "sensor_status_ready": "Sensor integration ready",
        "sensor_awaiting_data": "Awaiting sensor data",
        "pest_activity_trend": "Pest Activity Trend (Catch / Trap / Day)",
        "hotspot_title": "Pest Infestation Hotspot Map",
        "hotspot_subtitle": "Real-time view of pest and disease incidence across Maharashtra.",
        "advisory_view_title": "Treatment Advisory",
        "advisory_view_subtitle": "Personalized and location-specific recommendations for better crop health.",
        "quick_actions": "Quick Actions",
        "action_download_pdf": "Download PDF",
        "action_share": "Share",
        "action_consult_expert": "Consult Expert",
        "opt_immediate": "1. Immediate Action",
        "opt_organic": "2. Organic / IPM Option",
        "opt_chemical": "3. Chemical Option",
        "opt_additional": "4. Additional Information & Monitoring",
        "safe_use_notice": "Strictly comply with Maharashtra Agriculture Dept & CIBRC recommendations. Use PPE.",
        "waiting_period_label": "Waiting Period (Pre-Harvest Interval)",
        "follow_up_date_label": "Recommended Follow-up Inspection",
        "need_help_title": "Need Expert Agronomic Guidance?",
        "need_help_desc": "Connect with Taluka Agriculture Officer or KVK SMS advisory helpline."
    },

    "mr": {
        # Navigation & Brand
        "app_title": "फाल्कन-एआय | पीक आरोग्य निर्णय सहाय्य प्रणाली",
        "service_subtitle": "महाराष्ट्र राज्य नाविन्यता सोसायटी · SIH26131",
        "nav_farmer_portal": "शेतकरी सेवा",
        "nav_expert_desk": "कृषी तज्ज्ञ पुनरावलोकन",
        "nav_officer_dashboard": "कृषी अधिकारी डॅशबोर्ड",
        "nav_login": "प्रवेश / नोंदणी",
        "nav_logout": "बाहेर पडा",
        "language_select": "भाषा",

        # Hero & Upload
        "hero_eyebrow": "लवकर निदान व एकात्मिक पीक कीड-रोग व्यवस्थापन",
        "hero_title": "एआय तंत्रज्ञान आणि कृषी तज्ज्ञांच्या सल्ल्याने पिकांचे रक्षण करा",
        "hero_desc": "बाधित पिकाचे छायाचित्र अपलोड करा. झटपट एआय निदान, हवामान-आधारित धोका मूल्यांकन आणि अधिकृत कृषी सल्ला मिळवा.",
        "start_assessment": "पीक आरोग्य तपासणी सुरू करा",
        "upload_subtext": "मोबाईल कॅमेऱ्याने स्पष्ट फोटो काढा किंवा गॅलरीतून निवडा.",
        "btn_open_camera": "कॅमेरा उघडा",
        "btn_upload_pc": "फोटो निवडा",
        "drop_zone_text": "पिकाचा फोटो येथे टाका किंवा फाईल निवडा",
        "drop_zone_sub": "JPG, JPEG, PNG किंवा WEBP (कमाल १५ MB)",
        "step1_select_crop": "१. पीक निवडा",
        "step2_select_location": "२. शेत व ठिकाण",
        "step3_select_stage": "३. पिकाची वाढ अवस्था",
        "step4_upload_image": "४. पानाचा फोटो अपलोड करा",
        "btn_run_diagnosis": "एआय रोग निदान व धोका तपासा",
        "btn_analyzing": "फोटो व स्थानिक हवामान तपासत आहे...",

        # Quality & Errors
        "quality_issue_title": "फोटोची गुणवत्ता अपुरी आहे",
        "quality_issue_msg": "विश्वसनीय विश्लेषणासाठी फोटोची गुणवत्ता पुरेशी नाही. कृपया पिकाचा बाधित भाग स्पष्ट दिसेल असा दुसरा फोटो अपलोड करा.",
        "invalid_file": "अवैध फाईल प्रकार. कृपया वैध फोटो निवडा.",

        # Statuses
        "status_identified": "रोग/कीड निश्चित ओळखली",
        "status_healthy": "निरोगी पीक",
        "status_uncertain": "संशयित / अनिश्चित (तज्ज्ञ पुनरावलोकन आवश्यक)",
        "status_unknown": "अपरिचित / अनाकलनीय लक्षणे (तज्ज्ञांकडे वर्ग)",
        "status_image_quality_issue": "फोटो अस्पष्ट / अपुरी गुणवत्ता",
        "status_pending_expert": "कृषी तज्ज्ञांच्या तपासणीसाठी प्रलंबित",
        "status_verified": "कृषी तज्ज्ञांनी प्रमाणित केलेले निदान",
        "status_lab_referral": "प्रयोगशाळा तपासणीसाठी शिफारस",
        "status_follow_up": "पाठपुरावा निरीक्षण आवश्यक",
        "status_closed": "प्रकरण पूर्ण व बंद",

        # Taxonomy & Roles
        "type_disease": "पीक रोग (बुरशी / जिवाणू / विषाणू)",
        "type_pest": "कीटकांचा प्रादुर्भाव (कीड)",
        "type_healthy": "निरोगी पीक",
        "type_unknown": "अनाकलनीय लक्षण",

        # Severity & Risk
        "severity_none": "नाही",
        "severity_low": "कमी (सौम्य)",
        "severity_moderate": "मध्यम",
        "severity_high": "जास्त (तीव्र)",
        "severity_critical": "अतिगंभीर",
        "severity_not_assessed": "तपासले नाही",
        "risk_low": "कमी धोका",
        "risk_moderate": "मध्यम धोका",
        "risk_high": "उच्च धोका",
        "risk_critical": "अतिगंभीर प्रादुर्भाव धोका",
        "risk_factors_title": "धोका निर्माण करणारे घटक",
        "confidence_label": "एआय अचूकता (विश्वासार्हता)",
        "severity_label": "पानांवरील तीव्रता",
        "damage_area_label": "अंदाजित बाधित क्षेत्र",
        "leaf_area_label": "पानाचा आकार",
        "weather_context_title": "स्थानिक सूक्ष्म-हवामान परिस्थिती",
        "weather_temp": "तापमान",
        "weather_humidity": "हवेतील आर्द्रता",
        "weather_rain": "पाऊस",
        "weather_source": "माहिती स्रोत",
        "weather_unavailable": "या स्थानासाठी थेट हवामान उपलब्ध नाही",

        # Advisory Sections
        "advisory_title": "एकात्मिक कीड व रोग व्यवस्थापन (IPM) सल्ला",
        "immediate_action_title": "त्वरित करावयाची उपाययोजना",
        "monitoring_title": "शेत पाहणी व निरीक्षण",
        "cultural_title": "मशागती व प्रतिबंधात्मक उपाय",
        "biological_title": "जैविक नियंत्रण पद्धती",
        "chemical_title": "सुरक्षित रासायनिक उपाय (फवारणी)",
        "safety_title": "शेतकरी सुरक्षितता व कायदेशीर खबरदारी",
        "referral_alert_title": "कृषी अधिकारी / केव्हीके कडे कधी संपर्क साधावा",
        "follow_up_alert": "शिफारस: पुढील {days} दिवसांत पुन्हा पाहणी करून फोटो अपलोड करा",

        # Follow up & Confirmation
        "followup_title": "पाठपुरावा निरीक्षण व प्रत्यक्ष शेतातील परिणाम",
        "outcome_improved": "स्थिती सुधारली",
        "outcome_unchanged": "स्थिती जैसे थे आहे",
        "outcome_worsened": "स्थिती अधिक बिघडली",
        "outcome_resolved": "रोग/कीड पूर्णपणे नियंत्रणात आली",
        "btn_submit_followup": "पाठपुरावा फोटो अपलोड करा",
        "btn_confirm_outcome": "प्रत्यक्ष शेत परिणाम नोंदवा",

        # Expert Desk
        "expert_desk_title": "कृषी तज्ज्ञ व कृषी डॉक्टर पुनरावलोकन पोर्टल",
        "pending_cases_count": "तपासणीसाठी प्रलंबित प्रकरणे",
        "btn_confirm_ai": "एआय निदान मान्य करा",
        "btn_correct_ai": "निदान दुरुस्त करा",
        "btn_refer_lab": "प्रयोगशाळेकडे वर्ग करा",
        "btn_request_image": "अधिक स्पष्ट फोटो मागा",
        "expert_notes_placeholder": "कृषी सल्ला, औषध शिफारस किंवा सूचना लिहा...",

        # Officer Dashboard & GIS
        "dashboard_title": "महाराष्ट्र कृषी अधिकारी भौगोलिक बुद्धिमत्ता (GIS)",
        "total_observations": "एकूण नोंदवलेली प्रकरणे",
        "disease_cases": "रोग प्रादुर्भाव",
        "pest_cases": "कीड प्रादुर्भाव",
        "high_risk_alerts": "उच्च धोक्याचे इशारे",
        "hotspot_map_title": "भौगोलिक हॉटस्पॉट नकाशा (महाराष्ट्र राज्य)",
        "district_distribution_title": "जिल्हानिहाय प्रादुर्भाव प्रमाण",

        # Footer
        "footer_text": "फाल्कन-एआय · स्मार्ट इंडिया हॅकेथॉन २०२६ (SIH26131) · कौशल्य, रोजगार, उद्योजकता व नाविन्यता विभाग, महाराष्ट्र शासन",

        # Reference Navigation & Dashboard
        "sidebar_subtitle": "पिकांचे उत्तम आरोग्य · समृद्ध महाराष्ट्र",
        "nav_dashboard": "डॅशबोर्ड",
        "nav_diagnose": "पीक निदान",
        "nav_fields": "माझी शेती",
        "nav_alerts": "कीड-रोग अलर्ट",
        "nav_weather": "हवामान व धोका",
        "nav_hotspots": "हॉटस्पॉट नकाशा",
        "nav_advisory": "उपचार सल्ला",
        "nav_reports": "अहवाल व विश्लेषण",
        "nav_expert_connect": "कृषी तज्ज्ञ सल्ला",
        "nav_knowledge": "ज्ञान केंद्र",
        "nav_sensors": "स्मार्ट ट्रॅप व सेन्सर्स",
        "search_placeholder": "पीक, रोग, सल्ला शोधा...",
        "hero_headline": "निरोगी पिके, उज्ज्वल भविष्य",
        "hero_supporting": "एआय • शेतकरी • शाश्वत शेती",
        "hero_quote": "निरोगी शेती, समृद्ध महाराष्ट्र",
        "kpi_fields": "माझी शेती",
        "kpi_main_crop": "मुख्य पीक",
        "kpi_crop_health": "पीक आरोग्य",
        "kpi_current_weather": "सद्य हवामान",
        "recent_diagnosis_title": "मागील पीक निदान",
        "risk_forecast_title": "७ दिवसांचा रोग धोका अंदाज",
        "upcoming_alerts_title": "आगामी सूचना व अलर्ट",
        "btn_get_advisory": "उपचार सल्ला पहा",
        "btn_save_result": "निकाल जतन करा",
        "btn_track_case": "प्रकरण स्थिती पहा",
        "btn_upload_another": "दुसरा फोटो अपलोड करा",
        "unknown_state_title": "या लक्षणांचे ठामपणे निदान होऊ शकले नाही.",
        "unknown_state_desc": "हे प्रकरण कृषी तज्ज्ञांच्या तपासणीसाठी वर्ग करण्यात आले आहे.",
        "sensor_dashboard_title": "स्मार्ट ट्रॅप व शेती सेन्सर्स",
        "sensor_dashboard_subtitle": "शेतातील उपकरणांकडून मिळणारी थेट माहिती.",
        "sensor_status_ready": "सेन्सर जोडणीसाठी सज्ज",
        "sensor_awaiting_data": "माहितीची प्रतीक्षा",
        "pest_activity_trend": "कीड हालचाल प्रमाण (ट्रॅप/दिवस)",
        "hotspot_title": "कीड प्रादुर्भाव भौगोलिक हॉटस्पॉट नकाशा",
        "hotspot_subtitle": "महाराष्ट्र राज्यातील कीड व रोगांचे थेट भौगोलिक दृश्य.",
        "advisory_view_title": "एकात्मिक उपचार सल्ला",
        "advisory_view_subtitle": "उत्तम पीक आरोग्यासाठी वैयक्तिकृत व स्थानिक हवामान-आधारित शिफारसी.",
        "quick_actions": "जलद कृती",
        "action_download_pdf": "पीडीएफ डाउनलोड",
        "action_share": "शेअर करा",
        "action_consult_expert": "तज्ज्ञांचा सल्ला घ्या",
        "opt_immediate": "१. त्वरित करावयाची उपाययोजना",
        "opt_organic": "२. सेंद्रिय / जैविक व मशागतीचे उपाय",
        "opt_chemical": "३. रासायनिक उपाय (नियंत्रित फवारणी)",
        "opt_additional": "४. अतिरिक्त माहिती, खबरदारी व पाठपुरावा",
        "safe_use_notice": "महाराष्ट्र कृषी विभाग व CIBRC शिफारसींचे तंतोतंत पालन करा. संरक्षक पोशाख वापरा.",
        "waiting_period_label": "फवारणीनंतर काढणी प्रतीक्षा कालावधी (PHI)",
        "follow_up_date_label": "पुढील पाहणीची शिफारस",
        "need_help_title": "तज्ज्ञ कृषी डॉक्टरांचे मार्गदर्शन हवे आहे का?",
        "need_help_desc": "तालुका कृषी अधिकारी किंवा केव्हीके कृषी विज्ञान केंद्राशी संपर्क साधा."
    },

    "hi": {
        # Navigation & Brand
        "app_title": "फाल्कन-एआई | फसल स्वास्थ्य निर्णय सहायता प्रणाली",
        "service_subtitle": "महाराष्ट्र राज्य नवाचार सोसायटी · SIH26131",
        "nav_farmer_portal": "किसान पोर्टल",
        "nav_expert_desk": "कृषि विशेषज्ञ समीक्षा",
        "nav_officer_dashboard": "कृषि अधिकारी डैशबोर्ड",
        "nav_login": "लॉग इन / पंजीकरण",
        "nav_logout": "लॉग आउट",
        "language_select": "भाषा",

        # Hero & Upload
        "hero_eyebrow": "प्रारंभिक पहचान एवं एकीकृत फसल रोग व कीट प्रबंधन",
        "hero_title": "एआई निदान और कृषि विशेषज्ञ मार्गदर्शन से फसलों की सुरक्षा करें",
        "hero_desc": "प्रभावित फसल की तस्वीर अपलोड करें। त्वरित एआई पहचान, मौसम-आधारित जोखिम मूल्यांकन और प्रमाणित कृषि सलाह प्राप्त करें।",
        "start_assessment": "फसल स्वास्थ्य जांच शुरू करें",
        "upload_subtext": "मोबाइल कैमरे से साफ फोटो लें या गैलरी से चुनें।",
        "btn_open_camera": "कैमरा खोलें",
        "btn_upload_pc": "फोटो चुनें",
        "drop_zone_text": "फसल की फोटो यहाँ खींचें या फाइल चुनें",
        "drop_zone_sub": "JPG, JPEG, PNG या WEBP (अधिकतम 15 MB)",
        "step1_select_crop": "1. फसल चुनें",
        "step2_select_location": "2. खेत व स्थान",
        "step3_select_stage": "3. फसल वृद्धि अवस्था",
        "step4_upload_image": "4. पत्ती की तस्वीर अपलोड करें",
        "btn_run_diagnosis": "एआई रोग पहचान एवं जोखिम जांचें",
        "btn_analyzing": "छवि व मौसम का विश्लेषण हो रहा है...",

        # Quality & Errors
        "quality_issue_title": "तस्वीर की गुणवत्ता अपर्याप्त है",
        "quality_issue_msg": "विश्वसनीय विश्लेषण के लिए तस्वीर की गुणवत्ता पर्याप्त नहीं है। कृपया प्रभावित हिस्से की स्पष्ट तस्वीर दोबारा अपलोड करें।",
        "invalid_file": "अमान्य फाइल। कृपया वैध तस्वीर चुनें।",

        # Statuses
        "status_identified": "सटीक पहचान हो गई",
        "status_healthy": "स्वस्थ फसल",
        "status_uncertain": "अनिश्चित (विशेषज्ञ समीक्षा आवश्यक)",
        "status_unknown": "अज्ञात लक्षण (विशेषज्ञ को भेजा गया)",
        "status_image_quality_issue": "धुंधली / अपर्याप्त गुणवत्ता वाली तस्वीर",
        "status_pending_expert": "कृषि विशेषज्ञ समीक्षा हेतु लंबित",
        "status_verified": "विशेषज्ञ द्वारा प्रमाणित निदान",
        "status_lab_referral": "प्रयोगशाला जांच हेतु अनुशंसित",
        "status_follow_up": "पुनरावलोकन आवश्यक",
        "status_closed": "मामला हल व बंद",

        # Taxonomy & Roles
        "type_disease": "फसल रोग (रोगजनक)",
        "type_pest": "कीट प्रकोप",
        "type_healthy": "स्वस्थ फसल",
        "type_unknown": "अज्ञात लक्षण",

        # Severity & Risk
        "severity_none": "कोई नहीं",
        "severity_low": "कम (हल्का)",
        "severity_moderate": "मध्यम",
        "severity_high": "अधिक (तीव्र)",
        "severity_critical": "अति गंभीर",
        "severity_not_assessed": "जांच नहीं की गई",
        "risk_low": "कम जोखिम",
        "risk_moderate": "मध्यम जोखिम",
        "risk_high": "उच्च जोखिम",
        "risk_critical": "अति गंभीर जोखिम",
        "risk_factors_title": "जोखिम कारक",
        "confidence_label": "एआई सटीकता",
        "severity_label": "पत्ती पर गंभीरता",
        "damage_area_label": "अनुमानित प्रभावित क्षेत्र",
        "leaf_area_label": "पत्ती क्षेत्र",
        "weather_context_title": "स्थानीय सूक्ष्म जलवायु स्थिति",
        "weather_temp": "तापमान",
        "weather_humidity": "आर्द्रता",
        "weather_rain": "वर्षा",
        "weather_source": "स्रोत",
        "weather_unavailable": "इस स्थान के लिए मौसम डेटा उपलब्ध नहीं है",

        # Advisory Sections
        "advisory_title": "एकीकृत कीट एवं रोग प्रबंधन (IPM) सलाह",
        "immediate_action_title": "तत्काल कार्रवाई",
        "monitoring_title": "खेत निगरानी",
        "cultural_title": "कृषि एवं निवारक उपाय",
        "biological_title": "जैविक नियंत्रण",
        "chemical_title": "सुरक्षित रासायनिक मार्गदर्शन",
        "safety_title": "किसान सुरक्षा एवं सावधानियां",
        "referral_alert_title": "कृषि अधिकारी / केवीके से कब संपर्क करें",
        "follow_up_alert": "अनुशंसा: अगले {days} दिनों में दोबारा जांच कर तस्वीर अपलोड करें",

        # Follow up & Confirmation
        "followup_title": "फॉलो-अप अवलोकन एवं खेत परिणाम",
        "outcome_improved": "स्थिति में सुधार हुआ",
        "outcome_unchanged": "स्थिति वैसी ही है",
        "outcome_worsened": "स्थिति और बिगड़ी",
        "outcome_resolved": "रोग/कीट पूरी तरह समाप्त",
        "btn_submit_followup": "फॉलो-अप फोटो अपलोड करें",
        "btn_confirm_outcome": "खेत परिणाम की पुष्टि करें",

        # Expert Desk
        "expert_desk_title": "कृषि विशेषज्ञ पोर्टल",
        "pending_cases_count": "समीक्षा हेतु लंबित मामले",
        "btn_confirm_ai": "एआई निदान की पुष्टि करें",
        "btn_correct_ai": "निदान सही करें",
        "btn_refer_lab": "प्रयोगशाला रेफर करें",
        "btn_request_image": "स्पष्ट फोटो मांगें",
        "expert_notes_placeholder": "सलाह या कीटनाशक निर्देश लिखें...",

        # Officer Dashboard & GIS
        "dashboard_title": "महाराष्ट्र कृषि अधिकारी जीआईएस इंटेलिजेंस",
        "total_observations": "कुल दर्ज मामले",
        "disease_cases": "रोग प्रकोप",
        "pest_cases": "कीट प्रकोप",
        "high_risk_alerts": "उच्च जोखिम चेतावनी",
        "hotspot_map_title": "भौगोलिक हॉटस्पॉट मानचित्र (महाराष्ट्र)",
        "district_distribution_title": "जिलावार प्रकोप दर",

        # Footer
        "footer_text": "फाल्कन-एआई · स्मार्ट इंडिया हैकाथॉन 2026 (SIH26131) · कौशल, रोजगार, उद्यमिता एवं नवाचार विभाग, महाराष्ट्र सरकार",

        # Reference Navigation & Dashboard
        "sidebar_subtitle": "फसलों का उत्तम स्वास्थ्य · समृद्ध महाराष्ट्र",
        "nav_dashboard": "डैशबोर्ड",
        "nav_diagnose": "फसल निदान",
        "nav_fields": "मेरे खेत",
        "nav_alerts": "कीट-रोग अलर्ट",
        "nav_weather": "मौसम व जोखिम",
        "nav_hotspots": "हॉटस्पॉट नक्शा",
        "nav_advisory": "उपचार सलाह",
        "nav_reports": "रिपोर्ट्स एवं विश्लेषण",
        "nav_expert_connect": "कृषि विशेषज्ञ परामर्श",
        "nav_knowledge": "ज्ञान केंद्र",
        "nav_sensors": "स्मार्ट ट्रैप एवं सेंसर्स",
        "search_placeholder": "फसल, रोग, सलाह खोजें...",
        "hero_headline": "स्वस्थ फसलें, उज्ज्वल भविष्य",
        "hero_supporting": "एआई • किसान • संधारणीय कृषि",
        "hero_quote": "निरोगी खेती, समृद्ध महाराष्ट्र",
        "kpi_fields": "मेरे खेत",
        "kpi_main_crop": "मुख्य फसल",
        "kpi_crop_health": "फसल स्वास्थ्य",
        "kpi_current_weather": "वर्तमान मौसम",
        "recent_diagnosis_title": "हालिया फसल निदान",
        "risk_forecast_title": "७ दिनों का रोग जोखिम पूर्वानुमान",
        "upcoming_alerts_title": "आगामी सूचनाएं एवं अलर्ट",
        "btn_get_advisory": "उपचार सलाह देखें",
        "btn_save_result": "परिणाम सहेजें",
        "btn_track_case": "मामला ट्रैक करें",
        "btn_upload_another": "दूसरी तस्वीर अपलोड करें",
        "unknown_state_title": "इस स्थिति की निश्चित पहचान नहीं हो सकी।",
        "unknown_state_desc": "यह मामला कृषि विशेषज्ञ समीक्षा के लिए भेज दिया गया है।",
        "sensor_dashboard_title": "स्मार्ट ट्रैप एवं फील्ड सेंसर्स",
        "sensor_dashboard_subtitle": "खेत में स्थापित उपकरणों से प्राप्त लाइव डेटा।",
        "sensor_status_ready": "सेंसर एकीकरण तैयार",
        "sensor_awaiting_data": "डेटा की प्रतीक्षा",
        "pest_activity_trend": "कीट गतिविधि रुझान (ट्रैप/दिन)",
        "hotspot_title": "कीट प्रकोप भौगोलिक हॉटस्पॉट नक्शा",
        "hotspot_subtitle": "महाराष्ट्र भर में कीट एवं रोग प्रकोप का वास्तविक दृश्य।",
        "advisory_view_title": "एकीकृत उपचार सलाह",
        "advisory_view_subtitle": "बेहतर फसल स्वास्थ्य के लिए व्यक्तिगत एवं स्थानीय सिफारिशें।",
        "quick_actions": "त्वरित कार्रवाई",
        "action_download_pdf": "पीडीएफ डाउनलोड",
        "action_share": "साझा करें",
        "action_consult_expert": "विशेषज्ञ से परामर्श लें",
        "opt_immediate": "१. तत्काल कार्रवाई",
        "opt_organic": "२. जैविक एवं एकीकृत नियंत्रण",
        "opt_chemical": "३. रासायनिक उपाय",
        "opt_additional": "४. अतिरिक्त जानकारी एवं निगरानी",
        "safe_use_notice": "महाराष्ट्र कृषि विभाग और CIBRC दिशानिर्देशों का कड़ाई से पालन करें।",
        "waiting_period_label": "कटाई प्रतीक्षा अवधि (PHI)",
        "follow_up_date_label": "अनुशंसित अगली जांच",
        "need_help_title": "कृषि विशेषज्ञ का मार्गदर्शन चाहिए?",
        "need_help_desc": "तालुका कृषि अधिकारी अथवा कृषि विज्ञान केंद्र से संपर्क करें।"
    }
}


def get_translation(key: str, lang: str = "mr") -> str:
    """Retrieves translation with fallback to English."""
    norm_lang = (lang or "mr").lower()
    lang_dict = TRANSLATIONS.get(norm_lang, TRANSLATIONS.get("en", {}))
    if key in lang_dict:
        return lang_dict[key]
    return TRANSLATIONS.get("en", {}).get(key, key)


def get_all_translations(lang: str = "mr") -> Dict[str, str]:
    """Returns complete catalog in requested language (mr, hi, en) with fallback."""
    norm_lang = (lang or "mr").lower()
    base = dict(TRANSLATIONS.get("en", {}))
    if norm_lang in TRANSLATIONS and norm_lang != "en":
        base.update(TRANSLATIONS[norm_lang])
    return base


