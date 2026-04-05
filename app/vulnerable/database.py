# ============================================
# database.py - Kasitli Zafiyetli Veritabani Katmani
# ============================================
# UYARI: Bu dosya SQL Injection zafiyeti icerir (DEMO amacli).

import sqlite3
import logging

# Loglama yapilandirmasi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Veritabanini ve ornek tabloyu olustur"""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Ornek kullanicilar ekle
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, email, password) "
        "VALUES (1, 'admin', 'admin@example.com', 'admin123')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, email, password) "
        "VALUES (2, 'user1', 'user1@example.com', 'pass456')"
    )
    conn.commit()
    conn.close()
    logger.info("Veritabani basariyla olusturuldu")


def get_user_vulnerable(username):
    """
    ZAFiYET-5: SQL Injection - Kullanici girdisi dogrudan SQL'e ekleniyor
    Saldirgan: username = "' OR '1'='1" gondererek tum kullanicilari alabilir
    """
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # TEHLIKELI: String birlestirme ile SQL sorgusu
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    logger.info("Calistirilan sorgu: %s", query)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
