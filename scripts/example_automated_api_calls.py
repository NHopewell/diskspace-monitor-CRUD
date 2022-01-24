from black import re
import requests, os

if __name__ == "__main__":

    api_va_base_url = "http://127.0.0.1:8000/v1/"
    system_components_endpoint = os.path.join(api_va_base_url, "system_components")
    system_events_endpoint = os.path.join(api_va_base_url, "component_events")
    resource_warnings_endpoint = os.path.join(api_va_base_url, "resource_warnings")

    # create crash dump component
    request_body = {
        "name": "CrashDump",
        "total_available_storage": 400    
        }
    requests.post(system_components_endpoint, json=request_body)

    # create versioning system
    request_body = {
        "name": "VersioningSystem",
        "total_available_storage": 200    
        }
    requests.post(system_components_endpoint, json=request_body)

    # create build system
    request_body = {
        "name": "BuildSystem",
        "total_available_storage": 600    
        }
    requests.post(system_components_endpoint, json=request_body)



    # read crash dump component
    response = requests.get(os.path.join(system_components_endpoint, "CrashDump")).json()
    print(response)


    # update crash dump component
    request_body = {
        "storage_limit": 90    
        }
    requests.patch(os.path.join(system_components_endpoint, "CrashDump"), json=request_body)

    request_body = {
        "storage_limit": 90    
        }
    requests.patch(os.path.join(system_components_endpoint, "BuildSystem"), json=request_body)


    response = requests.get(os.path.join(system_components_endpoint, "CrashDump")).json()
    print(response)



    # list all system components
    response = requests.get(system_components_endpoint).json()
    print(response)


    # delete versioning system
    requests.delete(os.path.join(system_components_endpoint, "VersioningSystem"))

    # list
    response = requests.get(system_components_endpoint).json()
    print(response)


    # test setting storage limit over 100%
    request_body = {
        "storage_limit": 101    
        }
    response = requests.patch(os.path.join(system_components_endpoint, "BuildSystem"), json=request_body)
    print(response.json())

    
    # set current storage useage over the storage limit
    request_body = {
        "current_storage_useage": 395   
    }
    requests.patch(os.path.join(system_components_endpoint, "CrashDump"), json=request_body)
    response = requests.get(os.path.join(system_components_endpoint, "CrashDump")).json()
    print(response)

    # set current storage useage over the storage limit
    request_body = {
        "current_storage_useage": 598   
    }
    requests.patch(os.path.join(system_components_endpoint, "BuildSystem"), json=request_body)
    response = requests.get(os.path.join(system_components_endpoint, "BuildSystem")).json()
    print(response)



    # get latest reported useage for crash dump
    response = requests.get(os.path.join(system_events_endpoint, "CrashDump")).json()
    print(response)
    print()

    # get event history of events for crashdump
    response = requests.get(os.path.join(system_events_endpoint, "CrashDump", "history")).json()
    print(response)
    print()

    # get most recent useage of all components
    response = requests.get(system_events_endpoint).json()
    print(response)
    print()


    # get list of resource warnings
    response = requests.get(resource_warnings_endpoint).json()
    print(response)
    



    

    
