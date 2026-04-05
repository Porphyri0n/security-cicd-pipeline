# Kurulum Rehberi

## On Kosullar

- Python 3.11+
- Docker & Docker Compose
- GitHub hesabi
- Discord veya Slack hesabi (webhook icin)

## Adim Adim Kurulum

### 1. Repo'yu klonla

```bash
git clone <repo-url>
cd secure-cicd-pipeline
```

### 2. Otomatik kurulum

```bash
bash scripts/setup.sh
```

### 3. Ortam degiskenlerini ayarla

```bash
cp .env.example .env
# .env dosyasini duzenle ve gercek degerleri gir
```

### 4. Discord/Slack Webhook URL'ini al

**Discord:**
1. Sunucunda bir kanal ac (orn: `#guvenlik-uyarilari`)
2. Kanal Ayarlari > Entegrasyonlar > Webhook Olustur
3. Webhook URL'ini kopyala

**Slack:**
1. https://api.slack.com/apps adresine git
2. "Create New App" > "From Scratch"
3. "Incoming Webhooks" > Aktif et
4. "Add New Webhook to Workspace" > Kanal sec

### 5. GitHub Secrets'a webhook URL'ini ekle

Repository Settings > Secrets and variables > Actions:
- `DISCORD_WEBHOOK_URL`: Discord webhook URL'i
- `SLACK_WEBHOOK_URL`: (opsiyonel) Slack webhook URL'i

### 6. Ilk push ve pipeline testi

```bash
git add .
git commit -m "Initial setup"
git push origin main
```

GitHub Actions sekmesinden pipeline'in calistigini izle.

## Lokal Gelistirme

### Uygulamayi calistirma

```bash
# Zafiyetli versiyon (sadece test icin)
python app/vulnerable/app.py

# Guvenli versiyon
python app/secure/app.py
```

### Semgrep taramasi yapma

```bash
bash scripts/run_local_scan.sh
```

### Testleri calistirma

```bash
pytest tests/ -v
```

### Docker ile calistirma

```bash
docker build -t secure-api:latest -f docker/Dockerfile .
docker run -p 5000:5000 secure-api:latest
```
