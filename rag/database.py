import chromadb
from chromadb.config import Settings


# Create or load vector database
client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="research_docs"
)


# -----------------------------
# ADD CHUNKS TO VECTOR DB
# -----------------------------
def add_chunks_to_db(chunks, embeddings, file_name):
    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"{file_name}_{i}")
        documents.append(chunk)
        metadatas.append({
            "source": file_name,
            "chunk_id": i
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


# -----------------------------
# SEARCH FUNCTION
# -----------------------------
def search_similar(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results