from airflow_rag_engine.evaluation.metrics import recall_at_k, precision_at_k, mrr


def test_recall_precision_mrr():
    retrieved = ["a", "b", "c"]
    relevant = {"b", "d"}
    assert recall_at_k(retrieved, relevant, 3) == 0.5
    assert precision_at_k(retrieved, relevant, 3) == 1 / 3
    assert mrr(retrieved, relevant) == 0.5
