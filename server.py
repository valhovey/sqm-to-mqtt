#!/usr/bin/python3

import serial
import json

def get_config():
    with open('config.json', 'r') as file:
        return json.load(file)

config = get_config()
PORT = config["serial-path"]
BAUD = config["baudrate"]

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

def parse_reading(reading):
    values = list(map(str.strip, reading.split(",")))
    sqm = float(values[1][:-1])
    temp = float(values[5][:-1])

    parsed = {
        "sqm": sqm,
        "temp_c": temp
    }

    return parsed

def get_mock_reading():
    return "r, 09.66m,0000012099Hz,0000000000c,0000000.000s, 024.8C"

if __name__ == "__main__":
    reading = get_mock_reading()
    parsed = parse_reading(reading)

    print(parsed)
