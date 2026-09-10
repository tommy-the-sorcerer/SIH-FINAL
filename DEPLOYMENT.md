# FALCON-AI: System Deployment & Operations Manual

**Smart India Hackathon 2026** | **Problem Statement SIH26131**  
**System Architecture:** Ground-Level Edge & Cloud-Native Diagnostic Platform  

---

## 1. System Requirements

### Hardware Requirements
* **Processor:** Minimum 4 Cores (x86_64 or ARM64). Recommended 8+ Cores for high-concurrency kiosks.
* **RAM:** Minimum 4.0 GB (FALCON-AI model + runtime uses ~1.2 GB peak RAM).
* **Storage:** Minimum 2.0 GB free disk space (includes model weights, static assets, and SQLite DB).
* **GPU:** Optional. FALCON-AI is optimized for low-latency CPU execution (p50 ~591 ms on multi-core CPU).

### Software Requirements
* **Operating System:** Linux (Ubuntu 20.04+, Debian 11+), Windows 10/11, or macOS.
* **Python Runtime:** Python 3.10, 3.11, or 3.12 (Python 3.11 recommended).
* **Container Engine (Optional):** Docker 20.10+ and Docker Compose v2+.

---

## 2. Option A: Local Bare-Metal / Virtualenv Deployment

### Step 1: Clone or Navigate to Repository
```bash
cd c:\Users\lenovo\Desktop\RoboticDrones\RoboticDrones
```

### Step 2: Initialize Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Model Weights
Ensure `Models/PlantDiseaseDetection.pt` (436 MB) is present in the `Models/` directory:
```bash
# Windows PowerShell
Test-Path Models/PlantDiseaseDetection.pt

# Linux / macOS
ls -lh Models/PlantDiseaseDetection.pt
```

### Step 5: Start the Application Server
```bash
# Run with Uvicorn on localhost:8000
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

Access the application in your browser at:
`http://localhost:8000`

---

## 3. Option B: Docker Container Deployment

FALCON-AI includes a production-hardened `Dockerfile` utilizing a lightweight Debian base with headless OpenCV to avoid missing X11 display dependencies.

### Step 1: Build the Docker Image
```bash
docker build -t falcon-ai:latest .
```

### Step 2: Run the Docker Container
```bash
docker run -d \
  --name falcon-ai-instance \
  -p 8000:8000 \
  --restart unless-stopped \
  -v $(pwd)/database:/app/database \
  falcon-ai:latest
```

### Step 3: Verify Container Health
```bash
docker ps
docker logs falcon-ai-instance
curl http://localhost:8000/health
```

---

## 4. Option C: Docker Compose Orchestration

For turnkey deployment including volume mounts and healthcheck monitors:

```bash
docker-compose up -d --build
```

To view logs or stop:
```bash
# Tail real-time application logs
docker-compose logs -f

# Gracefully terminate services
docker-compose down
```

---

## 5. System Health & Monitoring Endpoints

| Endpoint | Method | Purpose | Typical Response |
| :--- | :--- | :--- | :--- |
| `/health` | `GET` | Container / Kubernetes liveness probe | `{"status": "healthy", "timestamp": ...}` |
| `/api/health` | `GET` | Detailed subsystem status (DB, Model, Cache) | `{"database": "connected", "model": "loaded"}` |
| `/metrics` | `GET` | Prometheus telemetry & inference count | Latency summaries, total diagnostic queries |

---

## 6. Offline & Edge Kiosk Configuration

FALCON-AI is designed to function in rural connectivity dead zones:
1. **Model Cache:** All YOLOv8 weights and PyTorch modules run locally on CPU; no cloud inference API is queried for computer vision.
2. **Weather Fallback:** If the Open-Meteo weather API is unreachable due to cellular dropout, FALCON-AI seamlessly falls back to historical agro-climatic averages for the selected Maharashtra district.
3. **Local Database:** SQLite operates in WAL (Write-Ahead Logging) mode, buffering local diagnostic events until backhaul connectivity is restored.

---

## 7. Troubleshooting

* **Issue: `libGL.so.1: cannot open shared object file` on Linux:**  
  *Solution:* Ensure `opencv-python-headless` is used instead of standard `opencv-python`, or install `apt-get install -y libgl1-mesa-glx libglib2.0-0`.
* **Issue: `Port 8000 already in use`:**  
  *Solution:* Run on an alternate port: `uvicorn main:app --host 0.0.0.0 --port 8080`.
* **Issue: High CPU utilization during startup:**  
  *Solution:* Model weight initialization requires ~0.27s on startup to deserialize PyTorch layers; subsequent steady-state requests consume only transient inference cycles (~590ms per image).
