import os 
import subprocess

files = os.listdir('videos')
for file in files:
    tutorial_number = file.split('#')[1].split(' -')[0]
    fiel_name = file.split(' Sigma')[0]
    print(tutorial_number, fiel_name)
    subprocess.run(['ffmpeg', '-i', f'videos/{file}', f'audios/{tutorial_number}_{fiel_name}.mp3'])