import whisper
import json
import os

# Load Whisper model for speech-to-text
model = whisper.load_model('large-v2')

# Get all mp3 files from audios folder
audios = os.listdir('audios')

for audio in audios:
    print(audio)

    # Process only files that follow the pattern: number_title.mp3
    if('_' in audio):

        # Extract lecture number and title from file name
        number = audio.split('_')[0]
        title = audio.split('_')[1][:-5]
        print(number, title)

        # Convert audio to text using Whisper
        result = model.transcribe(
            audio=f'audios/{audio}',
            language='hi',
            task='translate',
            word_timestamps=False
            )

        print(result)
            
        chunks = []

        # Create small text chunks with timestamps
        for segment in result['segments']:
            chunks.append({
                'number': number, 
                'title':title, 
                'start': segment['start'], 
                'end': segment['end'], 
                'text': segment['text']
                })
        # Store chunks and full transcript
        chunks_with_metedata = {
            'chunks': chunks, 
            'text': result['text']
            }

        print(chunks_with_metedata)
        
        # Save transcript data as JSON file
        with open(f'jsons/{audio}.json', 'w') as f:
            json.dump(chunks_with_metedata, f)