from fastapi.testclient import TestClient
from app import app, root_path
import pytest

# Ensure startup scripts are fired
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Set api root for test
api_root_path = root_path + "/network_scan"

def test_get_network_scan(client):
    response = client.get(f"{api_root_path}/4.2.2.0/30")
    data = response.json()

    # Verify
    assert response.status_code                                     == 200
    assert data["network"]                                          == "4.2.2.0/30"
    assert len(data["ping_scan_results"])                           == 2

    assert data["ping_scan_results"][0]["device_address"]           == "4.2.2.1"
    assert data["ping_scan_results"][0]["online"]                   == True
    assert data["ping_scan_results"][0]["average_rtt"]               > 0
    assert data["ping_scan_results"][0]["jitter"]                   >= 0
    assert data["ping_scan_results"][0]["max_rtt"]                  >= 0
    assert data["ping_scan_results"][0]["min_rtt"]                  >= 0
    assert data["ping_scan_results"][0]["packets_sent"]             == 4
    assert data["ping_scan_results"][0]["packets_received"]         == 4
    assert data["ping_scan_results"][0]["packet_loss"]              == 0

    assert data["ping_scan_results"][1]["device_address"]           == "4.2.2.2"
    assert data["ping_scan_results"][1]["online"]                   == True
    assert data["ping_scan_results"][1]["average_rtt"]               > 0
    assert data["ping_scan_results"][1]["jitter"]                   >= 0
    assert data["ping_scan_results"][1]["max_rtt"]                  >= 0
    assert data["ping_scan_results"][1]["min_rtt"]                  >= 0
    assert data["ping_scan_results"][1]["packets_sent"]             == 4
    assert data["ping_scan_results"][1]["packets_received"]         == 4
    assert data["ping_scan_results"][1]["packet_loss"]              == 0

    assert len(data["tcp_port_scan_results"])                           == 2

    assert data["tcp_port_scan_results"][0]["device_address"]           == "4.2.2.1"
    assert data["tcp_port_scan_results"][0]["port"]                     == 53
    assert data["tcp_port_scan_results"][0]["open"]                     == True
    assert data["tcp_port_scan_results"][0]["scan_duration"]            > 0

    assert data["tcp_port_scan_results"][1]["device_address"]           == "4.2.2.2"
    assert data["tcp_port_scan_results"][1]["port"]                     == 53
    assert data["tcp_port_scan_results"][1]["open"]                     == True
    assert data["tcp_port_scan_results"][1]["scan_duration"]            > 0


def test_get_network_scan_with_settings(client):
    response = client.get(f"{api_root_path}/4.2.2.0/30?tcp_port_scan_range=53,80,100-110&tcp_port_scan_timeout=123&ping_scan_size=5&ping_scan_timeout=1&ping_scan_count=1&ping_scan_interval=1")
    data = response.json()

    # Verify
    assert response.status_code                                     == 200
    assert data["network"]                                          == "4.2.2.0/30"
    assert len(data["ping_scan_results"])                           == 2

    assert data["ping_scan_results"][0]["device_address"]           == "4.2.2.1"
    assert data["ping_scan_results"][0]["online"]                   == True
    assert data["ping_scan_results"][0]["average_rtt"]               > 0
    assert data["ping_scan_results"][0]["jitter"]                   >= 0
    assert data["ping_scan_results"][0]["max_rtt"]                  >= 0
    assert data["ping_scan_results"][0]["min_rtt"]                  >= 0
    assert data["ping_scan_results"][0]["packets_sent"]             == 1
    assert data["ping_scan_results"][0]["packets_received"]         == 1
    assert data["ping_scan_results"][0]["packet_loss"]              == 0

    assert data["ping_scan_results"][1]["device_address"]           == "4.2.2.2"
    assert data["ping_scan_results"][1]["online"]                   == True
    assert data["ping_scan_results"][1]["average_rtt"]               > 0
    assert data["ping_scan_results"][1]["jitter"]                   >= 0
    assert data["ping_scan_results"][1]["max_rtt"]                  >= 0
    assert data["ping_scan_results"][1]["min_rtt"]                  >= 0
    assert data["ping_scan_results"][1]["packets_sent"]             == 1
    assert data["ping_scan_results"][1]["packets_received"]         == 1
    assert data["ping_scan_results"][1]["packet_loss"]              == 0

    assert len(data["tcp_port_scan_results"])                           == 2

    assert data["tcp_port_scan_results"][0]["device_address"]           == "4.2.2.1"
    assert data["tcp_port_scan_results"][0]["port"]                     == 53
    assert data["tcp_port_scan_results"][0]["open"]                     == True
    assert data["tcp_port_scan_results"][0]["scan_duration"]            > 0

    assert data["tcp_port_scan_results"][1]["device_address"]           == "4.2.2.2"
    assert data["tcp_port_scan_results"][1]["port"]                     == 53
    assert data["tcp_port_scan_results"][1]["open"]                     == True
    assert data["tcp_port_scan_results"][1]["scan_duration"]            > 0
