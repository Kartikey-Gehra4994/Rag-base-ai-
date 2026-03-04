import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import numpy as np
import joblib

def create_embedding(text_list):
    r = requests.post('http://localhost:11434/api/embed',json={
        'model':'bge-m3',
        'input':text_list
    })
    embedding = r.json()['embeddings']
    return embedding

df = joblib.load('embed/embedding.joblib')

incoming_query = input('Ask a Question: ')
question_embadding = create_embedding([incoming_query])[0]

# Find similariys of question_embadding with other embeddings
# similarities = cosine_similarity(df['embedding'].values, )
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)

similaritis = cosine_similarity(np.vstack(df['embedding']), [question_embadding]).flatten()
top_results = 3
print(similaritis)
max_idx = similaritis.argsort()[::-1][0:top_results]
new_df = df.iloc[max_idx]
print(new_df[['title', 'number', 'text']])