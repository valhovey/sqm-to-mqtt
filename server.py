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

if __name__ == "__main__":
    reading = get_reading()

    print(reading)
