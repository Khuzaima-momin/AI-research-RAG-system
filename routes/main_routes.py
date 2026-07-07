from flask import Blueprint, render_template, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename

# -----------------------------
# RAG MODULES
# -----------------------------
from rag.parser import extract_text
from rag.chunker import chunk_text
from rag.embeddings import get_embeddings
from rag.database import (
    add_chunks_to_db,
    clear_database
)
from rag.retriever import (
    retrieve_chunks,
    build_context
)
from rag.generator import generate_answer
from rag.memory import memory

# -----------------------------
# Blueprint
# -----------------------------
main = Blueprint("main", __name__)

# -----------------------------
# Configuration
# -----------------------------
UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================================
# FILE VALIDATION
# ==========================================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================================
# STANDARD JSON RESPONSES
# ==========================================================

def success_response(query, answer, sources=None):

    return jsonify({

        "success": True,

        "query": query,

        "answer": answer,

        "sources": sources or []

    })


def error_response(message, code=400):

    return jsonify({

        "success": False,

        "error": message

    }), code


# ==========================================================
# HOME PAGE
# ==========================================================

@main.route("/")
def home():

    files = sorted(os.listdir(UPLOAD_FOLDER))

    return render_template(

        "index.html",

        files=files

    )


# ==========================================================
# HEALTH CHECK
# ==========================================================

@main.route("/health")
def health():

    return jsonify({

        "status": "healthy",

        "uploaded_documents": len(os.listdir(UPLOAD_FOLDER)),

        "conversation_messages": memory.size()

    })


# ==========================================================
# CLEAR CHAT MEMORY
# ==========================================================

@main.route("/clear-chat", methods=["POST"])
def clear_chat():

    memory.clear()

    return jsonify({

        "success": True,

        "message": "Conversation memory cleared."

    })
# ==========================================================
# UPLOAD DOCUMENT
# ==========================================================

@main.route("/upload", methods=["POST"])
def upload_file():

    print("\n========== UPLOAD STARTED ==========")

    # -----------------------------
    # Validate Request
    # -----------------------------
    if "file" not in request.files:
        return error_response("No file received.", 400)

    file = request.files["file"]

    if file.filename == "":
        return error_response("No file selected.", 400)

    if not allowed_file(file.filename):
        return error_response("Unsupported file type.", 400)

    # -----------------------------
    # Save File
    # -----------------------------
    filename = secure_filename(file.filename)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    print("Saved:", filepath)

    try:

        # -----------------------------
        # Extract Text
        # -----------------------------
        text = extract_text(filepath)

        if not text.strip():
            return error_response(
                "No readable text found in the uploaded document.",
                400
            )

        print("✓ Text extracted")

        # -----------------------------
        # Chunk Document
        # -----------------------------
        chunks = chunk_text(text)

        if len(chunks) == 0:
            return error_response(
                "Chunking failed.",
                500
            )

        print(f"✓ Chunks Created : {len(chunks)}")

        # -----------------------------
        # Create Embeddings
        # -----------------------------
        embeddings = get_embeddings(chunks)

        print("✓ Embeddings Created")


        # ---------------------------------
# Remove previous documents
# ---------------------------------
        clear_database()

        print("✓ Previous database cleared")

        # -----------------------------
        # Store in ChromaDB
        # -----------------------------
        add_chunks_to_db(
            chunks,
            embeddings,
            filename
        )

        print("✓ Stored in Vector Database")

        print("========== UPLOAD COMPLETE ==========\n")

        return jsonify({

            "success": True,

            "filename": filename,

            "chunks": len(chunks),

            "message": "Document indexed successfully."

        })

    except Exception as e:

        print("\nUPLOAD ERROR")
        print(str(e))

        return error_response(
            str(e),
            500
        )
    
    # ==========================================================
# CHAT API
# ==========================================================

@main.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        query = data.get("query", "").strip()

        if not query:
            return error_response("Empty query.", 400)

        # Save user message
        memory.add_user_message(query)

        # Retrieve relevant chunks
        results = retrieve_chunks(query)

        chunks = results.get("documents", [[]])[0]

        if not chunks:
            return success_response(
                query,
                "I couldn't find this information in the uploaded documents."
            )

        # Build context
        context = build_context(chunks)

        # Build conversation history
        history = memory.build_history()

        # Generate answer
        answer = generate_answer(
            query=query,
            context=context,
            conversation_history=history
        )

        # Save assistant response
        memory.add_ai_message(answer)

        return success_response(
            query=query,
            answer=answer,
            sources=results.get("metadatas", [[]])[0]
        )

    except Exception as e:

        print("\nCHAT ERROR")
        print(str(e))

        return error_response(str(e), 500)