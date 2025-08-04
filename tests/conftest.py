import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR)) 

import pytest
from fastapi.testclient import TestClient
from src.main import app 

@pytest.fixture
def client():
    return TestClient(app)