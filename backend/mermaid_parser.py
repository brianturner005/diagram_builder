import re
from dataclasses import dataclass, field


# Maps classDef names to hex fill colors (matches the AI prompt's classDef palette)
CLASS_COLORS: dict[str, str] = {
    "process":  "#2E86AB",
    "decision": "#E67E22",
    "terminal": "#27AE60",
    "database": "#8E44AD",
    "external": "#566573",
    "service":  "#17A589",
    "alert":    "#E74C3C",
}

# Default color when no class is assigned
DEFAULT_COLOR = "#2E86AB"


@dataclass
class DiagramNode:
    id: str
    label: str
    shape: str = "rectangle"   # rectangle, diamond, circle, cylinder, rounded
    css_class: str = ""        # classDef name applied to this node
    fill_color: str = DEFAULT_COLOR


@dataclass
class DiagramEdge:
    source: str
    target: str
    label: str = ""
    arrow_type: str = "arrow"


@dataclass
class ParsedDiagram:
    diagram_type: str
    nodes: list[DiagramNode] = field(default_factory=list)
    edges: list[DiagramEdge] = field(default_factory=list)
    subgraphs: dict[str, list[str]] = field(default_factory=dict)


def parse_mermaid(mermaid_code: str) -> ParsedDiagram:
    lines = mermaid_code.strip().split("\n")
    first_line = lines[0].strip().lower()

    if first_line.startswith("flowchart") or first_line.startswith("graph"):
        return _parse_flow_graph(mermaid_code)

    return ParsedDiagram(diagram_type="unknown")


def _parse_flow_graph(code: str) -> ParsedDiagram:
    lines = code.strip().split("\n")
    header = lines[0].strip()
    diagram_type = "flowchart" if header.lower().startswith("flowchart") else "graph"

    nodes: dict[str, DiagramNode] = {}
    edges: list[DiagramEdge] = []
    subgraphs: dict[str, list[str]] = {}
    current_subgraph: str | None = None
    # classDef name → fill color (parsed from the diagram itself)
    class_colors: dict[str, str] = dict(CLASS_COLORS)

    # Patterns for node shapes
    node_patterns = [
        (r'\[\((.+?)\)\]', "cylinder"),   # [(label)]
        (r'\{(.+?)\}',     "diamond"),    # {label}
        (r'\(\((.+?)\)\)', "circle"),     # ((label))
        (r'\((.+?)\)',     "rounded"),    # (label)
        (r'\[(.+?)\]',     "rectangle"),  # [label]
    ]

    edge_pattern = re.compile(
        r'([A-Za-z0-9_]+)'
        r'\s*'
        r'(-->|---|-\.-?>|===>|-.->|==>)'
        r'(?:\|([^|]+)\|)?'
        r'\s*'
        r'([A-Za-z0-9_]+)'
    )

    node_def_pattern = re.compile(r'^([A-Za-z0-9_]+)(\[|\(|\{)')

    # classDef line: classDef name fill:#hex,...
    classdef_pattern = re.compile(r'^classDef\s+(\w+)\s+.*?fill:([#\w]+)', re.IGNORECASE)

    # class assignment line: class nodeId,nodeId2 className
    class_assign_pattern = re.compile(r'^class\s+([\w,\s]+)\s+(\w+)$')

    def extract_node(node_id: str, rest: str) -> DiagramNode:
        # Strip :::className suffix before matching shape
        css_class = ""
        class_match = re.search(r':::(\w+)', rest)
        if class_match:
            css_class = class_match.group(1)
            rest = rest[:class_match.start()]

        for pattern, shape in node_patterns:
            m = re.match(pattern, rest)
            if m:
                label = m.group(1).strip()
                color = class_colors.get(css_class, _shape_default_color(shape))
                return DiagramNode(id=node_id, label=label, shape=shape,
                                   css_class=css_class, fill_color=color)

        color = class_colors.get(css_class, DEFAULT_COLOR)
        return DiagramNode(id=node_id, label=node_id, shape="rectangle",
                           css_class=css_class, fill_color=color)

    for raw_line in lines[1:]:
        line = raw_line.strip()

        if not line or line.startswith("%%"):
            continue

        # Parse classDef to capture any custom colors defined in the diagram
        cd_match = classdef_pattern.match(line)
        if cd_match:
            class_colors[cd_match.group(1)] = cd_match.group(2)
            continue

        # Parse `class nodeId className` assignments
        ca_match = class_assign_pattern.match(line)
        if ca_match:
            ids = [i.strip() for i in ca_match.group(1).split(",")]
            css_class = ca_match.group(2).strip()
            for nid in ids:
                if nid in nodes:
                    nodes[nid].css_class = css_class
                    nodes[nid].fill_color = class_colors.get(css_class, DEFAULT_COLOR)
            continue

        if line.lower().startswith("subgraph"):
            parts = line.split(None, 1)
            name = parts[1].strip().strip('"') if len(parts) > 1 else "group"
            current_subgraph = name
            subgraphs[name] = []
            continue

        if line == "end":
            current_subgraph = None
            continue

        edge_match = edge_pattern.search(line)
        if edge_match:
            src_id = edge_match.group(1)
            arrow = edge_match.group(2)
            edge_label = (edge_match.group(3) or "").strip()
            tgt_id = edge_match.group(4)

            arrow_type = "arrow" if "-->" in arrow or "==>" in arrow else "line"
            edges.append(DiagramEdge(source=src_id, target=tgt_id,
                                     label=edge_label, arrow_type=arrow_type))

            for node_id in (src_id, tgt_id):
                if node_id not in nodes:
                    node_match = re.search(
                        r'\b' + re.escape(node_id) + r'(\[|\(|\{)(.*?)(?=\s*(?:-->|---|==>|$))',
                        line
                    )
                    if node_match:
                        rest = node_match.group(1) + node_match.group(2)
                        nodes[node_id] = extract_node(node_id, rest)
                    else:
                        nodes[node_id] = DiagramNode(id=node_id, label=node_id,
                                                     shape="rectangle", fill_color=DEFAULT_COLOR)
                if current_subgraph and node_id not in subgraphs[current_subgraph]:
                    subgraphs[current_subgraph].append(node_id)
            continue

        nd_match = node_def_pattern.match(line)
        if nd_match:
            node_id = nd_match.group(1)
            rest = line[len(node_id):]
            if node_id not in nodes:
                nodes[node_id] = extract_node(node_id, rest)
            if current_subgraph and node_id not in subgraphs[current_subgraph]:
                subgraphs[current_subgraph].append(node_id)

    return ParsedDiagram(
        diagram_type=diagram_type,
        nodes=list(nodes.values()),
        edges=edges,
        subgraphs=subgraphs,
    )


def _shape_default_color(shape: str) -> str:
    return {
        "diamond":   CLASS_COLORS["decision"],
        "cylinder":  CLASS_COLORS["database"],
        "circle":    CLASS_COLORS["terminal"],
        "rounded":   CLASS_COLORS["terminal"],
        "rectangle": CLASS_COLORS["process"],
    }.get(shape, DEFAULT_COLOR)
