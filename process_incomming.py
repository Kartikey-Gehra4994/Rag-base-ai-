import os
from groq import Groq
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import numpy as np
import joblib
import cohere

# from openai import OpenAI
# from config import api_key

from dotenv import load_dotenv
load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Create embedding for user query
def create_embedding(text):
    response = co.embed(
        texts=text,
        model="embed-english-v3.0",
        input_type="search_document" 
    )
    return response.embeddings

# Send prompt to Groq LLM using api and get response
def inference(prompt):
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

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

1. Use plain text only.
2. Do not use Markdown formatting.
3. Do not use symbols such as *, #, -, _, |, or emojis.
4. Do not create tables.
5. Do not use headings with special characters.
6. Write the answer naturally, like a professional human assistant.
'''

## send prompt and get responce from LLM
responce = inference(prompt) # Groq responce
print(responce)

## save responce into responce.txt
with open('responce.txt', 'w') as f:
    f.write(responce)
