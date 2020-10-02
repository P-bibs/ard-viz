#!/usr/bin/python3
import os
import struct
import subprocess
import tempfile
import serial

BARS_NUMBER = 10
# OUTPUT_BIT_FORMAT = "8bit"
OUTPUT_BIT_FORMAT = "16bit"
# RAW_TARGET = "/tmp/cava.fifo"
RAW_TARGET = "/dev/stdout"

conpat = """
[general]
bars = %d
framerate = 40
[output]
method = raw
raw_target = %s
bit_format = %s
"""

config = conpat % (BARS_NUMBER, RAW_TARGET, OUTPUT_BIT_FORMAT)
bytetype, bytesize, bytenorm = ("H", 2, 65535) if OUTPUT_BIT_FORMAT == "16bit" else ("B", 1, 255)


def run():
    with tempfile.NamedTemporaryFile() as config_file:
        config_file.write(config.encode())
        config_file.flush()

        process = subprocess.Popen(["cava", "-p", config_file.name], stdout=subprocess.PIPE)
        chunk = bytesize * BARS_NUMBER
        fmt = bytetype * BARS_NUMBER

        if RAW_TARGET != "/dev/stdout":
            if not os.path.exists(RAW_TARGET):
                os.mkfifo(RAW_TARGET)
            source = open(RAW_TARGET, "rb")
        else:
            source = process.stdout

        with serial.Serial("/dev/ttyACM0", 9600) as ser:
            max_amp = 0.1
            print(ser.name)         # check which port was really used
            while True:
                data = source.read(chunk)
                if len(data) < chunk:
                    break
                # sample = [i for i in struct.unpack(fmt, data)]  # raw values without norming
                sample = [i / bytenorm for i in struct.unpack(fmt, data)]

                max_amp = max(max(sample), max_amp)
                normalized_amplitudes = [ min(int((amp / max_amp) * 130), 130) for amp in sample]
                wire_val = bytes(normalized_amplitudes)
                # print(normalized_amplitudes)
                # print(wire_val)
                # print("")
                # print("Sending: " + str(normalized_amplitude))
                ser.write(wire_val)
                print(normalized_amplitudes)
                if (ser.in_waiting > 0):
                    print(int.from_bytes(ser.read(), "big"))
                    print("")
    



if __name__ == "__main__":
    run()