import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from ai_service import generate_diagram
from mermaid_parser import parse_mermaid
from visio_exporter import export_to_visio

app = FastAPI(title="Diagram Builder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    description: str
    diagram_type: str = "auto"


class ExportVisioRequest(BaseModel):
    mermaid_code: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate")
def generate(req: GenerateRequest):
    if not req.description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty")

    try:
        result = generate_diagram(req.description, req.diagram_type)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {exc}")

    return result


@app.post("/api/export/visio")
def export_visio(req: ExportVisioRequest):
    if not req.mermaid_code.strip():
        raise HTTPException(status_code=400, detail="mermaid_code cannot be empty")

    try:
        diagram = parse_mermaid(req.mermaid_code)
        if not diagram.nodes:
            raise ValueError(
                "Could not parse any nodes from the Mermaid code. "
                "Only flowchart and graph diagram types support Visio export."
            )
        vsdx_bytes = export_to_visio(diagram)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Visio export failed: {exc}")

    return Response(
        content=vsdx_bytes,
        media_type="application/vnd.ms-visio.drawing",
        headers={"Content-Disposition": 'attachment; filename="diagram.vsdx"'},
    )
