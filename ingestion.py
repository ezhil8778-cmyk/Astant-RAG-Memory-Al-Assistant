"""
ingestion.py
Loads plain-text knowledge base documents (regulations, syllabus, FAQs, notices)
and splits them into overlapping word-based chunks for indexing.
"""

import os


def load_documents(data_dir="data"):
    """
    Reads every .txt file in data_dir.
    Returns a list of dicts: {"category": str, "filename": str, "text": str}
    """
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            category = filename.split("_")[0].lower()  # e.g. regulations_2024.txt -> "regulations"
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "category": category,
                "filename": filename,
                "text": text
            })
    return documents


def chunk_text(text, chunk_size=150, overlap=30):
    """
    Splits text into overlapping word-based chunks.
    chunk_size: number of words per chunk
    overlap: number of words shared between consecutive chunks
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_chunk_corpus(documents):
    """
    Turns loaded documents into a flat list of chunks with metadata.
    Returns: list of {"category": str, "filename": str, "chunk": str}
    """
    corpus = []
    for doc in documents:
        for chunk in chunk_text(doc["text"]):
            corpus.append({
                "category": doc["category"],
                "filename": doc["filename"],
                "chunk": chunk
            })
    return corpus
