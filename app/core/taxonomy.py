"""
Agricultural Taxonomy, Maharashtra Agro-climatic Configuration, and IPM Knowledge Base
SIH26131: Early Detection and Management of Crop Diseases and Pest Infestations
"""

from typing import Dict, Any, List, Optional

# ==============================================================================
# 1. MAHARASHTRA DISTRICTS, TALUKAS & CENTROID COORDINATES
# ==============================================================================

MAHARASHTRA_DISTRICTS: Dict[str, Dict[str, Any]] = {
    "Pune": {
        "lat": 18.5204, "lon": 73.8567, "agro_zone": "Western Maharashtra / Scarcity Zone",
        "talukas": ["Pune City", "Haveli", "Baramati", "Shirur", "Daund", "Indapur", "Junnar", "Khed", "Ambegaon", "Maval", "Mulshi", "Velhe", "Bhor", "Purandar"]
    },
    "Nashik": {
        "lat": 19.9975, "lon": 73.7898, "agro_zone": "Western Ghat / Transition Zone",
        "talukas": ["Nashik", "Niphad", "Dindori", "Yeola", "Sinnar", "Malegaon", "Chandwad", "Kalwan", "Baglan", "Deola", "Igatpuri", "Trimbakeshwar", "Surgana", "Peint"]
    },
    "Nagpur": {
        "lat": 21.1458, "lon": 79.0882, "agro_zone": "Eastern Vidarbha Zone",
        "talukas": ["Nagpur Urban", "Nagpur Rural", "Kamptee", "Hingna", "Katol", "Narkhed", "Savner", "Kalameshwar", "Ramtek", "Mouda", "Umred", "Kuhi", "Bhiwapur"]
    },
    "Chhatrapati Sambhajinagar": {
        "lat": 19.8762, "lon": 75.3433, "agro_zone": "Marathwada Central Zone",
        "talukas": ["Chhatrapati Sambhajinagar", "Paithan", "Gangapur", "Vaijapur", "Kannad", "Khuldabad", "Sillod", "Soegaon", "Phulambri"]
    },
    "Amravati": {
        "lat": 20.9374, "lon": 77.7796, "agro_zone": "Western Vidarbha Zone",
        "talukas": ["Amravati", "Bhatkuli", "Nandgaon Khandeshwar", "Dharni", "Chikhaldara", "Achalpur", "Chandurbazar", "Morshi", "Warud", "Daryapur", "Anjangaon Surji", "Chandur Railway", "Dhamangaon Railway", "Teosa"]
    },
    "Kolhapur": {
        "lat": 16.7050, "lon": 74.2433, "agro_zone": "Sub-Montane Zone",
        "talukas": ["Karveer", "Panhala", "Shahuwadi", "Kagal", "Hatkanangale", "Shirol", "Radhanagari", "Gaganbawda", "Bhudargad", "Ajra", "Gadhinglaj", "Chandgad"]
    },
    "Solapur": {
        "lat": 17.6599, "lon": 75.9064, "agro_zone": "Scarcity Zone",
        "talukas": ["Solapur North", "Solapur South", "Barshi", "Akkalkot", "Mohol", "Madha", "Karmala", "Pandharpur", "Sangola", "Malshiras", "Mangalwedha"]
    },
    "Ahmednagar": {
        "lat": 19.0948, "lon": 74.7480, "agro_zone": "Scarcity Zone",
        "talukas": ["Nagar", "Rahuri", "Shrirampur", "Nevasa", "Shevgaon", "Pathardi", "Jamkhed", "Karjat", "Shrigonda", "Parner", "Sangamner", "Akole", "Kopargaon", "Rahata"]
    },
    "Sangli": {
        "lat": 16.8524, "lon": 74.5815, "agro_zone": "Western Maharashtra Plain",
        "talukas": ["Miraj", "Tasgaon", "Khanapur (Vita)", "Atpadi", "Jat", "Kavathe Mahankal", "Walwa (Islampur)", "Shirala", "Kadegaon", "Palus"]
    },
    "Satara": {
        "lat": 17.6805, "lon": 73.9935, "agro_zone": "Western Ghat / Sub-Montane",
        "talukas": ["Satara", "Karad", "Wai", "Mahabaleshwar", "Phaltan", "Maan (Dahiwadi)", "Khatav (Vaduj)", "Koregaon", "Patan", "Jaoli", "Khandala"]
    },
    "Jalgaon": {
        "lat": 21.0077, "lon": 75.5626, "agro_zone": "Khandesh Tapi Basin",
        "talukas": ["Jalgaon", "Bhusawal", "Raver", "Muktainagar", "Bodwad", "Yawal", "Chopda", "Erandol", "Dharangaon", "Pachora", "Bhadgaon", "Chalisgaon", "Jamner", "Parola", "Amalner"]
    },
    "Latur": {
        "lat": 18.4088, "lon": 76.5604, "agro_zone": "Marathwada Southern Zone",
        "talukas": ["Latur", "Ausa", "Renapur", "Ahmedpur", "Chakur", "Shirur Anantpal", "Nilanga", "Deoni", "Udgir", "Jalkot"]
    },
    "Nanded": {
        "lat": 19.1383, "lon": 77.3210, "agro_zone": "Marathwada East / Godavari Basin",
        "talukas": ["Nanded", "Ardhapur", "Mudkhed", "Bhokar", "Umri", "Loha", "Kandhar", "Kinwat", "Himayatnagar", "Hadgaon", "Mahur", "Deglur", "Mukhed", "Dharmabad", "Biloli", "Naigaon"]
    },
    "Akola": {
        "lat": 20.7002, "lon": 77.0082, "agro_zone": "Western Vidarbha Zone",
        "talukas": ["Akola", "Akot", "Telhara", "Balapur", "Patur", "Barshitakli", "Murtizapur"]
    },
    "Yavatmal": {
        "lat": 20.3888, "lon": 78.1204, "agro_zone": "Central Vidarbha Zone",
        "talukas": ["Yavatmal", "Arni", "Babhulgaon", "Kalamb", "Darwha", "Digras", "Ner", "Pusad", "Umarkhed", "Mahagaon", "Kelapur (Pandharkawada)", "Ghatanji", "Wani", "Maregaon", "Zari Jamani", "Ralegaon"]
    }
}

# Add default lookup for any other Maharashtra district
DEFAULT_COORDINATES = {"lat": 19.7515, "lon": 75.7139} # Maharashtra geographic center


# ==============================================================================
# 2. CROP CONFIGURATION (MAHARASHTRA PRIORITY)
# ==============================================================================

CROPS: Dict[str, Dict[str, Any]] = {
    "soybean": {
        "code": "soybean",
        "display_name": "Soybean",
        "marathi_name": "सोयाबीन",
        "hindi_name": "सोयाबीन",
        "seasons": ["KHARIF"],
        "category": "Oilseeds / Legumes",
        "model_supported": True,
        "key_diseases": ["soybean_rust", "yellow_mosaic_virus"],
        "key_pests": ["stem_fly", "girdle_beetle", "spodoptera_litura"],
        "susceptible_stages": ["flowering", "fruiting_pod"],
        "description": "Prime kharif oilseed crop in Maharashtra with trained foliar specimen classification."
    },
    "cotton": {
        "code": "cotton",
        "display_name": "Cotton",
        "marathi_name": "कापूस",
        "hindi_name": "कपास",
        "seasons": ["KHARIF"],
        "category": "Cash Crops / Fiber",
        "model_supported": True,
        "key_diseases": ["cotton_bacterial_blight", "cotton_leaf_curl"],
        "key_pests": ["pink_bollworm", "whitefly", "aphids"],
        "susceptible_stages": ["vegetative", "flowering", "fruiting_pod"],
        "description": "Major commercial fiber cash crop in Vidarbha and Marathwada regions with bollworm and blight detection."
    },
    "maize": {
        "code": "maize",
        "display_name": "Maize / Corn",
        "marathi_name": "मका",
        "hindi_name": "मक्का",
        "seasons": ["KHARIF", "RABI"],
        "category": "Cereals",
        "model_supported": True,
        "key_diseases": ["corn_rust", "corn_northern_leaf_blight", "corn_gray_leaf_spot", "corn_smut", "corn_charcoal"],
        "key_pests": ["fall_armyworm", "stem_borer", "corn_insects_damages"],
        "susceptible_stages": ["vegetative", "flowering"],
        "description": "Major food and feed cereal crop with 21 trained diagnostic conditions."
    },
    "tomato": {
        "code": "tomato",
        "display_name": "Tomato",
        "marathi_name": "टोमॅटो",
        "hindi_name": "टमाटर",
        "seasons": ["KHARIF", "RABI", "SUMMER"],
        "category": "Vegetables / Horticulture",
        "model_supported": True,
        "key_diseases": ["tomato_early_blight", "tomato_late_blight", "tomato_leaf_mold", "tomato_septoria_leaf_spot", "tomato_bacterial_leaf_spot", "tomato_bacterial_wilt", "tomato_mosaic_virus", "tomato_yellow_leaf_curl_virus"],
        "key_pests": ["tuta_absoluta", "fruit_borer", "whitefly"],
        "susceptible_stages": ["vegetative", "flowering", "fruiting_pod"],
        "description": "High-value horticulture crop with comprehensive 14-condition model coverage."
    },
    "grape": {
        "code": "grape",
        "display_name": "Grape",
        "marathi_name": "द्राक्ष",
        "hindi_name": "अंगूर",
        "seasons": ["ANNUAL"],
        "category": "Horticulture / Fruit",
        "model_supported": True,
        "key_diseases": ["grape_downy_mildew", "grape_leaf_spot", "grape_black_rot", "grapevine_leafroll_disease"],
        "key_pests": ["flea_beetle", "mealybug", "thrips"],
        "susceptible_stages": ["flowering", "fruiting_pod"],
        "description": "Export powerhouse crop in Nashik, Sangli, and Solapur with downy mildew and leafroll detection."
    },
    "citrus": {
        "code": "citrus",
        "display_name": "Citrus / Orange",
        "marathi_name": "संत्रा / मोसंबी",
        "hindi_name": "संतरा / मौसमी",
        "seasons": ["ANNUAL"],
        "category": "Horticulture / Fruit",
        "model_supported": True,
        "key_diseases": ["citrus_greening_disease", "citrus_canker"],
        "key_pests": ["citrus_psylla", "leaf_miner", "fruit_sucking_moth"],
        "susceptible_stages": ["flowering", "fruiting_pod"],
        "description": "Nagpur Mandarin orange and Vidarbha sweet lime orchards with greening and canker detection."
    },
    "potato": {
        "code": "potato",
        "display_name": "Potato",
        "marathi_name": "बटाटा",
        "hindi_name": "आलू",
        "seasons": ["RABI"],
        "category": "Tubers / Vegetables",
        "model_supported": True,
        "key_diseases": ["potato_early_blight", "potato_late_blight"],
        "key_pests": ["aphids", "tuber_moth"],
        "susceptible_stages": ["vegetative", "flowering", "maturity"],
        "description": "Major tuber crop in Pune and Satara with early and late blight models."
    },
    "garlic": {
        "code": "garlic",
        "display_name": "Garlic / Onion",
        "marathi_name": "लसूण / कांदा",
        "hindi_name": "लहसुन / प्याज",
        "seasons": ["RABI"],
        "category": "Spices / Bulbs",
        "model_supported": True,
        "key_diseases": ["garlic_leaf_blight", "garlic_rust", "onion_purple_blotch"],
        "key_pests": ["thrips", "mites"],
        "susceptible_stages": ["vegetative", "maturity"],
        "description": "Commercial bulb cash crops across Maharashtra with leaf blight and rust models."
    },
    "banana": {
        "code": "banana",
        "display_name": "Banana",
        "marathi_name": "केळी",
        "hindi_name": "केला",
        "seasons": ["ANNUAL"],
        "category": "Fruit / Plantation",
        "model_supported": True,
        "key_diseases": ["banana_panama_disease"],
        "key_pests": ["weevil", "aphids"],
        "susceptible_stages": ["vegetative", "flowering", "fruiting_pod"],
        "description": "Major perennial fruit crop of Jalgaon district with Panama wilt model."
    },
    "cucumber": {
        "code": "cucumber",
        "display_name": "Cucumber",
        "marathi_name": "काकडी",
        "hindi_name": "खीरा",
        "seasons": ["KHARIF", "RABI", "SUMMER"],
        "category": "Cucurbits / Vegetables",
        "model_supported": True,
        "key_diseases": ["cucumber_angular_spot", "cucumber_bacterial_wilt", "cucumber_powdery_mildew"],
        "key_pests": ["fruit_fly", "whitefly"],
        "susceptible_stages": ["vegetative", "flowering", "fruiting_pod"],
        "description": "Vine vegetable crop with angular leaf spot, bacterial wilt, and powdery mildew detection."
    },
    "bean": {
        "code": "bean",
        "display_name": "Bean / Pulses",
        "marathi_name": "घेवडा / कडधान्य",
        "hindi_name": "सेम / दालें",
        "seasons": ["KHARIF", "RABI"],
        "category": "Legumes / Pulses",
        "model_supported": True,
        "key_diseases": ["bean_rust", "bean_halo_blight", "bean_mosaic_virus"],
        "key_pests": ["aphids", "pod_borer"],
        "susceptible_stages": ["vegetative", "flowering", "fruiting_pod"],
        "description": "Grain and vegetable legumes with rust, halo blight, and mosaic virus models."
    }
}

# ==============================================================================
# 3. CROP GROWTH STAGES
# ==============================================================================

GROWTH_STAGES: Dict[str, Dict[str, str]] = {
    "seedling": {
        "code": "seedling",
        "name_en": "Seedling Stage (1 to 20 days)",
        "name_mr": "Seedling Stage (1 to 20 days)",
        "name_hi": "Seedling Stage (1 to 20 days)",
        "risk_multiplier": "1.1"
    },
    "vegetative": {
        "code": "vegetative",
        "name_en": "Vegetative Stage (21 to 45 days)",
        "name_mr": "Vegetative Stage (21 to 45 days)",
        "name_hi": "Vegetative Stage (21 to 45 days)",
        "risk_multiplier": "1.0"
    },
    "flowering": {
        "code": "flowering",
        "name_en": "Flowering Stage (46 to 65 days)",
        "name_mr": "Flowering Stage (46 to 65 days)",
        "name_hi": "Flowering Stage (46 to 65 days)",
        "risk_multiplier": "1.3"
    },
    "fruiting_pod": {
        "code": "fruiting_pod",
        "name_en": "Pod / Fruit Development",
        "name_mr": "Pod / Fruit Development",
        "name_hi": "Pod / Fruit Development",
        "risk_multiplier": "1.4"
    },
    "maturity": {
        "code": "maturity",
        "name_en": "Maturity / Pre-harvest",
        "name_mr": "Maturity / Pre-harvest",
        "name_hi": "Maturity / Pre-harvest",
        "risk_multiplier": "0.9"
    }
}

# ==============================================================================
# 4. YOLO MODEL CLASS MAPPING (116 CLASSES -> TAXONOMY)
# ==============================================================================

YOLO_CLASS_TAXONOMY: Dict[int, Dict[str, Any]] = {
    0: {"raw": "corn rust", "crop": "maize", "type": "DISEASE", "code": "corn_rust", "display": "Corn Common Rust"},
    1: {"raw": "cherry leaf", "crop": "cherry", "type": "HEALTHY", "code": "cherry_leaf", "display": "Cherry Leaf"},
    2: {"raw": "soybean leaf", "crop": "soybean", "type": "HEALTHY", "code": "soybean_leaf", "display": "Soybean Leaf"},
    3: {"raw": "strawberry leaf", "crop": "strawberry", "type": "HEALTHY", "code": "strawberry_leaf", "display": "Strawberry Leaf"},
    4: {"raw": "corn northern leaf blight", "crop": "maize", "type": "DISEASE", "code": "corn_northern_leaf_blight", "display": "Corn Northern Leaf Blight"},
    5: {"raw": "coffee leaf", "crop": "coffee", "type": "HEALTHY", "code": "coffee_leaf", "display": "Coffee Leaf"},
    6: {"raw": "cauliflower alternaria leaf spot", "crop": "cauliflower", "type": "DISEASE", "code": "cauliflower_alternaria", "display": "Cauliflower Alternaria Spot"},
    7: {"raw": "celery leaf", "crop": "celery", "type": "HEALTHY", "code": "celery_leaf", "display": "Celery Leaf"},
    8: {"raw": "strawberry anthracnose", "crop": "strawberry", "type": "DISEASE", "code": "strawberry_anthracnose", "display": "Strawberry Anthracnose"},
    9: {"raw": "basil leaf", "crop": "basil", "type": "HEALTHY", "code": "basil_leaf", "display": "Basil Leaf"},
    10: {"raw": "citrus greening disease", "crop": "citrus", "type": "DISEASE", "code": "citrus_greening_disease", "display": "Citrus Greening (HLB)"},
    11: {"raw": "grape downy mildew", "crop": "grape", "type": "DISEASE", "code": "grape_downy_mildew", "display": "Grape Downy Mildew"},
    12: {"raw": "blueberry rust", "crop": "blueberry", "type": "DISEASE", "code": "blueberry_rust", "display": "Blueberry Rust"},
    13: {"raw": "celery anthracnose", "crop": "celery", "type": "DISEASE", "code": "celery_anthracnose", "display": "Celery Anthracnose"},
    14: {"raw": "ginger leaf", "crop": "ginger", "type": "HEALTHY", "code": "ginger_leaf", "display": "Ginger Leaf"},
    15: {"raw": "cucumber angular leaf spot", "crop": "cucumber", "type": "DISEASE", "code": "cucumber_angular_spot", "display": "Cucumber Angular Leaf Spot"},
    16: {"raw": "broccoli downy mildew", "crop": "broccoli", "type": "DISEASE", "code": "broccoli_downy_mildew", "display": "Broccoli Downy Mildew"},
    17: {"raw": "blueberry leaf", "crop": "blueberry", "type": "HEALTHY", "code": "blueberry_leaf", "display": "Blueberry Leaf"},
    18: {"raw": "cucumber bacterial wilt", "crop": "cucumber", "type": "DISEASE", "code": "cucumber_bacterial_wilt", "display": "Cucumber Bacterial Wilt"},
    19: {"raw": "grape leaf", "crop": "grape", "type": "HEALTHY", "code": "grape_leaf", "display": "Grape Leaf"},
    20: {"raw": "garlic leaf", "crop": "garlic", "type": "HEALTHY", "code": "garlic_leaf", "display": "Garlic Leaf"},
    21: {"raw": "plum leaf", "crop": "plum", "type": "HEALTHY", "code": "plum_leaf", "display": "Plum Leaf"},
    22: {"raw": "ginger sheath blight", "crop": "ginger", "type": "DISEASE", "code": "ginger_sheath_blight", "display": "Ginger Sheath Blight"},
    23: {"raw": "rice leaf", "crop": "rice", "type": "HEALTHY", "code": "rice_leaf", "display": "Rice Leaf"},
    24: {"raw": "cabbage leaf", "crop": "cabbage", "type": "HEALTHY", "code": "cabbage_leaf", "display": "Cabbage Leaf"},
    25: {"raw": "corn gray leaf spot", "crop": "maize", "type": "DISEASE", "code": "corn_gray_leaf_spot", "display": "Corn Gray Leaf Spot"},
    26: {"raw": "eggplant leaf", "crop": "brinjal", "type": "HEALTHY", "code": "eggplant_leaf", "display": "Eggplant Leaf"},
    27: {"raw": "basil downy mildew", "crop": "basil", "type": "DISEASE", "code": "basil_downy_mildew", "display": "Basil Downy Mildew"},
    28: {"raw": "tomato bacterial leaf spot", "crop": "tomato", "type": "DISEASE", "code": "tomato_bacterial_leaf_spot", "display": "Tomato Bacterial Spot"},
    29: {"raw": "cherry leaf spot", "crop": "cherry", "type": "DISEASE", "code": "cherry_leaf_spot", "display": "Cherry Leaf Spot"},
    30: {"raw": "cucumber leaf", "crop": "cucumber", "type": "HEALTHY", "code": "cucumber_leaf", "display": "Cucumber Leaf"},
    31: {"raw": "apple black rot", "crop": "apple", "type": "DISEASE", "code": "apple_black_rot", "display": "Apple Black Rot"},
    32: {"raw": "eggplant cercospora leaf spot", "crop": "brinjal", "type": "DISEASE", "code": "eggplant_cercospora", "display": "Eggplant Cercospora Spot"},
    33: {"raw": "maple leaf", "crop": "other", "type": "HEALTHY", "code": "maple_leaf", "display": "Maple Leaf"},
    34: {"raw": "cucumber powdery mildew", "crop": "cucumber", "type": "DISEASE", "code": "cucumber_powdery_mildew", "display": "Cucumber Powdery Mildew"},
    35: {"raw": "bean rust", "crop": "bean", "type": "DISEASE", "code": "bean_rust", "display": "Bean Rust"},
    36: {"raw": "rice sheath blight", "crop": "rice", "type": "DISEASE", "code": "rice_sheath_blight", "display": "Rice Sheath Blight"},
    37: {"raw": "zucchini yellow mosaic virus", "crop": "zucchini", "type": "DISEASE", "code": "zucchini_mosaic_virus", "display": "Zucchini Yellow Mosaic"},
    38: {"raw": "bean leaf", "crop": "bean", "type": "HEALTHY", "code": "bean_leaf", "display": "Bean Leaf"},
    39: {"raw": "citrus canker", "crop": "citrus", "type": "DISEASE", "code": "citrus_canker", "display": "Citrus Canker"},
    40: {"raw": "peach leaf curl", "crop": "peach", "type": "DISEASE", "code": "peach_leaf_curl", "display": "Peach Leaf Curl"},
    41: {"raw": "maple tar spot", "crop": "other", "type": "DISEASE", "code": "maple_tar_spot", "display": "Maple Tar Spot"},
    42: {"raw": "tomato leaf mold", "crop": "tomato", "type": "DISEASE", "code": "tomato_leaf_mold", "display": "Tomato Leaf Mold"},
    43: {"raw": "plum pocket disease", "crop": "plum", "type": "DISEASE", "code": "plum_pocket", "display": "Plum Pocket Disease"},
    44: {"raw": "tomato early blight", "crop": "tomato", "type": "DISEASE", "code": "tomato_early_blight", "display": "Tomato Early Blight"},
    45: {"raw": "cherry powdery mildew", "crop": "cherry", "type": "DISEASE", "code": "cherry_powdery_mildew", "display": "Cherry Powdery Mildew"},
    46: {"raw": "grape leaf spot", "crop": "grape", "type": "DISEASE", "code": "grape_leaf_spot", "display": "Grape Leaf Spot"},
    47: {"raw": "bell pepper leaf spot", "crop": "pepper", "type": "DISEASE", "code": "pepper_leaf_spot", "display": "Bell Pepper Leaf Spot"},
    48: {"raw": "apple rust", "crop": "apple", "type": "DISEASE", "code": "apple_rust", "display": "Apple Rust"},
    49: {"raw": "cabbage alternaria leaf spot", "crop": "cabbage", "type": "DISEASE", "code": "cabbage_alternaria", "display": "Cabbage Alternaria Spot"},
    50: {"raw": "tobacco mosaic virus", "crop": "tobacco", "type": "DISEASE", "code": "tobacco_mosaic", "display": "Tobacco Mosaic Virus"},
    51: {"raw": "apple mosaic virus", "crop": "apple", "type": "DISEASE", "code": "apple_mosaic", "display": "Apple Mosaic Virus"},
    52: {"raw": "potato late blight", "crop": "potato", "type": "DISEASE", "code": "potato_late_blight", "display": "Potato Late Blight"},
    53: {"raw": "tomato septoria leaf spot", "crop": "tomato", "type": "DISEASE", "code": "tomato_septoria_leaf_spot", "display": "Tomato Septoria Leaf Spot"},
    54: {"raw": "potato leaf", "crop": "potato", "type": "HEALTHY", "code": "potato_leaf", "display": "Potato Leaf"},
    55: {"raw": "lettuce mosaic virus", "crop": "lettuce", "type": "DISEASE", "code": "lettuce_mosaic", "display": "Lettuce Mosaic"},
    56: {"raw": "garlic leaf blight", "crop": "garlic", "type": "DISEASE", "code": "garlic_leaf_blight", "display": "Garlic Leaf Blight"},
    57: {"raw": "grapevine leafroll disease", "crop": "grape", "type": "DISEASE", "code": "grapevine_leafroll_disease", "display": "Grapevine Leafroll Disease"},
    58: {"raw": "carrot cavity spot", "crop": "carrot", "type": "DISEASE", "code": "carrot_cavity_spot", "display": "Carrot Cavity Spot"},
    59: {"raw": "cauliflower leaf", "crop": "cauliflower", "type": "HEALTHY", "code": "cauliflower_leaf", "display": "Cauliflower Leaf"},
    60: {"raw": "rice blast", "crop": "rice", "type": "DISEASE", "code": "rice_blast", "display": "Rice Blast"},
    61: {"raw": "tomato late blight", "crop": "tomato", "type": "DISEASE", "code": "tomato_late_blight", "display": "Tomato Late Blight"},
    62: {"raw": "banana panama disease", "crop": "banana", "type": "DISEASE", "code": "banana_panama_disease", "display": "Banana Panama Disease"},
    63: {"raw": "ginger leaf spot", "crop": "ginger", "type": "DISEASE", "code": "ginger_leaf_spot", "display": "Ginger Leaf Spot"},
    64: {"raw": "garlic rust", "crop": "garlic", "type": "DISEASE", "code": "garlic_rust", "display": "Garlic Rust"},
    65: {"raw": "banana leaf", "crop": "banana", "type": "HEALTHY", "code": "banana_leaf", "display": "Banana Leaf"},
    66: {"raw": "lettuce downy mildew", "crop": "lettuce", "type": "DISEASE", "code": "lettuce_downy_mildew", "display": "Lettuce Downy Mildew"},
    67: {"raw": "grape black rot", "crop": "grape", "type": "DISEASE", "code": "grape_black_rot", "display": "Grape Black Rot"},
    68: {"raw": "raspberry leaf", "crop": "raspberry", "type": "HEALTHY", "code": "raspberry_leaf", "display": "Raspberry Leaf"},
    69: {"raw": "tomato mosaic virus", "crop": "tomato", "type": "DISEASE", "code": "tomato_mosaic_virus", "display": "Tomato Mosaic Virus"},
    70: {"raw": "tomato leaf", "crop": "tomato", "type": "HEALTHY", "code": "tomato_leaf", "display": "Tomato Leaf"},
    71: {"raw": "squash powdery mildew", "crop": "squash", "type": "DISEASE", "code": "squash_powdery_mildew", "display": "Squash Powdery Mildew"},
    72: {"raw": "squash leaf", "crop": "squash", "type": "HEALTHY", "code": "squash_leaf", "display": "Squash Leaf"},
    73: {"raw": "corn leaf", "crop": "maize", "type": "HEALTHY", "code": "corn_leaf", "display": "Corn Leaf"},
    74: {"raw": "lettuce leaf", "crop": "lettuce", "type": "HEALTHY", "code": "lettuce_leaf", "display": "Lettuce Leaf"},
    75: {"raw": "tobacco leaf", "crop": "tobacco", "type": "HEALTHY", "code": "tobacco_leaf", "display": "Tobacco Leaf"},
    76: {"raw": "bean halo blight", "crop": "bean", "type": "DISEASE", "code": "bean_halo_blight", "display": "Bean Halo Blight"},
    77: {"raw": "apple leaf", "crop": "apple", "type": "HEALTHY", "code": "apple_leaf", "display": "Apple Leaf"},
    78: {"raw": "bell pepper leaf", "crop": "pepper", "type": "HEALTHY", "code": "bell_pepper_leaf", "display": "Bell Pepper Leaf"},
    79: {"raw": "broccoli leaf", "crop": "broccoli", "type": "HEALTHY", "code": "broccoli_leaf", "display": "Broccoli Leaf"},
    80: {"raw": "apple scab", "crop": "apple", "type": "DISEASE", "code": "apple_scab", "display": "Apple Scab"},
    81: {"raw": "strawberry leaf scorch", "crop": "strawberry", "type": "DISEASE", "code": "strawberry_leaf_scorch", "display": "Strawberry Leaf Scorch"},
    82: {"raw": "corn smut", "crop": "maize", "type": "DISEASE", "code": "corn_smut", "display": "Corn Smut"},
    83: {"raw": "coffee leaf rust", "crop": "coffee", "type": "DISEASE", "code": "coffee_rust", "display": "Coffee Leaf Rust"},
    84: {"raw": "peach leaf", "crop": "peach", "type": "HEALTHY", "code": "peach_leaf", "display": "Peach Leaf"},
    85: {"raw": "bean mosaic virus", "crop": "bean", "type": "DISEASE", "code": "bean_mosaic", "display": "Bean Mosaic Virus"},
    86: {"raw": "celery early blight", "crop": "celery", "type": "DISEASE", "code": "celery_early_blight", "display": "Celery Early Blight"},
    87: {"raw": "potato early blight", "crop": "potato", "type": "DISEASE", "code": "potato_early_blight", "display": "Potato Early Blight"},
    88: {"raw": "tomato yellow leaf curl virus", "crop": "tomato", "type": "DISEASE", "code": "tomato_yellow_leaf_curl_virus", "display": "Tomato Yellow Leaf Curl Virus"},
    89: {"raw": "Cassava Bacterial Blight", "crop": "cassava", "type": "DISEASE", "code": "cassava_bacterial_blight", "display": "Cassava Bacterial Blight"},
    90: {"raw": "Cassava Brown Leaf Spot", "crop": "cassava", "type": "DISEASE", "code": "cassava_brown_spot", "display": "Cassava Brown Leaf Spot"},
    91: {"raw": "Cassava Healthy", "crop": "cassava", "type": "HEALTHY", "code": "cassava_healthy", "display": "Cassava Healthy Leaf"},
    92: {"raw": "Cassava Mosaic", "crop": "cassava", "type": "DISEASE", "code": "cassava_mosaic", "display": "Cassava Mosaic Disease"},
    93: {"raw": "Cassava Root Rot", "crop": "cassava", "type": "DISEASE", "code": "cassava_root_rot", "display": "Cassava Root Rot"},
    94: {"raw": "Corn Brown Spots", "crop": "maize", "type": "DISEASE", "code": "corn_brown_spots", "display": "Corn Brown Spots"},
    95: {"raw": "Corn Charcoal", "crop": "maize", "type": "DISEASE", "code": "corn_charcoal", "display": "Corn Charcoal Rot"},
    96: {"raw": "Corn Chlorotic Leaf Spot", "crop": "maize", "type": "DISEASE", "code": "corn_chlorotic_spot", "display": "Corn Chlorotic Leaf Spot"},
    97: {"raw": "Corn Gray leaf spot", "crop": "maize", "type": "DISEASE", "code": "corn_gray_leaf_spot", "display": "Corn Gray Leaf Spot"},
    98: {"raw": "Corn Healthy", "crop": "maize", "type": "HEALTHY", "code": "corn_healthy", "display": "Corn Healthy Leaf"},
    # CRITICAL: EXPLICIT PEST OBSERVATION TYPE!
    99: {"raw": "Corn Insects Damages", "crop": "maize", "type": "PEST", "code": "corn_insects_damages", "display": "Corn Insect Damage (Fall Armyworm / Borer)"},
    100: {"raw": "Corn Mildew", "crop": "maize", "type": "DISEASE", "code": "corn_mildew", "display": "Corn Downy Mildew"},
    101: {"raw": "Corn Purple Discoloration", "crop": "maize", "type": "DISEASE", "code": "corn_purple_discoloration", "display": "Corn Phosphorus Stress / Discoloration"},
    102: {"raw": "Corn Smut", "crop": "maize", "type": "DISEASE", "code": "corn_smut", "display": "Corn Common Smut"},
    103: {"raw": "Corn Streak", "crop": "maize", "type": "DISEASE", "code": "corn_streak_virus", "display": "Corn Streak Virus"},
    104: {"raw": "Corn Stripe", "crop": "maize", "type": "DISEASE", "code": "corn_stripe_virus", "display": "Corn Stripe Virus"},
    105: {"raw": "Corn Violet Decoloration", "crop": "maize", "type": "DISEASE", "code": "corn_violet_decoloration", "display": "Corn Violet Discoloration"},
    106: {"raw": "Corn Yellow Spots", "crop": "maize", "type": "DISEASE", "code": "corn_yellow_spots", "display": "Corn Yellow Spots"},
    107: {"raw": "Corn Yellowing", "crop": "maize", "type": "DISEASE", "code": "corn_yellowing", "display": "Corn Nitrogen Stress / Yellowing"},
    108: {"raw": "Corn leaf blight", "crop": "maize", "type": "DISEASE", "code": "corn_leaf_blight", "display": "Corn Leaf Blight"},
    109: {"raw": "Corn rust leaf", "crop": "maize", "type": "DISEASE", "code": "corn_rust", "display": "Corn Rust"},
    110: {"raw": "Tomato Brown Spots", "crop": "tomato", "type": "DISEASE", "code": "tomato_brown_spots", "display": "Tomato Brown Leaf Spots"},
    111: {"raw": "Tomato bacterial wilt", "crop": "tomato", "type": "DISEASE", "code": "tomato_bacterial_wilt", "display": "Tomato Bacterial Wilt"},
    112: {"raw": "Tomato blight leaf", "crop": "tomato", "type": "DISEASE", "code": "tomato_blight_leaf", "display": "Tomato Leaf Blight"},
    113: {"raw": "Tomato healthy", "crop": "tomato", "type": "HEALTHY", "code": "tomato_healthy", "display": "Tomato Healthy Leaf"},
    114: {"raw": "Tomato leaf mosaic virus", "crop": "tomato", "type": "DISEASE", "code": "tomato_mosaic_virus", "display": "Tomato Mosaic Virus"},
    115: {"raw": "Tomato leaf yellow virus", "crop": "tomato", "type": "DISEASE", "code": "tomato_yellow_leaf_curl_virus", "display": "Tomato Yellow Leaf Curl"}
}


# ==============================================================================
# 5. INTEGRATED PEST MANAGEMENT (IPM) CURATED KNOWLEDGE BASE
# ==============================================================================

IPM_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    # ------------------ MAIZE / CORN ------------------
    "corn_rust": {
        "condition_name": "Corn Common Rust (Puccinia sorghi)",
        "marathi_name": "Corn Common Rust (Puccinia sorghi)",
        "hindi_name": "Corn Common Rust (Puccinia sorghi)",
        "type": "DISEASE",
        "crop": "maize",
        "immediate_action": "Isolate heavily rusted plants. Avoid overhead sprinkler irrigation which splashes fungal spores.",
        "monitoring": "Inspect lower leaves twice weekly for circular to elongate reddish-brown pustules on both leaf surfaces.",
        "cultural": "Maintain optimum plant spacing (60 x 20 cm) for air circulation; destroy crop residues post-harvest.",
        "mechanical": "Handpick and burn early infected leaves in small holdings before widespread pustule rupture.",
        "biological": "Apply bio-control agent Trichoderma harzianum or Bacillus subtilis @ 5g/L water at early symptom appearance.",
        "chemical": "If pustule coverage exceeds 10% on ear leaves, apply university-recommended contact or systemic fungicide (e.g. Mancozeb 75 WP @ 2.5g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L). Always strictly follow label instructions and pre-harvest intervals.",
        "safety": "Wear PPE during spraying. Do not spray during windy conditions. Check CIBRC registration before purchase.",
        "referral_threshold": "Pustules rapidly advancing to upper canopy prior to silking stage.",
        "follow_up_days": 5
    },
    "corn_insects_damages": {
        "condition_name": "Corn Insect Damage (Fall Armyworm - Spodoptera frugiperda)",
        "marathi_name": "Corn Insect Damage (Fall Armyworm - Spodoptera frugiperda)",
        "hindi_name": "Corn Insect Damage (Fall Armyworm - Spodoptera frugiperda)",
        "type": "PEST",
        "crop": "maize",
        "immediate_action": "Check the central whorl of plants for sawdust-like frass and leaf pinholes.",
        "monitoring": "Scout 20 consecutive plants across 5 spots per acre. Install FAW pheromone traps @ 5 per acre.",
        "cultural": "Deep summer plowing to expose pupae to predatory birds; intercrop with cowpea or pigeon pea.",
        "mechanical": "Hand collection and destruction of egg masses and young larvae; apply dry sand/sawdust mixed with lime into whorls.",
        "biological": "Release egg parasitoids Trichogramma pretiosum @ 50,000/acre; spray Bacillus thuringiensis (Bt) kurstaki @ 2g/L or Metarhizium rileyi @ 5g/L.",
        "chemical": "If whorl damage exceeds 10% in vegetative or 5% in late whorl, spray authorized green-label insecticides (e.g. Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L) directly into whorls. Comply with Maharashtra Agriculture Dept advisories.",
        "safety": "Direct nozzle into whorl. Avoid contamination of water bodies. Wear gloves and mask.",
        "referral_threshold": "Extensive whorl destruction in >20% plants or infestation at tassel emergence.",
        "follow_up_days": 4
    },
    "corn_northern_leaf_blight": {
        "condition_name": "Corn Northern Leaf Blight (Exserohilum turcicum)",
        "marathi_name": "Corn Northern Leaf Blight (Exserohilum turcicum)",
        "hindi_name": "Corn Northern Leaf Blight (Exserohilum turcicum)",
        "type": "DISEASE",
        "crop": "maize",
        "immediate_action": "Remove infected lower leaves to curb upward spore migration.",
        "monitoring": "Scout for long, elliptical, grayish-green to tan cigar-shaped lesions (2.5 to 15 cm long).",
        "cultural": "Rotate with non-host legume crops (soybean/chickpea); avoid excessive nitrogen fertilization.",
        "mechanical": "Plow down corn residue to speed decomposition.",
        "biological": "Seed treatment with Trichoderma viride @ 4g/kg seed; foliar spray of Pseudomonas fluorescens @ 5g/L.",
        "chemical": "Apply Mancozeb 75 WP @ 2.5g/L or Propiconazole 25 EC @ 1 ml/L at first sign of lesions on lower leaves.",
        "safety": "Adhere strictly to waiting periods before harvesting fodder or green cobs.",
        "referral_threshold": "Lesions merging and blighting more than 30% of leaf area before grain fill.",
        "follow_up_days": 6
    },

    # ------------------ TOMATO ------------------
    "tomato_early_blight": {
        "condition_name": "Tomato Early Blight (Alternaria solani)",
        "marathi_name": "Tomato Early Blight (Alternaria solani)",
        "hindi_name": "Tomato Early Blight (Alternaria solani)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "Prune and dispose of lowest foliage touching wet soil; mulch around base with clean straw.",
        "monitoring": "Look for concentric brown rings ('target board' effect) surrounded by yellow chlorotic halo on older leaves.",
        "cultural": "Stake plants for better ventilation; water at root zone via drip, never wetting leaves.",
        "mechanical": "Remove diseased leaves promptly using sanitized shears.",
        "biological": "Foliar application of Trichoderma harzianum @ 5g/L or Ampelomyces quisqualis.",
        "chemical": "Spray Chlorothalonil 75 WP @ 2g/L or Mancozeb 75 WP @ 2.5g/L protectively, or Azoxystrobin 23% SC @ 1 ml/L if already established.",
        "safety": "Never spray before rain. Observe 3 to 5-day pre-harvest intervals.",
        "referral_threshold": "Lesions spreading to stems, petioles, or causing collar rot.",
        "follow_up_days": 5
    },
    "tomato_late_blight": {
        "condition_name": "Tomato Late Blight (Phytophthora infestans)",
        "marathi_name": "Tomato Late Blight (Phytophthora infestans)",
        "hindi_name": "Tomato Late Blight (Phytophthora infestans)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "CRITICAL EMERGENCY: Immediately halt sprinkler irrigation. Destroy infected plants if outbreak is isolated.",
        "monitoring": "Check daily during cloudy, cool (18-22°C), high humidity (>90%) weather for water-soaked greasy lesions with white fungal down on underside.",
        "cultural": "Ensure rapid drainage; destroy all cull piles and infected fruits.",
        "mechanical": "Roguing of diseased plants in sealed plastic bags to prevent airborne spore dispersal.",
        "biological": "Prophylactic bio-spray with Bacillus subtilis @ 5g/L.",
        "chemical": "Apply systemic Cymoxanil 8% + Mancozeb 64% WP @ 2.5g/L or Dimethomorph 50% WP @ 1g/L immediately upon first suspicion.",
        "safety": "Wear respiratory mask and goggles. Rotate chemical mode of action (FRAC codes) to prevent resistance.",
        "referral_threshold": "Rapid water-soaking spreading to green fruits and stems within 24-48 hours.",
        "follow_up_days": 3
    },
    "tomato_bacterial_wilt": {
        "condition_name": "Tomato Bacterial Wilt (Ralstonia solanacearum)",
        "marathi_name": "Tomato Bacterial Wilt (Ralstonia solanacearum)",
        "hindi_name": "Tomato Bacterial Wilt (Ralstonia solanacearum)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "Uproot wilted plants along with surrounding root soil; place in pit with lime powder.",
        "monitoring": "Look for sudden daytime wilting while foliage remains green, recovering slightly at night initially.",
        "cultural": "Adopt 3-year crop rotation with non-solanaceous crops (maize, sorghum); raise pH with agricultural lime.",
        "mechanical": "Clean farm tools between fields using 10% bleach solution.",
        "biological": "Root dip with Pseudomonas fluorescens @ 10g/L prior to transplanting; soil drench with Trichoderma viride.",
        "chemical": "Drench soil around neighboring healthy plants with Copper Oxychloride 50 WP @ 3g/L + Streptocycline @ 0.1g/L.",
        "safety": "Do not flood-irrigate an infected plot as water rapidly spreads bacterium to all healthy beds.",
        "referral_threshold": "More than 5% plants wilting simultaneously across bed lines.",
        "follow_up_days": 4
    },

    # ------------------ GRAPE ------------------
    "grape_downy_mildew": {
        "condition_name": "Grape Downy Mildew (Plasmopara viticola)",
        "marathi_name": "Grape Downy Mildew (Plasmopara viticola)",
        "hindi_name": "Grape Downy Mildew (Plasmopara viticola)",
        "type": "DISEASE",
        "crop": "grape",
        "immediate_action": "Aerate canopy by selective shoot positioning and leaf thinning around grape bunches.",
        "monitoring": "Inspect upper leaf surfaces for yellowish translucent 'oil spots' and corresponding white downy fungal growth below.",
        "cultural": "Keep vineyard floor free of weeds; maintain efficient drainage to reduce micro-climate humidity.",
        "mechanical": "Prune out water sprouts and suckers near soil line.",
        "biological": "Spray Ampelomyces or Trichoderma formulations during low-pressure windows.",
        "chemical": "Apply Bordeaux mixture (1%) or Copper Hydroxide 53.8% DF @ 1.5g/L preventively. Under active infection post-rain, apply Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L or Mandipropamid 23.4% SC @ 0.8 ml/L.",
        "safety": "Follow strict export residue compliance (MRL standards issued by NRC Grapes, Pune).",
        "referral_threshold": "Infection appearing on young inflorescences, bunch rachis, or berry stems.",
        "follow_up_days": 4
    },

    # ------------------ RICE ------------------
    "rice_blast": {
        "condition_name": "Rice Blast (Magnaporthe oryzae)",
        "marathi_name": "Rice Blast (Magnaporthe oryzae)",
        "hindi_name": "Rice Blast (Magnaporthe oryzae)",
        "type": "DISEASE",
        "crop": "rice",
        "immediate_action": "Drain excess water temporarily and suspend top-dressing of urea / nitrogen fertilizer.",
        "monitoring": "Check for spindle or diamond-shaped lesions with gray/whitish centers and dark reddish-brown borders.",
        "cultural": "Split nitrogen application into 3-4 doses; avoid planting overly dense seedling stands.",
        "mechanical": "Remove collateral weed hosts on bunds (e.g. Echinochloa grass).",
        "biological": "Seed treatment with Pseudomonas fluorescens @ 10g/kg; foliar spray @ 5g/L at boot leaf stage.",
        "chemical": "Spray Tricyclazole 75 WP @ 0.6g/L or Isoprothiolane 40 EC @ 1.5 ml/L at first appearance of leaf blast or early heading.",
        "safety": "Calibrate spray equipment carefully. Keep water drained for 24 hours post-spraying.",
        "referral_threshold": "Neck blast or nodal blast lesions emerging around panicle base.",
        "follow_up_days": 6
    },
    "rice_sheath_blight": {
        "condition_name": "Rice Sheath Blight (Rhizoctonia solani)",
        "marathi_name": "Rice Sheath Blight (Rhizoctonia solani)",
        "hindi_name": "Rice Sheath Blight (Rhizoctonia solani)",
        "type": "DISEASE",
        "crop": "rice",
        "immediate_action": "Reduce standing water level to 2-3 cm; avoid high nitrogen levels.",
        "monitoring": "Examine leaf sheaths just above waterline for greenish-grey oval water-soaked lesions with irregular brown borders.",
        "cultural": "Deep plowing before sowing to bury sclerotia; optimum plant spacing.",
        "mechanical": "Skim off floating sclerotia from standing water during puddling.",
        "biological": "Soil application of Trichoderma viride enriched FYM @ 20 kg/acre.",
        "chemical": "Spray Hexaconazole 5 EC @ 2 ml/L or Validamycin 3L @ 2.5 ml/L directed toward base of hills.",
        "safety": "Spray nozzle must be aimed at the lower canopy/sheaths, not top leaves.",
        "referral_threshold": "Lesions ascending to flag leaf sheath in >15% of hills.",
        "follow_up_days": 6
    },

    # ------------------ SOYBEAN (EXPERT ASSISTED / CALIBRATED) ------------------
    "soybean_rust": {
        "condition_name": "Soybean Asian Rust (Phakopsora pachyrhizi)",
        "marathi_name": "Soybean Asian Rust (Phakopsora pachyrhizi)",
        "hindi_name": "Soybean Asian Rust (Phakopsora pachyrhizi)",
        "type": "DISEASE",
        "crop": "soybean",
        "immediate_action": "Notify local Taluka Agriculture Officer or KVK immediately upon suspicion.",
        "monitoring": "Use a 10x hand lens to inspect underside of lower leaves for tiny volcano-like pustules (uredinia).",
        "cultural": "Avoid delayed sowing; choose tolerant cultivars recommended by MPKV Rahuri / VNMKV Parbhani.",
        "mechanical": "Eradicate alternate legume hosts on field boundaries.",
        "biological": "Prophylactic application of bio-fungicide formulations.",
        "chemical": "Upon official community alert or initial localized finding, spray Hexaconazole 5 EC @ 1 ml/L or Propiconazole 25 EC @ 1 ml/L.",
        "safety": "Ensure full canopy coverage. Never harvest green forage for livestock within 21 days of spraying.",
        "referral_threshold": "Any verified pustule appearance prior to pod-filling stage.",
        "follow_up_days": 4
    },

    # ------------------ CITRUS ------------------
    "citrus_canker": {
        "condition_name": "Citrus Canker (Xanthomonas axonopodis pv. citri)",
        "marathi_name": "Citrus Canker (Xanthomonas axonopodis pv. citri)",
        "hindi_name": "Citrus Canker (Xanthomonas axonopodis pv. citri)",
        "type": "DISEASE",
        "crop": "citrus",
        "immediate_action": "Prune severely infected twigs during dry weather; burn immediately.",
        "monitoring": "Look for raised, corky, crater-like lesions with oily or chlorotic yellow halos on leaves and fruits.",
        "cultural": "Plant windbreaks (Casuarina / Sesbania) to reduce leaf rubbing and wind-driven rain splashes.",
        "mechanical": "Disinfect pruning tools with 1% potassium permanganate.",
        "biological": "Spray neem seed kernel extract (NSKE 5%) to control leaf miners whose tunnels allow bacterial entry.",
        "chemical": "Prune infected twigs then spray Copper Oxychloride 50 WP @ 3g/L + Streptocycline @ 0.1g/L at flush emergence.",
        "safety": "Avoid spraying during rainfall. Wear safety gear.",
        "referral_threshold": "Lesions spreading across young developing fruit skin causing premature fruit drop.",
        "follow_up_days": 7
    },
    "citrus_greening_disease": {
        "condition_name": "Citrus Greening / Huanglongbing (Candidatus Liberibacter)",
        "marathi_name": "Citrus Greening / Huanglongbing (Candidatus Liberibacter)",
        "hindi_name": "Citrus Greening / Huanglongbing (Candidatus Liberibacter)",
        "type": "DISEASE",
        "crop": "citrus",
        "immediate_action": "Strictly withhold heavy chemical sprays. Control vector (Asian Citrus Psylla) and apply micronutrient foliar spray.",
        "monitoring": "Examine new flush for blotchy mottle (asymmetrical yellowing across veins) and upright chlorotic leaves.",
        "cultural": "Remove severely declining, unproductive trees to eliminate pathogen reservoir in the orchard.",
        "mechanical": "Install yellow sticky traps @ 10/acre to monitor citrus psylla population.",
        "biological": "Conserve predatory lacewings (Chrysoperla) and syrphid fly larvae feeding on psylla nymphs.",
        "chemical": "Spray Imidacloprid 17.8% SL @ 0.5 ml/L or Thiamethoxam 25 WG @ 0.3g/L during new flush emergence to control psyllids. Spray Zinc Sulphate (0.5%) + Ferrous Sulphate (0.2%) + Urea (1%) to alleviate chlorosis.",
        "safety": "Never spray synthetic insecticides during honeybee foraging hours (morning flowering window).",
        "referral_threshold": "Premature lopsided fruit dropping with dark aborted seeds.",
        "follow_up_days": 7
    },

    # ------------------ COTTON ------------------
    "cotton_bacterial_blight": {
        "condition_name": "Cotton Bacterial Blight / Black Arm (Xanthomonas citri pv. malvacearum)",
        "marathi_name": "Cotton Bacterial Blight / Black Arm (Xanthomonas citri pv. malvacearum)",
        "hindi_name": "Cotton Bacterial Blight / Black Arm (Xanthomonas citri pv. malvacearum)",
        "type": "DISEASE",
        "crop": "cotton",
        "immediate_action": "Avoid overhead sprinkler irrigation to stop water-splash spread.",
        "monitoring": "Check lower leaves for angular water-soaked lesions bounded by veinlets.",
        "cultural": "Destroy infected crop residues after harvest; practice crop rotation with sorghum or maize.",
        "mechanical": "Remove lower infected leaves showing severe black arm lesions.",
        "biological": "Seed dressing with Pseudomonas fluorescens @ 10g/kg seed.",
        "chemical": "Spray Copper Oxychloride 50 WP @ 2.5g/L + Streptocycline @ 0.1g/L at first appearance of angular spots.",
        "safety": "Do not mix bactericide with acidic organophosphate insecticides.",
        "referral_threshold": "Lesions girdling the main stem (black arm phase).",
        "follow_up_days": 5
    },
    "cotton_pink_bollworm": {
        "condition_name": "Cotton Pink Bollworm (Pectinophora gossypiella)",
        "marathi_name": "Cotton Pink Bollworm (Pectinophora gossypiella)",
        "hindi_name": "Cotton Pink Bollworm (Pectinophora gossypiella)",
        "type": "PEST",
        "crop": "cotton",
        "immediate_action": "Install pheromone traps and inspect rosette flowers immediately.",
        "monitoring": "Check 20 green bolls per acre for entry/exit holes and pinkish larvae inside.",
        "cultural": "Avoid extending the cotton crop beyond 150-160 days to break pest life cycle.",
        "mechanical": "Collect and destroy rosette flowers and dropped bolls in kerosene-mixed water.",
        "biological": "Release Trichogramma bactrae egg parasitoids @ 60,000/acre at weekly intervals.",
        "chemical": "If trap catch exceeds 8 moths/trap/night for 3 days, spray Chlorpyrifos 20 EC @ 2 ml/L or Profenofos 50 EC @ 2 ml/L.",
        "safety": "Follow CIBRC approved schedules. Never use banned Monocrotophos.",
        "referral_threshold": "More than 10% green bolls damaged at flowering/boll stage.",
        "follow_up_days": 4
    },

    # ------------------ TUR / PIGEONPEA ------------------
    "tur_sterility_mosaic": {
        "condition_name": "Pigeonpea Sterility Mosaic Disease (SMD)",
        "marathi_name": "Pigeonpea Sterility Mosaic Disease (SMD)",
        "hindi_name": "Pigeonpea Sterility Mosaic Disease (SMD)",
        "type": "DISEASE",
        "crop": "tur",
        "immediate_action": "Rogue out infected stunted plants in early vegetative stage to prevent vector spread.",
        "monitoring": "Check for excessive vegetative bushy branching, small leaves with light green mosaic, and lack of flowering.",
        "cultural": "Grow SMD-resistant varieties (e.g. BSMR 736, BDN 711) recommended by MPKV/VNMKV.",
        "mechanical": "Uproot and bury isolated infected plants.",
        "biological": "Conserve predatory phytoseiid mites.",
        "chemical": "Spray Fenazaquin 10 EC @ 1.5 ml/L or Propargite 57 EC @ 2.5 ml/L to control the vector eriophyid mite (Aceria cajani).",
        "safety": "Acaricide spray must cover the underside of leaves where mites congregate.",
        "referral_threshold": "Mosaic spreading along prevailing wind direction across >5% of plot.",
        "follow_up_days": 5
    },

    # ------------------ ONION ------------------
    "onion_purple_blotch": {
        "condition_name": "Onion Purple Blotch (Alternaria porri)",
        "marathi_name": "Onion Purple Blotch (Alternaria porri)",
        "hindi_name": "Onion Purple Blotch (Alternaria porri)",
        "type": "DISEASE",
        "crop": "onion",
        "immediate_action": "Ensure field drainage and avoid late-evening sprinkler irrigation.",
        "monitoring": "Look for small water-soaked lesions that enlarge into sunken purple spots with concentric rings.",
        "cultural": "Follow 2-3 year crop rotation; avoid excessive nitrogen fertilization.",
        "mechanical": "Remove and burn severely blighted leaves.",
        "biological": "Seed and seedling dip with Trichoderma viride @ 5g/L.",
        "chemical": "Spray Mancozeb 75 WP @ 2.5g/L or Tebuconazole 25.9 EC @ 1 ml/L with sticker/spreader.",
        "safety": "Always use non-ionic sticker (surfactant) because onion leaves are waxy.",
        "referral_threshold": "Lesions girdling the seed stalk causing seed-head snapping.",
        "follow_up_days": 6
    },

    # ------------------ GRAM / CHICKPEA ------------------
    "gram_fusarium_wilt": {
        "condition_name": "Chickpea Fusarium Wilt (Fusarium oxysporum f. sp. ciceris)",
        "marathi_name": "Chickpea Fusarium Wilt (Fusarium oxysporum f. sp. ciceris)",
        "hindi_name": "Chickpea Fusarium Wilt (Fusarium oxysporum f. sp. ciceris)",
        "type": "DISEASE",
        "crop": "gram",
        "immediate_action": "Avoid excessive irrigation. Stop soil disturbance around wilting root zones.",
        "monitoring": "Split lower stem longitudinally to check for dark brown to black vascular discoloration in xylem.",
        "cultural": "Deep summer plowing; 3-year crop rotation with non-hosts (wheat, mustard); use resistant cultivars (Digvijay, Vijay).",
        "mechanical": "Uproot wilting plants and burn them to prevent soil-borne inoculum build-up.",
        "biological": "Seed treatment with Trichoderma viride @ 4g/kg seed.",
        "chemical": "Soil drenching around healthy adjacent plants with Carbendazim 50 WP @ 1g/L or Captan @ 2g/L.",
        "safety": "Fungicides cannot cure already wilted vascular-blocked plants; focus on protecting surrounding stand.",
        "referral_threshold": "Wilt clusters spreading rapidly along furrow irrigation paths.",
        "follow_up_days": 7
    },

    # ------------------ WHEAT ------------------
    "wheat_brown_rust": {
        "condition_name": "Wheat Brown / Leaf Rust (Puccinia triticina)",
        "marathi_name": "Wheat Brown / Leaf Rust (Puccinia triticina)",
        "hindi_name": "Wheat Brown / Leaf Rust (Puccinia triticina)",
        "type": "DISEASE",
        "crop": "wheat",
        "immediate_action": "Scout field edges and identify whether pustules are active orange-brown powder.",
        "monitoring": "Examine upper leaf surface for randomly scattered round orange-brown pustules.",
        "cultural": "Timely sowing (November 1-15 in Maharashtra); use rust-resistant cultivars (Phule Samadhan, Netravati).",
        "mechanical": "Eradicate wild grasses and self-sown wheat seedlings.",
        "biological": "Conserve hyperparasitic fungus Darluca filum on rust pustules.",
        "chemical": "Spray Propiconazole 25 EC @ 1 ml/L or Tebuconazole 25.9 EC @ 1 ml/L at first sign of rust.",
        "safety": "Ensure uniform coverage of flag leaves which contribute 70% to grain filling.",
        "referral_threshold": "Rust appearing on flag leaf prior to flowering stage.",
        "follow_up_days": 5
    },

    # ------------------ POTATO ------------------
    "potato_early_blight": {
        "condition_name": "Potato Early Blight (Alternaria solani)",
        "marathi_name": "Potato Early Blight (Alternaria solani)",
        "hindi_name": "Potato Early Blight (Alternaria solani)",
        "type": "DISEASE",
        "crop": "potato",
        "immediate_action": "Remove and destroy lower infected leaves showing concentric ring lesions.",
        "monitoring": "Inspect lower and middle canopy for dark brown circular spots with characteristic concentric rings (target-board pattern).",
        "cultural": "Practice 2-3 year crop rotation with non-solanaceous crops; maintain adequate plant nutrition especially potassium and phosphorus.",
        "mechanical": "Improve air circulation by proper plant spacing (60 x 30 cm) and hilling practices.",
        "biological": "Spray Trichoderma harzianum @ 5g/L or Bacillus subtilis formulation prophylactically.",
        "chemical": "Spray Mancozeb 75 WP @ 2.5g/L or Chlorothalonil 75 WP @ 2g/L protectively. For established infections, apply Azoxystrobin 23 SC @ 1 ml/L.",
        "safety": "Observe 7-day pre-harvest interval. Avoid spraying during high winds.",
        "referral_threshold": "Lesions rapidly spreading to tuber through soil splash.",
        "follow_up_days": 5
    },
    "potato_late_blight": {
        "condition_name": "Potato Late Blight (Phytophthora infestans)",
        "marathi_name": "Potato Late Blight (Phytophthora infestans)",
        "hindi_name": "Potato Late Blight (Phytophthora infestans)",
        "type": "DISEASE",
        "crop": "potato",
        "immediate_action": "EMERGENCY: Stop overhead irrigation immediately. Apply fungicide within 24 hours of symptom detection.",
        "monitoring": "Check for water-soaked irregular dark brown lesions on leaf tips/margins with white sporulation on underside during humid mornings.",
        "cultural": "Use certified disease-free seed tubers only. Ensure proper drainage. Hill soil around base to prevent tuber infection.",
        "mechanical": "Destroy all volunteer potato plants and cull piles. Remove haulms 10-14 days before harvest.",
        "biological": "Prophylactic spray with Bacillus subtilis @ 5g/L during favorable weather forecasts.",
        "chemical": "Apply Cymoxanil 8% + Mancozeb 64% WP @ 2.5g/L or Dimethomorph 50 WP @ 1g/L immediately. Alternate chemistry to prevent resistance.",
        "safety": "Rotate FRAC groups (systemic + contact). Wear respiratory protection. Never store blighted tubers.",
        "referral_threshold": "Rapid spread during cool (12-18°C) rainy periods with >90% humidity.",
        "follow_up_days": 3
    },

    # ------------------ GARLIC / ONION ------------------
    "garlic_leaf_blight": {
        "condition_name": "Garlic Leaf Blight (Stemphylium vesicarium)",
        "marathi_name": "Garlic Leaf Blight (Stemphylium vesicarium)",
        "hindi_name": "Garlic Leaf Blight (Stemphylium vesicarium)",
        "type": "DISEASE",
        "crop": "garlic",
        "immediate_action": "Remove severely blighted leaf tips and ensure field drainage.",
        "monitoring": "Look for small yellowish to orange flecks that enlarge into elongated, light purple lesions on leaf blades.",
        "cultural": "Avoid excessive irrigation and overhead watering. Maintain 15 x 10 cm spacing for air circulation.",
        "mechanical": "Remove crop debris after harvest; do not leave garlic stumps in field.",
        "biological": "Spray Trichoderma viride @ 5g/L as preventive at 30-45 DAS.",
        "chemical": "Spray Mancozeb 75 WP @ 2.5g/L or Tebuconazole 25.9 EC @ 1 ml/L at first symptom appearance. Repeat at 10-day intervals.",
        "safety": "Add non-ionic sticker for better adhesion on waxy garlic leaves.",
        "referral_threshold": "Blight spreading to seed stalks causing drying of inflorescence.",
        "follow_up_days": 7
    },
    "garlic_rust": {
        "condition_name": "Garlic Rust (Puccinia allii)",
        "marathi_name": "Garlic Rust (Puccinia allii)",
        "hindi_name": "Garlic Rust (Puccinia allii)",
        "type": "DISEASE",
        "crop": "garlic",
        "immediate_action": "Remove heavily infected lower leaves showing orange pustules.",
        "monitoring": "Check for small, circular to elliptical orange-red pustules (uredinia) on both leaf surfaces.",
        "cultural": "Avoid dense planting; ensure proper nutrient balance with adequate potash fertilization.",
        "mechanical": "Destroy infected plant debris and volunteer garlic/onion plants.",
        "biological": "Spray neem oil 1% or Trichoderma formulation prophylactically.",
        "chemical": "Spray Hexaconazole 5 EC @ 2 ml/L or Propiconazole 25 EC @ 1 ml/L at first appearance of rust pustules.",
        "safety": "Follow label instructions strictly. Observe pre-harvest interval of 15 days.",
        "referral_threshold": "Rust pustules covering >25% leaf area causing premature drying.",
        "follow_up_days": 6
    },

    # ------------------ BANANA ------------------
    "banana_panama_disease": {
        "condition_name": "Banana Panama Disease / Fusarium Wilt (Fusarium oxysporum f.sp. cubense)",
        "marathi_name": "Banana Panama Disease / Fusarium Wilt (Fusarium oxysporum f.sp. cubense)",
        "hindi_name": "Banana Panama Disease / Fusarium Wilt (Fusarium oxysporum f.sp. cubense)",
        "type": "DISEASE",
        "crop": "banana",
        "immediate_action": "DO NOT irrigate from water flowing through infected plots. Quarantine affected area immediately.",
        "monitoring": "Observe for yellowing of lower leaves at margins, wilting, and longitudinal splitting of pseudostem base. Cut pseudostem to check for brown/red vascular discoloration.",
        "cultural": "Use tissue-culture (TC) certified disease-free plantlets ONLY. Practice minimum 3-year rotation with paddy or sugarcane.",
        "mechanical": "Uproot entire infected plant including corm; drench pit with 2% formalin. Disinfect all tools with 10% bleach.",
        "biological": "Apply Trichoderma viride enriched FYM @ 50g/plant in planting pit. Apply Pseudomonas fluorescens @ 20g/plant as soil drench.",
        "chemical": "Drench surrounding healthy plant basins with Carbendazim 50 WP @ 2g/L. No chemical cure exists for infected plants.",
        "safety": "Panama Wilt is soil-borne and INCURABLE in infected plants. Focus entirely on prevention and containment.",
        "referral_threshold": "Any confirmed vascular discoloration requires immediate notification to District Agriculture Officer.",
        "follow_up_days": 14
    },

    # ------------------ CUCUMBER ------------------
    "cucumber_angular_spot": {
        "condition_name": "Cucumber Angular Leaf Spot (Pseudomonas syringae pv. lachrymans)",
        "marathi_name": "Cucumber Angular Leaf Spot (Pseudomonas syringae pv. lachrymans)",
        "hindi_name": "Cucumber Angular Leaf Spot (Pseudomonas syringae pv. lachrymans)",
        "type": "DISEASE",
        "crop": "cucumber",
        "immediate_action": "Avoid overhead irrigation and handling plants when foliage is wet.",
        "monitoring": "Look for water-soaked angular spots bounded by leaf veins that turn tan-brown and tear out, giving leaves a ragged appearance.",
        "cultural": "Use disease-free certified seeds. Practice 2-year crop rotation with non-cucurbit crops.",
        "mechanical": "Remove and destroy severely infected leaves; sanitize tools between plants.",
        "biological": "Spray Bacillus subtilis formulation @ 5g/L as preventive.",
        "chemical": "Spray Copper Oxychloride 50 WP @ 3g/L or Copper Hydroxide 53.8 DF @ 2g/L at first symptom. Add Streptocycline @ 0.1g/L for severe cases.",
        "safety": "Copper sprays can cause phytotoxicity on young seedlings. Test on a few plants first.",
        "referral_threshold": "Infection spreading to fruit causing water-soaked lesions on cucumbers.",
        "follow_up_days": 5
    },
    "cucumber_bacterial_wilt": {
        "condition_name": "Cucumber Bacterial Wilt (Erwinia tracheiphila)",
        "marathi_name": "Cucumber Bacterial Wilt (Erwinia tracheiphila)",
        "hindi_name": "Cucumber Bacterial Wilt (Erwinia tracheiphila)",
        "type": "DISEASE",
        "crop": "cucumber",
        "immediate_action": "Remove wilted vines immediately and destroy. Do not compost infected plant material.",
        "monitoring": "Cut stem of wilting plant; press cut ends together and pull apart slowly. Bacterial ooze will form sticky white threads.",
        "cultural": "Control striped and spotted cucumber beetles (vectors) from seedling stage. Use row covers until flowering.",
        "mechanical": "Install yellow sticky traps for cucumber beetles @ 5/50m row.",
        "biological": "Apply Beauveria bassiana formulation for beetle control; spray neem oil 1% on foliage.",
        "chemical": "Spray Imidacloprid 17.8 SL @ 0.5 ml/L or Thiamethoxam 25 WG @ 0.3g/L to control beetle vectors at seedling stage.",
        "safety": "No chemical cure for bacterial wilt itself. Focus on vector control. Avoid spraying during pollination hours.",
        "referral_threshold": "Multiple plants wilting rapidly across bed with beetle populations present.",
        "follow_up_days": 3
    },
    "cucumber_powdery_mildew": {
        "condition_name": "Cucumber Powdery Mildew (Erysiphe cichoracearum / Podosphaera xanthii)",
        "marathi_name": "Cucumber Powdery Mildew (Erysiphe cichoracearum / Podosphaera xanthii)",
        "hindi_name": "Cucumber Powdery Mildew (Erysiphe cichoracearum / Podosphaera xanthii)",
        "type": "DISEASE",
        "crop": "cucumber",
        "immediate_action": "Remove heavily infected lower leaves to reduce spore load.",
        "monitoring": "Check upper leaf surfaces for circular white powdery fungal colonies that expand and merge.",
        "cultural": "Ensure adequate plant spacing for air circulation. Avoid excess nitrogen. Grow resistant varieties.",
        "mechanical": "Prune dense canopy to improve light penetration and air flow.",
        "biological": "Spray milk solution (10%) or potassium bicarbonate @ 5g/L as organic alternative.",
        "chemical": "Spray Wettable Sulphur 80 WP @ 3g/L or Hexaconazole 5 EC @ 1 ml/L at first appearance. Alternate with Azoxystrobin 23 SC @ 1 ml/L.",
        "safety": "Do not apply sulphur when temperature exceeds 35°C to avoid phytotoxicity. Observe 5-day PHI.",
        "referral_threshold": "Mildew covering >40% of leaf area causing premature vine senescence.",
        "follow_up_days": 5
    },

    # ------------------ BEAN ------------------
    "bean_rust": {
        "condition_name": "Bean Rust (Uromyces appendiculatus)",
        "marathi_name": "Bean Rust (Uromyces appendiculatus)",
        "hindi_name": "Bean Rust (Uromyces appendiculatus)",
        "type": "DISEASE",
        "crop": "bean",
        "immediate_action": "Remove and destroy infected lower leaves showing reddish-brown pustules.",
        "monitoring": "Check underside of leaves for small, circular, reddish-brown to dark brown pustules (uredinia) surrounded by yellow halos.",
        "cultural": "Use rust-resistant bean varieties. Avoid overhead irrigation. Practice crop rotation with non-legume crops.",
        "mechanical": "Destroy infected crop residues after harvest. Remove volunteer bean plants.",
        "biological": "Spray Trichoderma viride @ 5g/L or neem oil 2% as preventive.",
        "chemical": "Spray Mancozeb 75 WP @ 2.5g/L protectively or Hexaconazole 5 EC @ 1 ml/L at first pustule appearance.",
        "safety": "Follow CIBRC guidelines. Observe 7-day pre-harvest interval for green beans.",
        "referral_threshold": "Rust pustules spreading to pods or covering >30% leaf area.",
        "follow_up_days": 5
    },
    "bean_halo_blight": {
        "condition_name": "Bean Halo Blight (Pseudomonas savastanoi pv. phaseolicola)",
        "marathi_name": "Bean Halo Blight (Pseudomonas savastanoi pv. phaseolicola)",
        "hindi_name": "Bean Halo Blight (Pseudomonas savastanoi pv. phaseolicola)",
        "type": "DISEASE",
        "crop": "bean",
        "immediate_action": "Do not work in the field when foliage is wet. Remove severely affected plants.",
        "monitoring": "Look for small, water-soaked spots surrounded by a broad, greenish-yellow (halo) zone on leaves.",
        "cultural": "Use certified disease-free seeds. Practice 2-3 year rotation with cereals. Avoid overhead irrigation.",
        "mechanical": "Rogue out infected plants and burn. Sanitize tools and equipment.",
        "biological": "Seed treatment with Pseudomonas fluorescens @ 10g/kg seed.",
        "chemical": "Spray Copper Oxychloride 50 WP @ 3g/L + Streptocycline @ 0.1g/L at first symptom.",
        "safety": "Avoid field operations during wet weather to prevent mechanical transmission.",
        "referral_threshold": "Greasy spots appearing on pods affecting seed quality.",
        "follow_up_days": 5
    },
    "bean_mosaic": {
        "condition_name": "Bean Common Mosaic Virus (BCMV)",
        "marathi_name": "Bean Common Mosaic Virus (BCMV)",
        "hindi_name": "Bean Common Mosaic Virus (BCMV)",
        "type": "DISEASE",
        "crop": "bean",
        "immediate_action": "Rogue out plants showing mosaic, leaf curling, and stunting immediately.",
        "monitoring": "Look for irregular light-green to dark-green mosaic pattern on trifoliate leaves with downward curling and puckering.",
        "cultural": "Use virus-free certified seeds and resistant varieties. Control aphid vectors from seedling stage.",
        "mechanical": "Remove and destroy infected plants in sealed bags to prevent aphid-mediated spread.",
        "biological": "Spray neem oil 2% or yellow sticky traps for aphid monitoring.",
        "chemical": "Control aphid vectors with Imidacloprid 17.8 SL @ 0.3 ml/L or Thiamethoxam 25 WG @ 0.2g/L. No cure for virus-infected plants.",
        "safety": "Viral diseases have NO chemical cure. Focus on vector control and seed health.",
        "referral_threshold": "Mosaic symptoms in >10% of plants suggesting seed-borne infection.",
        "follow_up_days": 7
    },

    # ------------------ GRAPE (Additional) ------------------
    "grape_leaf_spot": {
        "condition_name": "Grape Leaf Spot / Isariopsis Leaf Spot (Pseudocercospora vitis)",
        "marathi_name": "Grape Leaf Spot / Isariopsis Leaf Spot (Pseudocercospora vitis)",
        "hindi_name": "Grape Leaf Spot / Isariopsis Leaf Spot (Pseudocercospora vitis)",
        "type": "DISEASE",
        "crop": "grape",
        "immediate_action": "Remove and destroy lower infected leaves. Improve canopy ventilation by shoot positioning.",
        "monitoring": "Check for dark brown angular spots on upper leaf surface with corresponding velvety dark sporulation on underside.",
        "cultural": "Maintain clean vineyard floor. Avoid excessive nitrogen. Ensure proper training system for air circulation.",
        "mechanical": "Collect and burn fallen infected leaves to reduce inoculum.",
        "biological": "Spray Trichoderma formulation @ 5g/L during low-pressure period.",
        "chemical": "Spray Carbendazim 50 WP @ 1g/L or Thiophanate-methyl 70 WP @ 1g/L. Export vineyards should use NRC-Grapes approved schedule.",
        "safety": "Follow strict MRL (Maximum Residue Limit) compliance for export-grade grapes.",
        "referral_threshold": "Defoliation exceeding 25% of vine canopy.",
        "follow_up_days": 5
    },
    "grape_black_rot": {
        "condition_name": "Grape Black Rot (Guignardia bidwellii)",
        "marathi_name": "Grape Black Rot (Guignardia bidwellii)",
        "hindi_name": "Grape Black Rot (Guignardia bidwellii)",
        "type": "DISEASE",
        "crop": "grape",
        "immediate_action": "Remove mummified berries and infected shoot tips immediately.",
        "monitoring": "Look for small reddish-brown circular lesions with black pycnidia on leaves; watch for rapid berry shriveling into hard black mummies.",
        "cultural": "Prune vines well for canopy openness. Remove mummies during winter pruning. Maintain proper drainage.",
        "mechanical": "Collect and destroy all mummified berries from vine and ground to break the disease cycle.",
        "biological": "Apply Bacillus subtilis @ 5g/L during pre-bloom to veraison.",
        "chemical": "Spray Mancozeb 75 WP @ 2.5g/L or Myclobutanil 10 WP @ 0.5g/L from bud break to veraison at 10-day intervals.",
        "safety": "Critical timing: protect berries from pea-size to veraison. Follow NRC export residue norms.",
        "referral_threshold": "Berry infection exceeding 5% of the cluster count.",
        "follow_up_days": 5
    },
    "grapevine_leafroll_disease": {
        "condition_name": "Grapevine Leafroll Disease (GLRaV complex)",
        "marathi_name": "Grapevine Leafroll Disease (GLRaV complex)",
        "hindi_name": "Grapevine Leafroll Disease (GLRaV complex)",
        "type": "DISEASE",
        "crop": "grape",
        "immediate_action": "Mark and monitor affected vines. Do NOT use cuttings from infected vines for propagation.",
        "monitoring": "In red varieties: red/purple leaf rolling from margins; in green varieties: downward rolling with interveinal chlorosis. Symptoms intensify post-veraison.",
        "cultural": "Use virus-indexed certified planting material ONLY. Control mealybug vectors. Rogue severely affected vines.",
        "mechanical": "Remove mealybug colonies on trunk bark using stiff brush. Apply sticky bands on trunks.",
        "biological": "Release Cryptolaemus montrouzieri (ladybird beetle) for mealybug biocontrol.",
        "chemical": "Spray Buprofezin 25 SC @ 1.5 ml/L or Spirotetramat 150 OD @ 1 ml/L for mealybug vector control.",
        "safety": "Leafroll is a viral disease with NO chemical cure. Management is only through clean planting material and vector control.",
        "referral_threshold": "Any vine showing leafroll symptoms should be reported for vineyard-level survey.",
        "follow_up_days": 14
    },

    # ------------------ TOMATO (Additional conditions in model) ------------------
    "tomato_leaf_mold": {
        "condition_name": "Tomato Leaf Mold (Passalora fulva / Cladosporium fulvum)",
        "marathi_name": "Tomato Leaf Mold (Passalora fulva / Cladosporium fulvum)",
        "hindi_name": "Tomato Leaf Mold (Passalora fulva / Cladosporium fulvum)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "Improve ventilation in polyhouse/shade-net by opening side vents and removing dense lower foliage.",
        "monitoring": "Check upper leaf surface for pale green-yellow spots; flip leaf to see olive-green to brown velvety mold growth underneath.",
        "cultural": "Maintain relative humidity below 85% in protected cultivation. Ensure adequate plant spacing.",
        "mechanical": "Remove and destroy infected lower leaves. Avoid overhead watering.",
        "biological": "Spray Bacillus subtilis @ 5g/L or Trichoderma viride @ 5g/L preventively.",
        "chemical": "Spray Chlorothalonil 75 WP @ 2g/L or Difenoconazole 25 EC @ 0.5 ml/L at first sign of mold.",
        "safety": "Primarily a problem in protected cultivation. Increase air movement with fans.",
        "referral_threshold": "Mold covering >30% of leaf area causing premature defoliation.",
        "follow_up_days": 5
    },
    "tomato_septoria_leaf_spot": {
        "condition_name": "Tomato Septoria Leaf Spot (Septoria lycopersici)",
        "marathi_name": "Tomato Septoria Leaf Spot (Septoria lycopersici)",
        "hindi_name": "Tomato Septoria Leaf Spot (Septoria lycopersici)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "Remove infected lower leaves immediately; avoid overhead irrigation.",
        "monitoring": "Look for numerous small (2-3mm), circular spots with dark brown margins and grey-white centers with tiny black pycnidia.",
        "cultural": "Stake plants and mulch with plastic/straw to prevent soil splash. Rotate with non-solanaceous crops for 2 years.",
        "mechanical": "Prune lower 30cm of foliage to prevent soil-splash infection.",
        "biological": "Foliar spray of Bacillus amyloliquefaciens or Trichoderma harzianum @ 5g/L.",
        "chemical": "Spray Mancozeb 75 WP @ 2.5g/L or Copper Oxychloride 50 WP @ 3g/L at first appearance. Alternate with Azoxystrobin 23 SC @ 1 ml/L.",
        "safety": "This disease progresses from bottom upward; prioritize lower canopy coverage during spraying.",
        "referral_threshold": "Defoliation reaching mid-canopy during fruit development stage.",
        "follow_up_days": 5
    },
    "tomato_bacterial_leaf_spot": {
        "condition_name": "Tomato Bacterial Leaf Spot (Xanthomonas vesicatoria)",
        "marathi_name": "Tomato Bacterial Leaf Spot (Xanthomonas vesicatoria)",
        "hindi_name": "Tomato Bacterial Leaf Spot (Xanthomonas vesicatoria)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "Avoid overhead irrigation and working in wet fields. Remove heavily spotted lower leaves.",
        "monitoring": "Check for small, dark, water-soaked, angular to irregular spots that become raised and scabby on fruit.",
        "cultural": "Use hot-water treated seeds (50°C, 25 min). Rotate with non-solanaceous crops. Avoid excess nitrogen.",
        "mechanical": "Sanitize stakes, cages, and tools with 10% bleach between rows.",
        "biological": "Seed treatment with Pseudomonas fluorescens @ 10g/kg seed.",
        "chemical": "Spray Copper Hydroxide 53.8 DF @ 2g/L + Mancozeb 75 WP @ 2g/L as protectant. Add Streptocycline @ 0.1g/L for severe infection.",
        "safety": "Copper accumulation in soil can be toxic. Limit copper sprays to 4 per season.",
        "referral_threshold": "Bacterial spots appearing on green fruits causing unmarketable produce.",
        "follow_up_days": 5
    },
    "tomato_mosaic_virus": {
        "condition_name": "Tomato Mosaic Virus (ToMV)",
        "marathi_name": "Tomato Mosaic Virus (ToMV)",
        "hindi_name": "Tomato Mosaic Virus (ToMV)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "Rogue out infected plants immediately. Wash hands with milk solution before touching healthy plants.",
        "monitoring": "Look for light-dark green mosaic mottling on leaves, leaf distortion, and stunted growth. Fruits may show internal browning.",
        "cultural": "Use ToMV-resistant varieties. Soak seeds in 10% Trisodium Phosphate for 15 minutes before sowing.",
        "mechanical": "Disinfect all tools, trays, and stakes with 10% bleach. Do not smoke tobacco near tomato fields.",
        "biological": "No biological control available. Prevention through hygiene only.",
        "chemical": "NO CHEMICAL TREATMENT EXISTS for viral diseases. Focus on prevention and vector control.",
        "safety": "Extremely contagious through mechanical contact. Workers must wash hands between plants.",
        "referral_threshold": "Any confirmed mosaic symptoms in nursery stock.",
        "follow_up_days": 7
    },
    "tomato_yellow_leaf_curl_virus": {
        "condition_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "marathi_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "hindi_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "type": "DISEASE",
        "crop": "tomato",
        "immediate_action": "Rogue out infected stunted plants with upward curling yellow leaves. Control whitefly vectors aggressively.",
        "monitoring": "Check for severe upward curling of leaves, yellowing of leaf margins, stunting, and flower drop. Whitefly presence on leaf underside.",
        "cultural": "Use TYLCV-resistant hybrids. Install 40-mesh nylon net barriers around nurseries. Use reflective mulch.",
        "mechanical": "Install yellow sticky traps @ 10/acre for whitefly monitoring.",
        "biological": "Release Encarsia formosa parasitoid wasps; spray Beauveria bassiana @ 5g/L for whitefly.",
        "chemical": "Control whitefly vectors: Spiromesifen 22.9 SC @ 0.7 ml/L or Diafenthiuron 50 WP @ 1g/L. Rotate insecticide groups.",
        "safety": "TYLCV is vector-transmitted (whitefly). No chemical cure for virus. Focus entirely on vector management.",
        "referral_threshold": "TYLCV incidence >5% in commercial transplanting field.",
        "follow_up_days": 7
    },

    "healthy": {
        "condition_name": "Healthy Crop Foliage",
        "marathi_name": "निरोगी पीक पाने",
        "hindi_name": "स्वस्थ फसल पत्ती",
        "type": "HEALTHY",
        "crop": "any",
        "immediate_action": "Healthy Specimen - Optimal Vigor. No chemical or pesticide application required.",
        "monitoring": "Continue routine weekly field scouting. Monitor leaf undersides and apical growth weekly for early signs of pest incursions.",
        "cultural": "Preventative Maintenance: Maintain weed-free bunds and field borders. Practice crop rotation and maintain balanced aeration between plant rows.",
        "mechanical": "Hydration Tips: Maintain optimal root-zone soil moisture via scheduled drip irrigation. Avoid water stagnation or excessive moisture stress during vegetative and flowering stages.",
        "biological": "Balanced N-P-K Fertilizer Schedule: Apply fertilizers as per Soil Health Card recommendations. Avoid excess nitrogen which promotes succulent foliage prone to sucking pests; supplement with bio-stimulants and micronutrients.",
        "chemical": "General Crop Care: Strictly conserve beneficial natural predators (ladybird beetles, chrysoperla, spiders). Do NOT spray broad-spectrum chemical pesticides on healthy crops.",
        "safety": "Ensure adequate personal protection during routine cultural operations and maintain calibrated irrigation pressure.",
        "referral_threshold": "Scout immediately if foliar discoloration, chlorosis, or pest threshold exceeds 5%.",
        "follow_up_days": 10
    },
    "unknown_condition": {
        "condition_name": "Unidentified / Complex Symptoms (Expert Review Required)",
        "marathi_name": "Unidentified / Complex Symptoms (Expert Review Required)",
        "hindi_name": "Unidentified / Complex Symptoms (Expert Review Required)",
        "type": "UNKNOWN",
        "crop": "any",
        "immediate_action": "DO NOT APPLY PESTICIDES OR CHEMICAL CONCOCTIONS. Take clear photographs of upper and lower leaf surfaces, stem, and whole plant.",
        "monitoring": "Observe whether symptoms are localized to a single plant or widespread along irrigation channels.",
        "cultural": "Note down recent fertilization, pesticide sprays, irrigation dates, and weather anomalies.",
        "mechanical": "Tag the affected plant with a flag for field officer inspection.",
        "biological": "Collect suspected specimen in clean, dry paper envelope for laboratory inspection.",
        "chemical": "Strictly withhold pesticide spraying until agricultural university / KVK expert provides prescription.",
        "safety": "Misidentified spraying risks severe crop phytotoxicity and financial loss.",
        "referral_threshold": "Immediate escalation to Agricultural Officer / Krishi Vigyan Kendra.",
        "follow_up_days": 3
    }
}


def get_crop_config(crop_code: str) -> Optional[Dict[str, Any]]:
    return CROPS.get(crop_code.lower())


def get_district_info(district_name: str) -> Dict[str, Any]:
    return MAHARASHTRA_DISTRICTS.get(district_name, {
        "lat": DEFAULT_COORDINATES["lat"],
        "lon": DEFAULT_COORDINATES["lon"],
        "agro_zone": "Maharashtra General",
        "talukas": []
    })


def get_ipm_advisory(condition_code: str, observation_type: str = "DISEASE") -> Dict[str, Any]:
    if observation_type == "HEALTHY":
        return IPM_KNOWLEDGE_BASE["healthy"]
    if condition_code in IPM_KNOWLEDGE_BASE:
        return IPM_KNOWLEDGE_BASE[condition_code]
    return IPM_KNOWLEDGE_BASE["unknown_condition"]
