"""
Pytest fixture'lari.
Her iki uygulama versiyonu icin Flask test client'i sagla.
Modul cache temizligi ile izole calisir.
"""
import pytest
import sys
import os


def _clean_app_modules():
    """app, database, config modullerini cache'den temizle"""
    for mod_name in list(sys.modules.keys()):
        if mod_name in ('app', 'database', 'config'):
            del sys.modules[mod_name]


def _remove_db():
    """Calisma dizinindeki app.db dosyasini temizle"""
    if os.path.exists("app.db"):
        os.remove("app.db")


@pytest.fixture
def vulnerable_client():
    """Zafiyetli uygulamanin test client'i"""
    _clean_app_modules()
    _remove_db()
    vuln_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'vulnerable'))
    sys.path.insert(0, vuln_path)
    import app as vuln_app
    import database as vuln_db
    vuln_app.app.config['TESTING'] = True
    vuln_db.init_db()
    with vuln_app.app.test_client() as client:
        yield client
    # Temizlik
    if vuln_path in sys.path:
        sys.path.remove(vuln_path)
    _clean_app_modules()
    _remove_db()


@pytest.fixture
def secure_client():
    """Guvenli uygulamanin test client'i"""
    _clean_app_modules()
    _remove_db()
    secure_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'secure'))
    sys.path.insert(0, secure_path)
    # Ortam degiskenlerini ayarla (guvenli config icin)
    os.environ["API_SECRET_KEY"] = "test-secret-key"
    os.environ["DEBUG_MODE"] = "false"
    import app as secure_app
    import database as secure_db
    secure_app.app.config['TESTING'] = True
    secure_db.init_db()
    with secure_app.app.test_client() as client:
        yield client
    # Temizlik
    if secure_path in sys.path:
        sys.path.remove(secure_path)
    _clean_app_modules()
    _remove_db()
