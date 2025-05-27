<!-- Improved compatibility of back to top link -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/CharlesJGantt/benchPi-Dashboard">
    <img src="docs/dashboard-preview.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">benchPi-Dashboard</h3>

  <p align="center">
    A Flask-powered Raspberry Pi dashboard for real-time weather, system stats, and aircraft tracking.
    <br />
    <a href="https://github.com/CharlesJGantt/benchPi-Dashboard"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/CharlesJGantt/benchPi-Dashboard/issues">Report Bug</a>
    ·
    <a href="https://github.com/CharlesJGantt/benchPi-Dashboard/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>📘 Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

![Product Screenshot](docs/dashboard-preview.png)

`benchPi-Dashboard` is a lightweight, real-time web dashboard for Raspberry Pi devices. It provides:

- 🌦 Live weather from OpenWeatherMap
- 💻 System stats (CPU temp, uptime, timestamp)
- ✈️ Aircraft tracking via `dump1090-fa`
- 📊 Historical data charts (Chart.js + Bootstrap tabs)
- 🔐 Secure secret config and logging design

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

* [Python 3.9+](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [Chart.js](https://www.chartjs.org/)
* [Bootstrap 5](https://getbootstrap.com/)
* [OpenWeatherMap API](https://openweathermap.org/)
* [dump1090-fa](https://github.com/flightaware/dump1090)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

```bash
sudo apt update
sudo apt install python3-pip git
pip3 install flask requests
```

### Installation

1. Clone the repo

```bash
git clone git@github.com:CharlesJGantt/benchPi-Dashboard.git
cd benchPi-Dashboard
```

2. Copy the config template

```bash
cp config_example.py config.py
```

3. Add your OpenWeatherMap API key and location

```python
# config.py
OPENWEATHER_API_KEY = "your_api_key"
LATITUDE = 33.5296
LONGITUDE = -81.8344
```

4. Start the app

```bash
python3 app.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Visit the dashboard at:

```
http://<raspberry-pi-ip>:5000
```

### Chart Tabs:
- 🌡 Temp, Feels Like, Humidity
- 💨 Wind Speed
- 📈 Pressure

Weather logs are stored at:

```
/home/benchpi/pi-dashboard/logs/weather_log.json
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [x] Historical weather charting
- [x] Secrets handling via config.py
- [ ] Add Docker support
- [ ] Auto-restart on crash/system reboot
- [ ] Real-time chart updates (AJAX/WebSocket)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Pull requests welcome!

1. Fork the repo  
2. Create your branch (`git checkout -b feature/my-feature`)  
3. Commit your changes  
4. Push to GitHub  
5. Open a pull request  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

**Charles Gantt**  
📬 [charlesjgantt.com](https://charlesjgantt.com)  
🐙 [github.com/CharlesJGantt](https://github.com/CharlesJGantt)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & BADGES -->
[contributors-shield]: https://img.shields.io/github/contributors/CharlesJGantt/benchPi-Dashboard.svg?style=for-the-badge
[contributors-url]: https://github.com/CharlesJGantt/benchPi-Dashboard/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/CharlesJGantt/benchPi-Dashboard.svg?style=for-the-badge
[forks-url]: https://github.com/CharlesJGantt/benchPi-Dashboard/network/members
[stars-shield]: https://img.shields.io/github/stars/CharlesJGantt/benchPi-Dashboard.svg?style=for-the-badge
[stars-url]: https://github.com/CharlesJGantt/benchPi-Dashboard/stargazers
[issues-shield]: https://img.shields.io/github/issues/CharlesJGantt/benchPi-Dashboard.svg?style=for-the-badge
[issues-url]: https://github.com/CharlesJGantt/benchPi-Dashboard/issues
[license-shield]: https://img.shields.io/github/license/CharlesJGantt/benchPi-Dashboard.svg?style=for-the-badge
[license-url]: https://github.com/CharlesJGantt/benchPi-Dashboard/blob/main/LICENSE
