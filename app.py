from flask import Flask, render_template, request
import requests
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from groq import Groq
from dotenv import load_dotenv

# load env
load_dotenv()

app = Flask(__name__)

# Load embeddings once when server starts
df = joblib.load('embed_merged_json/embedding.joblib')

# Create embedding for user query
def create_embedding(text_list):
    r = requests.post('http://localhost:11434/api/embed',json={
        'model':'bge-m3',
        'input':text_list
    })
    embedding = r.json()['embeddings']
    return embedding

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def inference(prompt):

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return chat.choices[0].message.content

@app.route("/")
def home():
    return render_template('index.html', answer=None)

@app.route("/ask", methods=['POST'])
def ask():
    question = request.form['question']
    print("Question received")
    print('Thinking...')
    question_embadding = create_embedding([question])[0]

    # Calculate similarity between question and stored embeddings
    similaritis = cosine_similarity(np.vstack(df['embedding']), [question_embadding]).flatten()
    # print(similaritis)

    top_results = 3

    # Select top most relevant chunks
    max_idx = similaritis.argsort()[::-1][0:top_results]
    new_df = df.iloc[max_idx]
    # print(new_df)

    # Create prompt using retrieved video chunks
    prompt = f"""
    You are an AI assistant helping students learn from the Sigma Web Development Course.

    Below are some subtitle chunks extracted from course videos. 
    Each chunk contains:
    - video title
    - video number
    - start time 
    - end time 
    - spoken text

    Course Context:
    {new_df[['title','number','start','end','text']].to_json(orient='records')}

    Student Question:
    "{question}"

    Instructions:

    1. Answer the question using ONLY the information from the provided course context.
    2. Clearly mention:
    - Video number
    - Approximate timestamp where the topic is explained
    3. Explain the answer in a simple and helpful way, like a teacher guiding a student.
    4. If multiple chunks relate to the question, combine the information.
    5. Do NOT mention the raw JSON or data format in your answer.
    6. If the question is unrelated to the course, politely say that you can only answer questions related to the Sigma Web Development course.

    Response Format:

    Topic:
    Video Number:
    Timestamp:
    Explanation:

    If the answer cannot be found in the provided context, say:
    "I couldn't find this topic in the Sigma Web Development course videos."
"""

    ## send prompt and get responce from LLM
    responce = inference(prompt)
    print("Generating answer...")

    return render_template('index.html', answer=responce)

if __name__ == "__main__":
    app.run(debug=True)