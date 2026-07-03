from sentence_transformers import SentenceTransformer

# Lightweight model (fast + good)
model = SentenceTransformer("all-MiniLM-L6-v2")


# Convert text → vector
def get_embedding(text):
    return model.encode(text).tolist()


# Convert multiple chunks → vectors
def get_embeddings(chunks):
    return model.encode(chunks).tolist()