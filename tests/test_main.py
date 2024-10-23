<<<<<<< HEAD
=======
# tests/test_main.py

>>>>>>> 5cfe47628bd955ed584dca6d74d5efd65e29a718
import os
import sys
from fastapi.testclient import TestClient

<<<<<<< HEAD
# Add the parent directory to the system path for module importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app

# Create an instance of TestClient for testing the FastAPI application
client = TestClient(app)

def test_calculate_sum():
    # Test case 1: valid input data
=======
# Добавляем путь к каталогу приложения
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.main import app  # Импортируем app

# создаём инстанс TestClient для тестирования FastAPI приложения
client = TestClient(app)

def test_calculate_sum():
    # Test case 1: валидные входные данные
>>>>>>> 5cfe47628bd955ed584dca6d74d5efd65e29a718
    response = client.get("/sum/?a=5&b=10")
    assert response.status_code == 200
    assert response.json() == {"result": 15}

<<<<<<< HEAD
    # Test case 2: negative numbers
=======
    # Test case 2: отрицательные числа
>>>>>>> 5cfe47628bd955ed584dca6d74d5efd65e29a718
    response = client.get("/sum/?a=-8&b=-3")
    assert response.status_code == 200
    assert response.json() == {"result": -11}

<<<<<<< HEAD
    # Test case 3: zero and a positive number
=======
    # Test case 3: ноль и положительное число
>>>>>>> 5cfe47628bd955ed584dca6d74d5efd65e29a718
    response = client.get("/sum/?a=0&b=7")
    assert response.status_code == 200
    assert response.json() == {"result": 7}

<<<<<<< HEAD
    # Test case 4: one number not provided
=======
    # Test case 4: одно число не введено
>>>>>>> 5cfe47628bd955ed584dca6d74d5efd65e29a718
    response = client.get("/sum/?a=3")
    assert response.status_code == 422  # Unprocessable Entity (validation error)
    assert response.json() == {
        "detail": [
            {
<<<<<<< HEAD
                "loc": ["query", "b"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
=======
                "input": None,  # Обновлено
                "loc": ["query", "b"],
                "msg": "Field required",  # Обновлено
                "type": "missing"  # Обновлено
            }
        ]
    }
    
>>>>>>> 5cfe47628bd955ed584dca6d74d5efd65e29a718
