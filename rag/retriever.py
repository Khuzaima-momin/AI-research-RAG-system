"""
Enterprise Retrieval Module
---------------------------
Responsible for retrieving the most relevant chunks
from the Chroma vector database.
"""

from rag.database import collection
from rag.embeddings import get_embedding


def retrieve_chunks(query: str, top_k: int = 5):
    """
    Retrieve the most relevant document chunks.

    Parameters
    ----------
    query : str
        User question.

    top_k : int
        Number of chunks to retrieve.

    Returns
    -------
    dict
        Clean retrieval results.
    """

    try:

        # -----------------------------
        # Generate query embedding
        # -----------------------------
        query_embedding = get_embedding(query)

        # -----------------------------
        # Search Vector Database
        # -----------------------------
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        cleaned_documents = []
        cleaned_metadata = []
        cleaned_distances = []

        seen = set()

        # -----------------------------
        # Remove duplicate chunks
        # -----------------------------
        for doc, meta, distance in zip(documents, metadatas, distances):

            if not doc:
                continue

            doc = doc.strip()

            if doc in seen:
                continue

            seen.add(doc)

            cleaned_documents.append(doc)
            cleaned_metadata.append(meta)
            cleaned_distances.append(distance)

        print("\n========== RETRIEVAL ==========")
        print("Query:", query)
        print("Retrieved Chunks:", len(cleaned_documents))

        for i, (doc, dist) in enumerate(zip(cleaned_documents,
                                            cleaned_distances), start=1):

            preview = doc[:120].replace("\n", " ")

            print(f"\nChunk {i}")
            print(f"Distance : {dist:.4f}")
            print(f"Preview  : {preview}...")

        print("===============================\n")

        return {
            "documents": [cleaned_documents],
            "metadatas": [cleaned_metadata],
            "distances": [cleaned_distances]
        }

    except Exception as e:

        print("\nRETRIEVAL ERROR")
        print(str(e))

        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }


def build_context(chunks):
    """
    Convert retrieved chunks into a single context string
    that will be passed to Gemini.
    """

    if not chunks:
        return ""

    context = ""

    for i, chunk in enumerate(chunks, start=1):

        context += f"\n\n===== Document Chunk {i} =====\n"
        context += chunk

    return context.strip()