from src.resource.patient import get_patient_from_server, summarize_pt_fields, human_name

def main():
    print("Hello from fhirtextualhr!")
    x = get_patient_from_server("1")
    print(summarize_pt_fields(x))
    print(human_name(x))


if __name__ == "__main__":
    main()
