import re
import os
import glob
from datetime import datetime
import requests


def safe_calculate(expression):
    try:
        expression = expression.replace(" ", "")
        if not re.match(r'^[0-9+\-*/().%\s]+$', expression):
            return None
        if "__" in expression or "import" in expression:
            return None
        expression = expression.replace("^", "**")
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except:
        return None


def get_current_time():
    return datetime.now().strftime("%H:%M")


def fetch_weather(location="London"):
    """Fetches simple weather data using the open-meteo API."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_resp = requests.get(geo_url, timeout=5).json()

        if not geo_resp.get("results"):
            return f"❌ Couldn't find location '{location}'"

        lat = geo_resp["results"][0]["latitude"]
        lon = geo_resp["results"][0]["longitude"]
        name = geo_resp["results"][0]["name"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_resp = requests.get(weather_url, timeout=5).json()

        temp = w_resp["current_weather"]["temperature"]
        wind = w_resp["current_weather"]["windspeed"]

        return f"🌡️ The weather in {name} is currently {temp}°C with wind speeds of {wind} km/h."
    except Exception:
        return "⚠️ Could not fetch weather right now."


def file_search(query, max_results=15):
    """Search for files matching a query in common user directories."""
    results = []
    search_dirs = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Videos"),
        os.path.expanduser("~/Music"),
    ]

    query_lower = query.lower()

    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        try:
            for root, dirs, files in os.walk(search_dir):
                # Skip hidden and system directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for f in files:
                    if query_lower in f.lower():
                        full_path = os.path.join(root, f)
                        try:
                            size = os.path.getsize(full_path)
                            if size < 1024:
                                size_str = f"{size} B"
                            elif size < 1024 * 1024:
                                size_str = f"{size / 1024:.1f} KB"
                            else:
                                size_str = f"{size / (1024 * 1024):.1f} MB"
                            results.append((f, size_str, root))
                        except:
                            results.append((f, "Unknown Size", root))

                        if len(results) >= max_results:
                            return results
        except PermissionError:
            continue

    return results

