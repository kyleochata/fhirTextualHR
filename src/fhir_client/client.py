from __future__ import annotations

import base64
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import os
import requests
from pathlib import Path

# Configure base url, username, password

# Get path to .env file
client_dir = Path(__file__).parent
project_root = client_dir.parent.parent
env_path = project_root / '.env'

load_dotenv(env_path)

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL") or ""
USERNAME = os.getenv("USERNAME") or ""
PASSWORD = os.getenv("PASSWORD") or ""

def _basic_auth_header(user: str, pwd: str) -> str:
    token = f"{user}:{pwd}".encode("utf-8")
    return "Basic "+base64.b64encode(token).decode("ascii")

# Set headers
HEADERS = {
    "Authorization": _basic_auth_header(USERNAME, PASSWORD),
    "Accept": "*/*",
    "Content-Type":  "application/fhir+json",
    "Prefer": "return=representation",
}
# HTTP Helpers

#_full_url(path: str) -> str: adds path to stipped FHIR base url
def _full_url(path: str) -> str:
    return f"{FHIR_BASE_URL.rstrip("/")}/{path.lstrip("/")}"

# _get(path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]: calls _full_url
def _get(path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    url = _full_url(path)
    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=15,
    )

    if not response.ok:
        raise RuntimeError(_format_error(response))
    try:
        return response.json()
    except ValueError:
        raise RuntimeError("FHIR server returned non-JSON response")

# _format_error(response: requests.Response) -> str: return issue or response code
def _format_error(response: requests.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return f"HTTP {response.status_code}: {response.text}"
    
    if isinstance(body, dict) and body.get("resourceaType") == "OperationOutcome":
        issues = body.get("issue", [])
        if issues:
            issue = issues[0]
            details = issue.get("details", {}).get("text")
            diagnostics = issue.get("diagnostics")
            return f"FHIR error: {details or diagnostics or 'OperationOutcome'}"
    return f"HTTP {response.status_code}: {body}"

# Public FHIR functions

# get_resource(r_type: str, r_id: str) -> Dict[str, Any]: GET /<resource_type>/<id>
def get_resource(resource_type: str, resource_id: str) -> Dict[str, Any]:
    return _get(f"{resource_type}/{resource_id}")

# search(r_type: str, **params: str) -> Dict[str, Any]: GET /<resource_type>?param=value&...
def search(resource_type: str, **params: str) -> Dict[str, Any]:
    return _get(resource_type, params=params)

# extract_resource(bundle: Dict[str, Any]) -> List[Dict[str, Any]]: Extract resource objects from a bundle
def extract_resource(bundle: Dict[str, Any]) -> List[Dict[str,Any]]:
    entries = bundle.get("entry", [])
    resources: List[Dict[str, Any]] = []

    for entry in entries:
        resource = entry.get("resource")
        if isinstance(resource, dict):
            resources.append(resource)

    return resources
# Convenience helpers (human-friendly)

# human_name(patient: Dict[str, Any]) -> str: returns "{given} {family}" name
def human_name(patient: Dict[str, Any]) -> str:
    names = patient.get("name", [])
    if not names:
        return "no name found"
    name = names[0]
    if "text" in name:
        return name["text"]
    given = " ".join(name.get("given", []))
    family = name.get("family", "")
    return f"{given} {family}".strip()

# summarize_patient(patient: Dict[str, Any])-> Dict[str, str]: returns id, name, gender, birthDate
def summarize_patient(patient: Dict[str, Any]) -> Dict[str, str]:
    return {
        "id": patient.get("id", ""),
        "name": human_name(patient),
        "gender": patient.get("gender", ""),
        "birthDate": patient.get("birthDate", ""),
    }


if __name__ == "__main__": 
    print(f"base:\t{FHIR_BASE_URL}\nusername:\t{USERNAME}\npassword:\t{PASSWORD}")