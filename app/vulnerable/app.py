# ============================================
# app.py - Kasitli Zafiyetli Flask API
# ============================================
# UYARI: Bu uygulama DEMO amaclidir. ASLA uretimde kullanilmamalidir.
# Semgrep CI/CD boru hattinin calistigini kanitlamak icin
# bilerek guvenlik aciklari icerir.

from flask import Flask, request, jsonify
from database import init_db, get_user_vulnerable
from config import API_SECRET_KEY, DEBUG_MODE
import subprocess
import logging

# Loglama yapilandirmasi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = API_SECRET_KEY


@app.route("/")
def index():
    """Ana sayfa - API durum kontrolu"""
    logger.info("Ana sayfaya istek geldi")
    return jsonify({"status": "running", "message": "Vulnerable API v1.0"})


@app.route("/api/user", methods=["GET"])
def get_user():
    """
    ZAFiYET-5: SQL Injection endpoint'i
    Kullanim: GET /api/user?username=admin
    Saldiri: GET /api/user?username=' OR '1'='1
    """
    username = request.args.get("username", "")
    logger.info("Kullanici sorgusu: %s", username)
    results = get_user_vulnerable(username)
    return jsonify({"users": results})


@app.route("/api/ping", methods=["POST"])
def ping():
    """
    ZAFiYET-6: OS Command Injection
    Kullanicidan gelen host degeri dogrudan shell komutuna veriliyor
    """
    data = request.get_json()
    host = data.get("host", "")
    logger.info("Ping istegi: %s", host)
    # TEHLIKELI: Kullanici girdisi dogrudan shell komutunda
    result = subprocess.os.popen("ping -c 1 " + host).read()
    return jsonify({"result": result})


@app.route("/api/debug")
def debug_info():
    """
    ZAFiYET-7: Hassas bilgi sizintisi
    Debug bilgileri disariya acik
    """
    import os
    logger.info("Debug endpoint'ine erisim")
    return jsonify({
        "env_vars": dict(os.environ),
        "debug_mode": DEBUG_MODE,
        "secret_key": API_SECRET_KEY  # TEHLIKELI: Gizli anahtar disari sizdirildi
    })


if __name__ == "__main__":
    init_db()
    # ZAFiYET: debug=True uretimde tehlikeli
    app.run(host="0.0.0.0", port=5000, debug=True)
