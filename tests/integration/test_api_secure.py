"""Guvenli API'nin normal kullanim senaryolarini test et."""


def test_index_returns_200(secure_client):
    """Ana sayfa 200 donmeli"""
    response = secure_client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_valid_user_query(secure_client):
    """Gecerli kullanici sorgusu 200 donmeli"""
    response = secure_client.get("/api/user?username=admin")
    assert response.status_code == 200


def test_invalid_user_query(secure_client):
    """Gecersiz kullanici adi formati 400 donmeli"""
    response = secure_client.get("/api/user?username=<script>alert(1)</script>")
    assert response.status_code == 400


def test_valid_ping(secure_client):
    """Gecerli ping istegi 200 veya 408 donmeli"""
    response = secure_client.post("/api/ping",
        json={"host": "localhost"})
    # timeout kabul edilebilir (CI ortaminda ping calismayabilir)
    assert response.status_code in [200, 408]


def test_ping_rejects_flag_injection(secure_client):
    """Tire ile baslayan host degeri (bayrak enjeksiyonu) 400 donmeli"""
    response = secure_client.post("/api/ping", json={"host": "-c"})
    assert response.status_code == 400


def test_secure_api_version(secure_client):
    """Guvenli API versiyonu dogru olmali"""
    response = secure_client.get("/")
    data = response.get_json()
    assert "Secure" in data["message"]
