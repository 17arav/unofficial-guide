import os

def chunk_text(text, chunk_size=500, overlap=100):
    """Splits text into chunks of `chunk_size` with `overlap`."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        # Move the start pointer forward, but step back by the overlap amount
        start = start + chunk_size - overlap
    return chunks

def load_and_chunk_documents(data_dir="data"):
    all_chunks = []
    
    # Loop through every file in the data folder
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
                
                # We skip empty files
                if len(text) == 0:
                    continue
                
                # Chunk the document
                doc_chunks = chunk_text(text, chunk_size=500, overlap=100)
                
                # Save the chunk along with where it came from (metadata)
                for i, chunk in enumerate(doc_chunks):
                    all_chunks.append({
                        "id": f"{filename}_chunk_{i}",
                        "text": chunk,
                        "metadata": {"source": filename}
                    })
                    
    return all_chunks

if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    
    print(f"Total chunks created: {len(chunks)}\n")
    print("Here are 5 representative chunks for inspection:\n")
    
    # Print the first 5 chunks to visually inspect them
    for i in range(min(5, len(chunks))):
        print(f"--- Chunk {i+1} (Source: {chunks[i]['metadata']['source']}) ---")
        print(chunks[i]["text"])
        print("-" * 50 + "\n")