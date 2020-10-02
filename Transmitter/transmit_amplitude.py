try:
    import pyaudio
    import numpy as np
    import time
    import sys
except:
    print("Something didn't import")

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
RATE = 16000
CHUNK = 1024 # 1024bytes of data red from a buffer
RECORD_SECONDS = 0.1

audio = pyaudio.PyAudio()

# chosen_device_index = -1
# for x in range(0,audio.get_device_count()):
#     info = audio.get_device_info_by_index(x)
#     # print(audio.get_device_info_by_index(x))
#     if info["name"] == "pulse":
#         chosen_device_index = info["index"]
#         print("Chosen index: ", chosen_device_index)

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    # input_device_index=chosen_device_index)
                    frames_per_buffer=CHUNK)

global keep_going
keep_going = True



# Open the connection and start streaming the data
stream.start_stream()
print("\n+---------------------------------+")
print("| Press Ctrl+C to Break Recording |")
print("+---------------------------------+\n")

# Loop so program doesn't end while the stream callback's
# itself for new data
while keep_going:
    chunk = stream.read(CHUNK)
    decoded = numpy.fromstring(data, 'Float32');
    print(decoded)

    except KeyboardInterrupt:
        keep_going=False

# Close up shop (currently not used because KeyboardInterrupt
# is the only way to close)
stream.stop_stream()
stream.close()

audio.terminate()