"""test_api.py

tests the application API functions. 

This file is intentionally incomplete for the sake of time.
"""
from fastapi.testclient import TestClient

from diskspacemonitor.api.v1.main import app

# FastAPI test client
client = TestClient(app)

def test_read_system_component_ok():
    response = client.get("/v1/system_components")
    assert response.status_code == 200


def test_post_system_component():
    response = client.post(
        "/v1/system_components",
        json={"name": "CrashDump", "total_available_storage": 400}
    )

    assert response.status_code == 200

def test_system_component_name_not_found():
    response = client.get("/v1/system_components/ImaginaryComponent")

    actual = response.json()
    expected =  {
            "Error": "ImaginaryComponent does not exist in the monitored system."
        }

    assert actual == expected


def test_reject_duplicate_system_component():
    client.post(
        "/v1/system_components",
        json={"component_name": "CrashDump", "total_available_storage": 400}
    )
    second_response = client.post(
        "/v1/system_components",
        json={"component_name": "CrashDump", "total_available_storage": 400}
    )

    assert second_response.status_code == 422


        