import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_service import generate_diagram, update_diagram

app = FastAPI(title="Diagram Builder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    description: str


class UpdateRequest(BaseModel):
    existing_xml: str
    change_description: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate")
def generate(req: GenerateRequest):
    if not req.description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty")
    try:
        return generate_diagram(req.description)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {exc}")


@app.post("/api/update")
def update(req: UpdateRequest):
    if not req.change_description.strip():
        raise HTTPException(status_code=400, detail="Change description cannot be empty")
    if not req.existing_xml.strip():
        raise HTTPException(status_code=400, detail="No existing diagram to update")
    try:
        return update_diagram(req.existing_xml, req.change_description)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI update failed: {exc}")
