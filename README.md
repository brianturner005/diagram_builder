# Diagram Builder

A web app that converts plain-English descriptions into diagrams using Google Gemini AI. Type what you want, get a live preview, and export to Mermaid, SVG, PNG, or Visio (.vsdx).

## Prerequisites

- Python 3.11+
- Node.js 18+
- A [Google Gemini API key](https://aistudio.google.com/apikey) (free)

## Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

cp ../.env.example .env
# Open .env and set GEMINI_API_KEY=your_key_here

uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd vite-project
npm install --legacy-peer-deps
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

Both servers must be running at the same time. The frontend proxies `/api` requests to the backend automatically.

## Usage

1. Enter a plain-English description in the text box, e.g.:
   > *"A three-tier web architecture with a load balancer, two app servers behind it, and a shared PostgreSQL database"*
2. Optionally choose a diagram type (Auto-detect works well in most cases)
3. Click **Generate Diagram** — the diagram appears instantly as a live preview
4. Export using any of the four buttons:
   | Format | How |
   |---|---|
   | Mermaid (.mmd) | Downloads the raw diagram code |
   | SVG | Exports the rendered vector image |
   | PNG | Exports a rasterized image with white background |
   | Visio (.vsdx) | Server-side export, openable and editable in Microsoft Visio |

## Diagram types supported

- Flowcharts and decision trees
- Network and architecture diagrams
- Org charts and hierarchies
- Sequence diagrams (system/actor interactions)
- Class diagrams
- ER diagrams (database schemas)
- Mind maps

## How it works

```
User description
      │
      ▼
Google Gemini AI (gemini-2.0-flash)
      │  generates Mermaid.js code
      ▼
Browser renders live preview (Mermaid.js)
      │
      ├─── SVG / PNG ──► client-side export
      ├─── Mermaid ────► .mmd file download
      └─── Visio ──────► FastAPI backend
                              │  parses Mermaid → nodes & edges
                              │  BFS layout algorithm assigns positions
                              │  vsdx library writes .vsdx file
                              ▼
                         diagram.vsdx download
```

## Project structure

```
diagram_builder/
├── backend/
│   ├── main.py             # FastAPI app, API endpoints
│   ├── ai_service.py       # Gemini API integration
│   ├── mermaid_parser.py   # Extracts nodes/edges from Mermaid code
│   ├── visio_exporter.py   # Lays out and writes .vsdx files
│   └── requirements.txt
└── vite-project/
    └── src/
        ├── App.jsx
        ├── api.js                        # fetch wrappers
        └── components/
            ├── DiagramInput.jsx          # description textarea + controls
            ├── DiagramPreview.jsx        # live Mermaid rendering
            └── ExportPanel.jsx           # export buttons
```

## Stack

| Layer | Technology |
|---|---|
| AI | Google Gemini SDK (`gemini-2.0-flash`) |
| Backend | Python, FastAPI, uvicorn |
| Visio export | `vsdx` Python library |
| Frontend | React 18, Vite |
| Diagram rendering | Mermaid.js |
