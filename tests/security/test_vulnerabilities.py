"""
Zafiyetli endpoint'lere gercek saldiri senaryolari uygula.
Zafiyetli versiyonda saldiri BASARILI olmali.
Guvenli versiyonda saldiri ENGELLENMELI.
"""


def test_sql_injection_works_on_vulnerable(vulnerable_client):
    """Zafiyetli API'da SQL Injection calismali (demo amacli)"""
    response = vulnerable_client.get("/api/user?username=' OR '1'='1")
    data = response.get_json()
    # Tum kullanicilar donmeli (injection basarili)
    assert len(data["users"]) > 1, "SQL Injection calismadi (zafiyetli kodda calismalidir)"


def test_sql_injection_blocked_on_secure(secure_client):
    """Guvenli API'da SQL Injection ENGELLENMELI"""
    response = secure_client.get("/api/user?username=' OR '1'='1")
    assert response.status_code == 400, "SQL Injection engellenmedi!"


def test_command_injection_blocked_on_secure(secure_client):
    """Guvenli API'da Command Injection ENGELLENMELI"""
    response = secure_client.post("/api/ping",
        json={"host": "google.com; cat /etc/passwd"})
    assert response.status_code == 400, "Command Injection engellenmedi!"


def test_debug_endpoint_removed_on_secure(secure_client):
    """Guvenli API'da /api/debug endpoint'i OLMAMALI"""
    response = secure_client.get("/api/debug")
    assert response.status_code == 404, "/api/debug hala erisilebilir!"
