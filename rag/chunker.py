def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits text into overlapping chunks for RAG
    """

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        # move forward with overlap
        start = end - overlap

    return chunks