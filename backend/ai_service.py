import anthropic
import os

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


SYSTEM_PROMPT = """You are a diagram specification expert. Given a natural language description, generate valid Mermaid.js diagram code.

Rules:
- Return ONLY the raw Mermaid code, no markdown fences, no explanation, no extra text
- Choose the most appropriate diagram type:
  - flowchart TD or flowchart LR for processes, workflows, decision trees
  - graph TD for org charts, hierarchies, architecture diagrams
  - sequenceDiagram for interactions between systems or actors
  - classDiagram for object or data models
  - erDiagram for database schemas
  - mindmap for concept maps
- Use clear, concise node labels (3-5 words max)
- For architecture diagrams, group related components using subgraph blocks
- Node IDs must be alphanumeric only (no spaces or special characters)
- Ensure the code is syntactically valid Mermaid.js"""


def generate_diagram(description: str, diagram_type: str = "auto") -> dict:
    client = _get_client()

    user_message = f"Generate a diagram for: {description}"
    if diagram_type != "auto":
        user_message += f"\n\nUse diagram type: {diagram_type}"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    mermaid_code = message.content[0].text.strip()
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
