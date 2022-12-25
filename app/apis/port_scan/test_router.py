from fastapi.testclient import TestClient
from app import app, root_path
import pytest

# Ensure startup scripts are fired
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Set api root for test
api_root_path = root_path + "/port_scan"

def test_get_port_scan_tcp_open(client):
    response = client.get(f"{api_root_path}/google.com/80")
    data = response.json()

    # Compare first ip from main call to specific ip network call
    assert response.status_code                     == 200
    assert data["device_address"]                   == "google.com"
    assert data["port"]                             == 80
    assert data["open"]                             == True
    assert data["scan_duration"]                    > 0
    assert data["scan_duration"]                    <= 500
    assert data["port_scan_settings"]["timeout"]    == 500
    assert data["port_scan_settings"]["protocol"]   == "tcp"

def test_get_port_scan_tcp_open_custom_scan_settings(client):
    response = client.get(f"{api_root_path}/google.com/80?timeout=123&protocol=tcp")
    data = response.json()

    # Compare first ip from main call to specific ip network call
    assert response.status_code                     == 200
    assert data["device_address"]                   == "google.com"
    assert data["port"]                             == 80
    assert data["open"]                             == True
    assert data["scan_duration"]                    > 0
    assert data["scan_duration"]                    <= 123
    assert data["port_scan_settings"]["timeout"]    == 123
    assert data["port_scan_settings"]["protocol"]   == "tcp"

def test_get_port_scan_tcp_closed(client):
    response = client.get(f"{api_root_path}/google.com/81")
    data = response.json()

    # Compare first ip from main call to specific ip network call
    assert response.status_code                     == 200
    assert data["device_address"]                   == "google.com"
    assert data["port"]                             == 81
    assert data["open"]                             == False
    assert data["scan_duration"]                    > 0
    assert data["scan_duration"]                    <= 500
    assert data["port_scan_settings"]["timeout"]    == 500
    assert data["port_scan_settings"]["protocol"]   == "tcp"