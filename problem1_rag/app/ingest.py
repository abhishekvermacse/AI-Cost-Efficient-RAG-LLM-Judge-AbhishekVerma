import os
import hashlib
import chromadb

from sentence_transformers import SentenceTransformer

from app.config import (
    DATA_FOLDER,
    CHROMA_DB_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL
)

from app.utils import load_document


# ---------------------------------------
# Split document into chunks
# ---------------------------------------

def split_into_chunks(text):

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# ---------------------------------------
# Create unique chunk id
# ---------------------------------------

def create_chunk_hash(chunk):

    return hashlib.md5(
        chunk.encode("utf-8")
    ).hexdigest()


# ---------------------------------------
# Initialize ChromaDB
# ---------------------------------------

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="document_chunks"
)


# ---------------------------------------
# Load Embedding Model
# ---------------------------------------

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# ---------------------------------------
# Main Ingestion
# ---------------------------------------

def ingest_documents():

    supported_extensions = [
        ".pdf",
        ".html",
        ".md"
    ]

    if not os.path.exists(DATA_FOLDER):

        print("Data folder not found.")

        return

    total_files = 0
    stored_chunks = 0
    skipped_chunks = 0

    files = os.listdir(DATA_FOLDER)

    for file_name in files:

        file_path = os.path.join(
            DATA_FOLDER,
            file_name
        )

        if not os.path.isfile(file_path):
            continue

        extension = os.path.splitext(
            file_name
        )[1].lower()

        if extension not in supported_extensions:
            continue

        total_files += 1

        print(f"\nReading : {file_name}")

        try:

            document = load_document(file_path)

        except Exception as error:

            print(error)

            continue

        chunks = split_into_chunks(document)

        print(f"Chunks Found : {len(chunks)}")

        for index, chunk in enumerate(chunks):

            chunk_id = create_chunk_hash(chunk)

            existing = collection.get(
                ids=[chunk_id]
            )

            if existing["ids"]:

                skipped_chunks += 1

                continue

            embedding = embedding_model.encode(
                chunk
            ).tolist()

            metadata = {
                "file_name": file_name,
                "chunk_number": index,
                "source": file_path,
                "hash": chunk_id
            }

            collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[metadata]
            )

            stored_chunks += 1

        print(f"Finished : {file_name}")

    print("\n========================================")
    print("Document Ingestion Completed")
    print("========================================")
    print(f"Files Processed : {total_files}")
    print(f"Stored Chunks   : {stored_chunks}")
    print(f"Skipped Chunks  : {skipped_chunks}")
    print(f"Collection Name : document_chunks")
    print(f"Database Path   : {CHROMA_DB_PATH}")
    print("========================================")


if __name__ == "__main__":
    ingest_documents()