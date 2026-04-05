# Sistem Mimarisi

## Genel Bakis

Bu proje, yazilimcilarin canli sisteme zafiyetli kod gondermesini engelleyen otomatik
guvenlik kapilari (security gates) insa eder. GitHub Actions, Semgrep ve webhook
bildirimleri kullanarak tam otomatik bir DevSecOps boru hatti saglar.

Hedef kullanici: DevSecOps ekipleri, yazilim muhendisleri, guvenlik analistleri.

## Mimari Diyagram

```
Developer --> Git Push --> GitHub Actions --> Semgrep Scan
                                                  |
                                            +-----+-----+
                                            |           |
                                         FAIL         PASS
                                            |           |
                                       Webhook     Docker Build
                                       Bildirim         |
                                     (Discord/       Deploy
                                      Slack)
```

## Bilesen Aciklamalari

| Bilesen | Klasor | Aciklama |
|---------|--------|----------|
| Zafiyetli API | `app/vulnerable/` | Demo amacli kasitli zafiyetli Flask API |
| Guvenli API | `app/secure/` | Tum zafiyetleri giderilmis uretim versiyonu |
| Semgrep Kurallari | `semgrep/` | Ozel ve hazir guvenlik tarama kurallari |
| CI/CD Pipeline | `.github/workflows/` | GitHub Actions guvenlik kapisi |
| Docker | `docker/` | Konteynerizasyon yapilandirmasi |
| Bildirimler | `notifications/` | Discord/Slack webhook entegrasyonu |
| Testler | `tests/` | Guvenlik ve entegrasyon testleri |
| Scriptler | `scripts/` | Kurulum, tarama ve demo otomasyon scriptleri |

## Veri Akisi

1. Gelistirici kod yazar ve GitHub'a push eder
2. GitHub Actions otomatik tetiklenir
3. Semgrep tum kodu statik analiz ile tarar
4. Bulgu varsa: pipeline durur, Discord/Slack'e uyari gonderilir
5. Bulgu yoksa: Docker image olusturulur
6. Docker build basariliysa: deploy adimina gecilir (sadece main branch)

## Guvenlik Katmanlari

- **Katman 1:** Semgrep statik analiz (SAST)
- **Katman 2:** GitHub Actions security gate (otomatik engel)
- **Katman 3:** Docker guvenlik uygulamalari (non-root user, minimal image)
- **Katman 4:** Webhook bildirimleri (anlik farkindalik)
