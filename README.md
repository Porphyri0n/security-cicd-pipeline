# Kendi Kendini Denetleyen Guvenli CI/CD Boru Hatti

Yazilimcilarin canli sisteme zafiyetli kod gondermesini engelleyen otomatik
guvenlik kapilari (security gates) iceren CI/CD boru hatti.

## Ne Yapar?

Bir gelistirici kodu push ettiginde:
1. **GitHub Actions** tetiklenir
2. **Semgrep** ile statik guvenlik analizi yapilir
3. Zafiyet bulunursa deploy **ENGELLENIR**
4. **Discord/Slack**'e otomatik hata raporu gonderilir

## Hizli Baslangic

```bash
# 1. Repo'yu klonla
git clone <repo-url> && cd secure-cicd-pipeline

# 2. Kurulumu calistir
bash scripts/setup.sh

# 3. Demo'yu izle
bash scripts/demo.sh
```

## Ozellikler

- **Statik Analiz:** Semgrep ile SQL Injection, Command Injection, hard-coded secret tespiti
- **Otomatik Engelleme:** Guvenlik acigi bulunan kod deploy edilemez
- **Anlik Bildirim:** Discord/Slack webhook ile uyari sistemi
- **Docker Destegi:** Guvenli konteynerizasyon (non-root, minimal image)
- **Egitim Odakli:** Zafiyetli ve guvenli kod yan yana karsilastirma
- **Ozel Kurallar:** Projeye ozel Semgrep kural seti

## Teknoloji Stack'i

| Teknoloji | Amac |
|-----------|------|
| Python/Flask | Web API (zafiyetli + guvenli) |
| Docker | Konteynerizasyon |
| GitHub Actions | CI/CD otomasyon |
| Semgrep | Statik kod analizi (SAST) |
| Webhook | Discord/Slack bildirim |

## Proje Yapisi

```
secure-cicd-pipeline/
├── app/
│   ├── vulnerable/    # Kasitli zafiyetli kod (demo)
│   └── secure/        # Guvenli uretim kodu
├── semgrep/
│   ├── custom/        # Ozel Semgrep kurallari
│   └── rules/         # Hazir kural setleri referansi
├── .github/workflows/ # CI/CD pipeline
├── docker/            # Dockerfile ve compose
├── notifications/     # Webhook bildirim sistemi
├── tests/             # Guvenlik ve entegrasyon testleri
├── scripts/           # Otomasyon scriptleri
└── docs/              # Dokumantasyon
```

## Dokumantasyon

- [Mimari](docs/ARCHITECTURE.md) - Sistem mimarisi ve akis diyagrami
- [Kurulum](docs/SETUP_GUIDE.md) - Adim adim kurulum rehberi
- [Guvenlik Kurallari](docs/SECURITY_RULES.md) - Semgrep kural aciklamalari
- [Katkida Bulunma](docs/CONTRIBUTING.md) - Gelistirme rehberi

## Lisans

MIT
