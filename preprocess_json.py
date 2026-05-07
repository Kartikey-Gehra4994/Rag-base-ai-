import requests
import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import cohere
from dotenv import load_dotenv
load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def create_embedding(text):
    response = co.embed(
        texts=text,
        model="embed-english-v3.0",
        input_type="search_document" 
    )
    return response.embeddings

# Get all merged json transcript files
jsons = os.listdir('merge_jsons')

my_dicts = []
chunk_id = 0

for json_file in jsons:

    # Load merged json file
    with open(f'jsons/{json_file}') as f:
        content = json.load(f)

    print(f'creating embeddings for {json_file}')
    
    # Generate embeddings for each chunk text
    texts = [c['text'] for c in content['chunks']]
    embeddings = create_embedding(texts)

    print("chunks:", len(texts))
    print("embeddings:", len(embeddings))

    for i, chunk in enumerate(content['chunks']):
        
        # Add unique id and embedding to each chunk
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        
        chunk_id += 1
        my_dicts.append(chunk)

# Convert all chunks into dataframe
df = pd.DataFrame.from_records(my_dicts) # Save this dataframe

# Save dataframe with embeddings for later retrieval (RAG search)
joblib.dump(df, 'embed_merged_json/embedding.joblib')
