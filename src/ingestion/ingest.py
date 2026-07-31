import os
import json
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# DATA_PATH = "data/sample.txt"
DATA_FOLDER = "data"
VECTOR_STORE_PATH = "vector_store/faiss.index"
CHUNKS_PATH = "vector_store/chunks.json"

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text
            text += "\n\n"

    return text

def load_all_documents(folder_path):
    all_text = ""

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".txt"):
            all_text += load_text(file_path)
            all_text += "\n\n"

        elif filename.endswith(".pdf"):
            all_text += load_pdf(file_path)
            all_text += "\n\n"

    return all_text

def load_documents_with_sources(folder_path):
    all_chunks = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".txt"):
            text = load_text(file_path)
            chunks = chunk_text_with_source(text, filename)
            all_chunks.extend(chunks)

        elif filename.endswith(".pdf"):
            text = load_pdf(file_path)
            chunks = chunk_text_with_source(text, filename)
            all_chunks.extend(chunks)

    return all_chunks

# def load_all_text_files(folder_path):
#     all_text = ""

#     for filename in os.listdir(folder_path):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(folder_path, filename)

#             with open(file_path, "r", encoding="utf-8") as file:
#                 all_text += file.read()
#                 all_text += "\n\n"

#     return all_text
        
# def chunk_text(text, chunk_size=300, overlap=50):
#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + chunk_size
#         chunk = text[start:end]
#         chunks.append(chunk.strip())
#         start = end - overlap

#     return [chunk for chunk in chunks if chunk]

def chunk_text(text):
    paragraphs = text.split("\n\n")

    chunks = []

    for paragraph in paragraphs:
        clean_paragraph = paragraph.strip()

        if clean_paragraph:
            chunks.append(clean_paragraph)

    return chunks

def chunk_text_with_source(text, source):
    paragraphs = text.split("\n\n")

    chunks = []

    for paragraph in paragraphs:
        clean_paragraph = paragraph.strip()

        if clean_paragraph:
            chunks.append({
                "text": clean_paragraph,
                "source": source
            })

    return chunks

def main():
    print("Loading document...")
    # text = load_text(DATA_PATH)
    # text = load_all_text_files(DATA_FOLDER)
    #text = load_all_documents(DATA_FOLDER)

    print("Splitting document into chunks...")
    #chunks = chunk_text(text)
    chunks = load_documents_with_sources(DATA_FOLDER)

    print(f"Total chunks created: {len(chunks)}")
        
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")
    #embeddings = model.encode(chunks)
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(chunk_texts)
    embeddings = np.array(embeddings).astype("float32")

    print("Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    print("Adding embeddings to FAISS...")
    index.add(embeddings)

    print("Saving FAISS index...")
    faiss.write_index(index, VECTOR_STORE_PATH)

    print("Saving chunks...")
    with open(CHUNKS_PATH, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=4)

    print("Ingestion completed successfully!")

if __name__ == "__main__":
        main()