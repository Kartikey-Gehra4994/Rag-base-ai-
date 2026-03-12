import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import numpy as np
import joblib
# from openai import OpenAI
# from config import api_key

# Create embedding for user query
def create_embedding(text_list):
    r = requests.post('http://localhost:11434/api/embed',json={
        'model':'bge-m3',
        'input':text_list
    })
    embedding = r.json()['embeddings']
    return embedding

# Send prompt to local LLM and get response
def inference(prompt):
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': 'llama3.2',
        'prompt':  prompt,
        'stream': False
    })
    responce = r.json()
    return responce

# Send prompt to Openai LLM using api and get response
# client = OpenAI(api_key=api_key)
# def inference_openai(prompt):
#     response = client.responses.create(
#     model="gpt-5.4",
#     input=prompt
#     )
#     print(response.output_text)
#     return response.output_text

# Load embeddings dataframe created earlier
df = joblib.load('embed_merged_json/embedding.joblib')

# Get question from user
incoming_query = input('Ask a Question: ')
print('Thinking...')

# Convert user question into embedding
question_embadding = create_embedding([incoming_query])[0]

# Calculate similarity between question and stored embeddings
similaritis = cosine_similarity(np.vstack(df['embedding']), [question_embadding]).flatten()

top_results = 3

# Select top most relevant chunks
max_idx = similaritis.argsort()[::-1][0:top_results]
new_df = df.iloc[max_idx]

# Create prompt using retrieved video chunks
prompt = f'''I am teaching web development in my Sigma web development course. Here are video subtitle chunks containing video title,
video number, start time in seconds, end time in seconds, the text at that time:

{new_df[['title', 'number', 'start', 'end', 'text']].to_json(orient='records')}
`````````````````````````````````````````````
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much 
content is taught in which video (in which video and at what timestamp) and guide the user to go 
to that particular video. If user asks unrelated question, tell him that you can only answer 
questions related to the course
'''

## send prompt and get responce from LLM
responce = inference(prompt)['response'] # llama3.2 responce
print(responce)

## save responce into responce.txt
with open('responce.txt', 'w') as f:
    f.write(responce)
