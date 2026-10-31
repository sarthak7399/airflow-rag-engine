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
│   └── airflow-rag-engine/
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

## Local Models

### Embeddings: BAAI/bge-small-en-v1.5

The embedding model is loaded via `sentence-transformers` and downloaded on first use from Hugging Face.

- First run downloads weights into the Hugging Face cache:
  - Linux/macOS: `~/.cache/huggingface/hub/`
  - Windows: `%USERPROFILE%\.cache\huggingface\hub\`
- Subsequent runs use the cached weights (offline-capable).
- Set `HF_TOKEN` in `.env` for higher rate limits / private access.

To pre-download manually:

```bash
uv run python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"
```

### LLM: Qwen2.5-7B-Instruct (via Ollama)

Pulled and run locally with Ollama:

```bash
ollama pull qwen2.5:7b-instruct
```

---

## Environment Setup

This project uses [`uv`](https://docs.astral.sh/uv/) as the primary Python environment and dependency manager.

The project uses a local virtual environment named:

```text
airflowRagEngineENV
```

The virtual environment is intentionally excluded from Git. The environment itself is reproducible from `pyproject.toml` and `uv.lock`.

---

### 1. Install `uv`

#### Windows

Using PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify the installation:

```powershell
uv --version
```

#### Linux / macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify the installation:

```bash
uv --version
```

Restart the terminal or reload the shell if `uv` is not immediately available.

---

### 2. Create the virtual environment

Create the project virtual environment using `uv`:

```bash
uv venv airflowRagEngineENV
```

This creates:

```text
airflow-rag-engine/
└── airflowRagEngineENV/
```

The environment directory should **not** be committed to Git.

Add the following to `.gitignore`:

```gitignore
airflowRagEngineENV/
```

---

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.\airflowRagEngineENV\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
airflowRagEngineENV\Scripts\activate
```

#### Linux / macOS

```bash
source airflowRagEngineENV/bin/activate
```

After activation, the terminal should display:

```text
(airflowRagEngineENV)
```

To deactivate:

```bash
deactivate
```

---

## Dependency Management

The project uses three files with different responsibilities:

```text
pyproject.toml
      │
      │ project dependencies
      ▼
   uv.lock
      │
      │ exact resolved dependency versions
      ▼
 reproducible environment
```

### `pyproject.toml`

`pyproject.toml` is the **primary project configuration and dependency definition**.

It describes:

* Project metadata
* Python version requirements
* Runtime dependencies
* Development dependencies
* Build configuration
* Tool configuration

For example:

```toml
dependencies = [
    "pydantic",
    "pydantic-settings",
    "qdrant-client",
]
```

It answers:

> "What does this project need?"

---

### `uv.lock`

`uv.lock` is the **dependency lockfile generated by `uv`**.

It records the resolved dependency graph, including the specific package versions and dependency information required to reproduce the environment.

For example:

```text
pyproject.toml
      ↓
    uv
      ↓
  dependency resolution
      ↓
   uv.lock
```

It answers:

> "Exactly what versions of the dependencies were resolved for this project?"

The `uv.lock` file **should be committed to Git**.

This allows another developer to clone the repository and reproduce the same dependency environment using:

```bash
uv sync
```

Do **not** add `uv.lock` to `.gitignore`.

---

### `requirements.txt`

`requirements.txt` is provided as a conventional dependency file for compatibility and convenience.

It can be used with:

```bash
uv pip install -r requirements.txt
```

However, `pyproject.toml` + `uv.lock` is the preferred dependency-management workflow for this project.

When adding or removing dependencies during development, prefer:

```bash
uv add <package>
```

rather than manually editing `requirements.txt`.

---

## Install Dependencies

### Recommended: `uv sync`

After cloning the repository and creating the environment:

```bash
uv sync
```

`uv` will read the project configuration and lockfile and install the required dependencies.

This is the preferred setup method.

---

### Alternative: install from `requirements.txt`

If you want to install the dependencies listed in `requirements.txt` directly:

```bash
uv pip install -r requirements.txt
```

Verify installed packages:

```bash
uv pip list
```

---

## Adding Dependencies

Add a runtime dependency:

```bash
uv add <package-name>
```

For example:

```bash
uv add qdrant-client
```

Add a development dependency:

```bash
uv add --dev pytest
```

For example:

```bash
uv add --dev pytest ruff mypy
```

`uv` will update `pyproject.toml` and the lockfile accordingly.

---

## Removing Dependencies

Remove a dependency with:

```bash
uv remove <package-name>
```

For example:

```bash
uv remove qdrant-client
```

---

## Updating Dependencies

To update dependencies according to the project's version constraints:

```bash
uv lock --upgrade
```

Then synchronize the environment:

```bash
uv sync
```

Avoid upgrading dependencies blindly during development. Dependency upgrades should ideally be reviewed and tested before committing the resulting `uv.lock` changes.

---

## Verify the Environment

Check the Python version:

```bash
python --version
```

Check which Python executable is being used.

### Windows PowerShell

```powershell
Get-Command python
```

### Linux / macOS

```bash
which python
```

The executable should point to:

```text
airflowRagEngineENV
```

You can also verify directly from Python:

```bash
python -c "import sys; print(sys.executable)"
```

---

## Project File and Directory Policy

The repository separates source code, configuration, generated data, dependencies, and local development artifacts.

```text
airflow-rag-engine/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── requirements-dev.txt
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
│
├── scripts/
│
├── src/
│   └── airflow_rag_engine/
│
├── tests/
│
└── docs/
```

### Files that should be committed

The following should normally be committed:

```text
README.md
LICENSE
pyproject.toml
uv.lock
requirements.txt
requirements-dev.txt
.gitignore
.env.example
docker-compose.yml
configs/
src/
tests/
scripts/
docs/
```

### Files that should NOT be committed

The following should normally be excluded:

```text
airflowRagEngineENV/
.env
__pycache__/
.pytest_cache/
.ruff_cache/
.mypy_cache/
*.pyc
```

Add them to `.gitignore`.

---

## Data Directory Policy

The `data/` directory is used for the RAG pipeline's datasets and intermediate artifacts:

```text
data/
├── raw/
├── processed/
└── eval/
```

### `data/raw/`

Contains original downloaded or collected documents.

Examples:

```text
data/raw/
├── airflow-docs/
└── ...
```

### `data/processed/`

Contains normalized documents, chunks, and other generated pipeline artifacts.

Examples:

```text
data/processed/
├── documents.parquet
├── chunks.parquet
└── ...
```

### `data/eval/`

Contains evaluation datasets and experiment inputs.

Examples:

```text
data/eval/
├── questions.jsonl
├── ground_truth.jsonl
└── ...
```

Large datasets and generated artifacts should generally **not** be committed directly to Git.

The repository should instead contain the code and instructions required to reproduce them.

If a small dataset is required for tests or examples, it can be committed intentionally.

---

## Environment Variables

Environment-specific configuration should not be committed.

Use:

```text
.env.example
```

to document required environment variables.

Create a local `.env` file when required:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

The actual `.env` file should be excluded from Git:

```gitignore
.env
```

Never commit API keys, passwords, tokens, credentials, or other secrets.

---

## Reproducible Setup from a Fresh Clone

A new developer should be able to set up the project with:

```bash
git clone <repository-url>
cd airflow-rag-engine
```

Create the environment:

```bash
uv venv
```

Activate it.

Windows PowerShell:

```powershell
.\airflowRagEngineENV\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

Verify:

```bash
python --version
uv pip list
```

The project environment is now ready for development.


---

## License

This repository is intended to use an open-source license.

Third-party software and models retain their respective licenses.

Model and dependency licenses should be reviewed before redistribution or commercial deployment.
