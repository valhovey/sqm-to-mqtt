# SQM to Home Assistant MQTT

<img width="300" alt="image" src="https://github.com/user-attachments/assets/10ebb31f-af1a-40eb-bbf3-5502d51a30f9" />

Hello! I built this script to handle reading data from a Unihedron [SQM-LU](https://unihedron.com/projects/sqm-lu/) USB sky quality meter (SQM) and broadcast the readings over MQTT to Home Assistant. I also added the ability to query data from an Ambient Weather station if you have an API and APP key.

## Setup

Required that you have:
* Home Assistant installed locally
* an MQTT server
* the MQTT Home Assistant integration set up
* a SQM-LU meter hooked up via USB to a computer that you can run this on

Optional:
* Ambient Weather station API and app key
* InfluxDB host to store data long-term
* Pirate Weather API key for cloud coverage

Start by copying over `config.example.json` to `config.json` and update values for your setup. Latitude and longitude are not broadcast, they are only used to calculate the moon metadata like altitude and illuminance. You can leave Ambient Weather disabled if you don't have that set up. You can also configure InfluxDB if you'd like to publish this data in a way that is long-lived (since Home Assistant only retains a short window of data).

This project is managed with `uv`, which you can get set up using [their documentation](https://docs.astral.sh/uv/guides/install-python/). Installation can be done with `uv sync`. Make sure to source the virtual env with `source .venv/bin/activate` to get the packages in your environment.

To run this script, just run `python server.py`. This will fire up all of the required tools to connect to the SQM meter/Ambient Weather/MQTT and will then broadcast the sensor data to Home Assistant. Each run is a single data point, so you'll likely want to use `crontab` to set this up to run periodically.

As an example, here is a crontab setup to run this script every minute:
```
* * * * * cd /home/val/Documents/Programs/Python/sqm-to-mqtt && ./.venv/bin/python server.py
```
