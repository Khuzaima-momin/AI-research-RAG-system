from google import genai
from config import Config

# Initialize client
client = genai.Client(api_key=Config.GEMINI_API_KEY)


# -----------------------------
# GENERATE ANSWER
# -----------------------------
def generate_answer(query, context_chunks):

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI Research Assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{query}

If answer is not in context, say "Not found in documents".
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text