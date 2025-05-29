<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

## ClimaPi Dashboard

<p align="center">
  <img src="https://github.com/user-attachments/assets/bad1edca-66a3-4169-a18e-641ba2fa94dd" alt="ClimaPi Dashboard Screenshot" width="400"> 
</p>

A self-hosted weather visualization tool for Raspberry Pi that displays real-time conditions, forecasts, and historical data using OpenWeatherMap API, Flask, and Chart.js—all accessible through a sleek local web dashboard.

### About The Project

ClimaPi Dashboard is a fully self-hosted weather visualization tool built for Raspberry Pi and similar Linux-based microcomputers. It offers real-time weather monitoring, multi-day forecasting, and rich historical logging through a sleek, browser-accessible dashboard.

Built using Flask on the backend and Bootstrap + Chart.js on the frontend, ClimaPi leverages the OpenWeatherMap One Call 3.0 API to deliver accurate, up-to-date environmental data. Everything is rendered locally, giving users total control over polling schedules, data caching, and how weather is displayed.

This modular design empowers makers, hobbyists, and smart home tinkerers to monitor weather conditions without relying on third-party dashboards or services. Whether you're deploying it as part of a smart home, using it to learn web development, or integrating it into a DIY weather station, ClimaPi is simple to set up and easy to customize.

### Key Capabilities

*   ☀️ **Current Weather**: Displays real-time conditions including temperature, wind, pressure, humidity, and cloud cover.
*   📆 **Forecasts**: Shows 48-hour hourly forecasts and 8-day daily forecasts with visual summaries and icons.
*   🧐 **Overview Summaries**: Pulls AI-generated daily and tomorrow forecasts from OpenWeatherMap’s `/overview` endpoint.
*   ⚠️ **Weather Alerts**: Highlights active severe weather alerts when available.
*   📊 **Historical Logging**: Logs snapshots of key metrics (temp, feels like, wind, pressure, humidity) locally every poll.
*   💡 **Customizable UI**: Cards, layout, and styles can be adapted by modifying partial templates or creating new views.

ClimaPi is lightweight enough for a Raspberry Pi Zero yet powerful enough to serve as a full-fledged smart home component. It’s a transparent, hackable, and extensible foundation for anything weather-aware.

## Built With

*   [Python 3.9+](https://www.python.org/)
*   [Flask](https://flask.palletsprojects.com/)
*   [Chart.js](https://www.chartjs.org/)
*   [Bootstrap 5](https://getbootstrap.com/)
*   [OpenWeatherMap API](https://openweathermap.org/api/one-call-3)

## Getting Started

### Prerequisites

On modern Raspberry Pi OS (Bookworm and later), the default Python environment is managed to avoid unintended system-level changes. For this reason, using `pip3` globally is restricted. You have two recommended installation options:

#### Option 1: System-wide (no virtual environment)

If you're not using a virtual environment, you can safely install Flask and Requests via `apt`:

```plaintext
sudo apt update
sudo apt install python3-flask python3-requests git
```

This installs the required libraries using the system package manager.

#### Option 2: Virtual Environment (recommended)

For better project isolation and compatibility, you can use a Python virtual environment:

```plaintext
sudo apt install python3-venv git

# Clone the project
git clone https://github.com/CharlesJGantt/ClimaPi-Dashboard.git
cd ClimaPi-Dashboard

# Set up and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install project dependencies
pip install flask requests
```

Use the method that best suits your setup. The virtual environment approach is ideal for development, while the system-wide method is simpler for lightweight or single-use deployments.

### 🔑 Getting Your OpenWeatherMap API Key

To fetch live weather data, ClimaPi Dashboard uses the [OpenWeatherMap API](https://openweathermap.org/api). You'll need to sign up for a free API key to get started.

#### 🪜 Steps to Obtain Your API Key:

1.  **Create an Account**  
    Visit https://home.openweathermap.org/users/sign_up and create a free account.
2.  **Generate an API Key**  
    After logging in, go to the **API Keys** tab in your dashboard or directly to https://home.openweathermap.org/api_keys.  
    Click **"Create Key"**, give it a name (e.g., `ClimaPi`), and copy the generated key.
3.  **Activate Your Key**  
    It may take several minutes for a new key to become active.
4.  **Add Your Key to the Project**  
    Open the `config.py` file and replace the placeholder with your actual key:
        
    `OPENWEATHERMAP_API_KEY = "your_api_key_here"` 
    
    🔐 _Tip: For added security, consider loading your API key from an environment variable instead of hardcoding it._
    

#### 📌 Free Tier Limits & Billing Notes

*   The free tier includes **1,000 API calls per day**.
*   OpenWeatherMap may require a credit card on file to **enable API access**, even if you stay within the free tier limits.
*   **No charges will occur** as long as your usage stays below the 1,000 daily call limit — which ClimaPi is optimized to do.

✅ The dashboard is designed to **stay under 950 calls/day** by default, keeping you comfortably within the free tier.

### Installation

Once your dependencies are installed (see [Prerequisites](https://chatgpt.com/g/g-p-68349e2db43081918f3da71cebfd853a-tmwb-benchpi-project/c/6837cde8-bd00-8003-abf3-5f55195f8ebb#prerequisites)), you're ready to set up ClimaPi Dashboard.

1.  **Clone the Repository**

```plaintext
git clone https://github.com/CharlesJGantt/ClimaPi-Dashboard.git
cd ClimaPi-Dashboard

```

1.  **Create Your Config File**

Copy the example configuration file and update it with your OpenWeatherMap API key and location settings:

```plaintext
cp config_example.py config.py
nano config.py

```

Replace the placeholders in `config.py`:

```plaintext
OPENWEATHER_API_KEY = "your_key_here"
LATITUDE = "your_LAT_here"
LONGITUDE = "your_LONG_here"
UNITS = "imperial"  # Options: "imperial", "metric"

```

1.  **Launch the Dashboard (Development Mode)**

To start the Flask web server for local access:

```plaintext
python3 app.py --serve

```

Visit the dashboard in your browser at:

```plaintext
http://<your-pi-ip>:5000

```

> 💡 Tip: For live weather updates, schedule the data-fetching commands (`--onecall`, `--overview`, and `--summary`) using `cron` or another scheduler. The server does not auto-refresh data on its own.

### Run Flask Dashboard on Startup

To automatically start the ClimaPi Dashboard on system boot, you can use a `systemd` service.

1.  **Create a service file**:

```plaintext
sudo nano /etc/systemd/system/climapi-dashboard.service
```

1.  **Paste the following configuration** (edit paths to match your setup):

```plaintext
[Unit]
Description=ClimaPi Dashboard Web Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/ClimaPi-Dashboard/app.py --serve
WorkingDirectory=/home/pi/ClimaPi-Dashboard
Restart=always
User=pi
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

1.  **Enable and start the service**:

```plaintext
sudo systemctl daemon-reexec
sudo systemctl enable climapi-dashboard
sudo systemctl start climapi-dashboard
```

1.  **Check status**:

```plaintext
sudo systemctl status climapi-dashboard
```

Your Flask server will now auto-start on boot and be accessible at:

```plaintext
http://<your-pi-ip>:5000
```

> 🔁 If you ever update the app, remember to restart the service:

```plaintext
sudo systemctl restart climapi-dashboard
```

### Recommended Cron Jobs

To maintain an efficient and API-friendly polling schedule, set up the following cron jobs:

```plaintext
crontab -e
```

Add these lines:

```plaintext
# Fetch current, hourly, daily, and alerts every 3.5 minutes
*/3 * * * * /usr/bin/python3 /home/pi/ClimaPi-Dashboard/app.py --onecall
*/7 * * * * /usr/bin/python3 /home/pi/ClimaPi-Dashboard/app.py --onecall

# Fetch AI-generated overview every 4 hours
0 */4 * * * /usr/bin/python3 /home/pi/ClimaPi-Dashboard/app.py --overview

# Fetch daily summary twice per day
0 6,18 * * * /usr/bin/python3 /home/pi/ClimaPi-Dashboard/app.py --summary
```

> 📌 These entries stagger `--onecall` calls every ~3.5 minutes by alternating between 3 and 7-minute intervals, ensuring a spread-out pattern while averaging under the API limit.

## API Structure and Call Breakdown

ClimaPi Dashboard relies on scheduled calls to the OpenWeatherMap One Call 3.0 API. There are three endpoints used:

*   `/onecall`: Provides current, hourly, and daily forecast data.
*   `/onecall/overview`: AI-generated readable weather summary.
*   `/onecall/day_summary`: Aggregated metrics per day.

### Call Frequency & Strategy

Not all endpoints need to be called at the same rate. Here’s the recommended breakdown:

| API EndpointPurposeSuggested FrequencyUsed In Cards |   |   |   |
| --- | --- | --- | --- |
| `/onecall` | Current, hourly (48h), and 8-day daily forecast | Every 3.5 minutes | Current, Hourly, Daily, Alerts |
| `/onecall/overview` | Natural language summary for today/tomorrow | Every 4 hours | Weather Overview card |
| `/onecall/day_summary` | Daily aggregates (avg temp, wind, rain, humidity) | Every 12 hours | Summary Metrics card |

Each `--onecall` execution provides multiple subpaths used by various cards:

*   `current`: Real-time weather (temp, humidity, wind, visibility, pressure)
*   `hourly`: 48-hour forecast (temp, wind, clouds, rain)
*   `daily`: 8-day forecast (min/max, wind, humidity, cloud cover)
*   `alerts`: Severe weather warnings, if any

### Estimated API Load

| Frequency | `/onecall`/day | `/overview`/day | `/day_summary`/day | Total API Calls/day |
| --- | --- | --- | --- | --- |
| Every 3.5 min | ~411 | 6 | 2 | **~419** |
| Every 5 min | ~288 | 6 | 2 | ~296 |
| Every 10 min | ~144 | 6 | 2 | ~152 |

> ⚠️ Avoid calling all endpoints too frequently or you may exceed the 1,000 call/day free tier.

### Strategy Tips

*   Call `--onecall` frequently for real-time cards.
*   Call `--overview` and `--summary` via separate cron jobs spaced across the day.
*   Cache results locally and separate fetch scripts from the dashboard server to optimize usage.

This strategy ensures reliable updates while staying well within free tier limits and supports robust card rendering and logging for all metrics.

### API Endpoints:

Each OpenWeatherMap API call returns structured data via specific paths used by the dashboard to populate individual cards and charts.

*   `/onecall`: Core weather data including multiple nested subpaths:
    *   `current`: Supplies real-time measurements including temperature, humidity, pressure, wind, UVI, visibility, cloud cover, and sunrise/sunset. This data powers the 🌤️ **Current Weather** card.
    *   `hourly`: Provides forecasts in 1-hour increments for the next 48 hours, used to populate the ⏱️ **Next 48 Hours** table.
    *   `daily`: Offers 8-day forecasts with min/max temperature, UVI, humidity, and weather descriptions. Used for the 📅 **8-Day Forecast** card.
    *   `alerts`: Optional array of weather warnings or alerts, displayed in the 🚨 **Weather Alerts** card.
*   `/onecall/day_summary`: Daily-aggregated meteorological metrics including:
    *   Min/Max/Average temperature
    *   Precipitation totals
    *   Cloud cover and pressure (afternoon values)
    *   Max wind speed and direction  
        This data feeds the 📆 **Daily Summary** card.
*   `/onecall/overview`: Returns a pre-written AI-generated summary in plain English. Used to populate the 📖 **Weather Overview** card.
*   `/onecall/alerts`: May return independently if alerts exist, but is already included in `/onecall`. This is noted here for completeness but not separately called.

### Data Includes:

Each API call returns a wealth of weather-related metrics. Here’s a breakdown of what’s extracted and how it contributes to the dashboard's functionality:

#### From `/onecall/current`:

*   **Temperature (actual & feels-like)** – Displayed on the main conditions card.
*   **Humidity** – Used in real-time conditions and logged for analysis.
*   **Pressure** – Visualized in trend charts.
*   **Cloud cover** – Displayed as a percent-based value in current conditions.
*   **Visibility** – Shown in meters or miles depending on unit.
*   **Wind Speed, Gusts, Direction** – Used in current cards and wind history logs.
*   **UVI** – Helps determine UV safety level.
*   **Sunrise & Sunset** – Tracked for timeline displays and daily summaries.

#### From `/onecall/hourly`:

*   **Hourly Forecast (48h)** – Temperature, wind, humidity, and cloud cover plotted on charts.
*   **Rain/Snow Forecast** – Hourly predictions used in future precipitation estimates.

#### From `/onecall/daily`:

*   **Min/Max/Day Temperatures** – Used in the 8-day forecast.
*   **Humidity, Pressure, Wind (avg/max)** – Rendered in daily overview cards.
*   **Moon Phase** – Added for astronomy-aware planning or display.

#### From `/onecall/alerts`:

*   **Active Alerts** – Populated with event name, issuing agency, severity, timing, and description.

#### From `/onecall/day_summary`:

*   **Average Daily Temp (min/max/avg)**
*   **Avg Wind Speed and Max Gust**
*   **Rain and Snow Totals**
*   **Afternoon Pressure and Cloud Cover**

#### From `/onecall/overview`:

*   **Natural Language Summary** – Pre-generated report of current and upcoming conditions.

These data points are logged locally and visualized using cards, charts, and summary views. By breaking data out by subpath and purpose, ClimaPi optimizes API usage while ensuring each dashboard element is both useful and relevant.

## Usage

Once installed and configured, the ClimaPi Dashboard runs as a lightweight Flask web app on your local network.

### Web Access

Visit the dashboard from any device on your network:

```plaintext
http://<your-pi-ip>:5000
```

This serves the real-time and forecast weather data in a responsive browser UI.

### Weather Cards Displayed

The dashboard includes several dynamic cards, updated based on your polling schedule:

*   🧐 **Overview (AI Summary)** – From `/overview`, updated every 4 hours
*   ☀️ **Current Conditions** – From `/onecall/current`, updated every 3.5 minutes
*   📅 **Forecast Cards** – 48-hour and 8-day forecasts from `/onecall/hourly` and `/daily`
*   📊 **Aggregated Summary** – Daily averages and totals from `/day_summary`, updated every 12 hours
*   ⚠️ **Alerts and Warnings** – From `/onecall/alerts` (auto-included in `/onecall`)

These cards are automatically generated and populated by the backend Flask logic. They respond to local API data stored during each polling cycle.

### Data Logging

Every time a polling script runs—whether it's `--onecall`, `--overview`, or `--summary`—the resulting data is appended to a structured log file stored locally at:

```plaintext
/home/pi/ClimaPi-Dashboard/logs/weather_log.json
```

This file acts as the persistent data store for ClimaPi’s historical weather records. Each log entry is a complete JSON object, timestamped and segmented by the API endpoint and its subpaths (e.g., `current`, `hourly`, `daily`).

### What’s Included in the Log:

*   Full response from `/onecall`, including current, hourly, daily, and alerts.
*   AI-generated summaries from `/overview`.
*   Aggregated daily metrics from `/day_summary`.
*   Timestamps for each fetch event to track update cadence.

This structured log provides the backbone for:

*   📈 Custom charting and time-series analysis with Chart.js, Python scripts, or external tools.
*   📤 Exporting datasets for Excel/CSV for sharing, archiving, or backup.
*   🛠 Debugging failed API responses or stale dashboard data.
*   🔔 Triggering alerts or home automations when thresholds are met (e.g., high wind gusts, incoming rain).

### Log Management Tips:

*   Consider rotating the log file monthly to keep file size manageable.
*   Use tools like `jq`, `pandas`, or shell scripts to extract, parse, and summarize data.
*   You can even sync this log to the cloud or another machine for redundancy.

> 📚 Example: Want to chart temperature trends over the past week? Extract the `temp` field from all `current` blocks, grouped by timestamp, and feed it into a chart library. weather data is saved as structured JSON in:

```plaintext
/home/pi/ClimaPi-Dashboard/logs/weather_log.json
```

This log includes every value pulled from each API path and can be parsed for:

*   Historical charting (in Chart.js or external tools)
*   Export to CSV/Excel
*   Data audits or redundancy backups

Each polling event appends a new record, allowing for long-term local storage and independent analysis beyond the dashboard UI.

## Modifying the Dashboard

The ClimaPi Dashboard is designed with modularity in mind, making it easy to adapt the layout, add new cards, or extend the interface for additional sensors or data sources.

### Customize the Main Layout

The main layout is defined in `templates/index.html`. This file uses Jinja2 templating to include partials for each dashboard card and define the overall page structure using Bootstrap components.

You can:

*   Change card order by reordering `{% include %}` statements
*   Remove unused cards
*   Add new rows/columns for custom content

### Working with Partials

All cards are modular and stored in `templates/partials/`. Each HTML file in this directory represents a self-contained card rendered on the dashboard. For example:

*   `card_summary.html` – Daily averages from `/summary`
*   `card_current.html` – Real-time metrics from `/onecall/current`
*   `card_overview.html` – AI-generated forecast from `/overview`

Cards are included using Jinja syntax like:

```plaintext
{% include 'partials/card_summary.html' %}
```

### Add New Cards

To add a custom card:

1.  Create a new file in `templates/partials/`, e.g. `card_uv_index.html`
2.  Write your HTML structure (you can copy another card as a starting point)
3.  Add logic in `app.py` if the card needs custom data handling
4.  Include the card in `index.html` using `{% include 'partials/card_uv_index.html' %}`

### Update Styles

ClimaPi uses Bootstrap 5 for layout and style. You can:

*   Add inline styles in each card
*   Define new classes in a linked CSS file
*   Tweak the global style block in `index.html`

For more control, you can add a custom stylesheet and load it with:

```html
<link rel="stylesheet" href="/static/custom.css">
```

### Modify Configurations

Settings like units, coordinates, and API keys are stored in `config.py`. Modify this file to change how and where ClimaPi fetches data. To point to a different city or switch from imperial to metric:

```python
UNITS = "metric"
LATITUDE = "52.5200"
LONGITUDE = "13.4050"
```

> 💡 Tip: You can extend `config.py` with custom variables and use them inside Flask routes or templates to dynamically control behavior.

### Extend Flask Routes

Want to build a new section like an indoor dashboard or add charts for a sensor? You can:

1.  Create a new HTML file in `templates/`
2.  Add a new route in `app.py` using Flask’s `@app.route()`
3.  Pass data to the new view with `render_template()`

Example:

```python
@app.route("/indoors")
def indoors():
    return render_template("indoor_dashboard.html")
```

Then visit:

```plaintext
http://<your-pi-ip>:5000/indoors
```

This modular structure gives you full control over how the ClimaPi interface evolves. Add sensors, write new fetch scripts, or embed live cameras — the system is yours to expand. views in `templates/index.html`

## Creating New Templates

To add an entirely new view to ClimaPi (such as a page for indoor sensors, camera feeds, or air quality metrics), follow these steps. This process lets you build entire standalone pages that integrate seamlessly into the Flask backend and Bootstrap frontend.

### 1\. Create a New HTML Template

Inside the `templates/` directory, create your new view file:

```plaintext
touch templates/indoor_view.html

```

You can copy and modify the structure of `index.html` or any existing template as a starting point. Customize the layout with any Bootstrap cards, sections, or your own content blocks.

### 2\. Define a Flask Route

Add a new route to `app.py` that renders the new template:

```plaintext
@app.route("/indoor")
def indoor():
    return render_template("indoor_view.html")

```

This creates a new page accessible via:

```plaintext
http://<your-pi-ip>:5000/indoor

```

You can add logic to this route to pass custom variables to the template or load data from additional logs, APIs, or sensors.

### 3\. Include New Partials (Optional)

If your new view will include dashboard-style cards like the main interface, consider storing each visual component in its own partial. Place them in `templates/partials/` and include them in your new view like so:

```plaintext
{% include 'partials/card_air_quality.html' %}

```

This helps maintain clean, modular templates and allows for easy reuse.

### 4\. Add Navigation (Optional)

To make your new view accessible from other pages, add a link in your header or navbar:

```plaintext
<a class="nav-link" href="/indoor">Indoor Dashboard</a>

```

### 5\. Restart Flask

After making changes to routes or templates, restart the Flask server:

```plaintext
sudo systemctl restart climapi-dashboard

```

### 6\. Extend Further

Each new template can:

*   Pull in sensor logs or JSON data
*   Visualize with Chart.js
*   Display cards or tables
*   Embed images or live camera feeds
*   Include interactive JavaScript elements

ClimaPi is designed to grow with your needs. Whether you want a mobile-friendly greenhouse monitor or a multi-tabbed home dashboard, adding new views is as simple as creating a new template and route.

## Troubleshooting

### Flask Doesn’t Start

If the web dashboard doesn’t appear or Flask fails to start:

*   **Check Port 5000**: Ensure another service isn’t already using this port. Try `sudo lsof -i :5000` to check.
*   **Missing Config**: Make sure `config.py` exists and contains valid API keys and coordinates.
*   **Python Errors**: Run `python3 app.py --serve` manually to see traceback errors in the terminal.
*   **Permissions**: Ensure that the app has the necessary permissions to bind to a port and access required files.

To start Flask manually for debugging:

```plaintext
python3 app.py --serve
```

To start Flask as a service:

```plaintext
sudo systemctl start climapi-dashboard
```

To check status:

```plaintext
sudo systemctl status climapi-dashboard
```

### API Key Doesn’t Work

If you’re not seeing any weather data:

*   **Verify the API Key**: Confirm your OpenWeatherMap API key is correct and active.
*   **Enable One Call 3.0**: Log into your OpenWeatherMap account and ensure the One Call 3.0 API is enabled for your key.
*   **Daily Limit**: You may have exceeded your daily quota. Check your usage dashboard on OpenWeatherMap.

### Dashboard Loads Blank

*   **Check Logs**: Open `/home/pi/ClimaPi-Dashboard/logs/weather_log.json` and verify that entries are being written.
*   **API Failures**: Look for empty or malformed data entries, which can indicate failed API responses.
*   **JS Console Errors**: Open your browser's developer tools (F12) and check the Console tab for JavaScript errors.

### Charts Not Rendering

*   **Missing Data**: If chart data is `null` or empty, the card will not render.
*   **Key Mismatch**: Ensure the keys in the JSON match the ones expected in the dashboard's frontend logic.
*   **Frontend Debugging**: Inspect HTML source to see if the charts are present but hidden due to lack of data.

### Cron Jobs Not Working

*   **Validate Syntax**: Run `crontab -l` to confirm your scheduled jobs are correctly saved.
*   **Log Output**: Redirect output to a file for debugging, e.g.:

```plaintext
*/3 * * * * /usr/bin/python3 /home/pi/ClimaPi-Dashboard/app.py --onecall >> /home/pi/cronlog.txt 2>&1
```

*   **Cron Not Running**: Ensure `cron` is enabled: `sudo systemctl enable cron && sudo systemctl start cron`

These tips should help identify and resolve most installation, runtime, or data-fetching issues.

## Roadmap

Planned and Proposed Features for Future Releases:

*   🐳 **Docker Support**: Add Dockerfile and Compose configuration for easy deployment and version pinning.
*   🗂️ **Additional Cards**: More modular card templates for sunrise/sunset, UVI index, dew point, moon phase, and more.
*   ✈️ **SkyAware / PiAware Integration**: Plane tracking cards using data from dump1090-fa JSON endpoints.
*   🌡️ **Indoor/Outdoor Environmental API**: Create REST API endpoints to support integration with DIY sensor nodes (ESP32, Arduino, etc.) for indoor temperature, humidity, air quality, etc.
*   📡 **Sensor Auto-Discovery**: Auto-detect indoor/outdoor nodes reporting data via MQTT or REST.
*   🔧 **Settings UI**: Add a simple web-based config editor to change location, units, or toggle cards.
*   📆 **Data Export Tools**: CSV/Excel export of weather logs via web interface.
*   ☁️ **SkyCam Feed Embedding**: Embed live camera feeds from backyard or weather cams.
*   🔔 **Smart Home Triggers**: Optional webhook or MQTT publishing when thresholds (like wind speed or temp) are met.

Have a feature idea? Open an issue or submit a pull request!

## Contributing

1.  Fork the repo
2.  Create a branch: `git checkout -b feature/foo`
3.  Commit your changes
4.  Push to your fork
5.  Submit a pull request

## License

Distributed under the MIT License. See `LICENSE` for details.

## Contact

**Charles Gantt**  
🌐 [charlesjgantt.com](https://charlesjgantt.com/)  
🐝 [github.com/CharlesJGantt](https://github.com/CharlesJGantt)

<!-- MARKDOWN LINKS & BADGES -->
[contributors-shield]: https://img.shields.io/github/contributors/CharlesJGantt/ClimaPi-Dashboard.svg?style=for-the-badge
[contributors-url]: https://github.com/CharlesJGantt/ClimaPi-Dashboard/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/CharlesJGantt/ClimaPi-Dashboard.svg?style=for-the-badge
[forks-url]: https://github.com/CharlesJGantt/ClimaPi-Dashboard/network/members
[stars-shield]: https://img.shields.io/github/stars/CharlesJGantt/ClimaPi-Dashboard.svg?style=for-the-badge
[stars-url]: https://github.com/CharlesJGantt/ClimaPi-Dashboard/stargazers
[issues-shield]: https://img.shields.io/github/issues/CharlesJGantt/ClimaPi-Dashboard.svg?style=for-the-badge
[issues-url]: https://github.com/CharlesJGantt/ClimaPi-Dashboard/issues
[license-shield]: https://img.shields.io/github/license/CharlesJGantt/ClimaPi-Dashboard.svg?style=for-the-badge
[license-url]: https://github.com/CharlesJGantt/ClimaPi-Dashboard/blob/main/LICENSE
