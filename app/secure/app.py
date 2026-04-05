# ============================================
# app.py - Guvenli Flask API
# ============================================
# Tum zafiyetler giderilmis uretim versiyonu.

from flask import Flask, request, jsonify
from database import init_db, get_user_secure
from config import API_SECRET_KEY, DEBUG_MODE
import subprocess
import re
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
    return jsonify({"status": "running", "message": "Secure API v1.0"})


@app.route("/api/user", methods=["GET"])
def get_user():
    """Parametrik sorgu ile guvenli kullanici arama"""
    username = request.args.get("username", "")
    # Girdi dogrulama: sadece alfanumerik ve alt cizgi kabul et
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        logger.warning("Gecersiz kullanici adi denemesi: %s", username)
        return jsonify({"error": "Gecersiz kullanici adi formati"}), 400
    logger.info("Kullanici sorgusu: %s", username)
    results = get_user_secure(username)
    return jsonify({"users": results})


@app.route("/api/ping", methods=["POST"])
def ping():
    """DUZELTILDI: Girdi dogrulama + shell=False"""
    data = request.get_json()
    host = data.get("host", "")
    # Sadece IP veya domain formati kabul et
    if not re.match(r'^[a-zA-Z0-9.\-]+$', host):
        logger.warning("Gecersiz host denemesi: %s", host)
        return jsonify({"error": "Gecersiz host formati"}), 400
    try:
        result = subprocess.run(
            ["ping", "-c", "1", host],
            capture_output=True, text=True, timeout=5
        )
        return jsonify({"result": result.stdout})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Zaman asimi"}), 408


# DUZELTILDI: /api/debug endpoint'i tamamen kaldirildi


if __name__ == "__main__":
    import os
    init_db()
    # DUZELTILDI: Host ve debug modu ortam degiskenlerine bagli
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    app.run(host=host, port=port, debug=DEBUG_MODE)
