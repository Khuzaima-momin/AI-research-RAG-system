from flask import Blueprint, render_template, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename

from rag.parser import extract_text
from rag.chunker import chunk_text
from rag.embeddings import get_embeddings
from rag.database import add_chunks_to_db
from rag.retriever import retrieve_chunks
from rag.generator import generate_answer

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Helper: file validation
# -----------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# HOME PAGE
# -----------------------------
@main.route("/")
def home():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@main.route("/upload", methods=["POST"])
def upload_file():

    print("\n===== UPLOAD STARTED =====")

    # 1. CHECK FILE
    if "file" not in request.files:
        print("NO FILE PART FOUND")
        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        print("EMPTY FILE NAME")
        return redirect("/")

    if not allowed_file(file.filename):
        print("INVALID FILE TYPE:", file.filename)
        return redirect("/")

    # 2. SAVE FILE SAFELY
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    print("FILE SAVED:", filepath)

    try:
        # 3. EXTRACT TEXT
        text = extract_text(filepath)

        if not text:
            print("NO TEXT EXTRACTED FROM FILE")
            return redirect("/")

        print("TEXT EXTRACTION SUCCESS")

        # 4. CHUNK TEXT
        chunks = chunk_text(text)

        if not chunks:
            print("NO CHUNKS GENERATED")
            return redirect("/")

        print(f"CHUNKS CREATED: {len(chunks)}")

        # 5. EMBEDDINGS
        embeddings = get_embeddings(chunks)

        # 6. STORE IN VECTOR DB
        add_chunks_to_db(chunks, embeddings, filename)

        print("\nFILE INDEXED SUCCESSFULLY!")
        print("File:", filename)
        print("Chunks:", len(chunks))

    except Exception as e:
        print("\nERROR DURING INDEXING:")
        print(str(e))

    print("===== UPLOAD END =====\n")

    return redirect("/")


# -----------------------------
# CHAT API (RAG CORE)
# -----------------------------
@main.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Empty query"}), 400

        print("\n===== CHAT REQUEST =====")
        print("Query:", query)

        # 1. Retrieve relevant chunks
        results = retrieve_chunks(query)

        print("Raw retrieval result:", results)

        # 2. Safe extraction of chunks
        chunks = []

        if results:
            if isinstance(results, dict):
                if "documents" in results and results["documents"]:
                    chunks = results["documents"][0]

                elif "chunks" in results:
                    chunks = results["chunks"]

        print("Final chunks used:", chunks)

        # 3. Handle empty retrieval safely
        if not chunks:
            return jsonify({
                "query": query,
                "answer": "I couldn't find relevant information in the uploaded documents."
            })

        # 4. Generate response
        answer = generate_answer(query, chunks)

        print("Answer generated successfully")

        return jsonify({
            "query": query,
            "answer": answer
        })

    except Exception as e:
        print("CHAT ERROR:", str(e))

        return jsonify({
            "error": str(e),
            "answer": "Backend error occurred while processing your request."
        }), 500