# Semgrep Kural Setleri

## Kullanilan Hazir Kural Setleri

| Kural Seti         | Komut               | Aciklama                              |
|---------------------|---------------------|---------------------------------------|
| Python Guvenlik     | `p/python`          | Python'a ozel genel guvenlik kurallari|
| Flask Guvenlik      | `p/flask`           | Flask framework zafiyetleri           |
| Secret Tespiti      | `p/secrets`         | Hard-coded credential tespiti         |
| OWASP Top 10        | `p/owasp-top-ten`   | OWASP en yaygin 10 zafiyet           |

## Ozel Kurallar

`custom/` klasorunde projeye ozel yazilmis kurallar bulunur:
- `hardcoded-secrets.yml` → AWS key, password, token tespiti
- `sql-injection.yml` → String concat ve f-string ile SQL sorgusu tespiti
- `command-injection.yml` → os.popen, os.system, subprocess shell=True tespiti
- `sensitive-data-exposure.yml` → Ortam degiskeni sizintisi ve debug mode tespiti
