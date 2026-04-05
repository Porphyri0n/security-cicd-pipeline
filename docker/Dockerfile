# ---- Base Image ----
FROM python:3.11-slim AS base

# Guvenlik: root olmayan kullanici olustur
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Calisma dizini
WORKDIR /app

# Bagimliliklari once kopyala (Docker cache optimizasyonu)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala (secure versiyonu)
COPY app/secure/ .

# Guvenlik: root olmayan kullaniciya gec
USER appuser

# Docker icinde 0.0.0.0'a bind etmek gerekli
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

# Port ac
EXPOSE 5000

# Saglik kontrolu
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Uygulamayi baslat
CMD ["python", "app.py"]
