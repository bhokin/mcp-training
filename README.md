# MCP Workshop — Building Internal MCP Servers with Python & FastMCP

A hands-on workshop for software engineers to learn how to build MCP (Model Context Protocol) servers for internal tooling — using Python and [FastMCP](https://github.com/jlowin/fastmcp).

---

## What You'll Learn

| Chapter | Topic | Key Concept |
|---|---|---|
| 01 | Hello MCP | Tools, running a server, testing with Inspector |
| 02 | Database Tools | SQLite integration, real-world tool patterns |
| 03 | FastAPI Mounting | Production-ready HTTP server with Streamable HTTP transport |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/bhokin/mcp-training.git
cd mcp-training
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

Install for all the chapter you're working on:

```bash
pip install -r requirements.txt
```

---

## Running Each Chapter

```bash
# Chapter 01
python chapter-01-hello-mcp/server.py

# Chapter 02 — seed the database first
python chapter-02-database-tools/seed_db.py
python chapter-02-database-tools/server.py

# Chapter 03 — runs as HTTP server
cd chapter-03-fastapi-mounting
uvicorn main:app --reload
```

---

## Testing with MCP Inspector

1. Start your server
2. Open a new terminal, thn run `fastmcp dev inspector server.py`
3. Connect to your server and call tools interactively