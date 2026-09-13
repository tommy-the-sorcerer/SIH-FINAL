"""
Real Weather Integration via Open-Meteo Meteorological Service
Complies with SIH26131 rule: Never fabricate weather values.
"""

import logging
from typing import Dict, Any, Optional
import requests

import time

logger = logging.getLogger(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# In-memory weather cache: key -> (timestamp, data)
_WEATHER_CACHE: Dict[str, tuple[float, Dict[str, Any]]] = {}
_CACHE_TTL_SECONDS = 900.0  # 15 minutes


def get_current_weather(latitude: Optional[float], longitude: Optional[float], timeout_seconds: float = 1.2) -> Dict[str, Any]:
    """
    Fetches real-time weather from Open-Meteo for given coordinates.
    Cached for 15 minutes to provide instantaneous (<5ms) sub-second responses.
    Gracefully degrades with available=False if offline or coordinates missing.
    NEVER fabricates or hallucinates weather values.
    """
    if latitude is None or longitude is None:
        return {
            "available": False,
            "temperature": None,
            "humidity": None,
            "rainfall": None,
            "wind_speed": None,
            "source": "Unavailable",
            "message": "Coordinates not provided for weather lookup."
        }

    cache_key = f"{round(float(latitude), 2)}_{round(float(longitude), 2)}"
    now = time.time()
    if cache_key in _WEATHER_CACHE:
        cached_time, cached_data = _WEATHER_CACHE[cache_key]
        if (now - cached_time) < _CACHE_TTL_SECONDS:
            return cached_data

    try:
        lat = float(latitude)
        lon = float(longitude)
        if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
            return {
                "available": False,
                "temperature": None,
                "humidity": None,
                "rainfall": None,
                "wind_speed": None,
                "source": "Unavailable",
                "message": f"Coordinates ({lat}, {lon}) are out of valid geographic range."
            }

        params = {
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "timezone": "Asia/Kolkata"
        }
        response = requests.get(OPEN_METEO_URL, params=params, timeout=timeout_seconds)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            result = {
                "available": True,
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "rainfall": current.get("precipitation"),
                "wind_speed": current.get("wind_speed_10m"),
                "source": "Open-Meteo API",
                "message": "Live meteorological observation retrieved."
            }
            _WEATHER_CACHE[cache_key] = (time.time(), result)
            return result
        else:
            logger.warning(f"Open-Meteo returned status {response.status_code}")
            return {
                "available": False,
                "temperature": None,
                "humidity": None,
                "rainfall": None,
                "wind_speed": None,
                "source": "Unavailable",
                "message": f"Weather service responded with status {response.status_code}."
            }
    except Exception as exc:
        logger.warning(f"Weather fetch failed: {exc}")
        return {
            "available": False,
            "temperature": None,
            "humidity": None,
            "rainfall": None,
            "wind_speed": None,
            "source": "Unavailable",
            "message": "Live weather service currently unreachable. No fabricated values generated."
        }
