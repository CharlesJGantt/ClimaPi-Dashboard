```markdown
# 🖥️ benchPi-Dashboard

A Flask-powered Raspberry Pi dashboard for monitoring real-time **weather**, **system stats**, and **ADS-B aircraft tracking** — complete with historical charting using Chart.js.

![screenshot](docs/dashboard-preview.png) <!-- Optional: replace with your actual screenshot -->

---

## ✨ Features

- 🌡️ Real-time weather data via OpenWeatherMap API
- 💻 CPU temperature, uptime, and timestamp
- ✈️ Live ADS-B aircraft stats from `dump1090-fa`
- 📊 Historical charts:
  - Temp / Humidity / Feels Like (Tri-Chart)
  - Wind Speed
  - Barometric Pressure
- 🔐 Secrets and logs excluded from version control
- 🧠 Auto-refreshing interface (every 2 minutes)
- 🔋 Built for low-power Raspberry Pi deployments

---

## 📁 Project Structure

```
pi-dashboard/
├── app.py               # Main Flask app
├── dashboard.html       # Templated frontend (Jinja2 + Bootstrap + Chart.js)
├── config_example.py    # Template for API keys and location
├── .gitignore           # Excludes secrets, logs, caches
└── logs/
    └── weather_log.json # Auto-generated weather history
```

---

## ⚙️ Setup Instructions

### 1. 📦 Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install flask requests
```

### 2. 🔑 Add API Key & Location

Create a `config.py`:

```python
# config.py
OPENWEATHER_API_KEY = "your_openweathermap_api_key"
LATITUDE = 33.52960883457356
LONGITUDE = -81.8343796502794
```

> 🔒 **Important:** Never commit `config.py`. It is ignored via `.gitignore`.

---

### 3. 🚀 Run the App

```bash
python3 app.py
```

Visit in your browser at:  
➡️ `http://<your-pi-ip>:5000`

---

## 📉 Charting & History

The app logs each weather update to:
```
/home/benchpi/pi-dashboard/logs/weather_log.json
```

Each chart displays **full historical data** from this file across reboots.

---

## 🧼 Security Notes

- Secrets (`config.py`) are **never committed**
- Logs are stored locally and excluded from Git
- If you ever leak a key: regenerate it and delete the old one immediately

---

## 🧪 Roadmap Ideas

- 📦 Docker support
- 🔄 Live-updating charts with AJAX or WebSockets
- 📅 Historical data by day/month/year
- 🛰️ Map view of tracked aircraft with Leaflet.js

---

## 👨‍💻 Maintainer

Charles Gantt  
[github.com/CharlesJGantt](https://github.com/CharlesJGantt)  
[TheMakersWorkbench.com](https://themakersworkbench.com)

---

## 🪪 License

MIT — use it, fork it, build on it, just give credit.
```
