from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import os
import cohere
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

print("Loading embeddings...")
df = joblib.load("embed_merged_json/embedding.joblib")
print("Embeddings loaded!")

co = cohere.Client(
    os.getenv("COHERE_API_KEY")
    )

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
    )

# Create embedding for user query
def create_embedding(text):
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query" 
    )
    return response.embeddings[0]

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

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/ask")
def ask(request: QuestionRequest):

    question = request.question

    print("Question received:", question)
    print("Creating question embedding...")

    question_embedding = create_embedding(question)

    print("Calculating similarity...")

    similarities = cosine_similarity(
        np.vstack(df["embedding"]),
        [question_embedding]
    ).flatten()

    top_results = 3

    max_idx = similarities.argsort()[::-1][:top_results]

    new_df = df.iloc[max_idx]

    context = new_df[
        ["title", "number", "start", "end", "text"]
    ].to_json(
        orient="records"
    )

    prompt = f"""

    You are an AI assistant helping students learn from the Sigma Web Development Course.

    Your job is to help the user quickly find where a topic is taught in the course.

    USER QUESTION:
    {question}

    RELEVANT VIDEO CHUNKS:
    {context}

    INSTRUCTIONS:

    1. Answer only using the provided video chunks.
    2. Identify the most relevant video or videos.
    3. Provide the video number, video title, timestamp, and a short explanation.
    4. If multiple timestamps are relevant, mention them separately.
    5. Keep the answer concise and easy to read.
    6. Do not repeat the transcript unnecessarily.
    7. Do not invent any video number, title, timestamp, or information.
    8. Do not mention embeddings, chunks, retrieval, RAG, prompts, or internal processing.
    9. Use plain text only.
    10. Do not use Markdown formatting.
    11. Do not use symbols such as *, #, -, _, |, or emojis.
    12. Do not create tables.
    13. Write the answer naturally, like a professional human assistant.

    Use this simple structure:

    Topic Found

    Video: [Video Number]
    Title: [Video Title]
    Timestamp: [Start time] to [End time]

    What is taught:
    [Short 1–2 sentence explanation]

    Recommended starting point:
    Start at [timestamp] in Video [number].

    If another relevant section exists, write:

    Also relevant:
    [Timestamp] to [Timestamp]
    [Short description]

    If the retrieved content does not contain enough information, say:

    I couldn't find this topic in the retrieved course content.

    If the question is unrelated to the course, say:

    This question doesn't appear to be related to the course.
    """

    print("Generating answer...")

    response = inference(prompt)

    print("Answer generated successfully.")

    return {
        "answer": response
    }
