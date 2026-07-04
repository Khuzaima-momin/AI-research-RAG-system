import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text.

    - Removes extra spaces
    - Removes repeated newlines
    - Preserves paragraph structure
    """

    text = re.sub(r"\r", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=700, overlap=150):
    """
    Creates overlapping chunks for Retrieval-Augmented Generation (RAG).

    Parameters
    ----------
    text : str
        Complete extracted document text.

    chunk_size : int
        Maximum characters inside one chunk.

    overlap : int
        Number of overlapping characters between chunks.

    Returns
    -------
    list
        List of clean text chunks.
    """

    text = clean_text(text)

    if not text:
        return []

    chunks = []

    start = 0
    chunk_id = 1

    while start < len(text):

        end = start + chunk_size

        # Try not to cut a word in half
        if end < len(text):

            while end > start and text[end] != " ":
                end -= 1

        chunk = text[start:end].strip()

        if chunk:

            chunks.append(chunk)

            print(
                f"Chunk {chunk_id} | "
                f"Characters: {len(chunk)}"
            )

            chunk_id += 1

        start = max(end - overlap, start + 1)

    return chunks