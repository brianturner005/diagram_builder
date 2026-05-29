import json
import logging
import azure.functions as func
from ai_service import generate_diagram, update_diagram

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="generate", methods=["POST"])
def generate(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        description = body.get("description", "").strip()
        if not description:
            return _json_response({"detail": "Description cannot be empty"}, 400)
        return _json_response(generate_diagram(description))
    except Exception as exc:
        logging.error("generate failed: %s", exc)
        return _json_response({"detail": f"AI generation failed: {exc}"}, 500)


@app.route(route="update", methods=["POST"])
def update(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        existing_xml = body.get("existing_xml", "").strip()
        change_description = body.get("change_description", "").strip()
        if not existing_xml:
            return _json_response({"detail": "No existing diagram to update"}, 400)
        if not change_description:
            return _json_response({"detail": "Change description cannot be empty"}, 400)
        return _json_response(update_diagram(existing_xml, change_description))
    except Exception as exc:
        logging.error("update failed: %s", exc)
        return _json_response({"detail": f"AI update failed: {exc}"}, 500)


def _json_response(data: dict, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(data),
        status_code=status_code,
        mimetype="application/json",
    )
