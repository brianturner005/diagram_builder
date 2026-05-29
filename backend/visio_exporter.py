import os
import tempfile
from collections import deque

import vsdx

from mermaid_parser import ParsedDiagram, DiagramNode

# Layout constants (Visio units ≈ inches)
H_SPACING = 2.4
V_SPACING = 1.5
NODE_W = 1.8
NODE_H = 0.75
MARGIN_X = 1.5
MARGIN_Y = 9.0  # Visio Y axis is inverted (0 at bottom), so start high


def _hex_to_rgb_str(hex_color: str) -> str:
    """Convert #RRGGBB to 'R, G, B' string for vsdx color format."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"#{hex_color.upper()}"


def _bfs_layout(nodes: list[DiagramNode], edges) -> dict[str, tuple[float, float]]:
    if not nodes:
        return {}

    node_ids = {n.id for n in nodes}
    children: dict[str, list[str]] = {n.id: [] for n in nodes}
    parents: dict[str, list[str]] = {n.id: [] for n in nodes}

    for edge in edges:
        if edge.source in node_ids and edge.target in node_ids:
            children[edge.source].append(edge.target)
            parents[edge.target].append(edge.source)

    roots = [n.id for n in nodes if not parents[n.id]]
    if not roots:
        roots = [nodes[0].id]

    layer: dict[str, int] = {}
    queue: deque = deque()
    for root in roots:
        layer[root] = 0
        queue.append(root)

    while queue:
        current = queue.popleft()
        for child in children[current]:
            new_layer = layer[current] + 1
            if child not in layer or layer[child] < new_layer:
                layer[child] = new_layer
                queue.append(child)

    max_layer = max(layer.values(), default=0)
    for n in nodes:
        if n.id not in layer:
            max_layer += 1
            layer[n.id] = max_layer

    layers: dict[int, list[str]] = {}
    for nid, lyr in layer.items():
        layers.setdefault(lyr, []).append(nid)

    # Center each layer horizontally
    max_layer_width = max(len(v) for v in layers.values())
    positions: dict[str, tuple[float, float]] = {}

    for lyr in sorted(layers.keys()):
        layer_nodes = layers[lyr]
        total_w = len(layer_nodes) * (NODE_W + H_SPACING) - H_SPACING
        max_w = max_layer_width * (NODE_W + H_SPACING) - H_SPACING
        start_x = MARGIN_X + (max_w - total_w) / 2  # center the layer

        for col, nid in enumerate(layer_nodes):
            x = start_x + col * (NODE_W + H_SPACING)
            y = MARGIN_Y - lyr * (NODE_H + V_SPACING)
            positions[nid] = (x, y)

    return positions


def export_to_visio(diagram: ParsedDiagram) -> bytes:
    if not diagram.nodes:
        raise ValueError("Diagram has no nodes to export")

    positions = _bfs_layout(diagram.nodes, diagram.edges)

    basedir = os.path.dirname(os.path.abspath(vsdx.__file__))
    media_path = os.path.join(basedir, "media", "media.vsdx")

    with vsdx.VisioFile(media_path) as vis:
        page = vis.pages[0]

        # Clear existing template shapes
        for shape in list(page.child_shapes):
            shape.remove()

        media = vsdx.Media()
        shape_map: dict[str, vsdx.Shape] = {}

        for node in diagram.nodes:
            x, y = positions.get(node.id, (MARGIN_X, MARGIN_Y))

            base = media.circle if node.shape == "circle" else media.rectangle
            new_shape = base.copy(page)
            new_shape.x = x
            new_shape.y = y
            new_shape.text = node.label

            # Apply fill and text colors
            try:
                new_shape.fill_color = node.fill_color
                new_shape.text_color = "#FFFFFF"
                new_shape.line_color = _darken_hex(node.fill_color)
            except Exception:
                pass  # Color setting is best-effort

            shape_map[node.id] = new_shape

        # Add connections
        for edge in diagram.edges:
            src = shape_map.get(edge.source)
            tgt = shape_map.get(edge.target)
            if src and tgt:
                vsdx.Connect.create(page=page, from_shape=src, to_shape=tgt)

        with tempfile.NamedTemporaryFile(suffix=".vsdx", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            vis.save_vsdx(tmp_path)
            with open(tmp_path, "rb") as f:
                return f.read()
        finally:
            os.unlink(tmp_path)


def _darken_hex(hex_color: str, factor: float = 0.7) -> str:
    """Return a darkened version of a hex color for borders."""
    hex_color = hex_color.lstrip("#")
    r = int(int(hex_color[0:2], 16) * factor)
    g = int(int(hex_color[2:4], 16) * factor)
    b = int(int(hex_color[4:6], 16) * factor)
    return f"#{r:02X}{g:02X}{b:02X}"
