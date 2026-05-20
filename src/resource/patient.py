from fhir.resources.patient import Patient
from ..fhir_client.client import  get_resource
from typing import Dict, Any, List
def get_patient_from_server(patient_id: str) -> Patient:
    pt_dict = get_resource("Patient", patient_id)
    patient = Patient.model_validate(pt_dict)
    return patient

def summarize_pt_fields(pt: Patient) -> List[str]:
    return pt.summary_elements_sequence()

def human_name(patient: Patient) -> str:
    if not patient.name:
        return ""
    name = patient.name[0]

    for n in patient.name:
        if n.use == "official":
            name = n
            break
    
    given = ""
    if name.given:
        given = " ".join(g for g in name.given if g is not None)
    family = name.family or ""

    return f"{given} {family}".strip()
