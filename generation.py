"""
generation.py
Builds the final prompt from retrieved chunks + conversation history,
and generates an answer via an LLM API — or an offline extractive
fallback if no API key is configured.
"""

import os


def build_prompt(query, retrieved_chunks, recent_turns):
    context = "\n\n".join(
        f"[{c['category']}] {c['chunk']}" for c in retrieved_chunks
    )
    history = "\n".join(
        f"Q: {t['question']}\nA: {t['answer']}" for t in recent_turns
    )

    prompt = f"""You are Astant, an assistant that answers questions using only the
provided institutional documents. Do not use outside knowledge.

Conversation history:
{history}

Retrieved context:
{context}

Question: {query}

Answer clearly and cite the source category in your answer.
"""
    return prompt


def generate_answer(query, retrieved_chunks, recent_turns):
    """
    Uses the OpenAI API if an API key is configured; otherwise falls back
    to returning the single most relevant retrieved chunk directly.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not retrieved_chunks:
        return "I couldn't find anything relevant in the knowledge base for that question."

    if api_key:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = build_prompt(query, retrieved_chunks, recent_turns)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    # Offline extractive fallback — no API key needed
    top = retrieved_chunks[0]
    return f"(offline mode) Based on {top['category']} — {top['filename']}:\n\n{top['chunk']}"
