# Airflow RAG Engine

A self-hosted, open-source RAG system for querying Apache Airflow documentation.

The project is built from the ground up with a focus on **retrieval quality, evaluation, reproducibility, and production-oriented engineering** rather than simply building a chatbot.

The goal is to understand and implement the complete RAG lifecycle:

```text
Documentation
     ↓
Ingestion
     ↓
Cleaning & Metadata Extraction
     ↓
Section-Aware Chunking
     ↓
Embeddings
     ↓
Vector Database
     ↓
Retrieval
     ↓
Context Construction
     ↓
Local LLM Generation
     ↓
Evaluation
     ↓
API / Deployment
```

---

## Project Goals

This project explores how to build a reliable RAG system using only self-hosted and open-source components.

The primary goals are:

* Build the RAG pipeline from first principles
* Understand the trade-offs involved in document chunking
* Implement local embedding generation
* Store and retrieve vectors using a self-hosted vector database
* Run LLM inference locally
* Build a reproducible evaluation dataset
* Measure retrieval and generation quality
* Compare different retrieval strategies experimentally
* Add automated RAG evaluation
* Package the system as a deployable service
* Keep the entire core stack free of proprietary APIs and managed cloud dependencies

This is intentionally designed as an **engineering project**, not just a conversational demo.

---

## Why Airflow?

Apache Airflow is used as the initial knowledge domain because it provides a technically relevant and structured documentation corpus.

The project also aligns naturally with data engineering concepts such as:

* DAGs
* scheduling
* task execution
* operators
* sensors
* XCom
* connections
* variables
* executors
* task mapping
* datasets
* callbacks
* pools
* deployment
* configuration
* troubleshooting

Using a data-engineering-oriented corpus also makes the project relevant to the broader goal of building **Data Engineering + AI / AI Infrastructure** expertise.

---

## Architecture

### Initial Architecture

```text
                    ┌──────────────────────┐
                    │ Apache Airflow Docs  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Loader      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Cleaning & Metadata  │
                    │ Extraction           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Section-Aware        │
                    │ Chunker              │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Embedding Model      │
                    │ BGE-small-en-v1.5    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Qdrant               │
                    │ Vector Database      │
                    └──────────┬───────────┘
                               │
                         User Query
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Query Embedding      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Vector Retrieval     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Context Construction │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Local LLM            │
                    │ Qwen2.5-7B-Instruct  │
                    └──────────┬───────────┘
                               │
                               ▼
                            Answer
                               │
                               ▼
                    ┌──────────────────────┐
                    │ RAG Evaluation       │
                    │ Ragas                │
                    └──────────────────────┘
```

---

## Technology Stack

| Component            | Technology              | Purpose                               |
| -------------------- | ----------------------- | ------------------------------------- |
| Language             | Python 3.11+            | Application and pipeline code         |
| Package Manager      | uv                      | Dependency and environment management |
| Embeddings           | BAAI/bge-small-en-v1.5  | Local text embeddings                 |
| Embedding Framework  | sentence-transformers   | Embedding inference                   |
| Vector Database      | Qdrant                  | Self-hosted vector storage and search |
| LLM Runtime          | Ollama                  | Local LLM inference                   |
| Generation Model     | Qwen2.5-7B-Instruct     | Local answer generation               |
| Evaluation           | Ragas                   | RAG evaluation                        |
| API                  | FastAPI                 | Service interface                     |
| Containerization     | Docker / Docker Compose | Reproducible deployment               |
| Testing              | pytest                  | Automated testing                     |
| Linting / Formatting | Ruff                    | Code quality                          |
| Data Formats         | JSONL / Parquet         | Intermediate and processed data       |

---

## Open-Source Policy

The core project is intentionally designed around open-source and self-hosted components.

The project will **not** depend on:

* OpenAI API
* Anthropic API
* Gemini API
* Cohere API
* Pinecone
* Qdrant Cloud
* Managed vector databases
* Managed LLM APIs
* Managed embedding APIs
* Managed orchestration platforms

The intended architecture should be runnable locally without requiring a paid API.

### License Verification

Model and software licenses are treated separately.

For every major dependency, the project tracks:

1. Software license
2. Model license
3. Whether the component requires an external service
4. Whether inference can be performed locally

This distinction is important because an "open-weight" model is not necessarily equivalent to software distributed under a conventional open-source license.

---

## Repository Structure

```text
airflow-rag-engine/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── configs/
│   └── default.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── eval/
│
├── notebooks/
│   └── 01_exploration.ipynb
│
├── scripts/
│   ├── download_docs.py
│   ├── ingest.py
│   └── evaluate.py
│
├── src/
│   └── airflow_rag/
│       ├── __init__.py
│       │
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   └── chunker.py
│       │
│       ├── embeddings/
│       │   ├── __init__.py
│       │   └── model.py
│       │
│       ├── vectorstore/
│       │   ├── __init__.py
│       │   └── qdrant.py
│       │
│       ├── retrieval/
│       │   ├── __init__.py
│       │   └── retriever.py
│       │
│       ├── generation/
│       │   ├── __init__.py
│       │   ├── prompt.py
│       │   └── llm.py
│       │
│       ├── evaluation/
│       │   ├── __init__.py
│       │   └── ragas_eval.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── main.py
│       │
│       └── config.py
│
├── tests/
│   ├── test_chunking.py
│   ├── test_retrieval.py
│   └── test_api.py
│
└── docs/
    ├── architecture.md
    ├── evaluation.md
    └── experiments.md
```

---

## Development Roadmap

### Phase 1 — Repository & Ingestion

* [ ] Initialize Python project with `uv`
* [ ] Configure project structure
* [ ] Configure Ruff
* [ ] Configure pytest
* [ ] Add Docker Compose
* [ ] Run Qdrant locally
* [ ] Obtain Airflow documentation
* [ ] Implement document loader
* [ ] Normalize documentation
* [ ] Extract document metadata
* [ ] Implement section-aware chunking
* [ ] Add chunking tests
* [ ] Persist processed chunks

### Phase 2 — Embeddings & Retrieval

* [ ] Add local embedding model
* [ ] Generate document embeddings
* [ ] Create Qdrant collection
* [ ] Index document chunks
* [ ] Implement query embedding
* [ ] Implement top-k vector retrieval
* [ ] Add metadata filtering
* [ ] Add retrieval tests
* [ ] Build a CLI retrieval interface

### Phase 3 — Generation

* [ ] Install/configure Ollama
* [ ] Run local Qwen model
* [ ] Implement prompt construction
* [ ] Inject retrieved context
* [ ] Generate answers
* [ ] Return source references
* [ ] Add generation tests

### Phase 4 — Evaluation

* [ ] Build evaluation question set
* [ ] Define ground-truth answers
* [ ] Evaluate retrieval quality
* [ ] Implement Recall@K
* [ ] Implement Precision@K
* [ ] Implement MRR
* [ ] Integrate Ragas
* [ ] Evaluate faithfulness
* [ ] Evaluate answer relevance
* [ ] Track evaluation experiments

### Phase 5 — Retrieval Engineering

* [ ] Establish dense retrieval baseline
* [ ] Experiment with chunk sizes
* [ ] Experiment with chunk overlap
* [ ] Experiment with metadata filtering
* [ ] Investigate hybrid retrieval
* [ ] Investigate reranking
* [ ] Investigate query rewriting
* [ ] Compare retrieval configurations
* [ ] Document experiment results

### Phase 6 — Productionization

* [ ] Add FastAPI
* [ ] Add health endpoints
* [ ] Add structured logging
* [ ] Add configuration management
* [ ] Add error handling
* [ ] Add integration tests
* [ ] Add Docker deployment
* [ ] Add CI
* [ ] Document deployment
* [ ] Document architecture

---

## Evaluation Philosophy

The system should not be judged by whether it can answer a handful of questions.

The goal is to measure the system systematically.

### Retrieval Metrics

The initial retrieval evaluation will include:

* Recall@K
* Precision@K
* Mean Reciprocal Rank (MRR)

Later experiments may include:

* context relevance
* reranking quality
* retrieval latency

### Generation Metrics

The generation evaluation will include:

* Faithfulness
* Answer relevance
* Context utilization

### Experimentation

Different configurations will be compared quantitatively.

For example:

```text
Configuration       Recall@5    MRR      Faithfulness
------------------------------------------------------
Chunk 256              TBD       TBD          TBD
Chunk 512              TBD       TBD          TBD
Chunk 768              TBD       TBD          TBD
```

The objective is to make architecture decisions based on measurements rather than assumptions.

---

## Design Principles

### 1. Understand before abstracting

The first implementation should avoid unnecessary RAG frameworks.

Core components such as:

* chunking
* embeddings
* retrieval
* prompt construction
* generation

should be understandable independently.

Framework abstractions can be introduced later when they provide clear value.

### 2. Measure before optimizing

Every major retrieval optimization should have an evaluation experiment behind it.

### 3. Keep data and code separate

Raw data, processed data, configuration, application code, and evaluation datasets should remain separate.

### 4. Reproducibility matters

A new developer should be able to clone the repository, install dependencies, start the infrastructure, and reproduce the pipeline.

### 5. Local-first architecture

The core system should work without proprietary APIs or paid cloud services.

### 6. Production-oriented engineering

The project will eventually include:

* configuration
* logging
* testing
* error handling
* health checks
* containers
* API boundaries
* evaluation
* reproducible experiments

---

## Example Target Usage

The eventual system should support questions such as:

```text
How does Airflow determine when a DAG run should be scheduled?
```

and produce an answer based on retrieved Airflow documentation, including references to the source sections used to construct the response.

The system should prefer:

```text
"I don't have enough information in the retrieved documentation."
```

over confidently generating unsupported information.

---

## Current Status

**Project status:** Early development

Current focus:

```text
Repository scaffolding
        ↓
Documentation ingestion
        ↓
Section-aware chunking
```

The first milestone is intentionally limited to ingestion and chunk quality.

Generation and evaluation will be added only after the retrieval foundation is established.

---

## Learning Objectives

This project is also being used to develop practical understanding of:

* Data ingestion
* Data transformation
* Data quality
* Vector databases
* Embeddings
* Information retrieval
* Ranking
* LLM inference
* RAG architecture
* RAG evaluation
* API design
* Docker
* Testing
* Observability
* System design
* AI infrastructure

The objective is not merely to demonstrate that an LLM can answer questions.

The objective is to understand **how to engineer, evaluate, and operate the systems around an LLM**.

---

## Environment Setup

### 1. Create and activate the virtual environment

Create a Python virtual environment named `airflowRagEngineENV`:

```bash
python3 -m venv airflowRagEngineENV
```

Activate it on **Linux / macOS**:

```bash
source airflowRagEngineENV/bin/activate
```

Activate it on **Windows PowerShell**:

```powershell
.\airflowRagEngineENV\Scripts\Activate.ps1
```

Activate it on **Windows Command Prompt**:

```cmd
airflowRagEngineENV\Scripts\activate
```

After activation, your terminal should show the environment name:

```text
(airflowRagEngineENV)
```

To deactivate the environment:

```bash
deactivate
```

---

### 2. Install `uv`

`uv` is used for fast Python package and dependency management.

#### Linux / macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal or reload your shell after installation.

Verify the installation:

```bash
uv --version
```

#### Windows

Using PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify the installation:

```powershell
uv --version
```

---

### 3. Install project dependencies

With `airflowRagEngineENV` activated, install the packages listed in `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

Verify the installed packages:

```bash
uv pip list
```

---

### 4. Verify the Python environment

Confirm that Python is being resolved from the project virtual environment:

```bash
python3 --version
```

On Windows PowerShell:

```powershell
Get-Command python
```

On Linux / macOS:

```bash
which python
```

The Python executable should point to `airflowRagEngineENV`.

---

### 5. Quick environment check

Run:

```bash
python -c "import sys; print(sys.executable)"
```

Expected output should contain:

```text
airflowRagEngineENV
```

The development environment is now ready for the RAG pipeline.

---

## License

This repository is intended to use an open-source license.

Third-party software and models retain their respective licenses.

Model and dependency licenses should be reviewed before redistribution or commercial deployment.
