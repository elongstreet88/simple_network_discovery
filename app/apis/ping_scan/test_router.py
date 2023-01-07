from fastapi.testclient import TestClient
from app import app, root_path
import pytest

# Ensure startup scripts are fired
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Set api root for test
api_root_path = root_path + "/ping_scan"

def test_get_ping_up(client):
    response = client.get(f"{api_root_path}/1.1.1.1")
    data = response.json()

    # Verify
    assert response.status_code                       == 200
    assert data["device_address"]                     == "1.1.1.1"
    assert data["online"]                             == True
    assert data["average_rtt"]                         > 0
    assert data["jitter"]                              > 0
    assert data["max_rtt"]                             > 0
    assert data["min_rtt"]                             > 0
    assert data["packets_sent"]                       == 4
    assert data["packets_received"]                   == 4
    assert data["packet_loss"]                        == 0

def test_get_ping_up_custom_scan_settings(client):
    response = client.get(f"{api_root_path}/1.1.1.1?ping_scan_size=5&ping_scan_timeout=1&ping_scan_count=1&ping_scan_interval=1")
    data = response.json()
    print(data)

    # Verify
    assert response.status_code                       == 200
    assert data["device_address"]                     == "1.1.1.1"
    assert data["online"]                             == True
    assert data["average_rtt"]                         > 0
    assert data["jitter"]                             >= 0
    assert data["max_rtt"]                             > 0
    assert data["min_rtt"]                             > 0
    assert data["packets_sent"]                       == 1
    assert data["packets_received"]                   == 1
    assert data["packet_loss"]                        == 0

def test_get_ping_down(client):
    response = client.get(f"{api_root_path}/0.0.0.0")
    data = response.json()

    # Verify
    assert response.status_code                       == 200
    assert data["device_address"]                     == "0.0.0.0"
    assert data["online"]                             == False
    assert data["average_rtt"]                        == 0
    assert data["jitter"]                             == 0
    assert data["max_rtt"]                            == 0
    assert data["min_rtt"]                            == 0
    assert data["packets_sent"]                       == 1
    assert data["packets_received"]                   == 0
    assert data["packet_loss"]                        == 1