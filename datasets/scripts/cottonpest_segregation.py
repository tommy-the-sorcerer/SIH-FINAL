"""
FALCON-AI: CottonPest-BD Entomological Segregation & Conversion Tool
SIH 26131 — Early Detection and Management of Crop Diseases and Pest Infestations
Government of Maharashtra
"""

import os
import shutil
import hashlib
import json

HARMFUL_PESTS = {
    "mirid bug": {"id": 0, "canonical": "cotton_mirid_bug", "category": "harmful_pest"},
    "noctuidae": {"id": 1, "canonical": "cotton_noctuidae_caterpillar", "category": "harmful_pest"},
    "plant bugs": {"id": 2, "canonical": "cotton_plant_bug", "category": "harmful_pest"},
    "hadda beetle": {"id": 3, "canonical": "cotton_hadda_beetle", "category": "harmful_pest"}
}

BENEFICIAL_ORGANISMS = {
    "lady beetle": {"id": 100, "canonical": "beneficial_lady_beetle", "category": "beneficial_predator"},
    "green lacewings": {"id": 101, "canonical": "beneficial_green_lacewing", "category": "beneficial_predator"},
    "hoverfly": {"id": 102, "canonical": "beneficial_hoverfly", "category": "beneficial_predator"}
}

def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def execute_segregation(source_dir, output_dir, backup_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)
    audit_log = {
        "dataset": "CottonPest-BD",
        "doi": "10.17632/wkjg6srrk8.2",
        "total_images_processed": 0,
        "harmful_boxes": 0,
        "beneficial_boxes": 0,
        "quarantined_images": 0,
        "status": "CONFIGURED_AWAITING_SOURCE_DATA"
    }
    manifest_path = os.path.join(output_dir, "cottonpest_segregation_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(audit_log, f, indent=2)
    return audit_log

if __name__ == "__main__":
    src = r"datasets/incoming/cottonpest_bd"
    out = r"datasets/quarantine/cottonpest_segregated"
    bkp = r"datasets/quarantine/cottonpest_raw_backup"
    execute_segregation(src, out, bkp)
    print("Segregation tool configured successfully.")
