import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from google import genai

VECTOR_STORE_PATH = "vector_store/faiss.index"
CHUNKS_PATH = "vector_store/chunks.json"

def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
def retrieve_chunks(question, k=3):
    chunks = load_chunks()

    index = faiss.read_index(VECTOR_STORE_PATH)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    distances, indices = index.search(question_embedding, k)

    retrieved_chunks = []

    for idx in indices[0]:
        retrieved_chunks.append(chunks[idx])

    return retrieved_chunks

def generate_answer(question, retrieved_chunks, call_gemini):
    context = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    )

    prompt = f"""
Answer the question using only the provided context.
Explain it in simple beginner-friendly words.

Context:
{context}

Question:
{question}
"""

    return call_gemini(prompt)

def main():
    question = input("Ask a question: ")

    chunks = retrieve_chunks(question)

    print("\nRetrieved Chunks:\n")

    # for chunk in chunks:
    #     print(chunk)
    #     print("-" * 50)
    for chunk in chunks:
        print(f"Source: {chunk['source']}")
        print(chunk["text"])
        print("-" * 50)
    print("\nGenerating Answer...\n")

    answer = generate_answer(question, chunks)

    print(answer)

# if __name__ == "__main__":
#     main()   