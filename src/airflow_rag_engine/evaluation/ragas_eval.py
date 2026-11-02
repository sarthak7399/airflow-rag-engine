def run_ragas(eval_rows: list[dict], llm=None, embeddings=None) -> list[dict]:
    from datasets import Dataset  # type: ignore[import-untyped]
    from ragas import evaluate
    from ragas.metrics import answer_relevancy, faithfulness

    dataset = Dataset.from_list(eval_rows)
    result = evaluate(dataset, metrics=[faithfulness, answer_relevancy], llm=llm, embeddings=embeddings)
    return result.to_pandas().to_dict(orient="records")  # type: ignore[union-attr]
