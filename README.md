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
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Middleware-FF6B35?style=flat-square)](https://github.com/openclaw)
[![AWS EC2](https://img.shields.io/badge/AWS-EC2-FF9900?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com/ec2)
[![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-DC244C?style=flat-square)](https://qdrant.tech)
[![Telegram](https://img.shields.io/badge/Telegram-Mobile_Client-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## What is R.I.S.H.I.?

R.I.S.H.I. is a **personal AI companion** that goes beyond a chatbot. It understands your full context, executes real tasks autonomously, searches the web, generates images, manages files, sends emails — and does all of this across devices through a unified backend.

The core intelligence runs on **AWS EC2**, orchestrated through **OpenClaw** as the middleware layer, with **GPT-4o** (via GitHub Copilot) as the primary reasoning brain and **Gemini** handling web search and embeddings.

> **Built for personal use.** Not a SaaS. Not a demo. A real tool I use daily.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│                                                                 │
│   ┌──────────────────────────┐   ┌──────────────────────────┐  │
│   │         Desktop          │   │          Mobile           │  │
│   │                          │   │                           │  │
│   │  OpenClaw TUI            │   │  Telegram Chat Client     │  │
│   │  OpenClaw Control Page   │   │  (natural language I/O)   │  │
│   └────────────┬─────────────┘   └────────────┬──────────────┘  │
│                │                              │                  │
└────────────────┼──────────────────────────────┼──────────────────┘
                 │                              │
                 └──────────────┬───────────────┘
                                │ HTTPS / WebSocket
┌───────────────────────────────▼──────────────────────────────────┐
│                       BACKEND — AWS EC2                           │
│                                                                   │
│   ┌───────────────────────────────────────────────────────────┐   │
│   │                        OpenClaw                            │   │
│   │               (Middleware Orchestration Layer)             │   │
│   │                                                           │   │
│   │  ┌───────────────┐  ┌──────────────┐  ┌───────────────┐  │   │
│   │  │  Agent Core   │  │  RAG Engine  │  │ Memory &      │  │   │
│   │  │               │  │              │  │ Context Store │  │   │
│   │  │ Web Search    │  │ Query →      │  │               │  │   │
│   │  │ Image Gen     │  │ Embed →      │  │ Full user     │  │   │
│   │  │ File Ops      │  │ Search →     │  │ context       │  │   │
│   │  │ Email         │  │ Augment →    │  │ Custom KB     │  │   │
│   │  │ + All OpenClaw│  │ Generate     │  │               │  │   │
│   │  │   abilities   │  │              │  │               │  │   │
│   │  └──────┬────────┘  └──────┬───────┘  └───────────────┘  │   │
│   └─────────┼─────────────────┼─────────────────────────────┘   │
│             │                 │                                   │
│   ┌─────────▼─────────────────▼─────────────────────────────┐    │
│   │                      LLM Layer                            │    │
│   │                                                           │    │
│   │   ┌──────────────────────┐   ┌──────────────────────┐    │    │
│   │   │  GPT-4o              │   │  Gemini              │    │    │
│   │   │  (GitHub Copilot)    │   │  (Gemini API)        │    │    │
│   │   │                      │   │                      │    │    │
│   │   │  Primary brain       │   │  Web search          │    │    │
│   │   │  Reasoning & chat    │   │  Embeddings (3072d)  │    │    │
│   │   └──────────────────────┘   └──────────────────────┘    │    │
│   └───────────────────────────────────────────────────────────┘   │
│                                                                   │
│   ┌───────────────────────────────────────────────────────────┐   │
│   │  Qdrant Vector DB   ·   HuggingFace Stable Diffusion      │   │
│   └───────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Core Features

### 🧠 Full User Context + Custom Knowledge Base
- Maintains persistent, structured context about the user across all sessions
- Ingests PDFs, Markdown, plain text, and web links into a personal knowledge base
- Uses **Gemini Embedding 2** (3072-dim, multimodal) via **Qdrant** for semantic retrieval
- Selective context injection — only relevant knowledge is pulled per query, keeping prompts lean

### 🔍 Real-Time Web Search
- Powered by **Gemini** — searches the web and synthesizes answers inline
- Triggered autonomously when queries require current information
- Results grounded back into the conversation context

### 🎨 Image Generation
- **Stable Diffusion** via HuggingFace for on-demand image generation
- Invoked naturally through conversation: *"generate an image of..."*
- Output delivered directly in the client (TUI or Telegram)

### 🤖 Autonomous Agent Actions
- **Email** — compose and send via natural language
- **File Operations** — read, write, manage files on the host system
- **Full OpenClaw ability set** — all native OpenClaw tools and automations available out of the box

### 🖥️ Multi-Client Access
- **Desktop**: OpenClaw TUI + OpenClaw Control Page — full-featured, keyboard-native interface
- **Mobile**: Telegram bot — send messages, trigger agents, receive responses and images from anywhere

### 🔀 Dual LLM Architecture

| Model | Provider | Role |
|---|---|---|
| GPT-4o | GitHub Copilot | Primary reasoning, conversation, task planning |
| Gemini | Gemini API | Web search, embeddings, multimodal tasks |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Middleware / Orchestration | OpenClaw |
| Hosting | AWS EC2 |
| Primary LLM | GPT-4o (GitHub Copilot) |
| Secondary LLM / Search | Gemini (Gemini API) |
| Vector DB | Qdrant |
| Embeddings | Gemini Embedding 2 (3072-dim) |
| Image Generation | Stable Diffusion (HuggingFace) |
| Desktop Client | OpenClaw TUI + Control Page |
| Mobile Client | Telegram Bot |
| Language | Python 3.11+ |

---

## Project Structure

```
RISHI/
├── agents/
│   ├── web_search.py           # Gemini-powered search agent
│   ├── image_gen.py            # HuggingFace Stable Diffusion
│   ├── email_agent.py          # Email compose + send
│   └── file_agent.py           # File read/write operations
│
├── rag/
│   ├── ingest.py               # Document ingestion pipeline
│   ├── retriever.py            # Qdrant query + semantic search
│   └── embedder.py             # Gemini Embedding 2 wrapper
│
├── memory/
│   └── context_store.py        # Full user context management
│
├── knowledge_base/             # Personal KB source documents
│   ├── *.pdf
│   └── *.md
│
├── openclaw/
│   └── config.yaml             # OpenClaw skill + tool config
│
├── telegram/
│   └── bot.py                  # Telegram mobile client handler
│
├── .env.example
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.11+
- AWS EC2 instance (t3.medium or above recommended)
- Qdrant (Docker or Qdrant Cloud)
- OpenClaw installed on the EC2 instance
- Telegram Bot token (via BotFather)

### Install & Run

```bash
git clone https://github.com/Hrick-08/RISHI.git
cd RISHI

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Fill in your keys (see below)

# Start Qdrant
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant

# Ingest your knowledge base
python -m rag.ingest --source ./knowledge_base/

# Start the Telegram bot
python telegram/bot.py
```

### OpenClaw

```bash
# Install OpenClaw on your EC2 instance per OpenClaw docs
# Configure skills and tool bindings in openclaw/config.yaml
# Launch via OpenClaw TUI or the Control Page in browser
```

---

## Environment Variables

```env
# LLM
GITHUB_COPILOT_TOKEN=
GEMINI_API_KEY=

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# HuggingFace
HF_API_TOKEN=

# Telegram
TELEGRAM_BOT_TOKEN=

# Email Agent
EMAIL_ADDRESS=
EMAIL_APP_PASSWORD=

# AWS
AWS_REGION=
EC2_HOST=
```

---

## Why I Built This

Every AI tool I tried either lacked memory, couldn't take real actions, or required me to hand over my data to a third-party SaaS. I wanted something that:

- Knew my full personal and project context
- Could actually *do* things — search, generate, email, manage files
- Ran on my own infrastructure
- Was accessible from anywhere — desktop terminal or phone

R.I.S.H.I. is that. It's not a product. It's infrastructure for thinking.

---

## Roadmap

- [x] OpenClaw middleware orchestration on AWS EC2
- [x] GPT-4o (GitHub Copilot) as primary reasoning brain
- [x] Gemini web search + embeddings
- [x] Qdrant RAG with custom knowledge base
- [x] Full user context persistence
- [x] Stable Diffusion image generation (HuggingFace)
- [x] Telegram mobile client
- [x] Email + file operations agents
- [ ] Context Orchestrator (selective skill/architecture injection via RAG)
- [ ] Proactive reminders and scheduled tasks
- [ ] Voice interface (faster-whisper STT + Piper TTS)
- [ ] Calendar and task management agent

---

## Author

**Hrick** — B.E. CSE (AI & ML), Chitkara University Punjab  
Web Developer @ GDG On Campus Chitkara  
[hrick.me](https://hrick.me) · [GitHub](https://github.com/Hrick-08)

---

<div align="center">
  <sub>Built for personal use. Shared for inspiration.</sub>
</div>
