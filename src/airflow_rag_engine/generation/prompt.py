def build_prompt(query: str, contexts: list[str]) -> str:
    context_block = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(contexts))
    return (
        "You are a helpful assistant answering questions about Apache Airflow documentation.\n"
        "Use only the provided context. If the answer is not in the context, say you don't have enough information.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )
