# CorrectiveRAG — Adaptive Agentic RAG with LangGraph 🦜🕸️

A production-oriented implementation of **Corrective RAG (CRAG)**, **Self-RAG**, and **Adaptive RAG** built with [LangGraph](https://github.com/langchain-ai/langgraph).

---

## 🧠 What is Corrective RAG?

Standard RAG pipelines blindly retrieve documents and generate answers — even when the retrieved documents are irrelevant or the answer is hallucinated. **Corrective RAG** adds intelligence to this pipeline by:

- **Routing** queries intelligently between vector store and web search
- **Grading** retrieved documents for relevance before using them
- **Detecting hallucinations** in generated answers
- **Self-correcting** by falling back to web search when local knowledge is insufficient

## 🏗️ Architecture

```
Question
   │
   ▼
[Router] ──── vectorstore ──▶ [Retrieve] ──▶ [Grade Documents]
   │                                                │
   │                               All relevant ◀──┤──▶ Some irrelevant
   │                                    │                     │
   └──── websearch ──────────────────▶ [Generate] ◀──── [Web Search]
                                          │
                              [Hallucination Grader]
                                          │
                           Grounded ◀─────┤──────▶ Not grounded → retry
                              │
                      [Answer Grader]
                              │
                  Useful ◀────┤────▶ Not useful → Web Search
                     │
                  [END] ✅
```

## ✨ Features

- **Smart Query Routing** — LLM decides whether to use the vector store or web search based on the question topic
- **Document Relevance Grading** — Each retrieved document is scored for relevance; irrelevant docs trigger web search
- **Hallucination Detection** — Generated answers are checked to ensure they're grounded in retrieved facts
- **Answer Quality Grading** — Final answers are evaluated for whether they actually address the question
- **Adaptive Fallback** — Seamlessly switches to Tavily web search when local knowledge is insufficient
- **Persistent Vector Store** — Chroma DB persists embeddings locally so ingestion only runs once

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Orchestration** | LangGraph |
| **LLM** | Groq (`openai/gpt-oss-120b`) |
| **Embeddings** | HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`) |
| **Vector Store** | Chroma (persistent, local) |
| **Web Search** | Tavily |
| **Document Loading** | LangChain WebBaseLoader |
| **Package Manager** | [uv](https://github.com/astral-sh/uv) |

## 📁 Project Structure

```
CorrectiveRAG/
├── graph/
│   ├── chains/
│   │   ├── answer_grader.py        # Grades if answer resolves the question
│   │   ├── generation.py           # RAG generation chain
│   │   ├── hallucination_grader.py # Detects hallucinations in answers
│   │   ├── retrieval_grader.py     # Grades document relevance
│   │   ├── router.py               # Routes question to vectorstore or web
│   │   └── tests/
│   │       └── test_chains.py      # Unit tests for chains
│   ├── nodes/
│   │   ├── generate.py             # Generate node
│   │   ├── grade_documents.py      # Grade documents node
│   │   ├── retrieve.py             # Retrieve node
│   │   └── web_search.py           # Web search node
│   ├── consts.py                   # Node name constants
│   ├── graph.py                    # Full LangGraph workflow
│   └── state.py                    # GraphState TypedDict
├── ingestion.py                    # One-time vector DB population
├── main.py                         # Entry point
├── requirements.txt
└── pyproject.toml
```

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here     # Used for embeddings fallback

# Optional — LangSmith tracing
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=corrective-rag
```

> **Get your API keys:**
> - Groq (free): https://console.groq.com
> - Tavily (free tier): https://app.tavily.com
> - Google AI Studio (free): https://aistudio.google.com

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### 1. Clone the repository

```bash
git clone https://github.com/jawaidaakif01/CorrectiveRAG-LangGraph.git
cd CorrectiveRAG
```

### 2. Install dependencies

```bash
uv sync
# or
uv add -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Fill in your API keys in .env
```

### 4. Run ingestion (first time only)

This fetches documents from the web and stores them in the local Chroma vector DB:

```bash
uv run ingestion.py
```

> ⚠️ Only needs to run **once**. Subsequent runs of `main.py` will automatically skip re-ingestion if the DB already has documents.

### 5. Run the RAG pipeline

```bash
uv run main.py
```

## 🔍 Example Output

```
---Route Question---
---ROUTE QUESTION TO RAG---
---RETRIEVE---
--- CHECK DOCUMENT RELEVANCE TO QUESTION---
---GRADE: DOCUMENT RELEVANT---
---GRADE: DOCUMENT RELEVANT---
---ASSESS GRADED DOCUMENTS---
---DECISION: GENERATE---
---GENERATE---
---CHECK HALLUCINATIONS---
---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---
---GRADE GENERATION vs QUESTION---
---DECISION: GENERATION ADDRESSES QUESTION---

{'question': 'what is agent memory',
 'generation': 'Agent memory refers to ...'}
```

## 🧪 Running Tests

```bash
uv run pytest graph/chains/tests/ -s -v
```

## 📚 Knowledge Base

The vector store is pre-loaded with articles from [Lilian Weng's blog](https://lilianweng.github.io/):

| Topic | URL |
|-------|-----|
| LLM-powered Autonomous Agents | https://lilianweng.github.io/posts/2023-06-23-agent/ |
| Prompt Engineering | https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/ |
| Adversarial Attacks on LLMs | https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/ |

Questions related to **agents**, **prompt engineering**, or **adversarial attacks** are routed to the vector store. All other questions fall back to Tavily web search.

## 🔗 References & Credits

- Original course: [Agentic RAG with LangGraph — Eden Marco](https://www.udemy.com/course/langgraph/)
- Based on: [LangChain Cookbook by Sophia Young & Lance Martin](https://github.com/mistralai/cookbook/tree/main/third_party/langchain)
- LangGraph documentation: https://langchain-ai.github.io/langgraph/
- Corrective RAG paper: [Yan et al. (2024)](https://arxiv.org/abs/2401.15884)
