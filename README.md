# 🍳 The Unofficial Guide: ASU Campus Dining Hacks

An intelligent, strictly grounded Retrieval-Augmented Generation (RAG) application that surfaces unofficial campus dining tips, reviews, and hacks for students. This system uses semantic search to bypass official marketing materials and find genuine student consensus regarding meal plans, M&G dollars, and dining hall quality.

## 🏗️ System Architecture

1. **Ingestion:** Raw text documents are scraped/compiled into individual source files within the `data/` directory.
2. **Chunking:** Text is processed via `ingest.py` into fixed 500-character blocks with a 100-character slide overlap to preserve conversational context.
3. **Vector Database:** Chunks are converted into 384-dimensional dense vector embeddings using the local `all-MiniLM-L6-v2` transformer model and stored in a local, persistent `ChromaDB` instance.
4. **Retrieval & Guardrails:** Queries pull the top 4 (`k=4`) context chunks. A deterministic system prompt strictly restricts the LLM from hallucinating or using out-of-network knowledge.
5. **Generation & UI:** The interface is served via `Gradio`, querying the `llama-3.3-70b-versatile` model on Groq for sub-second, fully cited text generation.

## 🚀 Getting Started

### 1. Clone and Initialize Environment
```bash
git clone [https://github.com/17arav/unofficial-guide.git](https://github.com/17arav/unofficial-guide.git)
cd unofficial-guide
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt


2. Configure Credentials
Create a .env file in the root directory:

GROQ_API_KEY=your_actual_groq_api_key_here

3. Build the Database and Launch
Bash
# Populate the raw text files
python fill_data.py

# Ingest, chunk, embed, and index documents
python embed.py

# Launch the interactive web UI
python app.py

Open your browser and navigate to http://127.0.0.1:7860.

🧪 Evaluation & Test Cases
The model is explicitly aligned against 5 core baseline student inquiries:

Freshman Strategy: Recommends minimal meal plans supplemented by flexible spending.

Barrett Premium Valuation: Flags the premium price point as historically inefficient for average users.

M&G Optimization: Guides users to prioritize external retail chains on campus rather than dining hall entries.

Meal Exchange Monitoring: Explains the reduction in value due to vendor policy shifts.

Local Folklore: Identifies high-performing localized items like dining hall sugar cookies.