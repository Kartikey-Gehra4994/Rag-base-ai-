import os 
import subprocess

# Get all video files from videos folder
files = os.listdir('videos')

for file in files:

    # Extract tutorial number and title from file name
    tutorial_number = file.split('#')[1].split(' -')[0]
    fiel_name = file.split(' Sigma')[0]
    
    print(tutorial_number, fiel_name)
    
     # Convert video to MP3 using ffmpeg
    subprocess.run(['ffmpeg', '-i', f'videos/{file}', f'audios/{tutorial_number}_{fiel_name}.mp3'])