import os
import time
import datetime
import requests
from pydub import AudioSegment
from subprocess import Popen, PIPE

# List of radio stations
RADIO_STATIONS = {
    "BBC World Service": "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    "Classic Rock": "http://stream-uk1.radioparadise.com/mp3-192",
    "Swiss Jazz" : "http://stream.srg-ssr.ch/m/rsj/mp3_128"
}

# Output directory
OUTPUT_DIR = "recorded_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Duration (random between 15 and 30 seconds)
import random

def record_audio(station_name, stream_url, duration):
    """Records audio from a given stream URL for a specific duration using ffmpeg."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{station_name.replace(' ', '_')}_{timestamp}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    print(f"Recording {station_name} for {duration} seconds...")
    
    command = [
        "ffmpeg",
        "-i", stream_url,
        "-t", str(duration),
        "-acodec", "mp3",
        "-y", filepath  # Overwrites existing file if any
    ]
    
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    process.communicate()

    if os.path.exists(filepath):
        print(f"Saved: {filepath}")
        return filepath, duration, timestamp
    else:
        print("Recording failed.")
        return None, None, None

# Store metadata
metadata_file = os.path.join(OUTPUT_DIR, "metadata.csv")
with open(metadata_file, "w") as meta:
    meta.write("Station Name, File Name, Timestamp, Duration (s)\n")

# Record 30 samples
for i in range(30):
    station_name, stream_url = random.choice(list(RADIO_STATIONS.items()))
    duration = random.randint(30, 50)  # Random duration between 30-90s
    filepath, recorded_duration, timestamp = record_audio(station_name, stream_url, duration)

    if filepath:
        # Save metadata
        with open(metadata_file, "a") as meta:
            meta.write(f"{station_name}, {filepath}, {timestamp}, {recorded_duration}\n")

    time.sleep(5)  # Pause between recordings

print("Audio dataset collection complete.")
