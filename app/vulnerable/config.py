# ============================================
# config.py - Kasitli Zafiyetli Yapilandirma
# ============================================
# UYARI: Bu dosya DEMO amaclidir. Gercek credential ICERMEZ.
# Semgrep tarafindan yakalanmasi gereken zafiyetler icerir.

# ZAFiYET-1: Hard-coded AWS anahtarlari (SAHTE degerler!)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ZAFiYET-2: Hard-coded veritabani sifresi
DATABASE_PASSWORD = "super_secret_password_123"

# ZAFiYET-3: Hard-coded API anahtari
API_SECRET_KEY = "sk-fake-api-key-do-not-use-in-production"

# ZAFiYET-4: Debug modu acik
DEBUG_MODE = True
