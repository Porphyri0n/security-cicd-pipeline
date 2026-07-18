# Kendi Kendini Denetleyen Guvenli CI/CD Boru Hatti

Yazilimcilarin canli sisteme zafiyetli kod gondermesini engelleyen otomatik
guvenlik kapilari (security gates) iceren CI/CD boru hatti.

## Ne Yapar?

Bir gelistirici kodu push ettiginde GitHub Actions uzerinde su kontroller calisir:

| Job | Gorev | Basarisiz Olursa |
|-----|-------|------------------|
| **Guvenlik Kapisi** | Uretim kodu (`app/secure/`) Semgrep ile taranir | Deploy engellenir + Discord/Slack'e uyari gider |
| **Kural Dogrulama** | Zafiyetli demo kod (`app/vulnerable/`) taranir, kurallarin zafiyetleri **yakaladigi** kanitlanir | Kural seti bozulmus demektir, pipeline durur |
| **Testler** | pytest ile guvenlik ve entegrasyon testleri kosulur | Pipeline durur |
| **Bagimlilik Denetimi** | pip-audit ile bilinen CVE'ler kontrol edilir | Pipeline durur |
| **Docker Build** | Tum kontroller gectiyse image olusturulur | Deploy engellenir |
| **Deploy** | Sadece `main` branch'te ve build basariliysa calisir | - |

Boylece pipeline hem uretim kodunu korur hem de kendi guvenlik kurallarinin
calistigini her push'ta dogrular.

## Hizli Baslangic

```bash
# 1. Repo'yu klonla
git clone <repo-url> && cd security-cicd-pipeline

# 2. Kurulumu calistir
bash scripts/setup.sh

# 3. Ortam degiskenlerini hazirla (.env ASLA commit edilmez)
cp .env.example .env

# 4. Demo'yu izle
bash scripts/demo.sh
```

Ayrintili kurulum (webhook, GitHub Secrets vb.) icin [Kurulum Rehberi](docs/SETUP_GUIDE.md).

## Ozellikler

- **Statik Analiz:** Semgrep ile SQL Injection, Command Injection, hard-coded secret tespiti
- **Otomatik Engelleme:** Guvenlik acigi bulunan kod deploy edilemez
- **Kendini Dogrulama:** Zafiyetli demo kod uzerinde kural seti her push'ta test edilir
- **Bagimlilik Guvenligi:** pip-audit ile CVE taramasi, Dependabot ile otomatik guncelleme
- **Anlik Bildirim:** Discord/Slack webhook ile uyari sistemi
- **Docker Destegi:** Guvenli konteynerizasyon (non-root kullanici, minimal imaj)
- **Egitim Odakli:** Zafiyetli ve guvenli kod yan yana karsilastirma
- **Ozel Kurallar:** Projeye ozel Semgrep kural seti (CWE referanslariyla)

## Teknoloji Stack'i

| Teknoloji | Amac |
|-----------|------|
| Python/Flask | Web API (zafiyetli + guvenli surum) |
| Docker | Konteynerizasyon |
| GitHub Actions | CI/CD otomasyon |
| Semgrep | Statik kod analizi (SAST) |
| pip-audit | Bagimlilik zafiyet taramasi (SCA) |
| Webhook | Discord/Slack bildirim |

## Proje Yapisi

```
security-cicd-pipeline/
├── app/
│   ├── vulnerable/    # Kasitli zafiyetli kod (demo - ASLA deploy edilmez)
│   └── secure/        # Guvenli uretim kodu (guvenlik kapisindan gecen)
├── semgrep/
│   ├── custom/        # Ozel Semgrep kurallari
│   └── rules/         # Hazir kural setleri referansi
├── .github/
│   ├── workflows/     # CI/CD pipeline (guvenlik kapisi)
│   └── dependabot.yml # Otomatik bagimlilik guncelleme
├── docker/            # Dockerfile ve compose
├── notifications/     # Webhook bildirim sistemi
├── tests/             # Guvenlik ve entegrasyon testleri
├── scripts/           # Otomasyon scriptleri
└── docs/              # Dokumantasyon
```

## Onemli Notlar

- `app/vulnerable/` klasoru **kasitli olarak** zafiyet icerir; Semgrep kurallarinin
  calistigini kanitlamak icin kullanilir. Docker imajina dahil edilmez
  (`.dockerignore`) ve guvenlik kapisi taramasina girmez.
- `.env` dosyasi gitignore'dadir ve asla commit edilmemelidir; sablon icin
  `.env.example` dosyasina bakin.
- Zafiyetli koddaki AWS anahtarlari AWS'nin resmi dokumantasyon ornekleridir,
  gercek degildir.

## Dokumantasyon

- [Mimari](docs/ARCHITECTURE.md) - Sistem mimarisi ve akis diyagrami
- [Kurulum](docs/SETUP_GUIDE.md) - Adim adim kurulum rehberi
- [Guvenlik Kurallari](docs/SECURITY_RULES.md) - Semgrep kural aciklamalari
- [Katkida Bulunma](docs/CONTRIBUTING.md) - Gelistirme rehberi

## Lisans

[MIT](LICENSE)
