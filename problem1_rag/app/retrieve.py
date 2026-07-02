import chromadb
from sentence_transformers import SentenceTransformer

from app.config import (
    CHROMA_DB_PATH,
    EMBEDDING_MODEL
)

# ----------------------------
# ChromaDB
# ----------------------------

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = client.get_collection(
    name="document_chunks"
)

# ----------------------------
# Embedding Model
# ----------------------------

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


def retrieve(query, top_k=5):
    """
    Retrieve the most relevant chunks.
    """

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        results = retrieve(question)

        print("\nTop Results:\n")

        for i, document in enumerate(results["documents"][0], start=1):

            metadata = results["metadatas"][0][i - 1]

            print("=" * 60)
            print(f"Result {i}")
            print(f"Source : {metadata['file_name']}")
            print(f"Chunk  : {metadata['chunk_number']}")
            print()
            print(document)
            print("=" * 60)