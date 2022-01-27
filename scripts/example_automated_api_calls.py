import requests
import os

if __name__ == "__main__":

    api_va_base_url = "http://127.0.0.1:8000/v1/"
    system_components_endpoint = os.path.join(api_va_base_url, "system_components")
    system_events_endpoint = os.path.join(api_va_base_url, "component_events")
    resource_warnings_endpoint = os.path.join(api_va_base_url, "resource_warnings")

    # create crash dump component
    print("Creating system component: CrashDump with 400G initial storage")
    request_body = {"name": "CrashDump", "total_available_storage": 400}
    requests.post(system_components_endpoint, json=request_body)

    # create versioning system
    print("Creating system component: VersioningSystem with 200G initial storage")
    request_body = {"name": "VersioningSystem", "total_available_storage": 200}
    requests.post(system_components_endpoint, json=request_body)

    # create build system
    print("Creating system component: BuildSystem with 600G initial storage")
    request_body = {"name": "BuildSystem", "total_available_storage": 600}
    requests.post(system_components_endpoint, json=request_body)
    print()

    # read crash dump component
    print("Reading system component: CrashDump")
    response = requests.get(
        os.path.join(system_components_endpoint, "CrashDump")
    ).json()
    print(response)
    print()

    # update crash dump component
    print("Updating system component: CrashDump with 90 storage limit.")
    request_body = {"storage_limit": 90}
    requests.patch(
        os.path.join(system_components_endpoint, "CrashDump"), json=request_body
    )

    response = requests.get(
        os.path.join(system_components_endpoint, "CrashDump")
    ).json()
    print(response)
    print()

    print("Updating system component: BuildSystem with 90 percent storage limit.")
    request_body = {"storage_limit": 90}
    requests.patch(
        os.path.join(system_components_endpoint, "BuildSystem"), json=request_body
    )

    response = requests.get(
        os.path.join(system_components_endpoint, "BuildSystem")
    ).json()
    print(response)
    print()

    # list all system components
    print("Listing all system components.")
    response = requests.get(system_components_endpoint).json()
    print(response)
    print()

    # delete versioning system
    print("Deleting system component: VersioningSystem.")
    requests.delete(os.path.join(system_components_endpoint, "VersioningSystem"))
    print()

    # list
    print("Listing all system components.")
    response = requests.get(system_components_endpoint).json()
    print(response)
    print()

    # test setting storage limit over 100%
    print("Testing that setting storage limit to 101 percent will fail")
    request_body = {"storage_limit": 101}
    response = requests.patch(
        os.path.join(system_components_endpoint, "BuildSystem"), json=request_body
    )
    print(response.json())
    print()

    # set current storage useage over the storage limit
    print(
        "Setting current storage limit of CrashDump to above storage limit threshold."
    )
    request_body = {"current_storage_useage": 395}
    requests.patch(
        os.path.join(system_components_endpoint, "CrashDump"), json=request_body
    )
    response = requests.get(
        os.path.join(system_components_endpoint, "CrashDump")
    ).json()
    print(response)
    print()

    # set current storage useage over the storage limit
    print(
        "Setting current storage limit of BuildSytem to above storage limit threshold."
    )
    request_body = {"current_storage_useage": 598}
    requests.patch(
        os.path.join(system_components_endpoint, "BuildSystem"), json=request_body
    )
    response = requests.get(
        os.path.join(system_components_endpoint, "BuildSystem")
    ).json()
    print(response)
    print()

    # get latest reported useage for crash dump
    print("Getting latest reported useage for CrashDump.")
    response = requests.get(os.path.join(system_events_endpoint, "CrashDump")).json()
    print(response)
    print()

    # get event history of events for crashdump
    print("Listing complete useage history for CrashDump.")
    response = requests.get(
        os.path.join(system_events_endpoint, "CrashDump", "history")
    ).json()
    print(response)
    print()

    # get most recent useage of all components
    print("Getting most recent useage for all components.")
    response = requests.get(system_events_endpoint).json()
    print(response)
    print()

    # get list of resource warnings
    print("Listing all resource warnings.")
    response = requests.get(resource_warnings_endpoint).json()
    print(response)
