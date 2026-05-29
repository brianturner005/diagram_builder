# Diagram Builder

A web app that converts plain-English descriptions into network and infrastructure diagrams using Google Gemini AI. Supports Cisco, AWS, Azure, GCP, and Kubernetes icons. Export as `.drawio` for editing in diagrams.net or importing into Visio.

## Prerequisites

- Python 3.11+
- Node.js 18+
- A [Google Gemini API key](https://aistudio.google.com/apikey) (free)

## Local Development

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

cp ../.env.example .env
# Open .env and set GEMINI_API_KEY=your_key_here

python -m uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd vite-project
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). Both servers must be running at the same time — the frontend proxies `/api` requests to the backend automatically.

## Deploying to Azure Static Web Apps

### 1. Create the Azure resource

1. Go to [portal.azure.com](https://portal.azure.com) and search for **Static Web Apps**
2. Click **Create** and fill in:
   - **Plan** — Free tier works fine
   - **Source** — GitHub → authorize → select this repo, branch `main`
   - **Build preset** — Custom
   - **App location** — `vite-project`
   - **API location** — `api`
   - **Output location** — `dist`
3. Click **Review + Create**

Azure automatically adds `AZURE_STATIC_WEB_APPS_API_TOKEN` as a secret to your GitHub repo. Until this step is done the workflow will skip the deploy step rather than fail (controlled by `skip_deploy_on_missing_secrets: true` in the workflow file).

### 2. Add your Gemini API key

In the Azure Portal, go to your Static Web App → **Configuration** → **Application settings** → **Add**:

```
Name:  GEMINI_API_KEY
Value: your_key_here
```

Click **Save**.

### 3. Deploy

Push any commit to `main` — the GitHub Actions workflow builds the frontend and deploys the Azure Functions automatically. Every subsequent push to `main` redeploys.

## Usage

- **Templates** — click any of the 8 preset cards to generate a diagram instantly
- **Custom description** — type anything in plain English and click Generate
- **Update diagram** — once a diagram is on screen, describe a change in the Update panel to modify it in place
- **Export** — download as `.drawio` (editable in [diagrams.net](https://app.diagrams.net) or importable into Visio), or click **Open in diagrams.net** to edit directly in the browser

## Supported diagram types

- Corporate and home networks (Cisco stencils)
- AWS architectures (EC2, S3, RDS, Lambda, CloudFront, etc.)
- Azure deployments (App Service, Functions, SQL, Storage, etc.)
- GCP infrastructure (Compute Engine, BigQuery, Cloud Run, Pub/Sub, etc.)
- Kubernetes clusters (pods, deployments, services, ingress, namespaces)
- DMZ and security architectures
- Any general network or infrastructure topology

## How it works

```
User description
      │
      ▼
Google Gemini (gemini-2.5-flash)
      │  generates draw.io XML with
      │  real network/cloud icons
      ▼
diagrams.net viewer
      │  renders live in browser
      ▼
Export as .drawio → open in diagrams.net or Visio
```

## Project structure

```
diagram_builder/
├── api/                        # Azure Functions (production)
│   ├── function_app.py         # /api/generate and /api/update endpoints
│   ├── ai_service.py           # Gemini API integration
│   ├── host.json
│   └── requirements.txt
├── backend/                    # FastAPI server (local development)
│   ├── main.py
│   ├── ai_service.py
│   └── requirements.txt
├── vite-project/               # React frontend
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       ├── templates.js
│       └── components/
│           ├── DiagramInput.jsx   # textarea + template cards
│           ├── DiagramPreview.jsx # diagrams.net viewer
│           ├── UpdatePanel.jsx    # iterative editing
│           └── ExportPanel.jsx    # download + open in editor
├── staticwebapp.config.json    # SWA routing config
└── .github/workflows/
    └── azure-static-web-apps.yml
```

## Stack

| Layer | Technology |
|---|---|
| AI | Google Gemini SDK (`gemini-2.5-flash`) |
| Backend (local) | Python, FastAPI, uvicorn |
| Backend (production) | Python Azure Functions |
| Frontend | React 18, Vite |
| Diagram rendering | diagrams.net embedded viewer |
| Hosting | Azure Static Web Apps |
