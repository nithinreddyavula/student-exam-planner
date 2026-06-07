# RAG AI Backend — Student Exam Planner

> Python · FastAPI · LangGraph · ChromaDB · OpenRouter · Spring Boot · Redis · Docker · AWS EC2

A production-grade two-service RAG (Retrieval-Augmented Generation) backend evaluated with RAGAS metrics. Built as a real-world AI deployment pattern — not a tutorial project.

**RAGAS evaluation results:**
| Metric | Score |
|--------|-------|
| Answer Relevancy | **0.93** |
| Faithfulness | **0.75** |
| Context Precision | **0.83** |

---

## 🏗️ Architecture

```
Client Request
      │
      ▼
┌─────────────────────────────┐
│   Spring Boot API Gateway   │  ← Port 8080
│   Redis Cache Layer         │  ← 96% latency reduction
└─────────────┬───────────────┘
              │ Cache miss → forward to RAG service
              ▼
┌─────────────────────────────┐
│   Python FastAPI RAG        │  ← Port 8000
│   LangGraph Stateful Agent  │
│   ChromaDB Vector Store     │
│   OpenRouter LLM API        │
└─────────────────────────────┘
```

**Redis caching impact:**
```
First query  →  6,000ms  (RAG pipeline: retrieve → grade → generate)
Repeat query →    211ms  (Redis cache hit)
Reduction    →     96%
```

---

## 🤖 LangGraph agent pipeline

```
User Query
    │
    ▼
[retrieve]  →  ChromaDB vector search on B.Tech PDF content
    │
    ▼
[grade_relevance]  →  LLM grades each retrieved chunk
    │                  Relevant chunks pass · Irrelevant chunks filtered
    ▼
[generate]  →  LLM generates answer from graded context
    │           Conditional logic reduces hallucinations
    ▼
Response
```

The conditional grading step is key — it filters out irrelevant retrieved chunks before generation, which is why Faithfulness is 0.75 and Context Precision is 0.83.

---

## ⚙️ Tech stack

| Service | Technology |
|---------|-----------|
| API Gateway | Java 17 · Spring Boot 3 · Spring Data · Redis |
| RAG Service | Python 3.11 · FastAPI · LangGraph · LangChain |
| Vector Store | ChromaDB |
| LLM | OpenRouter (cloud IP restriction workaround) |
| Embeddings | Hugging Face sentence-transformers |
| Evaluation | RAGAS |
| Containerisation | Docker · Docker Compose (4 containers) |
| Cloud | AWS EC2 (CPU-optimised builds) |

---

## 🚀 Running locally

```bash
# Clone the repo
git clone https://github.com/nithinreddyavula/rag-ai-backend
cd rag-ai-backend

# Add your OpenRouter API key
cp .env.example .env
# Edit .env → add OPENROUTER_API_KEY=your_key_here

# Start all 4 containers
docker-compose up -d

# Spring Boot gateway at http://localhost:8080
# FastAPI RAG service at http://localhost:8000
```

**Prerequisites:** Docker · Docker Compose · OpenRouter API key (free tier works)

---

## 📡 API endpoints

```
POST   /api/query              Submit a question → returns AI-generated answer
GET    /api/health             Health check for both services
GET    /api/cache/stats        Redis cache hit/miss statistics
DELETE /api/cache/clear        Clear Redis cache
```

---

## 📊 RAGAS evaluation

Evaluation was run on 20 questions generated from real B.Tech PDF content.

```python
# Run evaluation yourself
cd ragas_eval/
pip install ragas
python evaluate.py

# Results saved to eval_results.json
```

**What each metric means:**
- **Answer Relevancy (0.93)** — how relevant the generated answer is to the question
- **Faithfulness (0.75)** — how grounded the answer is in the retrieved context (no hallucination)
- **Context Precision (0.83)** — how precise the retrieved chunks are for the given question

---

## 🔧 Why OpenRouter instead of OpenAI?

AWS EC2 free-tier IP ranges are blocked by several LLM providers. OpenRouter routes through multiple providers and handles this transparently — no IP restrictions on standard queries.

---

## 📐 Design decisions

**Why two services instead of one?**
Separates concerns cleanly — the Spring Boot gateway handles auth, caching, and routing logic while the Python service focuses purely on RAG. This mirrors real-world AI deployment patterns where teams own different parts of the stack.

**Why LangGraph over a simple chain?**
LangGraph's stateful agent with conditional edges allows the `grade_relevance` step to filter irrelevant retrieved chunks before generation — measurably improving faithfulness and reducing hallucinations compared to a naive RAG chain.

---

## 🌐 Live deployment

Four-container stack deployed on AWS EC2 with CPU-optimised Docker builds. The system handles concurrent requests via Spring Boot's thread pool with Redis caching absorbing repeated queries.

## 👨‍💻 Connect With Me

**Nithin Kumar Reddy Avula**

* LinkedIn: https://www.linkedin.com/in/avula-nithin-kumar-reddy-0b0641323/
* GitHub: https://github.com/nithinreddyavula

Feel free to connect with me to discuss Backend Engineering, RAG Systems, LangGraph, FastAPI, Spring Boot, Redis, Vector Databases, and AI Infrastructure.

