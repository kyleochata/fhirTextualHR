from __future__ import annotations

import base64
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import os
import requests

# Configure base url, username, password
load_dotenv('../../.env')
FHIR_BASE_URL = os.getenv("FHIR_BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Set headers

# HTTP Helpers

#_full_url(path: str) -> str: adds path to stipped FHIR base url

# _get(path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]: calls _full_url

# _format_error(response: requests.Response) -> str: return issue or response code


# Public FHIR functions

# get_resource(r_type: str, r_id: str) -> Dict[str, Any]: GET /<resource_type>/<id>

# search(r_type: str, **params: str) -> Dict[str, Any]: GET /<resource_type>?param=value&...

# extract_resource(bundle: Dict[str, Any]) -> List[Dict[str, Any]]: Extract resource objects from a bundle

# Convenience helpers (human-friendly)

# human_name(patient: Dict[str, Any]) -> str: returns "{given} {family}" name

# summarize_patient(patient: Dict[str, Any])-> Dict[str, str]: returns id, name, gender, birthDate

if __name__ == "__main__": 
    print(f"base:\t{FHIR_BASE_URL}\nusername:\t{USERNAME}\npassword:\t{PASSWORD}")