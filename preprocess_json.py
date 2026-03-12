import requests
import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib

# Create embeddings for a list of texts using local embedding model
def create_embedding(text_list):
    r = requests.post('http://localhost:11434/api/embed',json={
        'model':'bge-m3',
        'input':text_list
    })
    embedding = r.json()['embeddings']
    print(embedding)
    return embedding

# Get all merged json transcript files
jsons = os.listdir('mergejsons')

my_dicts = []
chunk_id = 0

for json_file in jsons:

    # Load merged json file
    with open(f'jsons/{json_file}') as f:
        content = json.load(f)

    print(f'creating embeddings for {json_file}')
    
    # Generate embeddings for each chunk text
    embeddings = create_embedding([c['text'] for c in content['chunks']])

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
