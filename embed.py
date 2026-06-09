import os
from ingest import load_and_chunk_documents
from sentence_transformers import SentenceTransformer
import chromadb

def setup_vector_store():
    print("Loading and chunking raw documents...")
    chunks = load_and_chunk_documents()
    print(f"Loaded {len(chunks)} text chunks.")

    print("Initializing local embedding model (all-MiniLM-L6-v2)...")
    # This runs completely locally and will cache the model files on your device
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Initializing local vector store...")
    # Using a persistent client saves the database files to disk inside a '.chroma_db' folder
    chroma_client = chromadb.PersistentClient(path=".chroma_db")
    
    # Reset or create the collection
    collection_name = "campus_dining_guide"
    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    collection = chroma_client.create_collection(name=collection_name)

    print("Embedding chunks and storing them in ChromaDB...")
    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    
    # Generate embeddings locally
    embeddings = model.encode(texts).tolist()

    # Add items to our vector database
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )
    print("Vector database setup complete!")
    return collection, model

def retrieve_context(query, collection, model, k=4):
    """Encodes a search query and returns the top-k most semantically matching text chunks."""
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    
    # Format and return the extracted documents and their metadata
    retrieved_chunks = []
    if results and results["documents"]:
        for i in range(len(results["documents"][0])):
            retrieved_chunks.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i] if "distances" in results else None
            })
    return retrieved_chunks

if __name__ == "__main__":
    # Build database
    collection, model = setup_vector_store()
    
    # Quick test queries from our Evaluation Plan
    test_queries = [
        "Which meal plan should incoming freshmen buy?",
        "Is the Barrett dining hall worth the extra cost?",
        "What is the best way to use M&G dollars?"
    ]
    
    print("\n" + "="*40 + "\nRUNNING RETRIEVAL TESTS\n" + "="*40)
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        chunks = retrieve_context(query, collection, model, k=4)
        
        for idx, chunk in enumerate(chunks):
            print(f"  [{idx+1}] Source: {chunk['source']} (Distance: {chunk['distance']:.4f})")
            print(f"      Text: {chunk['text']}\n")