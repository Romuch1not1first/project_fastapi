import os
import sys
from fastapi.testclient import TestClient

# Add the parent directory to the system path for module importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app

# Create an instance of TestClient for testing the FastAPI application
client = TestClient(app)

def test_calculate_sum():
    # Test case 1: valid input data
    response = client.get("/sum/?a=5&b=10")
    assert response.status_code == 200
    assert response.json() == {"result": 15}

    # Test case 2: negative numbers
    response = client.get("/sum/?a=-8&b=-3")
    assert response.status_code == 200
    assert response.json() == {"result": -11}

    # Test case 3: zero and a positive number
    response = client.get("/sum/?a=0&b=7")
    assert response.status_code == 200
    assert response.json() == {"result": 7}

    # Test case 4: one number not provided
    response = client.get("/sum/?a=3")
    assert response.status_code == 422  # Unprocessable Entity (validation error)
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "b"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
