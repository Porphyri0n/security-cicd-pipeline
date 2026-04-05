# Katkida Bulunma Rehberi

## Yeni Guvenlik Kurali Ekleme

1. `semgrep/custom/` altinda yeni bir `.yml` dosyasi olusturun
2. Semgrep kural formatini takip edin:
   ```yaml
   rules:
     - id: custom-kural-adi
       pattern: |
         <tespit edilecek kod deseni>
       message: >
         Aciklama ve duzeltme onerisi
       severity: ERROR veya WARNING
       languages: [python]
       metadata:
         category: security
         cwe: "CWE-XXX"
   ```
3. Kurali zafiyetli koda karsi test edin:
   ```bash
   semgrep --config semgrep/custom/yeni-kural.yml app/vulnerable/
   ```
4. Guvenli kodun kurali tetiklemedigini dogrulayin

## Test Yazma

1. Uygun test klasorunu secin:
   - `tests/security/` - Guvenlik testleri
   - `tests/integration/` - Entegrasyon testleri
2. Test dosyasi adi `test_` ile baslamali
3. conftest.py'deki fixture'lari kullanin (`vulnerable_client`, `secure_client`)
4. Testleri calistirin:
   ```bash
   pytest tests/ -v
   ```

## PR Acma Sureci

1. Feature branch olusturun: `git checkout -b feature/aciklama`
2. Degisikliklerinizi yapin
3. Testlerin gectiginden emin olun: `pytest tests/ -v`
4. Semgrep taramasi yapin: `bash scripts/run_local_scan.sh`
5. PR acin ve asagidaki bilgileri ekleyin:
   - Ne degistirildi
   - Neden degistirildi
   - Nasil test edildi

## Kod Standartlari

- Python kodu PEP 8 uyumlu olmali
- Turkce yorum satirlari kullanin
- Tum hassas degerler ortam degiskenlerinden okunmali
- Yeni endpoint'ler girdi dogrulama icermeli
- Guvenli kodda Semgrep sifir bulgu raporlamali
