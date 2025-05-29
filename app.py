# app.py (ClimaPi Dashboard - fully portable with relative paths, daily/hourly parsing and full logging)
from flask import Flask, render_template, request
import os
import datetime
import requests
import json
import argparse
import pathlib
from config import OPENWEATHER_API_KEY, LATITUDE, LONGITUDE

app = Flask(__name__)

@app.template_filter("datetime")
def format_datetime(value):
    try:
        return datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M")
    except:
        return "N/A"

BASE_DIR = pathlib.Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
CACHE_FILE = LOG_DIR / "onecall_cache.json"
LOG_FILE = LOG_DIR / "onecall_log.json"
MAX_LOG_ENTRIES = 288
os.makedirs(LOG_DIR, exist_ok=True)

UNIT_MODES = ["imperial", "metric", "scientific", "all"]

def convert_temp(value):
    return {
        "imperial": value,
        "metric": round((value - 32) * 5 / 9, 2),
        "scientific": round((value - 32) * 5 / 9 + 273.15, 2)
    }

def convert_pressure(value):
    return {
        "imperial": value,
        "metric": round(value * 33.8639, 2),
        "scientific": round(value * 3386.39, 2)
    }

def convert_wind(value):
    return {
        "imperial": value,
        "metric": round(value * 1.60934, 2),
        "scientific": round(value * 0.44704, 2)
    }

def get_sysinfo():
    temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
    uptime = os.popen("uptime -p").readline()
    return {
        "cpu_temp": temp.strip(),
        "uptime": uptime.strip(),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def format_unix(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else "N/A"

def wind_dir_to_cardinal(deg):
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = int((deg + 22.5) / 45) % 8
    return dirs[ix] if deg is not None else "N/A"

def log_weather(entry):
    try:
        if os.path.exists(LOG_FILE):
            with open(str(LOG_FILE), "r") as f:
                log = json.load(f)
        else:
            log = []
        log.append(entry)
        log = log[-MAX_LOG_ENTRIES:]
        with open(str(LOG_FILE), "w") as f:
            json.dump(log, f)
    except Exception as e:
        print("❗ Error logging weather:", e)

def fetch_onecall():
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LATITUDE}&lon={LONGITUDE}&units=imperial&exclude=minutely&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            return
        data = response.json()

        current = data.get("current", {})
        daily = data.get("daily", [])
        hourly = data.get("hourly", [])
        alerts = data.get("alerts", [])

        entry = {
            "time": datetime.datetime.now().strftime("%H:%M"),
            "temp": current.get("temp"),
            "feels_like": current.get("feels_like"),
            "humidity": current.get("humidity"),
            "wind_speed": current.get("wind_speed"),
            "pressure": current.get("pressure")
        }
        log_weather(entry)

        cached = load_cached_weather()
        cached["current"] = {
            "temp": convert_temp(current.get("temp")),
            "feels_like": convert_temp(current.get("feels_like")),
            "pressure": convert_pressure(current.get("pressure")),
            "humidity": current.get("humidity"),
            "wind_speed": convert_wind(current.get("wind_speed")),
            "wind_deg": current.get("wind_deg"),
            "wind_cardinal": wind_dir_to_cardinal(current.get("wind_deg")),
            "uvi": current.get("uvi"),
            "visibility": current.get("visibility"),
            "clouds": current.get("clouds"),
            "dew_point": convert_temp(current.get("dew_point")),
            "weather": current.get("weather", [{}])[0],
            "sunrise": format_unix(current.get("sunrise")),
            "sunset": format_unix(current.get("sunset"))
        }

        cached["daily"] = [
            {
                "date": datetime.datetime.fromtimestamp(d["dt"]).strftime("%a %b %d"),
                "temp": {
                    "min": d["temp"]["min"],
                    "max": d["temp"]["max"]
                },
                "humidity": d["humidity"],
                "clouds": d["clouds"],
                "uvi": d["uvi"],
                "wind_speed": d["wind_speed"],
                "wind_cardinal": wind_dir_to_cardinal(d.get("wind_deg")),
                "description": d["weather"][0]["description"],
                "icon": d["weather"][0]["icon"]
            } for d in daily
        ]

        cached["hourly"] = [
            {
                "time": datetime.datetime.fromtimestamp(h["dt"]).strftime("%H:%M"),
                "temp": h["temp"],
                "humidity": h["humidity"],
                "wind_speed": h["wind_speed"],
                "wind_cardinal": wind_dir_to_cardinal(h.get("wind_deg")),
                "clouds": h["clouds"],
                "rain": h.get("rain", {}).get("1h", 0),
                "uvi": h.get("uvi", 0),
                "icon": h["weather"][0]["icon"],
                "description": h["weather"][0]["description"]
            } for h in hourly[:48]
        ]

        cached["alerts"] = alerts

        with open(str(CACHE_FILE), "w") as f:
            json.dump(cached, f)

        print("✅ fetch_onecall: cache updated with current, daily, hourly, alerts")

    except Exception as e:
        print("❗ Error fetching onecall:", e)

def fetch_overview():
    url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={LATITUDE}&lon={LONGITUDE}&units=imperial&appid={OPENWEATHER_API_KEY}"
    try:
        overview = requests.get(url).json().get("weather_overview", "")
        cached = load_cached_weather()
        cached["overview"] = overview
        with open(str(CACHE_FILE), "w") as f:
            json.dump(cached, f)
    except Exception as e:
        print("❗ Error fetching overview:", e)

def fetch_day_summary():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={LATITUDE}&lon={LONGITUDE}&date={date}&units=imperial&appid={OPENWEATHER_API_KEY}"
    try:
        data = requests.get(url).json()
        summary = {
    "temperature": data.get("temperature"),
    "humidity": data.get("humidity", {}).get("afternoon"),
    "pressure": data.get("pressure", {}).get("afternoon"),
    "precipitation": data.get("precipitation", {}).get("total"),
    "cloud_cover": data.get("cloud_cover", {}).get("afternoon"),
    "wind": {
        "speed": data.get("wind", {}).get("max", {}).get("speed"),
        "direction": data.get("wind", {}).get("max", {}).get("direction")
    }
}
        cached = load_cached_weather()
        cached["summary"] = summary
        with open(str(CACHE_FILE), "w") as f:
            json.dump(cached, f)
    except Exception as e:
        print("❗ Error fetching day summary:", e)

def load_weather_data():
    try:
        with open(str(LOG_FILE), "r") as f:
            log = json.load(f)
        labels = [entry["time"] for entry in log]
        temps = [entry["temp"] for entry in log]
        feels = [entry["feels_like"] for entry in log]
        hums = [entry["humidity"] for entry in log]
        wind = [entry["wind_speed"] for entry in log]
        pressure = [entry["pressure"] for entry in log]
        return labels, temps, feels, hums, wind, pressure
    except Exception as e:
        print("❗ Failed to load chart data:", e)
        return [], [], [], [], [], []

def load_cached_weather():
    try:
        if os.path.exists(CACHE_FILE):
            with open(str(CACHE_FILE), "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        return {}

@app.route("/")
def index():
    info = get_sysinfo()
    weather = load_cached_weather()
    print("🔎 Weather keys:", list(weather.keys()))

    labels, temps, feels, hums, wind, pressure = load_weather_data()
    units = request.args.get("units", "imperial")
    if units not in UNIT_MODES:
        units = "imperial"
    return render_template("dashboard.html", info=info, weather=weather, labels=labels, temps=temps,
                           feels=feels, hums=hums, wind=wind, pressure=pressure, units=units)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--onecall", action="store_true", help="Fetch onecall weather data")
    parser.add_argument("--overview", action="store_true", help="Fetch AI overview")
    parser.add_argument("--summary", action="store_true", help="Fetch day summary")
    parser.add_argument("--serve", action="store_true", help="Run Flask web server")
    args = parser.parse_args()

    if args.onecall:
        fetch_onecall()
    elif args.overview:
        fetch_overview()
    elif args.summary:
        fetch_day_summary()
    elif args.serve:
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        parser.print_help()
