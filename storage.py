"""
Database Storage and Relational Schema Management for FALCON-AI / SIH26131
Supports Users (RBAC), Farms, Cases, Expert Reviews, and Field Confirmations.
"""

import sqlite3
import hashlib
import secrets
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

DATABASE_PATH = Path(__file__).resolve().parent / "falcon_ai.db"


def _connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return key.hex(), salt


def verify_password(password: str, salt: str, password_hash: str) -> bool:
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return key.hex() == password_hash


def initialize_database():
    with _connect() as conn:
        conn.execute("PRAGMA journal_mode = WAL")
        # Legacy table kept for backwards compatibility
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                disease_name TEXT NOT NULL,
                confidence REAL NOT NULL,
                damage_percent REAL NOT NULL,
                action TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_diagnoses_phone_created ON diagnoses(phone, created_at DESC)"
        )

        # 1. Users Table (Farmers, Experts, Officers)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('FARMER', 'EXPERT', 'ADMIN')),
                preferred_language TEXT NOT NULL DEFAULT 'en',
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                organization TEXT,
                designation TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")

        # 2. Farms Table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS farms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                farm_name TEXT NOT NULL,
                state TEXT NOT NULL DEFAULT 'Maharashtra',
                district TEXT NOT NULL,
                taluka TEXT NOT NULL,
                village TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                area_acres REAL DEFAULT 2.5,
                primary_crop TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_farms_user ON farms(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_farms_district ON farms(district)")

        # 3. Cases Table (Central Observation Entity)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_number TEXT UNIQUE NOT NULL,
                farmer_id INTEGER NOT NULL REFERENCES users(id),
                farm_id INTEGER REFERENCES farms(id),
                crop_code TEXT NOT NULL,
                season TEXT NOT NULL CHECK(season IN ('KHARIF', 'RABI', 'SUMMER', 'ANNUAL')),
                growth_stage TEXT NOT NULL,
                state TEXT NOT NULL DEFAULT 'Maharashtra',
                district TEXT NOT NULL,
                taluka TEXT NOT NULL,
                village TEXT,
                latitude REAL,
                longitude REAL,
                image_path TEXT NOT NULL,
                overlay_path TEXT,
                image_quality_status TEXT NOT NULL DEFAULT 'VALID',
                ai_status TEXT NOT NULL CHECK(ai_status IN ('IDENTIFIED', 'HEALTHY', 'UNCERTAIN', 'UNKNOWN', 'IMAGE_QUALITY_ISSUE')),
                ai_raw_prediction TEXT,
                ai_condition_code TEXT,
                ai_observation_type TEXT CHECK(ai_observation_type IN ('DISEASE', 'PEST', 'HEALTHY', 'UNKNOWN')),
                ai_confidence REAL NOT NULL DEFAULT 0.0,
                leaf_area_percent REAL DEFAULT 0.0,
                damage_percent REAL DEFAULT 0.0,
                severity_level TEXT NOT NULL CHECK(severity_level IN ('NONE', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL', 'NOT_ASSESSED')),
                weather_snapshot_json TEXT,
                risk_level TEXT NOT NULL CHECK(risk_level IN ('LOW', 'MODERATE', 'HIGH', 'CRITICAL')),
                risk_score INTEGER NOT NULL DEFAULT 0,
                risk_factors_json TEXT,
                advisory_json TEXT,
                requires_expert INTEGER NOT NULL DEFAULT 0,
                case_status TEXT NOT NULL DEFAULT 'SUBMITTED' CHECK(case_status IN (
                    'SUBMITTED', 'AI_CONFIDENT', 'AI_UNCERTAIN', 'PENDING_EXPERT',
                    'UNDER_EXPERT_REVIEW', 'VERIFIED', 'LAB_REFERRAL', 'FOLLOW_UP_REQUIRED', 'CLOSED'
                )),
                final_diagnosis_code TEXT,
                final_condition_name TEXT,
                final_observation_type TEXT,
                final_verified_by INTEGER REFERENCES users(id),
                parent_case_id INTEGER REFERENCES cases(id),
                follow_up_outcome TEXT CHECK(follow_up_outcome IN ('IMPROVED', 'UNCHANGED', 'WORSENED', 'RESOLVED', 'UNKNOWN', NULL)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cases_farmer ON cases(farmer_id, created_at DESC)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cases_district ON cases(district, created_at DESC)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(case_status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cases_risk ON cases(risk_level)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cases_parent ON cases(parent_case_id)")

        # 4. Expert Reviews Table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expert_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
                expert_id INTEGER NOT NULL REFERENCES users(id),
                review_action TEXT NOT NULL CHECK(review_action IN (
                    'CONFIRM', 'CORRECT', 'SELECT_DISEASE', 'SELECT_PEST', 'MARK_UNKNOWN', 'LAB_REFERRAL', 'REQUEST_IMAGE'
                )),
                diagnosis_code TEXT,
                condition_name TEXT,
                observation_type TEXT,
                expert_confidence REAL,
                expert_severity TEXT,
                expert_notes TEXT,
                custom_advisory TEXT,
                follow_up_instructions TEXT,
                reviewed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_reviews_case ON expert_reviews(case_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_reviews_expert ON expert_reviews(expert_id)")

        # 5. Field Confirmations Table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS field_confirmations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
                confirmed_by INTEGER NOT NULL REFERENCES users(id),
                actual_condition_code TEXT NOT NULL,
                actual_condition_name TEXT,
                outcome TEXT NOT NULL CHECK(outcome IN ('IMPROVED', 'UNCHANGED', 'WORSENED', 'RESOLVED', 'UNKNOWN')),
                confirmation_notes TEXT,
                confirmed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # 6. User Activity Logs Table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                activity_type TEXT NOT NULL CHECK(activity_type IN ('LOGIN', 'SEARCH', 'DIAGNOSIS', 'VOICE_QUERY', 'LANGUAGE_CHANGE', 'VIEW_ADVISORY', 'LOGOUT')),
                query_text TEXT,
                metadata_json TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_user ON user_activity_logs(user_id, created_at DESC)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_type ON user_activity_logs(activity_type)")

        # 7. Plant expert registry for direct advisory escalation and WhatsApp contact sharing
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agronomy_experts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                institution TEXT NOT NULL,
                district TEXT NOT NULL,
                phone TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                expertise TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_agronomy_experts_district ON agronomy_experts(district)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_agronomy_experts_active ON agronomy_experts(active)")

        # Seed initial demo users if none exist
        _seed_demo_data(conn)
        _seed_predefined_staff_accounts(conn)
        _seed_expert_contacts(conn)


def _seed_expert_contacts(conn):
    existing = conn.execute("SELECT COUNT(*) FROM agronomy_experts").fetchone()[0]
    if existing > 0:
        return

    seed = [
        ("Dr. Sachin Patil", "Plant Pathologist", "MPKV Rahuri", "Ahmednagar", "+91 94230 11220", "+919423011220", "Cereal disease diagnosis, fungal leaf blights, seed health"),
        ("Dr. Vaishali Shinde", "Entomologist", "College of Agriculture, Pune", "Pune", "+91 98812 33441", "+919881233441", "Insect pest surveillance, armyworm, bollworm, pheromone monitoring"),
        ("Dr. Ashok Pawar", "Agronomy Advisor", "KVK Nashik", "Nashik", "+91 95035 66010", "+919503566010", "Integrated nutrient and disease management, crop scouting"),
        ("Dr. Meena Deshmukh", "Soil & Disease Expert", "Agricultural Research Station, Kolhapur", "Kolhapur", "+91 97654 30077", "+919765430077", "Soil-borne disease diagnosis, blast and wilt management"),
        ("Dr. Rajendra Kulkarni", "Field Crop Specialist", "Maharashtra State Agri Department", "Nanded", "+91 98221 57920", "+919822157920", "Regional outbreak tracking, pest risk alerts, field advisories")
    ]
    conn.executemany(
        """
        INSERT INTO agronomy_experts (name, role, institution, district, phone, whatsapp, expertise)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        seed
    )


AUTHORIZED_EXPERTS = [
    {"phone": "9000000001", "email": "expert1@falconai.demo", "name": "Dr. Anjali Deshmukh", "designation": "Plant Pathology", "organization": "Maharashtra Agricultural Expert Registry"},
    {"phone": "9000000002", "email": "expert2@falconai.demo", "name": "Dr. Vivek Kulkarni", "designation": "Entomology and Pest Management", "organization": "Maharashtra Agricultural Expert Registry"},
    {"phone": "9000000003", "email": "expert3@falconai.demo", "name": "Dr. Neha Patil", "designation": "Agronomy and Crop Management", "organization": "Maharashtra Agricultural Expert Registry"},
    {"phone": "9000000004", "email": "expert4@falconai.demo", "name": "Dr. Rahul Shinde", "designation": "Horticulture", "organization": "Maharashtra Agricultural Expert Registry"},
    {"phone": "9000000005", "email": "expert5@falconai.demo", "name": "Dr. Priya Jadhav", "designation": "Soil Science", "organization": "Maharashtra Agricultural Expert Registry"},
]

AUTHORIZED_OFFICERS = [
    {"phone": "9100000001", "email": "officer1@falconai.demo", "name": "Kavita Pawar", "designation": "District Agriculture Officer", "organization": "Department of Agriculture, Maharashtra State"},
    {"phone": "9100000002", "email": "officer2@falconai.demo", "name": "Mahesh Gaikwad", "designation": "Crop Protection and Surveillance", "organization": "Department of Agriculture, Maharashtra State"},
    {"phone": "9100000003", "email": "officer3@falconai.demo", "name": "Sneha More", "designation": "Taluka Agriculture Officer", "organization": "Department of Agriculture, Maharashtra State"},
    {"phone": "9100000004", "email": "officer4@falconai.demo", "name": "Amit Bhosale", "designation": "Agricultural Extension", "organization": "Department of Agriculture, Maharashtra State"},
]

AUTHORIZED_EXPERT_PHONES = {e["phone"] for e in AUTHORIZED_EXPERTS}
AUTHORIZED_EXPERT_EMAILS = {e["email"].lower() for e in AUTHORIZED_EXPERTS}
AUTHORIZED_EXPERT_IDENTIFIERS = AUTHORIZED_EXPERT_PHONES | AUTHORIZED_EXPERT_EMAILS

AUTHORIZED_OFFICER_PHONES = {o["phone"] for o in AUTHORIZED_OFFICERS}
AUTHORIZED_OFFICER_EMAILS = {o["email"].lower() for o in AUTHORIZED_OFFICERS}
AUTHORIZED_OFFICER_IDENTIFIERS = AUTHORIZED_OFFICER_PHONES | AUTHORIZED_OFFICER_EMAILS

AUTHORIZED_STAFF_IDENTIFIERS = AUTHORIZED_EXPERT_IDENTIFIERS | AUTHORIZED_OFFICER_IDENTIFIERS


def _seed_predefined_staff_accounts(conn):
    """
    Ensure the fixed demo expert and officer accounts exist with exact credentials,
    and enforce strict RBAC by demoting any other accounts with EXPERT or ADMIN roles to FARMER.
    """
    password_hash, salt = hash_password("Falcon@2026")

    for expert in AUTHORIZED_EXPERTS:
        row = conn.execute("SELECT id FROM users WHERE phone = ? OR email = ?", (expert["phone"], expert["email"])).fetchone()
        if row:
            conn.execute(
                """
                UPDATE users
                SET full_name = ?, role = 'EXPERT', password_hash = ?, salt = ?, organization = ?, designation = ?, email = ?, phone = ?
                WHERE id = ?
                """,
                (expert["name"], password_hash, salt, expert["organization"], expert["designation"], expert["email"], expert["phone"], row[0])
            )
        else:
            conn.execute(
                """
                INSERT INTO users (phone, email, full_name, role, preferred_language, password_hash, salt, organization, designation)
                VALUES (?, ?, ?, 'EXPERT', 'en', ?, ?, ?, ?)
                """,
                (expert["phone"], expert["email"], expert["name"], password_hash, salt, expert["organization"], expert["designation"])
            )

    for officer in AUTHORIZED_OFFICERS:
        row = conn.execute("SELECT id FROM users WHERE phone = ? OR email = ?", (officer["phone"], officer["email"])).fetchone()
        if row:
            conn.execute(
                """
                UPDATE users
                SET full_name = ?, role = 'ADMIN', password_hash = ?, salt = ?, organization = ?, designation = ?, email = ?, phone = ?
                WHERE id = ?
                """,
                (officer["name"], password_hash, salt, officer["organization"], officer["designation"], officer["email"], officer["phone"], row[0])
            )
        else:
            conn.execute(
                """
                INSERT INTO users (phone, email, full_name, role, preferred_language, password_hash, salt, organization, designation)
                VALUES (?, ?, ?, 'ADMIN', 'en', ?, ?, ?, ?)
                """,
                (officer["phone"], officer["email"], officer["name"], password_hash, salt, officer["organization"], officer["designation"])
            )

    # Demote any non-whitelisted users who currently have EXPERT or ADMIN roles to FARMER
    staff_phones = list(AUTHORIZED_EXPERT_PHONES | AUTHORIZED_OFFICER_PHONES)
    placeholders = ",".join("?" for _ in staff_phones)
    conn.execute(
        f"""
        UPDATE users
        SET role = 'FARMER'
        WHERE role IN ('EXPERT', 'ADMIN')
          AND phone NOT IN ({placeholders})
        """,
        staff_phones
    )


def _seed_demo_data(conn):
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if user_count > 0:
        return

    # 1. Seed Farmer: Ramesh Kumar
    pw_hash, salt = hash_password("farmer123")
    conn.execute(
        """
        INSERT INTO users (phone, email, full_name, role, preferred_language, password_hash, salt, organization, designation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        ("8008742279", "ramesh.patil@demo.falconai.in", "Ramesh Kumar Patil", "FARMER", "en", pw_hash, salt, "Niphad Shetkari Vikas Mandal", "Farmer")
    )
    farmer_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    expert_row = conn.execute("SELECT id FROM users WHERE role = 'EXPERT' LIMIT 1").fetchone()
    expert_id = expert_row[0] if expert_row else None

    # 4. Seed Farms for Ramesh
    conn.execute(
        """
        INSERT INTO farms (user_id, farm_name, state, district, taluka, village, latitude, longitude, area_acres, primary_crop)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (farmer_id, "Shree Ganesh Krishi Farm", "Maharashtra", "Nashik", "Niphad", "Pimpalgaon Baswant", 20.1705, 73.9885, 3.5, "grape")
    )
    farm1_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    conn.execute(
        """
        INSERT INTO farms (user_id, farm_name, state, district, taluka, village, latitude, longitude, area_acres, primary_crop)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (farmer_id, "Sahyadri Corn & Tomato Plot", "Maharashtra", "Pune", "Baramati", "Malegaon Khurd", 18.1512, 74.5770, 2.0, "maize")
    )
    farm2_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # 5. Seed Demonstration Cases for Hotspot & Officer Dashboard Intelligence
    seed_cases = [
        {
            "case_number": "CASE-MH-2026-0001",
            "farmer_id": farmer_id, "farm_id": farm1_id,
            "crop_code": "grape", "season": "ANNUAL", "growth_stage": "fruiting_pod",
            "district": "Nashik", "taluka": "Niphad", "village": "Pimpalgaon Baswant",
            "latitude": 20.1705, "longitude": 73.9885,
            "image_path": "/static/images/falcon-logo.svg",
            "ai_status": "IDENTIFIED",
            "ai_raw_prediction": "grape downy mildew",
            "ai_condition_code": "grape_downy_mildew",
            "ai_observation_type": "DISEASE",
            "ai_confidence": 88.5,
            "leaf_area_percent": 74.2, "damage_percent": 24.6,
            "severity_level": "MODERATE",
            "weather_snapshot_json": json.dumps({"temperature": 27.5, "humidity": 86.0, "rainfall": 14.2, "source": "Open-Meteo"}),
            "risk_level": "HIGH", "risk_score": 78,
            "risk_factors_json": json.dumps(["High relative humidity (>80%) creates fungal spore explosion window", "Susceptible fruit development stage", "Active localized downy mildew pressure"]),
            "advisory_json": json.dumps({"immediate_action": "Aerate canopy by leaf thinning around grape bunches.", "monitoring": "Check daily for oil spots.", "cultural": "Keep vineyard floor weed-free.", "chemical": "Apply Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L."}),
            "requires_expert": 0, "case_status": "VERIFIED",
            "final_diagnosis_code": "grape_downy_mildew", "final_condition_name": "Grape Downy Mildew",
            "final_observation_type": "DISEASE", "final_verified_by": expert_id
        },
        {
            "case_number": "CASE-MH-2026-0002",
            "farmer_id": farmer_id, "farm_id": farm2_id,
            "crop_code": "maize", "season": "KHARIF", "growth_stage": "vegetative",
            "district": "Pune", "taluka": "Baramati", "village": "Malegaon Khurd",
            "latitude": 18.1512, "longitude": 74.5770,
            "image_path": "/static/images/falcon-logo.svg",
            "ai_status": "IDENTIFIED",
            "ai_raw_prediction": "Corn Insects Damages",
            "ai_condition_code": "corn_insects_damages",
            "ai_observation_type": "PEST",
            "ai_confidence": 92.4,
            "leaf_area_percent": 68.0, "damage_percent": 18.5,
            "severity_level": "HIGH",
            "weather_snapshot_json": json.dumps({"temperature": 31.0, "humidity": 62.0, "rainfall": 0.0, "source": "Open-Meteo"}),
            "risk_level": "HIGH", "risk_score": 82,
            "risk_factors_json": json.dumps(["Identified invasive pest: Fall Armyworm", "Vegetative whorl damage can stunt cob development", "Dry warm conditions favorable for pest flight"]),
            "advisory_json": json.dumps({"immediate_action": "Check central whorl for frass and pinholes.", "monitoring": "Install FAW pheromone traps @ 5/acre.", "biological": "Release Trichogramma pretiosum.", "chemical": "Apply Chlorantraniliprole 18.5% SC @ 0.4 ml/L into whorls."}),
            "requires_expert": 0, "case_status": "AI_CONFIDENT",
            "final_diagnosis_code": "corn_insects_damages", "final_condition_name": "Corn Insect Damage (Fall Armyworm)",
            "final_observation_type": "PEST", "final_verified_by": None
        },
        {
            "case_number": "CASE-MH-2026-0003",
            "farmer_id": farmer_id, "farm_id": farm1_id,
            "crop_code": "soybean", "season": "KHARIF", "growth_stage": "flowering",
            "district": "Amravati", "taluka": "Achalpur", "village": "Chandur Bazar",
            "latitude": 20.9374, "longitude": 77.7796,
            "image_path": "/static/images/falcon-logo.svg",
            "ai_status": "UNCERTAIN",
            "ai_raw_prediction": "soybean leaf",
            "ai_condition_code": "soybean_leaf",
            "ai_observation_type": "UNKNOWN",
            "ai_confidence": 42.1,
            "leaf_area_percent": 55.4, "damage_percent": 14.8,
            "severity_level": "MODERATE",
            "weather_snapshot_json": json.dumps({"temperature": 29.2, "humidity": 78.0, "rainfall": 8.5, "source": "Open-Meteo"}),
            "risk_level": "MODERATE", "risk_score": 64,
            "risk_factors_json": json.dumps(["AI confidence is below safe threshold (42.1%)", "Soybean flowering is highly sensitive to fungal pustules", "Elevated humidity post-monsoon shower"]),
            "advisory_json": json.dumps({"immediate_action": "Do not spray without confirmation. Awaiting Agricultural Pathologist review.", "monitoring": "Check underside of lower leaves with hand lens."}),
            "requires_expert": 1, "case_status": "PENDING_EXPERT",
            "final_diagnosis_code": None, "final_condition_name": None,
            "final_observation_type": None, "final_verified_by": None
        },
        {
            "case_number": "CASE-MH-2026-0004",
            "farmer_id": farmer_id, "farm_id": farm1_id,
            "crop_code": "tomato", "season": "KHARIF", "growth_stage": "fruiting_pod",
            "district": "Chhatrapati Sambhajinagar", "taluka": "Paithan", "village": "Pachod",
            "latitude": 19.8762, "longitude": 75.3433,
            "image_path": "/static/images/falcon-logo.svg",
            "ai_status": "IDENTIFIED",
            "ai_raw_prediction": "tomato late blight",
            "ai_condition_code": "tomato_late_blight",
            "ai_observation_type": "DISEASE",
            "ai_confidence": 94.0,
            "leaf_area_percent": 82.0, "damage_percent": 35.0,
            "severity_level": "CRITICAL",
            "weather_snapshot_json": json.dumps({"temperature": 21.0, "humidity": 94.0, "rainfall": 28.0, "source": "Open-Meteo"}),
            "risk_level": "CRITICAL", "risk_score": 95,
            "risk_factors_json": json.dumps(["High destructive pathogen: Late Blight (Phytophthora infestans)", "Continuous cloudy weather with >90% humidity", "High lesion area on fruiting branches"]),
            "advisory_json": json.dumps({"immediate_action": "EMERGENCY: Halt overhead irrigation immediately. Remove collapsed vines.", "chemical": "Apply Cymoxanil 8% + Mancozeb 64% WP @ 2.5g/L."}),
            "requires_expert": 0, "case_status": "VERIFIED",
            "final_diagnosis_code": "tomato_late_blight", "final_condition_name": "Tomato Late Blight",
            "final_observation_type": "DISEASE", "final_verified_by": expert_id
        },
        {
            "case_number": "CASE-MH-2026-0005",
            "farmer_id": farmer_id, "farm_id": farm1_id,
            "crop_code": "citrus", "season": "ANNUAL", "growth_stage": "fruiting_pod",
            "district": "Nagpur", "taluka": "Katol", "village": "Kondhali",
            "latitude": 21.1458, "longitude": 79.0882,
            "image_path": "/static/images/falcon-logo.svg",
            "ai_status": "IDENTIFIED",
            "ai_raw_prediction": "citrus canker",
            "ai_condition_code": "citrus_canker",
            "ai_observation_type": "DISEASE",
            "ai_confidence": 91.2,
            "leaf_area_percent": 62.0, "damage_percent": 12.0,
            "severity_level": "LOW",
            "weather_snapshot_json": json.dumps({"temperature": 32.5, "humidity": 68.0, "rainfall": 2.0, "source": "Open-Meteo"}),
            "risk_level": "LOW", "risk_score": 38,
            "risk_factors_json": json.dumps(["Moderate lesion density", "Weather humidity below epidemic threshold"]),
            "advisory_json": json.dumps({"immediate_action": "Prune affected twigs and burn.", "chemical": "Spray Copper Oxychloride 50 WP @ 3g/L + Streptocycline @ 0.1g/L."}),
            "requires_expert": 0, "case_status": "AI_CONFIDENT",
            "final_diagnosis_code": "citrus_canker", "final_condition_name": "Citrus Canker",
            "final_observation_type": "DISEASE", "final_verified_by": None
        }
    ]

    for c in seed_cases:
        conn.execute(
            """
            INSERT INTO cases (
                case_number, farmer_id, farm_id, crop_code, season, growth_stage,
                state, district, taluka, village, latitude, longitude,
                image_path, ai_status, ai_raw_prediction, ai_condition_code,
                ai_observation_type, ai_confidence, leaf_area_percent, damage_percent,
                severity_level, weather_snapshot_json, risk_level, risk_score,
                risk_factors_json, advisory_json, requires_expert, case_status,
                final_diagnosis_code, final_condition_name, final_observation_type,
                final_verified_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                c["case_number"], c["farmer_id"], c["farm_id"], c["crop_code"], c["season"], c["growth_stage"],
                "Maharashtra", c["district"], c["taluka"], c["village"], c["latitude"], c["longitude"],
                c["image_path"], c["ai_status"], c["ai_raw_prediction"], c["ai_condition_code"],
                c["ai_observation_type"], c["ai_confidence"], c["leaf_area_percent"], c["damage_percent"],
                c["severity_level"], c["weather_snapshot_json"], c["risk_level"], c["risk_score"],
                c["risk_factors_json"], c["advisory_json"], c["requires_expert"], c["case_status"],
                c["final_diagnosis_code"], c["final_condition_name"], c["final_observation_type"],
                c["final_verified_by"]
            )
        )


# ==============================================================================
# USER OPERATIONS
# ==============================================================================

def get_user_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE phone = ?", (phone.strip(),)).fetchone()
        return dict(row) if row else None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def create_user(phone: str, full_name: str, password: str, role: str = "FARMER", preferred_language: str = "en", organization: str = "", designation: str = "", email: str = "") -> Dict[str, Any]:
    norm_role = role.upper()
    norm_phone = phone.strip()
    norm_email = email.strip().lower() if email else ""

    # Strict RBAC: Non-whitelisted accounts can NEVER be created as EXPERT or ADMIN
    if norm_role in ("EXPERT", "ADMIN"):
        is_expert_ok = (norm_role == "EXPERT") and (norm_phone in AUTHORIZED_EXPERT_PHONES or norm_email in AUTHORIZED_EXPERT_EMAILS)
        is_officer_ok = (norm_role == "ADMIN") and (norm_phone in AUTHORIZED_OFFICER_PHONES or norm_email in AUTHORIZED_OFFICER_EMAILS)
        if not (is_expert_ok or is_officer_ok):
            norm_role = "FARMER"

    pw_hash, salt = hash_password(password)
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (phone, email, full_name, role, preferred_language, password_hash, salt, organization, designation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (norm_phone, norm_email if norm_email else None, full_name.strip(), norm_role, preferred_language, pw_hash, salt, organization.strip(), designation.strip())
        )
        user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return get_user_by_id(user_id)


def update_user_language(user_id: int, language: str) -> bool:
    with _connect() as conn:
        conn.execute("UPDATE users SET preferred_language = ? WHERE id = ?", (language.lower(), user_id))
        return True


# ==============================================================================
# FARM OPERATIONS
# ==============================================================================

def create_farm(user_id: int, farm_name: str, district: str, taluka: str, village: str, latitude: Optional[float] = None, longitude: Optional[float] = None, area_acres: float = 2.5, primary_crop: str = "") -> Dict[str, Any]:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO farms (user_id, farm_name, state, district, taluka, village, latitude, longitude, area_acres, primary_crop)
            VALUES (?, ?, 'Maharashtra', ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, farm_name.strip(), district.strip(), taluka.strip(), village.strip(), latitude, longitude, area_acres, primary_crop)
        )
        farm_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        row = conn.execute("SELECT * FROM farms WHERE id = ?", (farm_id,)).fetchone()
        return dict(row)


def get_farms_by_user(user_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM farms WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
        return [dict(r) for r in rows]


def get_all_farms(district: Optional[str] = None) -> List[Dict[str, Any]]:
    with _connect() as conn:
        if district:
            rows = conn.execute("SELECT * FROM farms WHERE district = ? ORDER BY id ASC", (district,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM farms ORDER BY id ASC").fetchall()
        return [dict(r) for r in rows]



# ==============================================================================
# CASE OPERATIONS
# ==============================================================================

def create_case(case_dict: Dict[str, Any]) -> Dict[str, Any]:
    case_number = case_dict.get("case_number") or f"CASE-MH-{secrets.token_hex(4).upper()}"
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO cases (
                case_number, farmer_id, farm_id, crop_code, season, growth_stage,
                state, district, taluka, village, latitude, longitude,
                image_path, overlay_path, image_quality_status, ai_status,
                ai_raw_prediction, ai_condition_code, ai_observation_type,
                ai_confidence, leaf_area_percent, damage_percent, severity_level,
                weather_snapshot_json, risk_level, risk_score, risk_factors_json,
                advisory_json, requires_expert, case_status, parent_case_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                case_number,
                case_dict["farmer_id"],
                case_dict.get("farm_id"),
                case_dict["crop_code"],
                case_dict.get("season", "KHARIF"),
                case_dict.get("growth_stage", "vegetative"),
                case_dict.get("state", "Maharashtra"),
                case_dict["district"],
                case_dict.get("taluka", ""),
                case_dict.get("village", ""),
                case_dict.get("latitude"),
                case_dict.get("longitude"),
                case_dict["image_path"],
                case_dict.get("overlay_path"),
                case_dict.get("image_quality_status", "VALID"),
                case_dict["ai_status"],
                case_dict.get("ai_raw_prediction"),
                case_dict.get("ai_condition_code"),
                case_dict.get("ai_observation_type", "UNKNOWN"),
                float(case_dict.get("ai_confidence", 0.0)),
                float(case_dict.get("leaf_area_percent", 0.0)),
                float(case_dict.get("damage_percent", 0.0)),
                case_dict.get("severity_level", "NONE"),
                json.dumps(case_dict.get("weather_snapshot")) if case_dict.get("weather_snapshot") else None,
                case_dict.get("risk_level", "LOW"),
                int(case_dict.get("risk_score", 0)),
                json.dumps(case_dict.get("risk_factors", [])),
                json.dumps(case_dict.get("advisory", {})),
                1 if case_dict.get("requires_expert") else 0,
                case_dict.get("case_status", "SUBMITTED"),
                case_dict.get("parent_case_id")
            )
        )
        case_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return get_case_by_id(case_id)


def get_case_by_id(case_id: int) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT c.*, u.full_name as farmer_name, u.phone as farmer_phone,
                   f.farm_name, ev.full_name as verified_by_name
            FROM cases c
            JOIN users u ON c.farmer_id = u.id
            LEFT JOIN farms f ON c.farm_id = f.id
            LEFT JOIN users ev ON c.final_verified_by = ev.id
            WHERE c.id = ?
            """,
            (case_id,)
        ).fetchone()
        if not row:
            return None
        res = dict(row)
        res["weather_snapshot"] = json.loads(res["weather_snapshot_json"]) if res.get("weather_snapshot_json") else None
        res["risk_factors"] = json.loads(res["risk_factors_json"]) if res.get("risk_factors_json") else []
        res["advisory"] = json.loads(res["advisory_json"]) if res.get("advisory_json") else {}
        res["expert_reviews"] = get_reviews_for_case(case_id)
        res["field_confirmations"] = get_field_confirmations_for_case(case_id)
        res["followups"] = get_followups_for_case(case_id)
        return res


def get_cases(
    farmer_id: Optional[int] = None,
    status: Optional[str] = None,
    district: Optional[str] = None,
    crop_code: Optional[str] = None,
    requires_expert_only: bool = False,
    limit: int = 50
) -> List[Dict[str, Any]]:
    query = """
        SELECT c.*, u.full_name as farmer_name, u.phone as farmer_phone, f.farm_name
        FROM cases c
        JOIN users u ON c.farmer_id = u.id
        LEFT JOIN farms f ON c.farm_id = f.id
        WHERE 1=1
    """
    params = []
    if farmer_id:
        query += " AND c.farmer_id = ?"
        params.append(farmer_id)
    if status:
        query += " AND c.case_status = ?"
        params.append(status)
    if district:
        query += " AND c.district = ?"
        params.append(district)
    if crop_code:
        query += " AND c.crop_code = ?"
        params.append(crop_code)
    if requires_expert_only:
        query += " AND (c.requires_expert = 1 OR c.case_status IN ('PENDING_EXPERT', 'UNDER_EXPERT_REVIEW', 'AI_UNCERTAIN'))"

    query += " ORDER BY c.id DESC LIMIT ?"
    params.append(limit)

    with _connect() as conn:
        rows = conn.execute(query, params).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["weather_snapshot"] = json.loads(d["weather_snapshot_json"]) if d.get("weather_snapshot_json") else None
            d["risk_factors"] = json.loads(d["risk_factors_json"]) if d.get("risk_factors_json") else []
            d["advisory"] = json.loads(d["advisory_json"]) if d.get("advisory_json") else {}
            result.append(d)
        return result


def submit_expert_review(
    case_id: int,
    expert_id: int,
    review_action: str,
    diagnosis_code: Optional[str] = None,
    condition_name: Optional[str] = None,
    observation_type: Optional[str] = None,
    expert_confidence: float = 95.0,
    expert_severity: Optional[str] = None,
    expert_notes: str = "",
    custom_advisory: str = "",
    follow_up_instructions: str = ""
) -> Dict[str, Any]:
    with _connect() as conn:
        # 1. Insert review record
        conn.execute(
            """
            INSERT INTO expert_reviews (
                case_id, expert_id, review_action, diagnosis_code, condition_name,
                observation_type, expert_confidence, expert_severity,
                expert_notes, custom_advisory, follow_up_instructions
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                case_id, expert_id, review_action, diagnosis_code, condition_name,
                observation_type, expert_confidence, expert_severity,
                expert_notes, custom_advisory, follow_up_instructions
            )
        )

        # 2. Update case state
        new_status = "VERIFIED"
        if review_action == "LAB_REFERRAL":
            new_status = "LAB_REFERRAL"
        elif review_action == "REQUEST_IMAGE":
            new_status = "FOLLOW_UP_REQUIRED"

        conn.execute(
            """
            UPDATE cases
            SET case_status = ?,
                final_diagnosis_code = COALESCE(?, final_diagnosis_code),
                final_condition_name = COALESCE(?, final_condition_name),
                final_observation_type = COALESCE(?, final_observation_type),
                final_verified_by = ?,
                severity_level = COALESCE(?, severity_level),
                requires_expert = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (new_status, diagnosis_code, condition_name, observation_type, expert_id, expert_severity, case_id)
        )
    return get_case_by_id(case_id)


def submit_field_confirmation(
    case_id: int,
    user_id: int,
    actual_condition_code: str,
    actual_condition_name: str,
    outcome: str,
    notes: str = ""
) -> Dict[str, Any]:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO field_confirmations (case_id, confirmed_by, actual_condition_code, actual_condition_name, outcome, confirmation_notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (case_id, user_id, actual_condition_code, actual_condition_name, outcome, notes)
        )
        conn.execute(
            """
            UPDATE cases
            SET follow_up_outcome = ?,
                case_status = CASE WHEN ? = 'RESOLVED' THEN 'CLOSED' ELSE case_status END,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (outcome, outcome, case_id)
        )
    return get_case_by_id(case_id)


def get_dashboard_statistics() -> Dict[str, Any]:
    with _connect() as conn:
        total_cases = conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
        disease_cases = conn.execute("SELECT COUNT(*) FROM cases WHERE ai_observation_type = 'DISEASE' OR final_observation_type = 'DISEASE'").fetchone()[0]
        pest_cases = conn.execute("SELECT COUNT(*) FROM cases WHERE ai_observation_type = 'PEST' OR final_observation_type = 'PEST'").fetchone()[0]
        uncertain_cases = conn.execute("SELECT COUNT(*) FROM cases WHERE ai_status IN ('UNCERTAIN', 'UNKNOWN')").fetchone()[0]
        pending_expert = conn.execute("SELECT COUNT(*) FROM cases WHERE case_status IN ('PENDING_EXPERT', 'UNDER_EXPERT_REVIEW', 'AI_UNCERTAIN')").fetchone()[0]
        high_risk_cases = conn.execute("SELECT COUNT(*) FROM cases WHERE risk_level IN ('HIGH', 'CRITICAL')").fetchone()[0]

        # District-level distribution
        district_counts = conn.execute(
            """
            SELECT district, COUNT(*) as count,
                   SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as high_risk_count
            FROM cases
            GROUP BY district
            ORDER BY count DESC
            LIMIT 10
            """
        ).fetchall()

        # Crop-level distribution
        crop_counts = conn.execute(
            """
            SELECT crop_code, COUNT(*) as count
            FROM cases
            GROUP BY crop_code
            ORDER BY count DESC
            """
        ).fetchall()

        # Recent outbreaks / alerts
        recent_alerts = conn.execute(
            """
            SELECT c.id, c.case_number, c.crop_code, c.district, c.taluka,
                   COALESCE(c.final_condition_name, c.ai_raw_prediction) as condition,
                   c.risk_level, c.risk_score, c.created_at
            FROM cases c
            WHERE c.risk_level IN ('HIGH', 'CRITICAL')
            ORDER BY c.id DESC
            LIMIT 6
            """
        ).fetchall()

        return {
            "total_cases": total_cases,
            "disease_cases": disease_cases,
            "pest_cases": pest_cases,
            "uncertain_cases": uncertain_cases,
            "pending_expert": pending_expert,
            "high_risk_cases": high_risk_cases,
            "district_distribution": [dict(r) for r in district_counts],
            "crop_distribution": [dict(r) for r in crop_counts],
            "recent_alerts": [dict(r) for r in recent_alerts]
        }


def get_hotspot_data() -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT c.id, c.case_number, c.crop_code, c.district, c.taluka,
                   c.latitude, c.longitude, c.risk_level, c.risk_score,
                   c.severity_level, c.ai_observation_type,
                   COALESCE(c.final_condition_name, c.ai_raw_prediction) as condition_name,
                   c.created_at
            FROM cases c
            WHERE c.latitude IS NOT NULL AND c.longitude IS NOT NULL
            ORDER BY c.id DESC
            LIMIT 100
            """
        ).fetchall()
        return [dict(r) for r in rows]


def get_reviews_for_case(case_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM expert_reviews WHERE case_id = ? ORDER BY id DESC", (case_id,)).fetchall()
        return [dict(r) for r in rows]


def get_field_confirmations_for_case(case_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM field_confirmations WHERE case_id = ? ORDER BY id DESC", (case_id,)).fetchall()
        return [dict(r) for r in rows]


def get_followups_for_case(case_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM cases WHERE parent_case_id = ? ORDER BY id DESC", (case_id,)).fetchall()
        return [dict(r) for r in rows]


# Legacy support for main.py
def save_diagnosis(farmer_name, phone, result):
    if not farmer_name or not phone:
        return
    recommendation = result.get("recommendation") or {}
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO diagnoses
                (farmer_name, phone, status, disease_name, confidence, damage_percent, action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                farmer_name.strip(),
                phone.strip(),
                str(result.get("status", "Unavailable")),
                str(result.get("disease_name", "Unknown")),
                float(result.get("confidence", 0) or 0),
                float(result.get("damage_percent", 0) or 0),
                str(recommendation.get("action", "No action recorded")),
            ),
        )


def get_diagnoses(phone, limit=20):
    if not phone:
        return []
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT created_at, status, disease_name, confidence, damage_percent, action
            FROM diagnoses
            WHERE phone = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (phone.strip(), limit),
        ).fetchall()
        return [dict(row) for row in rows]


# ==============================================================================
# USER ACTIVITY LOGGING
# ==============================================================================

def log_user_activity(user_id: int, activity_type: str, query_text: str = "", metadata: Optional[Dict] = None) -> int:
    """Records a user activity event. Returns the log entry id."""
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO user_activity_logs (user_id, activity_type, query_text, metadata_json)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, activity_type, query_text, json.dumps(metadata) if metadata else None)
        )
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def get_user_activity_logs(user_id: int, activity_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves recent activity logs for a user, optionally filtered by type."""
    with _connect() as conn:
        if activity_type:
            rows = conn.execute(
                "SELECT * FROM user_activity_logs WHERE user_id = ? AND activity_type = ? ORDER BY id DESC LIMIT ?",
                (user_id, activity_type, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM user_activity_logs WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            if d.get("metadata_json"):
                try:
                    d["metadata"] = json.loads(d["metadata_json"])
                except Exception:
                    d["metadata"] = None
            result.append(d)
        return result


def get_agronomy_experts(district: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Returns registered agronomy experts for advisory escalation and direct WhatsApp contact sharing."""
    with _connect() as conn:
        if district:
            rows = conn.execute(
                "SELECT * FROM agronomy_experts WHERE active = 1 AND district = ? ORDER BY id ASC LIMIT ?",
                (district.strip(), limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM agronomy_experts WHERE active = 1 ORDER BY id ASC LIMIT ?",
                (limit,)
            ).fetchall()
        return [dict(r) for r in rows]


def escalate_case(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Escalates a case to the District Agricultural Desk for expert verification.
    If the case already exists, marks requires_expert=1 and case_status='PENDING_EXPERT'.
    Otherwise creates a new escalated case entry.
    """
    case_id = payload.get("case_id")
    with _connect() as conn:
        if case_id:
            row = conn.execute("SELECT id FROM cases WHERE id = ?", (case_id,)).fetchone()
            if row:
                conn.execute(
                    """
                    UPDATE cases
                    SET requires_expert = 1,
                        case_status = 'PENDING_EXPERT',
                        severity_level = COALESCE(?, severity_level),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (str(payload.get("severity", "HIGH")).upper(), case_id)
                )
                return get_case_by_id(case_id)

    # If case does not exist yet or was generated on client
    crop_name = str(payload.get("crop") or "maize").lower().strip()
    disease_name = str(payload.get("disease") or "Crop Disease")
    severity = str(payload.get("severity") or "CRITICAL").upper()
    loc = str(payload.get("location") or "Nashik, Maharashtra")
    dist = loc.split(",")[0].strip() if "," in loc else loc

    case_data = {
        "farmer_id": payload.get("farmer_id", 1),
        "crop_code": crop_name,
        "season": "KHARIF",
        "growth_stage": "vegetative",
        "district": dist or "Nashik",
        "taluka": "",
        "village": "",
        "latitude": payload.get("latitude", 20.0),
        "longitude": payload.get("longitude", 73.8),
        "image_path": payload.get("image_url") or "/static/images/image.jpeg",
        "ai_status": "IDENTIFIED",
        "ai_raw_prediction": disease_name,
        "ai_condition_code": disease_name.lower().replace(" ", "_"),
        "ai_observation_type": "DISEASE",
        "ai_confidence": float(payload.get("confidence", 92.0)),
        "leaf_area_percent": 60.0,
        "damage_percent": float(payload.get("damage_percent", 52.0)),
        "severity_level": severity,
        "risk_level": "CRITICAL" if severity in ["CRITICAL", "HIGH"] else "MODERATE",
        "risk_score": 88 if severity in ["CRITICAL", "HIGH"] else 55,
        "risk_factors": ["High risk epidemic conditions reported", "Escalated to District Agricultural Desk"],
        "advisory": {"immediate_action": "Emergency scouting dispatched. Helpline 1800-180-1551 notified."},
        "requires_expert": True,
        "case_status": "PENDING_EXPERT"
    }
    return create_case(case_data)

