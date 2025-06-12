import os
import subprocess
from pydub import AudioSegment


def send_notification(title: str, message: str):
    subprocess.run(["notify-send", title, message])


def enhance_audio_quality(input_file: str):
    bad_quality_audio = AudioSegment.from_file(input_file)

    # Normalize
    normalized_audio = bad_quality_audio.apply_gain(
        -bad_quality_audio.max_dBFS)

    # Simulate EQ
    highs = normalized_audio.high_pass_filter(6000).apply_gain(4.0)
    lows = normalized_audio.low_pass_filter(6000)
    enhanced_audio = lows.overlay(highs)

    # Ensure output directory exists
    output_dir = os.path.expanduser("~/Downloads/output")
    os.makedirs(output_dir, exist_ok=True)

    # Export the enhanced version
    file_name = os.path.basename(input_file)
    output_path = os.path.join(output_dir, file_name)
    enhanced_audio.export(output_path, format="mp3")
    print(f"Saved enhanced file to: {output_path}")


import_path = os.path.expanduser("~/Downloads/import")

for file in os.listdir(import_path):
    if file.endswith(".mp3"):
        full_path = os.path.join(import_path, file)
        send_notification("Processing Audio", f"Enhancing quality of {file}")

        enhance_audio_quality(full_path)

send_notification("Audio Processing Complete",
                  "All audio files have been processed and saved to ~/Downloads/output")
