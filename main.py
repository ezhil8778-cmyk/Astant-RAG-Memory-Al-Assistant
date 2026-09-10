"""
main.py
Command-line chat interface for Astant — a RAG + Memory assistant
for regulations, syllabus, FAQs, and notices.
"""

import uuid
from src.ingestion import load_documents, build_chunk_corpus
from src.retrieval import Retriever
from src.memory import SessionMemory
from src.generation import generate_answer


def main():
    print("Loading knowledge base...")
    documents = load_documents(data_dir="data")
    corpus = build_chunk_corpus(documents)
    retriever = Retriever(corpus)

    session_id = str(uuid.uuid4())[:8]
    memory = SessionMemory(session_id)

    print(f"Astant is ready. (session: {session_id})")
    print("Type your question, or 'clear' to reset memory, or 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() == "exit":
            print("Goodbye!")
            break
        if query.lower() == "clear":
            memory.clear()
            print("Session memory cleared.\n")
            continue

        retrieved = retriever.search(query, top_k=3)
        recent = memory.recent_turns(n=3)
        answer = generate_answer(query, retrieved, recent)

        print(f"\nAstant: {answer}\n")
        memory.add_turn(query, answer)


if __name__ == "__main__":
    main()
