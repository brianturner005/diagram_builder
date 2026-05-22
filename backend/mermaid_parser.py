import re
from dataclasses import dataclass, field


@dataclass
class DiagramNode:
    id: str
    label: str
    shape: str = "rectangle"  # rectangle, diamond, circle, cylinder, rounded


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

    # For unsupported diagram types, return minimal structure
    return ParsedDiagram(diagram_type="unknown")


def _parse_flow_graph(code: str) -> ParsedDiagram:
    lines = code.strip().split("\n")
    header = lines[0].strip()
    diagram_type = "flowchart" if header.lower().startswith("flowchart") else "graph"

    nodes: dict[str, DiagramNode] = {}
    edges: list[DiagramEdge] = []
    subgraphs: dict[str, list[str]] = {}
    current_subgraph: str | None = None

    # Patterns for node shapes in Mermaid
    node_patterns = [
        # cylinder [(label)]
        (r'\[(\((.+?)\))\]', "cylinder"),
        # diamond {label}
        (r'\{(.+?)\}', "diamond"),
        # circle ((label))
        (r'\(\((.+?)\)\)', "circle"),
        # rounded (label)
        (r'\((.+?)\)', "rounded"),
        # rectangle [label]
        (r'\[(.+?)\]', "rectangle"),
    ]

    # Edge pattern: ID -->|label| ID or ID --> ID or ID --- ID
    edge_pattern = re.compile(
        r'([A-Za-z0-9_]+)'           # source node
        r'\s*'
        r'(-->|---|\-\.\->|===>|-.->|==>)'  # arrow type
        r'(?:\|([^|]+)\|)?'          # optional label between pipes
        r'\s*'
        r'([A-Za-z0-9_]+)'           # target node
    )

    # Node definition pattern: ID[label] or ID{label} etc.
    node_def_pattern = re.compile(
        r'^([A-Za-z0-9_]+)'
        r'(\[|\(|\{|\[\()'
    )

    def extract_node(node_id: str, rest: str) -> DiagramNode:
        """Extract node shape and label from the remainder of a node definition."""
        for pattern, shape in node_patterns:
            m = re.match(pattern, rest)
            if m:
                label = m.group(1)
                # Strip nested parens for cylinder
                label = label.strip("()")
                return DiagramNode(id=node_id, label=label.strip(), shape=shape)
        return DiagramNode(id=node_id, label=node_id, shape="rectangle")

    for raw_line in lines[1:]:
        line = raw_line.strip()

        if not line or line.startswith("%%"):
            continue

        # Subgraph start
        if line.lower().startswith("subgraph"):
            parts = line.split(None, 1)
            name = parts[1].strip().strip('"') if len(parts) > 1 else "group"
            current_subgraph = name
            subgraphs[name] = []
            continue

        # Subgraph end
        if line == "end":
            current_subgraph = None
            continue

        # Edge detection
        edge_match = edge_pattern.search(line)
        if edge_match:
            src_id = edge_match.group(1)
            arrow = edge_match.group(2)
            edge_label = (edge_match.group(3) or "").strip()
            tgt_id = edge_match.group(4)

            arrow_type = "arrow" if "-->" in arrow else "line"
            edges.append(DiagramEdge(
                source=src_id,
                target=tgt_id,
                label=edge_label,
                arrow_type=arrow_type,
            ))

            # Parse inline node definitions on both sides of the edge
            for side, node_id in [("left", src_id), ("right", tgt_id)]:
                if node_id not in nodes:
                    # Find the node definition in the full line
                    node_match = re.search(
                        r'\b' + re.escape(node_id) + r'(\[|\(|\{|\[\()(.*?)(?=\s*(?:-->|---|$))',
                        line
                    )
                    if node_match:
                        rest = node_match.group(1) + node_match.group(2)
                        nodes[node_id] = extract_node(node_id, rest)
                    else:
                        nodes[node_id] = DiagramNode(id=node_id, label=node_id, shape="rectangle")

                if current_subgraph and node_id not in subgraphs[current_subgraph]:
                    subgraphs[current_subgraph].append(node_id)
            continue

        # Standalone node definition
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
