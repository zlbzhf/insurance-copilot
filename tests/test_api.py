from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_with_customer() -> None:
    payload = {
        "message": "客户预算有限，想知道先买什么",
        "customer": {
            "name": "王先生",
            "age": 35,
            "family_role": "家庭经济支柱，有娃，有房贷",
            "annual_budget": 8000,
            "existing_coverage": "有社保，暂无商业保险",
            "concerns": ["medical", "critical_illness", "life"],
            "risk_preference": "balanced",
        },
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "保障缺口" in body["answer"]
    assert body["suggested_actions"]
    assert body["compliance_notes"]
