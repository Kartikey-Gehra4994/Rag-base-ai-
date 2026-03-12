# RAG Based AI Teaching Assistant

This project builds a **Retrieval Augmented Generation (RAG)** based AI assistant that can answer questions from your own course videos.

The system converts course videos into text, creates embeddings, and retrieves the most relevant parts of the lecture to answer user questions using an LLM.

---

# How the System Works

The pipeline works in the following steps:

1. **Collect Videos**
   Put all lecture videos inside the `videos` folder.

2. **Convert Video to MP3**
   The script extracts audio from videos using `ffmpeg`.

3. **Convert MP3 to Text (JSON)**
   The Whisper model converts audio into transcript chunks with timestamps.

4. **Merge Chunks**
   Small transcript chunks are merged together to create better context for retrieval.

5. **Create Embeddings**
   Each chunk of text is converted into vector embeddings using the `bge-m3` model.

6. **User Query + Retrieval**
   When a user asks a question:

   * The question is converted into an embedding
   * Cosine similarity finds the most relevant chunks
   * These chunks are sent to the LLM

7. **Generate Answer**
   The LLM generates a human-like answer and tells the user which **video and timestamp** contains the explanation.

---

# Project Structure

```
project/
│
├── videos/                # Input lecture videos
├── audios/                # Extracted MP3 files
├── jsons/                 # Whisper transcript files
├── mergejsons/            # Merged transcript chunks
├── embed_merged_json/     # Vector embeddings (joblib)
│
├── video_to_mp3.py        # Convert videos to mp3
├── mp3_to_json.py         # Convert audio to transcript JSON
├── merge_chunks.py        # Merge small transcript chunks
├── preprocess_json.py     # Create embeddings
├── process_incomming.py   # Ask questions to the AI assistant
│
└── README.md
```

---

# Requirements

Install the required libraries:

```
pip install pandas numpy scikit-learn joblib requests openai-whisper
```

You also need:

* **FFmpeg** installed
* **Ollama** running locally
* Models:

  * `bge-m3` (for embeddings)
  * `llama3.2` (for answering)

Run:

```
ollama pull bge-m3
ollama pull llama3.2
```

---

# How to Run the Project

### Step 1 — Add Videos

Put your course videos in the `videos` folder.

---

### Step 2 — Convert Videos to Audio

```
python video_to_mp3.py
```

This creates MP3 files inside `audios/`.

---

### Step 3 — Convert Audio to Text

```
python mp3_to_json.py
```

This generates transcript JSON files inside `jsons/`.

---

### Step 4 — Merge Transcript Chunks

```
python merge_chunks.py
```

Merged chunks will be saved in `mergejsons/`.

---

### Step 5 — Create Embeddings

```
python preprocess_json.py
```

This creates:

```
embed_merged_json/embedding.joblib
```

---

### Step 6 — Ask Questions

```
python process_incomming.py
```

Example:

```
Ask a Question: What is CSS Flexbox?
```

The AI will:

* Find the most relevant lecture
* Tell you **which video**
* Tell you **the timestamp**
* Give a human-like explanation

---

# Example Output

```
Video: CSS Flexbox Tutorial
Timestamp: 10:32 - 12:10

Explanation:
Flexbox is used to align items inside a container...
```

---

# Why RAG is Used

Large language models do not know your private course data.

RAG solves this problem by:

1. Retrieving relevant information from your data
2. Sending it to the LLM
3. Generating an accurate answer

---

# Future Improvements

Possible improvements:

* Add a **web interface (Streamlit / React)**
* Store embeddings in **vector databases like FAISS**
* Add **multi-language support**
* Add **YouTube video support**

---

# Author

Kartikey Gehra - Data Science Enthusiast
