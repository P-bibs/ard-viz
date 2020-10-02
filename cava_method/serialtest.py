#!/usr/bin/python3
import os
import struct
import subprocess
import tempfile
import serial
import time



with serial.Serial("/dev/ttyACM0", 9600) as ser:
    print(ser.name)         # check which port was really used
    i = 0
    j = 0
    while True:
        i = i  + 1
        if (i > 1000):
            i = 0
            j += 1
            j = j % 255
            out_val = bytes([j])
            ser.write(out_val)
            print("Wrote: " + str(out_val))
        if (ser.in_waiting > 0):
            print(ser.read())
        
