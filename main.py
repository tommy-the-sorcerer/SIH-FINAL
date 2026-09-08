import time
from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pipeline import process_and_predict
from storage import get_diagnoses, initialize_database, save_diagnosis

app = FastAPI(title="FALCON-AI Crop Health Diagnosis")
initialize_database()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Pass current timestamp as version string to bypass browser cache
    cache_version = int(time.time())
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"v": cache_version}
    )

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    farmer_name: str | None = Form(default=None),
    farmer_phone: str | None = Form(default=None),
    soil_moisture: str | None = Form(default=None),
    temperature: str | None = Form(default=None),
    humidity: str | None = Form(default=None),
):
    image_bytes = await file.read()
    try:
        result = process_and_predict(image_bytes, soil_moisture, temperature, humidity)
        save_diagnosis(farmer_name, farmer_phone, result)
        return result
    except Exception:
        return {
            "status": "Unavailable",
            "disease_name": "Analysis unavailable",
            "confidence": 0.0,
            "message": "The image could not be analysed. Please try a clearer crop photo.",
            "is_valid_crop": False,
            "leaf_area_percent": 0.0,
            "damage_percent": 0.0,
            "markers": [],
            "overlay": None,
            "recommendation": {
                "action": "Retake the image and try again",
                "dosage": "No treatment recommendation available",
                "sensor_status": "Analysis unavailable",
                "reason": "The diagnostic engine returned an error."
            }
        }


@app.get("/history")
async def history(phone: str = ""):
    return {"items": get_diagnoses(phone)}