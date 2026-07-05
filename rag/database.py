"""
Enterprise Vector Database Module
---------------------------------
Handles all interaction with ChromaDB.

Features
--------
✓ Persistent Vector Database
✓ Rich Metadata Storage
✓ Duplicate-safe IDs
✓ Collection Statistics
✓ Delete Documents
✓ Clear Database
✓ Professional Logging
"""

import uuid
from datetime import datetime

import chromadb


# ==========================================================
# Create / Load Persistent Database
# ==========================================================

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="research_docs"
)


# ==========================================================
# Add Document Chunks
# ==========================================================

def add_chunks_to_db(chunks, embeddings, file_name):
    """
    Store document chunks inside ChromaDB.

    Parameters
    ----------
    chunks : list
        Document chunks.

    embeddings : list
        Embedding vectors.

    file_name : str
        Uploaded file name.
    """

    ids = []
    documents = []
    metadatas = []

    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n========== INDEXING ==========")
    print("File :", file_name)
    print("Chunks :", len(chunks))

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):

        chunk_id = str(uuid.uuid4())

        ids.append(chunk_id)

        documents.append(chunk)

        metadatas.append({

            "source": file_name,

            "chunk_number": index,

            "upload_time": upload_time,

            "character_count": len(chunk),

            "document_type": file_name.split(".")[-1].lower()

        })

        print(
            f"Chunk {index:02d} | "
            f"Characters: {len(chunk)}"
        )

    collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas

    )

    print("Indexing Complete")
    print("==============================\n")


# ==========================================================
# Vector Search
# ==========================================================

def search_similar(query_embedding, top_k=5):
    """
    Perform similarity search.
    """

    return collection.query(

        query_embeddings=[query_embedding],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )


# ==========================================================
# Collection Statistics
# ==========================================================

def collection_stats():
    """
    Display collection statistics.
    """

    count = collection.count()

    print("\n========== DATABASE ==========")
    print("Stored Chunks :", count)
    print("==============================\n")

    return count


# ==========================================================
# Delete Entire Collection
# ==========================================================

def clear_database():
    """
    Remove every indexed chunk.
    """

    all_data = collection.get()

    if all_data["ids"]:

        collection.delete(ids=all_data["ids"])

        print("Database Cleared")

    else:

        print("Database Already Empty")


# ==========================================================
# Delete One Document
# ==========================================================

def delete_document(file_name):
    """
    Delete all chunks belonging to one document.
    """

    data = collection.get()

    ids_to_delete = []

    metadatas = data.get("metadatas", [])

    ids = data.get("ids", [])

    for doc_id, metadata in zip(ids, metadatas):

        if metadata.get("source") == file_name:

            ids_to_delete.append(doc_id)

    if ids_to_delete:

        collection.delete(ids=ids_to_delete)

        print(f"Deleted document: {file_name}")

    else:

        print("Document not found.")