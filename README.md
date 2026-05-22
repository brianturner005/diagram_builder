# Diagram Builder

A web app that converts natural language descriptions into diagrams using Claude AI. Supports export to Mermaid, SVG, PNG, and Visio (.vsdx).

## Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd vite-project
npm install --legacy-peer-deps
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Usage

1. Type a description, e.g. *"A microservices architecture with API gateway, auth service, product service, and PostgreSQL database"*
2. Click **Generate Diagram**
3. Export as **Mermaid** (.mmd), **SVG**, **PNG**, or **Visio** (.vsdx)

## Diagram types supported

- Flowcharts and workflows
- Network and architecture diagrams
- Org charts and hierarchies
- Sequence diagrams
- Class diagrams
- ER diagrams
- Mind maps

## Stack

- **Backend**: Python + FastAPI + Anthropic SDK
- **Frontend**: React + Vite + Mermaid.js
- **Visio export**: `vsdx` Python library
