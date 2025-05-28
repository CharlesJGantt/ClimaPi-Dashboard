import time
import json
import board
import adafruit_dht
import os
from datetime import datetime

# Paths
LOG_DIR = "/home/benchpi/pi-dashboard/logs"
LOG_FILE = os.path.join(LOG_DIR, "indoor_env_log.json")
os.makedirs(LOG_DIR, exist_ok=True)

# Sensor setup
dht_device = adafruit_dht.DHT22(board.D4)

def generate_vulcan(temp_c, humidity):
    return f"Room temp nominal. {temp_c:.1f}°C at {humidity:.1f}% humidity."

def generate_klingon(temp_f, humidity):
    return f"qo' veQ: {temp_f:.1f}°F, {humidity:.1f}% sogh. Qapla'!"

def log_env_data():
    try:
        temp_c = dht_device.temperature
        humidity = dht_device.humidity
        temp_f = temp_c * 9 / 5 + 32

        entry = {
            "timestamp": datetime.now().isoformat(timespec='seconds'),
            "temp_f": round(temp_f, 1),
            "temp_c": round(temp_c, 1),
            "humidity": round(humidity, 1),
            "vulcan": generate_vulcan(temp_c, humidity),
            "klingon": generate_klingon(temp_f, humidity)
        }

        with open(LOG_FILE, "a") as f:
            json.dump(entry, f)
            f.write("\n")
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(timespec='seconds'),
                "error": str(e)
            }) + "\n")

# Loop every 2 minutes
while True:
    log_env_data()
    time.sleep(120)
