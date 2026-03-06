# how to use this Rag ai teaching assistent on your own data 
## step 1 - Collect your videos
Move all your video files to the videos folder

## step 2 - Convert to mp3
Convert all the video files to mp3 by running video_to_mp3 

## step 3 - convert mp3 to json
Convert all the mp3 files to json by running mp3_to_json

## step 4 - convert the json files to vectors
Use the file preprocess_json to convert the json files to a dataframe with Embedding and save it as a joblib

## step 5 - Prompt genration and feeding to LLM
Read the joblib file and load it into the memory.then create a relavent prompt as per the user query and feed it to the LLM