"""Convert draw.io XML to Visio .vsdx format (stdlib only, no extra deps)."""
import io
import re
import zipfile
from xml.etree import ElementTree as ET

PAGE_W = 11.0   # landscape letter, inches
PAGE_H = 8.5
MARGIN = 0.5


def generate_vsdx(drawio_xml: str) -> bytes:
    nodes, edges = _parse_drawio(drawio_xml)
    shapes_xml, connects_xml = _build_shapes(nodes, edges)
    return _pack_vsdx(shapes_xml, connects_xml)


# ── Parsing ───────────────────────────────────────────────────────────────────

def _parse_drawio(xml_str: str):
    root = ET.fromstring(xml_str.strip())
    raw = {}

    for cell in root.iter('mxCell'):
        cid = cell.get('id', '')
        if cid in ('0', '1'):
            continue
        raw[cid] = {
            'label':  cell.get('value', '') or '',
            'style':  cell.get('style', ''),
            'vertex': cell.get('vertex') == '1',
            'edge':   cell.get('edge') == '1',
            'source': cell.get('source', ''),
            'target': cell.get('target', ''),
            'parent': cell.get('parent', '1'),
            'geo':    cell.find('mxGeometry'),
        }

    nodes, edges = {}, []
    for cid, c in raw.items():
        if c['vertex'] and c['geo'] is not None:
            x = float(c['geo'].get('x', 0))
            y = float(c['geo'].get('y', 0))
            w = float(c['geo'].get('width', 60))
            h = float(c['geo'].get('height', 60))

            # Resolve one level of container offset
            pid = c['parent']
            if pid not in ('0', '1') and pid in raw and raw[pid]['geo'] is not None:
                x += float(raw[pid]['geo'].get('x', 0))
                y += float(raw[pid]['geo'].get('y', 0))

            s = c['style']
            nodes[cid] = {
                'label':  c['label'],
                'x': x, 'y': y, 'w': w, 'h': h,
                'fill':   _col(s, 'fillColor',   '#dae8fc'),
                'stroke': _col(s, 'strokeColor', '#6c8ebf'),
                'font':   _col(s, 'fontColor',   '#000000'),
            }
        elif c['edge'] and c['source'] and c['target']:
            edges.append({'src': c['source'], 'tgt': c['target'], 'label': c['label']})

    return nodes, edges


def _col(style: str, key: str, default: str) -> str:
    m = re.search(rf'{key}=([^;]+)', style)
    if m:
        v = m.group(1).strip()
        if v.startswith('#'):
            return v
    return default


# ── Coordinate conversion ─────────────────────────────────────────────────────

def _scale(nodes: dict) -> dict:
    if not nodes:
        return {}
    xs  = [n['x']           for n in nodes.values()]
    ys  = [n['y']           for n in nodes.values()]
    x2s = [n['x'] + n['w'] for n in nodes.values()]
    y2s = [n['y'] + n['h'] for n in nodes.values()]
    min_x, min_y = min(xs), min(ys)
    cw = max(x2s) - min_x
    ch = max(y2s) - min_y
    avail_w = PAGE_W - 2 * MARGIN
    avail_h = PAGE_H - 2 * MARGIN
    s = min(avail_w / cw, avail_h / ch) if cw and ch else 1 / 96
    out = {}
    for cid, n in nodes.items():
        cx = (n['x'] + n['w'] / 2 - min_x) * s + MARGIN
        # Visio Y origin is bottom-left; draw.io is top-left — flip it
        cy = PAGE_H - ((n['y'] + n['h'] / 2 - min_y) * s + MARGIN)
        out[cid] = {**n, 'px': cx, 'py': cy, 'pw': n['w'] * s, 'ph': n['h'] * s}
    return out


# ── Shape XML ─────────────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def _shape_xml(vid: int, n: dict) -> str:
    lbl = f'<Text><cp cp="0"/>{_esc(n["label"])}</Text>' if n['label'] else ''
    return (
        f'<Shape ID="{vid}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        f'<XForm>'
        f'<PinX>{n["px"]:.4f}</PinX><PinY>{n["py"]:.4f}</PinY>'
        f'<Width>{n["pw"]:.4f}</Width><Height>{n["ph"]:.4f}</Height>'
        f'<LocPinX F="Width*0.5">{n["pw"]/2:.4f}</LocPinX>'
        f'<LocPinY F="Height*0.5">{n["ph"]/2:.4f}</LocPinY>'
        f'<Angle>0</Angle><FlipX>0</FlipX><FlipY>0</FlipY><ResizeMode>0</ResizeMode>'
        f'</XForm>'
        f'<Fill><FillForegnd>{n["fill"]}</FillForegnd>'
        f'<FillBkgnd>#ffffff</FillBkgnd><FillPattern>1</FillPattern></Fill>'
        f'<Line><LineColor>{n["stroke"]}</LineColor>'
        f'<LineWeight>0.01389</LineWeight><LinePattern>1</LinePattern></Line>'
        f'<Char ix="0"><Color>{n["font"]}</Color><Size>0.0972</Size></Char>'
        f'{lbl}</Shape>'
    )


def _connector_xml(vid: int, src: dict, tgt: dict, label: str) -> str:
    bx, by = src['px'], src['py']
    ex, ey = tgt['px'], tgt['py']
    cx, cy = (bx + ex) / 2, (by + ey) / 2
    w = abs(ex - bx) or 0.001
    h = abs(ey - by) or 0.001
    lbl = f'<Text><cp cp="0"/>{_esc(label)}</Text>' if label else ''
    return (
        f'<Shape ID="{vid}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        f'<XForm>'
        f'<PinX>{cx:.4f}</PinX><PinY>{cy:.4f}</PinY>'
        f'<Width>{w:.4f}</Width><Height>{h:.4f}</Height>'
        f'<LocPinX F="Width*0.5">{w/2:.4f}</LocPinX>'
        f'<LocPinY F="Height*0.5">{h/2:.4f}</LocPinY>'
        f'<Angle>0</Angle><FlipX>0</FlipX><FlipY>0</FlipY>'
        f'</XForm>'
        f'<XForm1D>'
        f'<BeginX>{bx:.4f}</BeginX><BeginY>{by:.4f}</BeginY>'
        f'<EndX>{ex:.4f}</EndX><EndY>{ey:.4f}</EndY>'
        f'</XForm1D>'
        f'<Line><LineColor>#555555</LineColor>'
        f'<LineWeight>0.01389</LineWeight><LinePattern>1</LinePattern>'
        f'<EndArrow>4</EndArrow></Line>'
        f'<Fill><FillPattern>0</FillPattern></Fill>'
        f'{lbl}</Shape>'
    )


def _build_shapes(nodes: dict, edges: list):
    converted = _scale(nodes)
    id_map = {cid: i + 1 for i, cid in enumerate(converted)}
    next_id = len(id_map) + 1

    shapes, connects = [], []
    for cid, n in converted.items():
        shapes.append(_shape_xml(id_map[cid], n))

    for edge in edges:
        if edge['src'] not in id_map or edge['tgt'] not in id_map:
            continue
        src = converted[edge['src']]
        tgt = converted[edge['tgt']]
        eid = next_id
        next_id += 1
        shapes.append(_connector_xml(eid, src, tgt, edge['label']))
        sid, tid = id_map[edge['src']], id_map[edge['tgt']]
        connects += [
            f'<Connect FromSheet="{eid}" FromCell="BeginX" ToSheet="{sid}" ToCell="PinX"/>',
            f'<Connect FromSheet="{eid}" FromCell="EndX" ToSheet="{tid}" ToCell="PinX"/>',
        ]

    return '\n'.join(shapes), '\n'.join(connects)


# ── VSDX packaging ────────────────────────────────────────────────────────────

def _pack_vsdx(shapes_xml: str, connects_xml: str) -> bytes:
    page_xml = f'''\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PageContents xmlns="http://schemas.microsoft.com/office/visio/2012/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
              xml:space="preserve">
  <PageSheet UniqueID="{{00000001-0000-0000-0000-000000000001}}"
             LineStyle="0" FillStyle="0" TextStyle="0">
    <PageProps>
      <PageWidth>{PAGE_W}</PageWidth>
      <PageHeight>{PAGE_H}</PageHeight>
      <PrintPageOrientation>2</PrintPageOrientation>
    </PageProps>
  </PageSheet>
  <Shapes>
{shapes_xml}
  </Shapes>
  <Connects>
{connects_xml}
  </Connects>
</PageContents>'''

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', '''\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
  <Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
</Types>''')

        zf.writestr('_rels/.rels', '''\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.microsoft.com/visio/2010/relationships/document"
    Target="visio/document.xml"/>
</Relationships>''')

        zf.writestr('visio/document.xml', f'''\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main"
               xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
               xml:space="preserve">
  <DocumentProperties><Creator>Diagram Builder</Creator></DocumentProperties>
  <DocumentSheet NameU="TheDoc" UniqueID="{{00000002-0000-0000-0000-000000000001}}"
                 LineStyle="0" FillStyle="0" TextStyle="0"/>
  <StyleSheets>
    <StyleSheet ID="0" NameU="Normal" LineStyle="0" FillStyle="0" TextStyle="0"/>
  </StyleSheets>
  <Pages>
    <Page ID="1" NameU="Page-1" IsCustomName="1" IsCustomNameU="1"
          ViewScale="1" ViewCenterX="{PAGE_W/2}" ViewCenterY="{PAGE_H/2}">
      <Rel r:id="rId1"/>
    </Page>
  </Pages>
</VisioDocument>''')

        zf.writestr('visio/_rels/document.xml.rels', '''\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.microsoft.com/visio/2010/relationships/page"
    Target="pages/page1.xml"/>
</Relationships>''')

        zf.writestr('visio/pages/page1.xml', page_xml)

        zf.writestr('visio/pages/_rels/page1.xml.rels', '''\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>''')

    return buf.getvalue()
