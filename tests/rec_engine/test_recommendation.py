import pytest
from fastapi.testclient import TestClient
from src.recommendation_engine.pipeline import user_vectorizer, inference

from src.main import app

client = TestClient(app)


def test_show_questionnaire():
    response = client.get("/api/recommendations/questionnare")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<form" in response.text.lower()


def test_submit_form_valid(monkeypatch):
    
    monkeypatch.setattr(user_vectorizer, "build_user_vector", lambda *args, **kwargs: [0.1, 0.2, 0.3])
    monkeypatch.setattr(inference, "inference", lambda vec, k: {"recommendations": ["Mocked Game 1", "Mocked Game 2"]})

    response = client.post("/api/recommendations/submit", data={
        "game_mode": "singleplayer",
        "genres": ["rpg", "adventure"],
        "favourites": "Skyrim, Witcher 3",
        "genres_other": "soulslike"
    })

    assert response.status_code == 200
    json_resp = response.json()
    assert "recommendations" in json_resp
    assert isinstance(json_resp["recommendations"], list)


def test_submit_missing_required_field():
    response = client.post("/api/recommendations/submit", data={
        "genres": ["action"],
        "favourites": "Mass Effect"
    })
    assert response.status_code == 422