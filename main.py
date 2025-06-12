import os
from pydub import AudioSegment
import subprocess


def send_notification(title: str, message: str):
    subprocess.run(["notify-send", title, message])


def enhance_audio_quality(input_file: str, output_dir: str):
    audio = AudioSegment.from_file(input_file)
    normalized = audio.apply_gain(-audio.max_dBFS)
    highs = normalized.high_pass_filter(6000).apply_gain(4.0)
    lows = normalized.low_pass_filter(6000)
    enhanced = lows.overlay(highs)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(input_file))
    enhanced.export(output_path, format="mp3")
    return output_path


# Paths
input_dir = os.path.expanduser("~/Downloads/import")
output_dir = os.path.expanduser("~/Downloads/output")
files = [f for f in os.listdir(input_dir) if f.endswith(".mp3")]

total = len(files)

for i, file in enumerate(files, start=1):
    full_path = os.path.join(input_dir, file)
    print(f"[{i}/{total}] Processing {file}...")
    enhance_audio_quality(full_path, output_dir)
    percent = int((i / total) * 100)
    print(f"→ Done ({percent}%)")

send_notification("Audio Enhancement", "All files processed successfully!")
