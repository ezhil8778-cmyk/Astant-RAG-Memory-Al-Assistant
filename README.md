# Astant — RAG + Memory Assistant

**An Agentic AI Assistant for Regulations, Syllabus, FAQs and Notices**

Astant is a Retrieval-Augmented Generation (RAG) pipeline combined with a persistent conversational memory layer, built to help students and faculty get fast, natural-language answers to questions about academic regulations, syllabus content, exam rules, and institutional notices — grounded in actual source documents instead of guesswork.

---

## 📌 Problem Statement

Students and faculty routinely need quick answers to questions about academic regulations, syllabus content, examination rules, and institutional notices. This information is usually scattered across multiple PDFs, circulars, and web pages, making it time-consuming to search manually. Traditional keyword search fails to understand natural-language questions, often returns irrelevant results, and has no memory of prior interactions — forcing users to repeat context in every query.

## 💡 Solution

Astant ingests institutional documents (regulations, syllabi, FAQs, notices), splits them into chunks, and indexes them for semantic search. When a user asks a question, it retrieves the most relevant chunks, combines them with ongoing conversation history from memory, and generates an accurate, source-grounded answer — maintaining continuity across a multi-turn conversation.

---

## ✨ Key Features

- **Grounded answers** — every response is backed by a document retrieval step, with the source category and file available for inspection
- **Semantic search** — TF-IDF + cosine similarity retrieval instead of plain keyword matching
- **Session-aware memory** — conversation history persists per session so follow-up questions carry context
- **Offline-capable generation** — works end-to-end without an LLM API key via an extractive fallback, with an easy switch to full LLM generation
- **Easily extensible knowledge base** — new notices/circulars can be added as plain-text files without retraining
- **Lightweight, swappable architecture** — retrieval, memory, and generation are isolated modules that can each be upgraded independently (e.g. TF-IDF → dense embeddings, JSON store → Redis)

---

## 🏗️ How It Works

1. **Knowledge base authoring** — regulations, syllabus, FAQ, and notice documents written as plain-text files, one per category
2. **Ingestion** — documents cleaned and split into overlapping word-based chunks
3. **Indexing** — chunks converted into TF-IDF vectors for semantic matching
4. **Retrieval** — a query is matched against vectors using cosine similarity to find the most relevant chunks
5. **Memory** — every question-answer pair is stored in a per-session JSON file; recent turns are recalled for context
6. **Generation** — retrieved chunks + conversation history are combined into a prompt for the LLM (or offline extractive fallback)
7. **Interface** — a command-line chat loop for asking questions, viewing grounded answers, and clearing session memory

---

## 🛠️ Tech Stack

- **Python**
- **scikit-learn** — `TfidfVectorizer`, `cosine_similarity`
- **JSON** — per-session memory storage
- **LLM API** (optional, e.g. OpenAI) — with offline extractive fallback when no key is configured

---

## 🚀 Getting Started

```bash
git clone https://github.com/<your-username>/astant-rag-memory-assistant.git
cd astant-rag-memory-assistant
pip install -r requirements.txt
python main.py
```

> Add your LLM API key as an environment variable to enable full generation, or run without one to use the offline extractive fallback.

---

## 📂 Project Structure

```
astant-rag-memory-assistant/
├── data/               # Regulations, syllabus, FAQ, notice text files
├── retrieval/          # TF-IDF indexing & similarity search
├── memory/             # Per-session JSON memory store
├── generation/         # Prompt construction & LLM / fallback generation
├── main.py             # Command-line chat interface
├── requirements.txt
└── README.md
```

---

## 🔮 Future Enhancements

- Replace TF-IDF retrieval with dense embeddings (e.g. sentence-transformers + FAISS/Chroma) for better semantic matching at scale
- Support real PDF/DOCX ingestion for actual college regulation and syllabus documents
- Add a web-based chat interface in place of the command-line tool
- Automatic ingestion of new notices/circulars as they're published
- Role-based responses (student vs. faculty view)
- Persist memory in a database (e.g. SQLite/Redis) for multi-user deployment

---

## 📖 References

- scikit-learn documentation — `TfidfVectorizer` and `cosine_similarity`
- OpenAI API documentation
- Lewis, P. et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020

---

## 👤 Author

**Thamizh Ezhilan T**
B.E. Computer Science and Engineering, Anna University, BIT Campus, Trichy (2024–2027)
