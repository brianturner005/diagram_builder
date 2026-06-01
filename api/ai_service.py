import os
import google.generativeai as genai

_generate_model = None
_update_model = None


def _get_generate_model() -> genai.GenerativeModel:
    global _generate_model
    if _generate_model is None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        _generate_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=GENERATE_SYSTEM_PROMPT,
        )
    return _generate_model


def _get_update_model() -> genai.GenerativeModel:
    global _update_model
    if _update_model is None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        _update_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=UPDATE_SYSTEM_PROMPT,
        )
    return _update_model


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

SHAPE_LIBRARY = """
## Shape library — use shape= in the style attribute

### INTERNET & CLOUD
- Internet/WAN:        shape=mxgraph.network.cloud;                         120x80   fillColor=#dae8fc;strokeColor=#6c8ebf;

### SECURITY
- Firewall:            shape=mxgraph.cisco.firewalls.firewall;              60x60    fillColor=#f8cecc;strokeColor=#b85450;
- IDS/IPS:             shape=mxgraph.cisco.firewalls.generic_firewall;      60x60    fillColor=#f8cecc;strokeColor=#b85450;

### NETWORK DEVICES
- Router:              shape=mxgraph.cisco.routers.router;                  60x60    fillColor=#fff2cc;strokeColor=#d6b656;
- Layer-3 switch:      shape=mxgraph.cisco.switches.layer_3_switch;         60x60    fillColor=#fff2cc;strokeColor=#d6b656;
- Layer-2 switch:      shape=mxgraph.cisco.switches.workgroup_switch;       60x60    fillColor=#fff2cc;strokeColor=#d6b656;
- Wireless AP:         shape=mxgraph.cisco.wireless.access_point;           60x60    fillColor=#fff2cc;strokeColor=#d6b656;
- Load balancer:       shape=mxgraph.cisco.servers.load_balancer;           60x60    fillColor=#ffe6cc;strokeColor=#d79b00;

### SERVERS & COMPUTE
- Generic server:      shape=mxgraph.cisco.servers.standard_server;         50x70    fillColor=#dae8fc;strokeColor=#6c8ebf;
- Web server:          shape=mxgraph.cisco.servers.web_server;              50x70    fillColor=#dae8fc;strokeColor=#6c8ebf;
- App server:          shape=mxgraph.cisco.servers.application_server;      50x70    fillColor=#dae8fc;strokeColor=#6c8ebf;
- File server:         shape=mxgraph.cisco.servers.file_server;             50x70    fillColor=#dae8fc;strokeColor=#6c8ebf;

### STORAGE
- Database:            shape=mxgraph.cisco.storage.storage_server;          60x60    fillColor=#e1d5e7;strokeColor=#9673a6;
- NAS:                 shape=mxgraph.cisco.storage.nfs_server;              60x60    fillColor=#e1d5e7;strokeColor=#9673a6;

### CLIENTS & ENDPOINTS
- Desktop PC:          shape=mxgraph.cisco.computers_and_peripherals.pc;          50x60  fillColor=#d5e8d4;strokeColor=#82b366;
- Laptop:              shape=mxgraph.cisco.computers_and_peripherals.laptop;       60x50  fillColor=#d5e8d4;strokeColor=#82b366;
- Smartphone:          shape=mxgraph.cisco.computers_and_peripherals.handheld;     30x60  fillColor=#d5e8d4;strokeColor=#82b366;
- IP Phone:            shape=mxgraph.cisco.computers_and_peripherals.ip_phone;     40x60  fillColor=#d5e8d4;strokeColor=#82b366;
- Printer:             shape=mxgraph.cisco.computers_and_peripherals.printer;      60x50  fillColor=#d5e8d4;strokeColor=#82b366;

### AWS (use when description mentions AWS or specific AWS services)
- EC2 instance:        shape=mxgraph.aws4.ec2;                              60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- S3 bucket:           shape=mxgraph.aws4.s3;                               60x60    fillColor=#3F8624;strokeColor=#82b366;fontColor=#ffffff;
- RDS database:        shape=mxgraph.aws4.rds;                              60x60    fillColor=#3F8624;strokeColor=#82b366;fontColor=#ffffff;
- Lambda:              shape=mxgraph.aws4.lambda_function;                  60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- App Load Balancer:   shape=mxgraph.aws4.elastic_load_balancing;           60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- CloudFront:          shape=mxgraph.aws4.cloudfront;                       60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- API Gateway:         shape=mxgraph.aws4.api_gateway;                      60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- ECS / Fargate:       shape=mxgraph.aws4.ecs;                              60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- SQS queue:           shape=mxgraph.aws4.sqs;                              60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- SNS topic:           shape=mxgraph.aws4.sns;                              60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- ElastiCache:         shape=mxgraph.aws4.elasticache;                      60x60    fillColor=#FF9900;strokeColor=#d6b656;fontColor=#ffffff;
- VPC container:       style="shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;fillColor=#dae8fc;strokeColor=#6c8ebf;"

### AZURE (use when description mentions Azure or specific Azure services)
- Virtual Machine:     shape=mxgraph.azure.virtual_machine;                 60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- App Service:         shape=mxgraph.azure.app_service;                     60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- SQL Database:        shape=mxgraph.azure.sql_database;                    60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- Blob Storage:        shape=mxgraph.azure.storage;                         60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- VNet:                shape=mxgraph.azure.virtual_network;                 60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- Load Balancer:       shape=mxgraph.azure.load_balancer;                   60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- Azure Functions:     shape=mxgraph.azure.function;                        60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- API Management:      shape=mxgraph.azure.api_management;                  60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- AKS (K8s):           shape=mxgraph.azure.aks;                             60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- Cosmos DB:           shape=mxgraph.azure.cosmos_db;                       60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- Service Bus:         shape=mxgraph.azure.service_bus;                     60x60    fillColor=#0078D4;strokeColor=#005a9e;fontColor=#ffffff;
- VNet container:      style="swimlane;startSize=30;fillColor=#e6f3ff;strokeColor=#0078D4;fontColor=#0078D4;fontStyle=1;"

### GCP (use when description mentions GCP or Google Cloud services)
- Compute Engine:      shape=mxgraph.gcp2.compute_engine;                   60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- Cloud Storage:       shape=mxgraph.gcp2.cloud_storage;                    60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- Cloud SQL:           shape=mxgraph.gcp2.cloud_sql;                        60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- GKE:                 shape=mxgraph.gcp2.container_engine;                 60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- Cloud Functions:     shape=mxgraph.gcp2.cloud_functions;                  60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- App Engine:          shape=mxgraph.gcp2.app_engine;                       60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- Cloud Load Balancing:shape=mxgraph.gcp2.cloud_load_balancing;             60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- Pub/Sub:             shape=mxgraph.gcp2.cloud_pubsub;                     60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- BigQuery:            shape=mxgraph.gcp2.bigquery;                         60x60    fillColor=#4285F4;strokeColor=#1a56c4;fontColor=#ffffff;
- VPC container:       style="swimlane;startSize=30;fillColor=#e8f0fe;strokeColor=#4285F4;fontColor=#4285F4;fontStyle=1;"

### KUBERNETES (use when description mentions Kubernetes or K8s)
- Pod:                 shape=mxgraph.kubernetes.pod;                         60x60    fillColor=#326CE5;strokeColor=#1a4db5;fontColor=#ffffff;
- Node/Worker:         shape=mxgraph.kubernetes.node;                        60x60    fillColor=#326CE5;strokeColor=#1a4db5;fontColor=#ffffff;
- Deployment:          shape=mxgraph.kubernetes.deploy;                      60x60    fillColor=#326CE5;strokeColor=#1a4db5;fontColor=#ffffff;
- Service:             shape=mxgraph.kubernetes.svc;                         60x60    fillColor=#326CE5;strokeColor=#1a4db5;fontColor=#ffffff;
- Ingress:             shape=mxgraph.kubernetes.ing;                         60x60    fillColor=#326CE5;strokeColor=#1a4db5;fontColor=#ffffff;
- ConfigMap:           shape=mxgraph.kubernetes.cm;                          60x60    fillColor=#326CE5;strokeColor=#1a4db5;fontColor=#ffffff;
- Persistent Volume:   shape=mxgraph.kubernetes.pv;                          60x60    fillColor=#326CE5;strokeColor=#1a4db5;fontColor=#ffffff;
- Namespace container: style="swimlane;startSize=30;fillColor=#e8eeff;strokeColor=#326CE5;fontColor=#326CE5;fontStyle=1;"
- Control plane:       style="swimlane;startSize=30;fillColor=#fff3e0;strokeColor=#ff9800;fontColor=#e65100;fontStyle=1;"
"""

GENERATE_SYSTEM_PROMPT = f"""You are a network and infrastructure diagram expert. Generate draw.io XML diagrams with proper icons.

CRITICAL: Return ONLY raw XML. No markdown, no explanation, no extra text.

## Required XML structure
<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="1">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    [shapes and edges — IDs start at 2, must be unique integers]
  </root>
</mxGraphModel>

## Vertex template
<mxCell id="N" value="Label" style="shape=SHAPE;whiteSpace=wrap;html=1;fillColor=F;strokeColor=S;fontStyle=1;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="X" y="Y" width="W" height="H" as="geometry" />
</mxCell>

## Edge template
<mxCell id="N" value="Label" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" source="SRC" target="TGT" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

{SHAPE_LIBRARY}

## Layout rules
- Space shapes 120-160px apart
- Left-to-right for data flows, top-to-bottom for hierarchies
- Group devices in same zone inside a swimlane (children use parent="SWIMLANE_ID")
- Label edges with protocol or relationship (HTTPS, SQL, gRPC, etc.)
- Internet/WAN on far left or top; clients on edges; servers and DBs in middle
- Auto-detect the correct shape library from context (Cisco for generic networks, AWS/Azure/GCP for cloud, K8s for container workloads)
"""

UPDATE_SYSTEM_PROMPT = """You are a draw.io diagram editor. You will receive an existing diagram as XML and a description of the change to make.

CRITICAL: Return ONLY the complete updated XML. No markdown, no explanation, no extra text.

Rules:
- Preserve ALL existing shapes and connections not mentioned in the change
- Scan the existing XML to find the highest numeric ID, then assign new IDs starting from highest+1
- Use the same shape styles as similar existing elements in the diagram
- Maintain the general layout — place new elements near related existing ones
- If asked to remove something, delete its mxCell and any edges referencing its ID
- If asked to move something, update its mxGeometry x/y values
- Return the complete mxGraphModel XML, not just the changed parts
"""


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

_LIBRARY_HINTS = {
    "network":     "Use Cisco network shapes (routers, switches, firewalls, servers, etc.).",
    "aws":         "Use AWS shape library icons (EC2, S3, RDS, Lambda, ALB, CloudFront, etc.).",
    "azure":       "Use Azure shape library icons (VMs, App Services, SQL Database, AKS, etc.).",
    "gcp":         "Use GCP shape library icons (Compute Engine, Cloud SQL, GKE, Pub/Sub, etc.).",
    "kubernetes":  "Use Kubernetes shape library icons (Pods, Deployments, Services, Ingress, PVs, etc.).",
}


def generate_diagram(description: str, diagram_type: str = "auto") -> dict:
    model = _get_generate_model()
    user_msg = f"Generate a diagram for: {description}"
    hint = _LIBRARY_HINTS.get(diagram_type, "")
    if hint:
        user_msg += f"\n{hint}"
    response = model.generate_content(user_msg)
    return {"drawio_xml": _clean_xml(response.text)}


def update_diagram(existing_xml: str, change_description: str) -> dict:
    model = _get_update_model()
    prompt = (
        f"Here is the current diagram XML:\n\n{existing_xml}\n\n"
        f"Apply this change: {change_description}"
    )
    response = model.generate_content(prompt)
    return {"drawio_xml": _clean_xml(response.text)}


def _clean_xml(raw: str) -> str:
    text = raw.strip()
    if "```" in text:
        lines = text.splitlines()
        text = "\n".join(l for l in lines if not l.strip().startswith("```")).strip()
    if not text.startswith("<"):
        start = text.find("<mxGraphModel")
        if start != -1:
            text = text[start:]
    return text
