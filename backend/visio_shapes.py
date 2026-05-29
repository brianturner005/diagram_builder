"""
Visio master shape definitions mapped from mxGraph style strings.

Each master entry: (master_id, display_name, key_substrings_list, geom_fn)
The page shape fill/stroke colours are always taken from the draw.io style, so
masters only carry geometry — no hardcoded colour defaults.
"""

# ── Geometry generators ───────────────────────────────────────────────────────

def _rect():
    """Plain rectangle — Visio default, no extra Geom needed."""
    return ''


def _ellipse():
    return (
        '<Geom ix="0"><Ellipse ix="1">'
        '<X F="Width*0.5">0.5</X><Y F="Height*0.5">0.5</Y>'
        '<A F="Width*1">1</A><B F="Height*0.5">0.5</B>'
        '<C F="Width*0.5">0.5</C><D F="Height*0">0</D>'
        '</Ellipse></Geom>'
    )


def _diamond():
    return (
        '<Geom ix="0">'
        '<MoveTo ix="1"><X F="Width*0.5">0.5</X><Y F="Height*0">0</Y></MoveTo>'
        '<LineTo ix="2"><X F="Width*1">1</X><Y F="Height*0.5">0.5</Y></LineTo>'
        '<LineTo ix="3"><X F="Width*0.5">0.5</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="4"><X F="Width*0">0</X><Y F="Height*0.5">0.5</Y></LineTo>'
        '<LineTo ix="5"><X F="Width*0.5">0.5</X><Y F="Height*0">0</Y></LineTo>'
        '</Geom>'
    )


def _hexagon():
    return (
        '<Geom ix="0">'
        '<MoveTo ix="1"><X F="Width*0.25">0.25</X><Y F="Height*0">0</Y></MoveTo>'
        '<LineTo ix="2"><X F="Width*0.75">0.75</X><Y F="Height*0">0</Y></LineTo>'
        '<LineTo ix="3"><X F="Width*1">1</X><Y F="Height*0.5">0.5</Y></LineTo>'
        '<LineTo ix="4"><X F="Width*0.75">0.75</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="5"><X F="Width*0.25">0.25</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="6"><X F="Width*0">0</X><Y F="Height*0.5">0.5</Y></LineTo>'
        '<LineTo ix="7"><X F="Width*0.25">0.25</X><Y F="Height*0">0</Y></LineTo>'
        '</Geom>'
    )


def _parallelogram():
    return (
        '<Geom ix="0">'
        '<MoveTo ix="1"><X F="Width*0.2">0.2</X><Y F="Height*0">0</Y></MoveTo>'
        '<LineTo ix="2"><X F="Width*1">1</X><Y F="Height*0">0</Y></LineTo>'
        '<LineTo ix="3"><X F="Width*0.8">0.8</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="4"><X F="Width*0">0</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="5"><X F="Width*0.2">0.2</X><Y F="Height*0">0</Y></LineTo>'
        '</Geom>'
    )


def _trapezoid():
    """Wider at top — good for load balancers / ingress controllers."""
    return (
        '<Geom ix="0">'
        '<MoveTo ix="1"><X F="Width*0">0</X><Y F="Height*0">0</Y></MoveTo>'
        '<LineTo ix="2"><X F="Width*1">1</X><Y F="Height*0">0</Y></LineTo>'
        '<LineTo ix="3"><X F="Width*0.85">0.85</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="4"><X F="Width*0.15">0.15</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="5"><X F="Width*0">0</X><Y F="Height*0">0</Y></LineTo>'
        '</Geom>'
    )


def _database():
    """Rectangle with a horizontal cap line — classic database/cylinder look."""
    return (
        '<Geom ix="0">'
        '<MoveTo ix="1"><X F="Width*0">0</X><Y F="Height*0">0</Y></MoveTo>'
        '<LineTo ix="2"><X F="Width*1">1</X><Y F="Height*0">0</Y></LineTo>'
        '<LineTo ix="3"><X F="Width*1">1</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="4"><X F="Width*0">0</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="5"><X F="Width*0">0</X><Y F="Height*0">0</Y></LineTo>'
        '</Geom>'
        '<Geom ix="1">'  # cap line
        '<MoveTo ix="1"><X F="Width*0">0</X><Y F="Height*0.22">0.22</Y></MoveTo>'
        '<LineTo ix="2"><X F="Width*1">1</X><Y F="Height*0.22">0.22</Y></LineTo>'
        '</Geom>'
    )


def _pentagon():
    return (
        '<Geom ix="0">'
        '<MoveTo ix="1"><X F="Width*0.5">0.5</X><Y F="Height*0">0</Y></MoveTo>'
        '<LineTo ix="2"><X F="Width*1">1</X><Y F="Height*0.38">0.38</Y></LineTo>'
        '<LineTo ix="3"><X F="Width*0.81">0.81</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="4"><X F="Width*0.19">0.19</X><Y F="Height*1">1</Y></LineTo>'
        '<LineTo ix="5"><X F="Width*0">0</X><Y F="Height*0.38">0.38</Y></LineTo>'
        '<LineTo ix="6"><X F="Width*0.5">0.5</X><Y F="Height*0">0</Y></LineTo>'
        '</Geom>'
    )


# ── Master table ──────────────────────────────────────────────────────────────
# (master_id, name, [style substrings that map to this master], geom_fn)

MASTER_DEFS = [
    # ── Generic network / Cisco ───────────────────────────────────────────────
    (1,  'Internet',       ['mxgraph.network.cloud'],                      _ellipse),
    (2,  'Firewall',       ['cisco.firewalls'],                            _diamond),
    (3,  'Router',         ['cisco.routers.router'],                       _ellipse),
    (4,  'L3 Switch',      ['cisco.switches.layer_3_switch'],              _rect),
    (5,  'L2 Switch',      ['cisco.switches.workgroup_switch'],            _rect),
    (6,  'Wireless AP',    ['cisco.wireless'],                             _diamond),
    (7,  'Load Balancer',  ['cisco.servers.load_balancer'],                _trapezoid),
    (8,  'Web Server',     ['cisco.servers.web_server'],                   _rect),
    (9,  'App Server',     ['cisco.servers.application_server'],           _rect),
    (10, 'File Server',    ['cisco.servers.file_server'],                  _rect),
    (11, 'Server',         ['cisco.servers.standard_server', 'cisco.servers'], _rect),
    (12, 'Database',       ['cisco.storage.storage_server', 'cisco.storage'], _database),
    (13, 'NAS',            ['cisco.storage.nfs_server'],                  _database),
    (14, 'Desktop PC',     ['cisco.computers_and_peripherals.pc'],         _rect),
    (15, 'Laptop',         ['cisco.computers_and_peripherals.laptop'],     _rect),
    (16, 'Mobile',         ['cisco.computers_and_peripherals.handheld'],   _rect),
    (17, 'IP Phone',       ['cisco.computers_and_peripherals.ip_phone'],   _rect),
    (18, 'Printer',        ['cisco.computers_and_peripherals.printer'],    _rect),

    # ── AWS ───────────────────────────────────────────────────────────────────
    (20, 'EC2',            ['mxgraph.aws4.ec2'],                           _rect),
    (21, 'S3',             ['mxgraph.aws4.s3'],                            _database),
    (22, 'RDS',            ['mxgraph.aws4.rds'],                           _database),
    (23, 'Lambda',         ['mxgraph.aws4.lambda'],                        _hexagon),
    (24, 'ALB',            ['mxgraph.aws4.elastic_load_balancing'],        _trapezoid),
    (25, 'CloudFront',     ['mxgraph.aws4.cloudfront'],                    _ellipse),
    (26, 'API Gateway',    ['mxgraph.aws4.api_gateway'],                   _diamond),
    (27, 'ECS',            ['mxgraph.aws4.ecs'],                           _rect),
    (28, 'SQS',            ['mxgraph.aws4.sqs'],                           _parallelogram),
    (29, 'SNS',            ['mxgraph.aws4.sns'],                           _parallelogram),
    (30, 'ElastiCache',    ['mxgraph.aws4.elasticache'],                   _database),
    (31, 'VPC',            ['mxgraph.aws4.group'],                         _rect),

    # ── Azure ─────────────────────────────────────────────────────────────────
    (40, 'VM',             ['mxgraph.azure.virtual_machine'],              _rect),
    (41, 'App Service',    ['mxgraph.azure.app_service'],                  _rect),
    (42, 'Azure SQL',      ['mxgraph.azure.sql_database'],                 _database),
    (43, 'Blob Storage',   ['mxgraph.azure.storage'],                      _database),
    (44, 'VNet',           ['mxgraph.azure.virtual_network'],              _rect),
    (45, 'Azure LB',       ['mxgraph.azure.load_balancer'],                _trapezoid),
    (46, 'Functions',      ['mxgraph.azure.function'],                     _hexagon),
    (47, 'API Mgmt',       ['mxgraph.azure.api_management'],               _diamond),
    (48, 'AKS',            ['mxgraph.azure.aks'],                          _hexagon),
    (49, 'Cosmos DB',      ['mxgraph.azure.cosmos_db'],                    _database),
    (50, 'Service Bus',    ['mxgraph.azure.service_bus'],                  _parallelogram),

    # ── GCP ───────────────────────────────────────────────────────────────────
    (60, 'Compute Engine', ['mxgraph.gcp2.compute_engine'],                _rect),
    (61, 'Cloud Storage',  ['mxgraph.gcp2.cloud_storage'],                 _database),
    (62, 'Cloud SQL',      ['mxgraph.gcp2.cloud_sql'],                     _database),
    (63, 'GKE',            ['mxgraph.gcp2.container_engine'],              _hexagon),
    (64, 'Cloud Functions',['mxgraph.gcp2.cloud_functions'],               _hexagon),
    (65, 'App Engine',     ['mxgraph.gcp2.app_engine'],                    _rect),
    (66, 'Cloud LB',       ['mxgraph.gcp2.cloud_load_balancing'],          _trapezoid),
    (67, 'Pub/Sub',        ['mxgraph.gcp2.cloud_pubsub'],                  _parallelogram),
    (68, 'BigQuery',       ['mxgraph.gcp2.bigquery'],                      _database),

    # ── Kubernetes ────────────────────────────────────────────────────────────
    (70, 'Pod',            ['mxgraph.kubernetes.pod'],                     _hexagon),
    (71, 'K8s Node',       ['mxgraph.kubernetes.node'],                    _rect),
    (72, 'Deployment',     ['mxgraph.kubernetes.deploy'],                  _rect),
    (73, 'K8s Service',    ['mxgraph.kubernetes.svc'],                     _ellipse),
    (74, 'Ingress',        ['mxgraph.kubernetes.ing'],                     _trapezoid),
    (75, 'ConfigMap',      ['mxgraph.kubernetes.cm'],                      _rect),
    (76, 'PV',             ['mxgraph.kubernetes.pv'],                      _database),
]

# Fast lookup: style substring → master_id
_STYLE_MAP: dict[str, int] = {}
for _mid, _name, _keys, _geom_fn in MASTER_DEFS:
    for _k in _keys:
        _STYLE_MAP[_k] = _mid


def get_master_id(style: str) -> int | None:
    """Return the master_id for an mxGraph style string, or None for default."""
    for key, mid in _STYLE_MAP.items():
        if key in style:
            return mid
    return None


def master_geom_xml(master_id: int) -> str:
    """Return the Visio geometry XML for a given master_id."""
    for mid, _name, _keys, geom_fn in MASTER_DEFS:
        if mid == master_id:
            return geom_fn()
    return ''


def build_masters_xml() -> str:
    """Return the <Masters>...</Masters> XML block for embedding in document.xml."""
    parts = []
    for mid, name, _keys, geom_fn in MASTER_DEFS:
        geom = geom_fn()
        parts.append(
            f'<Master ID="{mid}" NameU="{name}" '
            f'UniqueID="{{0000{mid:04d}-0000-0000-0000-000000000001}}" '
            f'BaseID="{{0000{mid:04d}-0000-0000-0000-000000000002}}">'
            f'<PageSheet LineStyle="0" FillStyle="0" TextStyle="0"/>'
            f'<Shapes>'
            f'<Shape ID="1" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
            f'<XForm>'
            f'<PinX F="Width*0.5">0.5</PinX><PinY F="Height*0.5">0.5</PinY>'
            f'<Width>0.75</Width><Height>0.75</Height>'
            f'<LocPinX F="Width*0.5">0.375</LocPinX>'
            f'<LocPinY F="Height*0.5">0.375</LocPinY>'
            f'</XForm>'
            f'{geom}'
            f'</Shape>'
            f'</Shapes>'
            f'</Master>'
        )
    return '<Masters>\n' + '\n'.join(parts) + '\n</Masters>'
