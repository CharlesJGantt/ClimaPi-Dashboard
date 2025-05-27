```markdown
# 🖥️ benchPi-Dashboard

> A lightweight, real-time dashboard for Raspberry Pi that tracks local weather, system stats, and nearby aircraft — rendered beautifully with Flask, Bootstrap, and Chart.js.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-lightgrey)

---

## 🌐 Live Demo

> Coming soon — or host it yourself on a Pi using the instructions below!

---

## ✨ Features

- 🌦️ Real-time weather data from OpenWeatherMap
- 💻 CPU temperature, uptime, and current timestamp
- ✈️ ADS-B aircraft tracking via `dump1090-fa`
- 📊 Interactive, historical charts powered by Chart.js:
  - 🧊 Tri-Chart: Temp, Feels Like, Humidity
  - 💨 Wind Speed
  - 📈 Barometric Pressure
- 🔄 Auto-refreshing every 2 minutes
- 🔐 Secrets excluded from Git (see `.gitignore`)
- 📁 Weather logs persist across reboots

---

## 🧰 Project Structure

```text
pi-dashboard/
├── app.py               # Flask app
├── dashboard.html       # Templated frontend (Jinja2 + Bootstrap + Chart.js)
├── config_example.py    # Template for secrets (do not commit actual config)
├── logs/                # Weather data history (auto-generated, ignored by Git)
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

- ✅ Raspberry Pi (tested on Pi 4B)
- ✅ Python 3.9+
- ✅ Internet connection
- ✅ OpenWeatherMap API key
- Optional: `dump1090-fa` for aircraft tracking

---

## 🔧 Installation

```bash
sudo apt update
sudo apt install python3-pip git
pip3 install flask requests
```

Clone this repo:

```bash
git clone git@github.com:CharlesJGantt/benchPi-Dashboard.git
cd benchPi-Dashboard
```

---

## 🔑 Configuration

1. Copy the secrets template:

```bash
cp config_example.py config.py
```

2. Edit `config.py` with your location and OpenWeatherMap API key:

```python
# config.py
OPENWEATHER_API_KEY = "your_api_key_here"
LATITUDE = 33.5296
LONGITUDE = -81.8344
```

> 🔐 `config.py` is **ignored by Git** to prevent leaking secrets. Do not commit it.

---

## 🚀 Launch the App

From inside the repo folder:

```bash
python3 app.py
```

Open your browser to:

```
http://<your-raspberry-pi-ip>:5000
```

---

## 📉 Charting Overview

Weather data is saved to:

```
/home/benchpi/pi-dashboard/logs/weather_log.json
```

The dashboard renders this data on each refresh, showing full historical charts:

| Chart Tab        | Data Included                     |
|------------------|-----------------------------------|
| 🌡️ Tri-Chart     | Temp, Feels Like, Humidity        |
| 💨 Wind Speed    | Wind speed (m/s)                  |
| 📈 Barometric    | Air pressure (hPa)                |

---

## 🔐 Security Notes

- All secrets (`config.py`) are excluded via `.gitignore`
- If a key is accidentally pushed, rotate the key and run:
  ```bash
  git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch config.py" \
    --prune-empty --tag-name-filter cat -- --all
  git push origin --force
  ```

---

## 🧪 Troubleshooting

- ❌ **Charts not showing?** Check that `weather_log.json` is being written to `/logs/`
- ❌ **No weather data?** Verify your OpenWeatherMap API key works
- ❌ **ADS-B stats empty?** Confirm `dump1090-fa` is installed and running

---

## 📜 License

MIT License — use it, modify it, build cool things with it.

---

## 👤 Maintainer

**Charles Gantt**  
🔗 [charlesjgantt.com](https://charlesjgantt.com)  
🛠 [TheMakersWorkbench](https://themakersworkbench.com)  
🐙 [@CharlesJGantt](https://github.com/CharlesJGantt)

---
```
