<div align="center">

```
██████╗ ██╗███████╗██╗  ██╗██╗
██╔══██╗██║██╔════╝██║  ██║██║
██████╔╝██║███████╗███████║██║
██╔══██╗██║╚════██║██╔══██║██║
██║  ██║██║███████║██║  ██║██║
╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝
```

# R.I.S.H.I.
### Responsive Intelligent System for Human Interaction

*A Jarvis-style autonomous AI companion — built for personal use, production-grade by design.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Agent-FF6B35?style=flat-square)](https://github.com/openclaw)
[![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-DC244C?style=flat-square)](https://qdrant.tech)
[![Telegram](https://img.shields.io/badge/Telegram-Client-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org)
[![GitHub Models](https://img.shields.io/badge/GitHub_Models-LLM-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/marketplace/models)

</div>

---

## What is R.I.S.H.I.?

R.I.S.H.I. is a **personal AI companion** built code-first around a fully extensible tool system. It understands your personal context, searches your knowledge base semantically, and executes real tasks — all through a Telegram interface backed by a local FastAPI server.

The agent backbone is **OpenClaw**, driven by **GitHub Models GPT-4o mini** by default, with one-line switching to Groq, Nvidia NIM, or opencode/zen. Memory is persisted locally via SQLite. The RAG pipeline runs on local **Qdrant** with **OpenAI text-embedding-3-small** via GitHub Models.

> **Built for personal use.** Not a SaaS. Not a demo. A real tool I use daily.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   CLIENT LAYER                      │
│                                                     │
│         Telegram Bot (python-telegram-bot v20)      │
│         natural language I/O, any device            │
└─────────────────────┬───────────────────────────────┘
                      │ HTTPS webhook / polling
┌─────────────────────▼───────────────────────────────┐
│            BACKEND — FastAPI (main.py)               │
│                                                     │
│  session management · webhook endpoint · lifespan   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │                   bot/                       │   │
│  │   telegram_handler.py  ·  session.py         │   │
│  └──────────────────┬───────────────────────────┘   │
│                     │                               │
│  ┌──────────────────▼───────────────────────────┐   │
│  │                  agent/                      │   │
│  │                                              │   │
│  │   openclaw_runner.py  — tool-calling loop    │   │
│  │   llm_router.py       — backend switcher     │   │
│  │   prompt.py           — JARVIS system prompt │   │
│  └──────────────────┬───────────────────────────┘   │
│                     │ dispatches to                 │
│  ┌──────────────────▼───────────────────────────┐   │
│  │                  tools/                      │   │
│  │                                              │   │
│  │   __init__.py     — auto-registration        │   │
│  │   rag_search.py   — semantic KB lookup       │   │
│  │   memory_tool.py  — read/write user facts    │   │
│  │   [drop any .py here to add a new tool]      │   │
│  └───────┬──────────────────┬───────────────────┘   │
│          │                  │                       │
│  ┌───────▼──────┐  ┌────────▼───────────────────┐   │
│  │    rag/      │  │         memory/             │   │
│  │              │  │                             │   │
│  │ embedder.py  │  │  store.py                   │   │
│  │ qdrant_      │  │  memory.db (SQLite)          │   │
│  │  client.py   │  │                             │   │
│  │ ingest.py    │  └─────────────────────────────┘   │
│  └───────┬──────┘                                   │
│          │                                          │
│  ┌───────▼──────────────────────────────────────┐   │
│  │       Qdrant (local · port 6333)             │   │
│  │       vector store · rishi_knowledge         │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

           LLM ROUTER (agent/llm_router.py)

  GitHub Models GPT-4o mini  ←  default
  Groq                        ←  LLM_BACKEND=groq
  Nvidia NIM                  ←  LLM_BACKEND=nim
  opencode/zen                ←  LLM_BACKEND=zen

  Embeddings: text-embedding-3-small via GitHub Models
```

---

## Project Structure

```
RISHI/
├── main.py                     # FastAPI app, lifespan, webhook endpoint
├── config.py                   # Typed settings from .env (pydantic-settings)
├── requirements.txt
├── .env                        # secrets — gitignored
├── .env.example
│
├── agent/
│   ├── openclaw_runner.py      # OpenClaw tool-calling loop (up to 8 turns)
│   ├── llm_router.py           # Returns (AsyncOpenAI client, model) by backend
│   └── prompt.py               # JARVIS-style system prompt
│
├── bot/
│   ├── telegram_handler.py     # PTB v20 handlers, build_app()
│   └── session.py              # Per-user in-memory message history (last 20)
│
├── tools/
│   ├── __init__.py             # Auto-discovers all tools via pkgutil
│   ├── rag_search.py           # Tool: query Qdrant knowledge base
│   └── memory_tool.py          # Tool: read/write user facts to SQLite
│
├── rag/
│   ├── embedder.py             # text-embedding-3-small via GitHub Models
│   ├── qdrant_client.py        # Async Qdrant wrapper, ensure_collection()
│   └── ingest.py               # CLI: ingest PDFs/md/txt into Qdrant
│
├── memory/
│   ├── store.py                # aiosqlite CRUD: user_facts, summaries
│   └── memory.db               # SQLite file (gitignored)
│
└── uploads/                    # Gitignored upload staging area
```

---

## Core Features

### 🧠 Semantic Knowledge Base
- Ingest PDFs, Markdown, and plain text via the `ingest.py` CLI
- Embedded with **text-embedding-3-small** (1536-dim) via GitHub Models
- Stored in local **Qdrant** — semantic search on every query via `rag_search` tool
- Agent decides autonomously when to search the KB

### 💾 Persistent Memory
- User facts and conversation summaries stored in local **SQLite** (`memory.db`)
- `memory_tool` lets the agent read and write facts across sessions
- No cloud dependency — fully local

### 🔌 Plugin Tool System
- Drop a `.py` file in `/tools` with `TOOL_DEFINITION` + `async def run()` — auto-registered on restart
- No config changes, no imports to update
- Currently registered: `rag_search`, `memory_tool`

### 🔀 Swappable LLM Backend
- All backends are OpenAI-compatible — same agent loop, different client
- Switch via `.env`, restart uvicorn — no code changes

| Backend | Model | Use case |
|---|---|---|
| `github` (default) | gpt-4o-mini | balanced, free tier |
| `groq` | llama-3.3-70b-versatile | fast inference |
| `nim` | meta/llama-3.1-70b-instruct | GPU-grade inference |
| `zen` | configurable | opencode/zen routing |

### 📱 Telegram Interface
- Full async PTB v20 — webhook in prod, polling for local dev
- Per-user session with 20-message rolling history
- `/start` command + natural language message handling

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + uvicorn |
| Agent | OpenClaw (tool-calling loop) |
| Interface | python-telegram-bot v20 (async) |
| LLM (default) | GPT-4o mini via GitHub Models |
| LLM (alts) | Groq · Nvidia NIM · opencode/zen |
| Embeddings | text-embedding-3-small via GitHub Models |
| Vector DB | Qdrant (local, Docker) |
| Memory | SQLite via aiosqlite |
| Config | pydantic-settings + .env |
| Language | Python 3.11+ |

---

## Setup

### Prerequisites
- Python 3.11+
- Docker (for Qdrant)
- Telegram bot token via BotFather
- GitHub personal access token (for GitHub Models — LLM + embeddings)
- ngrok or any tunnel for webhook during local dev

### Installation

```cmd
:: 1. Create venv
python -m venv .venv
.venv\Scripts\activate

:: 2. Install dependencies
pip install -r requirements.txt

:: 3. Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

:: 4. Configure environment
copy .env.example .env
:: Fill in TELEGRAM_BOT_TOKEN, GITHUB_TOKEN
:: Leave WEBHOOK_URL empty for local polling mode
```

### Ingest Knowledge Base

```cmd
python -m rag.ingest --path .\docs\ --source "my notes"
```

### Run — local dev (polling, no webhook needed)

```cmd
uvicorn main:app --reload --port 8000
```

### Run — production (webhook)

```cmd
:: Set WEBHOOK_URL=https://your-domain.com in .env (no trailing slash)
uvicorn main:app --port 8000
```

### Switch LLM Backend

```env
LLM_BACKEND=groq
LLM_MODEL=llama-3.3-70b-versatile
```

---

## Adding a Custom Tool

1. Create `tools/my_tool.py`
2. Export `TOOL_DEFINITION` + `async def run(**kwargs) -> str`
3. Restart — auto-registered, nothing else to change

```python
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": "What this tool does.",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "The input."}
            },
            "required": ["input"]
        }
    }
}

async def run(input: str) -> str:
    return f"result for: {input}"
```

---

## Why I Built This

Every AI tool I tried either lacked memory, couldn't take real actions, or required handing data over to a third-party SaaS. I wanted something that:

- Knew my full personal and project context
- Could actually *do* things through a clean, extensible tool system
- Ran entirely on my own machine
- Was accessible from anywhere through Telegram

R.I.S.H.I. is that. It's not a product. It's infrastructure for thinking.

---

## Roadmap

- [x] FastAPI backend with webhook + polling support
- [x] OpenClaw agent with tool-calling loop
- [x] GitHub Models GPT-4o mini as default LLM
- [x] Multi-backend LLM router (Groq, NIM, zen)
- [x] Qdrant RAG with text-embedding-3-small
- [x] Plugin-style tool auto-registration
- [x] SQLite memory persistence
- [x] Telegram client (PTB v20 async)
- [x] Web search tool
- [ ] Web UI (Next.js + FastAPI SSE streaming)
- [ ] Desktop app (Electron wrapper)
- [ ] PWA (manifest + service worker)
- [ ] Voice interface (faster-whisper STT + Piper TTS)
- [ ] Proactive reminders and scheduled tasks
- [ ] Calendar and task management agent

---

## Author

**Hritabrata Das** — B.E. CSE (AI & ML), Chitkara University Punjab
[hrick.me](https://hrick.me) · [GitHub](https://github.com/Hrick-08) · [LinkedIn](http://linkedin.com/in/hritabrata-das)

---

<div align="center">
  <sub>Built for personal use. Shared for inspiration.</sub>
</div>