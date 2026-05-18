# ./client.py; GET /metadata

from client import FHIR_BASE_URL, get_resource

def main() -> None:
    print("\n FHIR SERVER PING")
    print("=" * 64)
    print(f"Base: {FHIR_BASE_URL}\n")
    
    metadata = get_resource("metadata", "")
    print(metadata.get("type", ""))
    print ("Server responded with CapabilityStatement")

    software = metadata.get("software", {})
    software_name = software.get("name", "unknown")
    software_version = software.get("version", "")

    if software_version:
        print(f"Software: {software_name} ({software_version})")
    else:
        print(f"Software: {software_name}")

    # --- Supported resources --------------------------------------

    print("\nSupported Resource Types (sample):")

    rest = metadata.get("rest", [])
    if rest:
        resources = rest[0].get("resource", [])
        types = [r.get("type") for r in resources if "type" in r]

        for resource_type in types[:10]:
            print(f" - {resource_type}")

        if len(types) > 10:
            print(" - ...")
    else:
        print(" (No REST metadata found)")

    print("\nPing successful.")




if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\n✘ Ping failed")
        print(f"Error: {exc}")