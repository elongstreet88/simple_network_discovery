from fastapi.testclient import TestClient
from app import app, root_path
import pytest

# Ensure startup scripts are fired
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Set api root for test
api_root_path = root_path + "/network_interface"

def test_get_network_interface(client):
    response = client.get(f"{api_root_path}")
    assert response.status_code == 200