# Sistem Mimarisi

## Genel Bakis

Bu proje, yazilimcilarin canli sisteme zafiyetli kod gondermesini engelleyen otomatik
guvenlik kapilari (security gates) insa eder. GitHub Actions, Semgrep ve webhook
bildirimleri kullanarak tam otomatik bir DevSecOps boru hatti saglar.

Hedef kullanici: DevSecOps ekipleri, yazilim muhendisleri, guvenlik analistleri.

## Mimari Diyagram

```
Developer --> Git Push --> GitHub Actions
                               |
              +----------------+----------------+----------------+
              |                |                |                |
       Guvenlik Kapisi   Kural Dogrulama     Testler      Bagimlilik
       (app/secure       (app/vulnerable     (pytest)      Denetimi
        Semgrep)          Semgrep - bulgu                 (pip-audit)
              |            BEKLENIYOR)          |                |
              |                |                |                |
              +----------------+-------+--------+----------------+
              |                        |
            FAIL                  HEPSI PASS
              |                        |
         Webhook Bildirim         Docker Build
         (Discord/Slack)               |
         Pipeline DURUR            Deploy (sadece main)
```

Not: Guvenlik kapisi sadece uretim kodunu (`app/secure/`) tarar. Zafiyetli
demo kod (`app/vulnerable/`) ayri bir job'da taranir ve orada bulgu
**bulunmasi beklenir** — bu, kural setinin calistigini her push'ta kanitlar.
Bulgu cikmazsa kurallar bozulmus demektir ve pipeline durur.

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
2. GitHub Actions otomatik tetiklenir; dort kontrol paralel calisir:
   - **Guvenlik Kapisi:** Semgrep uretim kodunu (`app/secure/`) tarar;
     ERROR seviyesinde bulgu varsa pipeline durur, Discord/Slack'e uyari gider
   - **Kural Dogrulama:** Semgrep zafiyetli demo kodu (`app/vulnerable/`)
     tarar; bulgu bulunamazsa kural seti bozulmus demektir, pipeline durur
   - **Testler:** pytest ile guvenlik ve entegrasyon testleri kosulur
   - **Bagimlilik Denetimi:** pip-audit bilinen CVE'leri kontrol eder
3. Tum kontroller gecerse: Docker image olusturulur
4. Docker build basariliysa: deploy adimina gecilir (sadece main branch)

## Guvenlik Katmanlari

- **Katman 1:** Semgrep statik analiz (SAST) + kural setinin kendini dogrulamasi
- **Katman 2:** pip-audit bagimlilik taramasi (SCA) + Dependabot guncellemeleri
- **Katman 3:** GitHub Actions security gate (otomatik engel, minimal izinler)
- **Katman 4:** Docker guvenlik uygulamalari (non-root user, minimal image)
- **Katman 5:** Webhook bildirimleri (anlik farkindalik)
