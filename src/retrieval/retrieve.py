import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


VECTOR_STORE_PATH = "vector_store/faiss.index"
CHUNKS_PATH = "vector_store/chunks.json"


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("Loading chunks...")
    chunks = load_chunks()

    print("Loading FAISS index...")
    index = faiss.read_index(VECTOR_STORE_PATH)

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    question = input("Ask a question: ")

    print("Creating question embedding...")
    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    print("Searching FAISS...")
    distances, indices = index.search(question_embedding, k=2)

    print("\nMost relevant chunks:\n")

    for idx in indices[0]:
        print(chunks[idx])
        print("-" * 50)


if __name__ == "__main__":
    main()