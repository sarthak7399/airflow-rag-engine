import os

import httpx

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434") + "/api/generate"
TAGS_URL = os.getenv("OLLAMA_URL", "http://localhost:11434") + "/api/tags"
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")


def _first_available_model() -> str:
    try:
        resp = httpx.get(TAGS_URL, timeout=10.0)
        resp.raise_for_status()
        models = resp.json().get("models", [])
        if models:
            return models[0]["name"]
    except Exception as e:  # noqa: BLE001
        import logging
        logging.getLogger(__name__).debug('ollama tags fetch failed: %s', e)
    return DEFAULT_MODEL


def generate(prompt: str, model: str = DEFAULT_MODEL, timeout: float = 120.0) -> str:
    try:
        resp = httpx.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            model = _first_available_model()
            resp = httpx.post(
                OLLAMA_URL,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=timeout,
            )
            resp.raise_for_status()
        else:
            raise
    return resp.json().get("response", "").strip()
