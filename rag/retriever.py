from rag.database import collection
from rag.embeddings import get_embedding


# -----------------------------
# SEARCH SIMILAR CHUNKS
# -----------------------------
def retrieve_chunks(query, top_k=3):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results