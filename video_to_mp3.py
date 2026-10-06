# Convert videos to MP3 and organize existing MP3 files

import os
import shutil
import subprocess

video_folder = "videos"
audio_folder = "audios"

# Create audios folder if it doesn't exist
os.makedirs(audio_folder, exist_ok=True)

files = os.listdir(video_folder)

for file in files:

    # Extract tutorial number
    tutorial_number = file.split("#")[1].split(" -")[0]

    # Extract clean file name
    file_name = file.split("  Sigma")[0]

    # Remove extension if present
    file_name = os.path.splitext(file_name)[0]

    # Final output name
    output_file = f"{tutorial_number}_{file_name}.mp3"
    output_path = os.path.join(audio_folder, output_file)

    input_path = os.path.join(video_folder, file)

    print(f"Processing: {file}")
    print(f"Output: {output_file}")

    # If file is already MP3
    if file.lower().endswith(".mp3"):

        shutil.copy2(input_path, output_path)

    # Otherwise convert video to MP3
    else:

        subprocess.run([
            "ffmpeg",
            "-i", input_path,
            "-vn",
            "-acodec", "libmp3lame",
            output_path
        ])

print("All files processed successfully!")