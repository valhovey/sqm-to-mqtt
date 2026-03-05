#!/usr/bin/python3

from skyfield.api import load, Topos
from skyfield.almanac import fraction_illuminated
from datetime import datetime, timezone
import serial
import json
import requests

def get_config():
    with open('config.json', 'r') as file:
        return json.load(file)

config = get_config()
PORT = config["serial-path"]
BAUD = config["baudrate"]
LAT = config["lat"]
LON = config["lon"]
AMBIENT_WEATHER_ENABLE = config["ambient_weather_enable"]
AMBIENT_API_KEY = config["ambient_weather"]["api_key"]
AMBIENT_APP_KEY = config["ambient_weather"]["app_key"]

def get_ambient_weather():
    url = "https://api.ambientweather.net/v1/devices"
    params = {
        "apiKey": AMBIENT_API_KEY,
        "applicationKey": AMBIENT_APP_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    devices = response.json()

    if not devices:
        print("No stations found")
        exit()

    # Each device contains a list of data points
    device = devices[0]

    last_data = device["lastData"]

    temperature = last_data.get("tempf")
    humidity = last_data.get("humidity")
    pressure = last_data.get("baromrelin")
    tempc = round((temperature - 32) * (5/9), 2)

    ambient = {
        "air_temp_c": tempc,
        "humidity_rh": humidity,
        "pressure_inHg": pressure
    }

    return ambient

def get_reading():
    with serial.Serial(
            port=PORT,
            baudrate=BAUD,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2
        ) as ser:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(b"rx\n")
        line = ser.readline()

        return line.decode(errors="replace").strip()

def get_moon_stats(now):
    eph = load('de421.bsp')
    moon = eph['moon']
    earth = eph['earth']
    observer = earth + Topos(latitude_degrees=LAT, longitude_degrees=LON)
    astrometric = observer.at(now).observe(moon)
    alt, az, _ = astrometric.apparent().altaz()
    illum = fraction_illuminated(eph, 'moon', now)

    moon = {
        "moon_alt_deg": round(alt.degrees, 2),
        "moon_az_deg": round(az.degrees, 2),
        "moon_illum": round(illum * 100, 2),
    }

    return moon

def parse_reading(reading):
    values = list(map(str.strip, reading.split(",")))
    sqm = float(values[1][:-1])
    temp = float(values[5][:-1])

    parsed = {
        "sqm": sqm,
        "sensor_temp_c": temp
    }

    return parsed

def get_all_data():
    ts = load.timescale()
    now_utc = datetime.now(timezone.utc)
    now = ts.from_datetime(now_utc)
    reading = get_reading()
    parsed = parse_reading(reading)
    moon = get_moon_stats(now)
    ambient = get_ambient_weather()

    return {
        "now": now_utc.isoformat(),
        **parsed,
        **moon,
        **ambient
    }

def get_mock_reading():
    return "r, 09.66m,0000012099Hz,0000000000c,0000000.000s, 024.8C"

if __name__ == "__main__":
    values = get_all_data()
    
    print(values)
