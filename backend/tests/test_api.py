import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_works():
    """Тест: получение списка записей"""
    response = client.get("/api/works")
    assert response.status_code == 200
    assert "items" in response.json()

def test_create_work():
    """Тест: создание новой записи"""
    new_work = {
        "doc_number": "TEST001",
        "status": "Утвержден",
        "work_type": "Тестовые работы",
        "department": "Тестовое подразделение"
    }
    response = client.post("/api/works", json=new_work)
    assert response.status_code in [200, 201]

def test_delete_work():
    """Тест: удаление записи"""
    # Создаём запись
    new_work = {
        "doc_number": "TEST002",
        "status": "Утвержден",
        "work_type": "Тестовые работы",
        "department": "Тестовое подразделение"
    }
    create_response = client.post("/api/works", json=new_work)
    
    if create_response.status_code in [200, 201]:
        work_id = create_response.json()["id"]
        delete_response = client.delete(f"/api/works/{work_id}")
        assert delete_response.status_code in [200, 204]