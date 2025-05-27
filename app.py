from flask import Flask, render_template
import os
import datetime
import requests
import json
from config import OPENWEATHER_API_KEY, LATITUDE, LONGITUDE

app = Flask(__name__)

LOG_FILE = "/home/benchpi/pi-dashboard/logs/weather_log.json"
MAX_LOG_ENTRIES = 288

def get_sysinfo():
    temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
    uptime = os.popen("uptime -p").readline()
    return {
        "cpu_temp": temp.strip(),
        "uptime": uptime.strip(),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def log_weather(entry):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                log = json.load(f)
        else:
            log = []
        log.append(entry)
        log = log[-MAX_LOG_ENTRIES:]
        with open(LOG_FILE, "w") as f:
            json.dump(log, f)
    except Exception as e:
        print("❗ Error logging weather:", e)

def load_weather_data():
    try:
        with open(LOG_FILE, "r") as f:
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

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&units=metric&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "visibility": data.get("visibility", "N/A"),
            "wind_speed": data["wind"].get("speed", "N/A"),
            "wind_deg": data["wind"].get("deg", "N/A"),
            "wind_gust": data["wind"].get("gust", "N/A"),
            "condition_main": data["weather"][0]["main"],
            "condition_desc": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "sunrise": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S'),
            "sunset": datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S'),
            "is_thunderstorm": "thunderstorm" in data["weather"][0]["description"].lower()
        }

        log_weather({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "temp": weather["temp"],
            "feels_like": weather["feels_like"],
            "humidity": weather["humidity"],
            "wind_speed": weather["wind_speed"],
            "pressure": weather["pressure"]
        })

        return weather
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    info = get_sysinfo()
    weather = get_weather()
    labels, temps, feels, hums, wind, pressure = load_weather_data()
    return render_template("dashboard.html", info=info, weather=weather, labels=labels,
                           temps=temps, feels=feels, hums=hums, wind=wind, pressure=pressure)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
