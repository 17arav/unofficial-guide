import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
import gradio as gr

# Load environment variables manually from .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# Initialize the Groq client
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key or groq_api_key == "your_key_here":
    raise ValueError("CRITICAL: Please add a valid GROQ_API_KEY to your .env file!")

client = Groq(api_key=groq_api_key)

print("Connecting to local ChromaDB and embedding model...")
chroma_client = chromadb.PersistentClient(path=".chroma_db")
collection = chroma_client.get_collection(name="campus_dining_guide")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def ask_unofficial_guide(query):
    # 1. Retrieve the top 4 most relevant chunks
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=4)
    
    retrieved_chunks = []
    sources = set()
    
    if results and results["documents"]:
        for i in range(len(results["documents"][0])):
            text = results["documents"][0][i]
            source = results["metadatas"][0][i]["source"]
            retrieved_chunks.append(f"Source: {source}\nContent: {text}")
            sources.add(source)
            
    context = "\n\n---\n\n".join(retrieved_chunks)
    
    # 2. Craft a strict grounding system prompt
    system_prompt = (
        "You are 'The Unofficial Guide', a helpful AI assistant for campus dining advice. "
        "Your task is to answer the user's question using ONLY the provided context snippets below. "
        "Strict Guidelines:\n"
        "1. Do not use any outside knowledge or general facts.\n"
        "2. Ground every single claim in the provided documents.\n"
        "3. You must explicitly mention the source filename (e.g., source_1.txt) when stating facts.\n"
        "4. If the provided context does not contain the answer, state exactly: "
        "'I do not have enough information in my database to answer that question.'"
    )
    
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"
    
    # 3. Call the Groq LLM
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Low temperature keeps the model deterministic and literal
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"Error calling Groq API: {str(e)}"
        
    return answer, "\n".join(sorted(list(sources)))

# 4. Define the Gradio Interface
with gr.Blocks(title="The Unofficial Guide: ASU Campus Dining Hacks") as demo:
    gr.Markdown("# 🍳 The Unofficial Guide: ASU Campus Dining Hacks")
    gr.Markdown("Ask plain-language questions about dining halls, M&G dollars, and meal plans to get grounded, cited answers.")
    
    with gr.Row():
        with gr.Column():
            query_input = gr.Textbox(label="Your Question", placeholder="e.g., Which meal plan should incoming freshmen buy?", lines=2)
            submit_btn = gr.Button("Ask the Guide", variant="primary")
            
    with gr.Row():
        with gr.Column():
            answer_output = gr.Textbox(label="Grounded Answer", lines=8, interactive=False)
            sources_output = gr.Textbox(label="Retrieved Document Sources", lines=3, interactive=False)
            
    # Set up actions for clicking the button or pressing enter
    submit_btn.click(ask_unofficial_guide, inputs=query_input, outputs=[answer_output, sources_output])
    query_input.submit(ask_unofficial_guide, inputs=query_input, outputs=[answer_output, sources_output])

if __name__ == "__main__":
    # Launch the web app locally
    demo.launch(server_name="127.0.0.1", server_port=7860)