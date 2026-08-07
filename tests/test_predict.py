from unittest.mock import AsyncMock, patch

@patch("app.routes.predict.service.predict",new_callable=AsyncMock)
def test_predict(mock_predict, client):
    mock_predict.return_value={
        "success":True,
        "res":"Mock response from Flowise"
    }
    response = client.post("/predict",json={"query":"Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["res"] == "Mock response from Flowise"

    mock_predict.assert_awaited_once_with("Hello")