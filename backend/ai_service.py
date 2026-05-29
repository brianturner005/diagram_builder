import os
import google.generativeai as genai

_model = None


def _get_model() -> genai.GenerativeModel:
    global _model
    if _model is None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        _model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
        )
    return _model


SYSTEM_PROMPT = """You are a professional diagram design expert. Given a natural language description, generate visually rich, well-styled Mermaid.js diagram code that looks like a polished Visio diagram.

CRITICAL: Return ONLY raw Mermaid code. No markdown fences, no explanation, no extra text.

## Shape conventions
Use the correct shape for each node's semantic meaning:
- `[Label]` — rectangular process or action node
- `{Label}` — diamond decision or gateway node
- `([Label])` — rounded terminal (start/end/trigger)
- `[(Label)]` — cylinder database or storage node
- `((Label))` — circle event or connector node
- `>Label]` — asymmetric flag/annotation node

## Styling — ALWAYS include these classDef blocks and apply them
```
classDef process fill:#2E86AB,stroke:#1a5276,color:#fff,stroke-width:2px
classDef decision fill:#E67E22,stroke:#a04000,color:#fff,stroke-width:2px
classDef terminal fill:#27AE60,stroke:#1e8449,color:#fff,stroke-width:2px
classDef database fill:#8E44AD,stroke:#6c3483,color:#fff,stroke-width:2px
classDef external fill:#566573,stroke:#2c3e50,color:#fff,stroke-width:2px
classDef service fill:#17A589,stroke:#0e6655,color:#fff,stroke-width:2px
classDef alert fill:#E74C3C,stroke:#a93226,color:#fff,stroke-width:2px
```

Apply classes inline using `:::className` after each node definition:
- Process/action nodes → `:::process`
- Decision nodes → `:::decision`
- Start/end terminals → `:::terminal`
- Databases/storage → `:::database`
- External systems → `:::external`
- Services/APIs → `:::service`
- Errors/warnings → `:::alert`

## Arrow styling
- Use `-->` for standard flow
- Use `-.->` for optional or async paths
- Use `==>` for critical or primary paths
- Always add labels to decision branches: `-->|Yes|` and `-->|No|`
- Add labels to other arrows where they clarify the relationship

## Layout rules
- Choose `flowchart TD` (top-down) for processes and pipelines
- Choose `flowchart LR` (left-right) for data flows and architectures
- Use `subgraph` blocks to group related components (e.g. by system, team, or layer)
- Keep node labels concise: 2-5 words maximum
- Node IDs must be alphanumeric with no spaces or special characters

## Diagram type selection
- `flowchart TD/LR` — processes, architectures, org charts, pipelines
- `sequenceDiagram` — system interactions, API calls, user flows
- `classDiagram` — data models, object relationships
- `erDiagram` — database schemas
- `mindmap` — concept maps, brainstorming

For sequenceDiagram, classDiagram, erDiagram, and mindmap: use the native styling features of those diagram types instead of classDef."""


def generate_diagram(description: str, diagram_type: str = "auto") -> dict:
    model = _get_model()

    user_message = f"Generate a diagram for: {description}"
    if diagram_type != "auto":
        user_message += f"\n\nUse diagram type: {diagram_type}"

    response = model.generate_content(user_message)
    mermaid_code = response.text.strip()

    # Strip accidental markdown fences if the model includes them
    if mermaid_code.startswith("```"):
        lines = mermaid_code.splitlines()
        mermaid_code = "\n".join(
            line for line in lines if not line.startswith("```")
        ).strip()

    detected_type = _detect_diagram_type(mermaid_code)
    return {"mermaid_code": mermaid_code, "diagram_type": detected_type}


def _detect_diagram_type(mermaid_code: str) -> str:
    first_line = mermaid_code.split("\n")[0].strip().lower()
    if first_line.startswith("flowchart"):
        return "flowchart"
    if first_line.startswith("graph"):
        return "graph"
    if first_line.startswith("sequencediagram"):
        return "sequence"
    if first_line.startswith("classdiagram"):
        return "class"
    if first_line.startswith("erdiagram"):
        return "er"
    if first_line.startswith("mindmap"):
        return "mindmap"
    return "unknown"
