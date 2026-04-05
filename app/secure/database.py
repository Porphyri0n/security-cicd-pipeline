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
            password_hash TEXT NOT NULL
        )
    """)
    # Ornek kullanicilar ekle (sifre hash olarak saklanmali)
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, email, password_hash) "
        "VALUES (1, 'admin', 'admin@example.com', 'hashed_admin123')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, email, password_hash) "
        "VALUES (2, 'user1', 'user1@example.com', 'hashed_pass456')"
    )
    conn.commit()
    conn.close()
    logger.info("Veritabani basariyla olusturuldu")


def get_user_secure(username):
    """
    DUZELTILDI: Parametrik sorgu - SQL Injection imkansiz
    """
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Guvenli: ? placeholder ile parametrik sorgu
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchall()
    conn.close()
    return result
