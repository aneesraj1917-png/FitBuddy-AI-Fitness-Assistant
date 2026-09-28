from fastapi.testclient import TestClient
from app.main import app
from app.database import create_tables

create_tables()
client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert 'FitBuddy' in response.text


def test_demo_generate_workout():
    payload = {
        'username': 'Test User',
        'user_id': 'TEST001',
        'age': 21,
        'weight': 60,
        'goal': 'muscle gain',
        'intensity': 'medium'
    }
    response = client.post('/api/generate-workout', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body['success'] is True
    assert 'workout_plan' in body
