import os
import tempfile
from collections import deque

import vsdx

from mermaid_parser import ParsedDiagram, DiagramNode

# Layout constants (Visio units ≈ inches)
H_SPACING = 2.2
V_SPACING = 1.4
NODE_W = 1.8
NODE_H = 0.8
MARGIN_X = 1.5
MARGIN_Y = 9.0  # Visio Y axis is inverted (0 at bottom), so start high


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

    positions: dict[str, tuple[float, float]] = {}
    for lyr in sorted(layers.keys()):
        layer_nodes = layers[lyr]
        for col, nid in enumerate(layer_nodes):
            x = MARGIN_X + col * (NODE_W + H_SPACING)
            # Visio Y decreases downward from MARGIN_Y
            y = MARGIN_Y - lyr * (NODE_H + V_SPACING)
            positions[nid] = (x, y)

    return positions


def export_to_visio(diagram: ParsedDiagram) -> bytes:
    if not diagram.nodes:
        raise ValueError("Diagram has no nodes to export")

    positions = _bfs_layout(diagram.nodes, diagram.edges)

    # Use the vsdx media.vsdx as a starting template
    basedir = os.path.dirname(os.path.abspath(vsdx.__file__))
    media_path = os.path.join(basedir, "media", "media.vsdx")

    with vsdx.VisioFile(media_path) as vis:
        page = vis.pages[0]

        # Clear all existing template shapes
        for shape in list(page.child_shapes):
            shape.remove()

        media = vsdx.Media()
        shape_map: dict[str, vsdx.Shape] = {}

        for node in diagram.nodes:
            x, y = positions.get(node.id, (MARGIN_X, MARGIN_Y))

            # Choose shape based on node type
            if node.shape == "circle":
                base = media.circle
            else:
                base = media.rectangle  # rectangle, rounded, diamond, cylinder all use rectangle

            new_shape = base.copy(page)
            new_shape.x = x
            new_shape.y = y
            new_shape.text = node.label
            shape_map[node.id] = new_shape

        # Add connections between shapes
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
