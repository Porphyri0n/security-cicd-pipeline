# Guvenlik Kurallari Referansi

Bu dokuman, projede kullanilan Semgrep kurallarini ve yakaladiklari
zafiyetleri aciklar.

## Ozel Kurallar (semgrep/custom/)

### 1. Hard-coded AWS Key (CWE-798)

- **Kural:** `custom-hardcoded-aws-key`
- **Dosya:** `semgrep/custom/hardcoded-secrets.yml`
- **Yakaladigi:** AWS_ACCESS_KEY_ID ve AWS_SECRET_ACCESS_KEY'in koda gomulmesi
- **Severity:** ERROR
- **Neden tehlikeli:** Kaynak koda erisimi olan herkes AWS kaynaklarina erisir
- **Duzeltme:**
  ```python
  # Yanlis
  AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
  AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

  # Dogru
  AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
  AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
  ```

### 2. Hard-coded Password/Secret (CWE-798)

- **Kural:** `custom-hardcoded-password`
- **Dosya:** `semgrep/custom/hardcoded-secrets.yml`
- **Yakaladigi:** Degisken adinda password, secret, key, token iceren hard-coded degerler (buyuk/kucuk harf duyarsiz)
- **Severity:** WARNING
- **Duzeltme:** Tum hassas degerleri ortam degiskenlerinden okuyun

### 3. SQL Injection - String Concatenation (CWE-89)

- **Kural:** `custom-sql-string-concat`
- **Dosya:** `semgrep/custom/sql-injection.yml`
- **Yakaladigi:** SQL sorgusunda string birlestirme ile kullanici girdisi kullanimi
- **Severity:** ERROR
- **Neden tehlikeli:** Saldirgan SQL komutlari enjekte ederek veritabanini manipule eder
- **Duzeltme:**
  ```python
  # Yanlis
  query = "SELECT * FROM users WHERE username = '" + username + "'"
  cursor.execute(query)

  # Dogru
  cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
  ```

### 4. SQL Injection - f-string (CWE-89)

- **Kural:** `custom-sql-fstring`
- **Dosya:** `semgrep/custom/sql-injection.yml`
- **Yakaladigi:** SQL sorgusunda f-string kullanimi
- **Severity:** ERROR
- **Duzeltme:** Parametrik sorgu kullanin

### 5. OS Command Injection - os.popen (CWE-78)

- **Kural:** `custom-os-popen-injection`
- **Dosya:** `semgrep/custom/command-injection.yml`
- **Yakaladigi:** os.popen() veya subprocess.os.popen() kullanimi
- **Severity:** ERROR
- **Neden tehlikeli:** Bu fonksiyonlar her zaman shell uzerinden calisir, saldirgan isletim sistemi komutlari enjekte edebilir
- **Duzeltme:**
  ```python
  # Yanlis
  result = subprocess.os.popen("ping -c 1 " + host).read()

  # Dogru
  result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
  ```

### 6. OS Command Injection - os.system (CWE-78)

- **Kural:** `custom-os-system-injection`
- **Dosya:** `semgrep/custom/command-injection.yml`
- **Yakaladigi:** os.system() kullanimi
- **Severity:** ERROR
- **Duzeltme:** subprocess.run() + shell=False kullanin

### 7. subprocess shell=True (CWE-78)

- **Kural:** `custom-subprocess-shell-true`
- **Dosya:** `semgrep/custom/command-injection.yml`
- **Yakaladigi:** subprocess.run(), subprocess.call() veya subprocess.Popen() fonksiyonlarinin shell=True parametresi ile kullanimi
- **Severity:** WARNING
- **Duzeltme:** `shell=False` kullanin ve komutu liste olarak verin

### 8. Ortam Degiskeni Sizintisi (CWE-215)

- **Kural:** `custom-env-vars-exposure`
- **Dosya:** `semgrep/custom/sensitive-data-exposure.yml`
- **Yakaladigi:** dict(os.environ) ile tum ortam degiskenlerinin disariya acilmasi
- **Severity:** ERROR
- **Neden tehlikeli:** API anahtarlari, veritabani sifreleri gibi hassas bilgiler sizabilir
- **Duzeltme:** Debug endpoint'lerini tamamen kaldirin veya erisimi kisitlayin

### 9. Flask Debug Mode (CWE-215)

- **Kural:** `custom-flask-debug-enabled`
- **Dosya:** `semgrep/custom/sensitive-data-exposure.yml`
- **Yakaladigi:** Flask uygulamasinin debug=True ile baslatilmasi
- **Severity:** WARNING
- **Neden tehlikeli:** Hata izleri ve interaktif debugger disariya acilir
- **Duzeltme:**
  ```python
  # Yanlis
  app.run(host="0.0.0.0", port=5000, debug=True)

  # Dogru
  debug = os.environ.get("DEBUG_MODE", "false").lower() == "true"
  app.run(host=host, port=port, debug=debug)
  ```

## Hazir Kural Setleri

| Kural Seti | Komut | Aciklama |
|------------|-------|----------|
| Python Guvenlik | `p/python` | Python'a ozel genel guvenlik kurallari |
| Flask Guvenlik | `p/flask` | Flask framework zafiyetleri |
| Secret Tespiti | `p/secrets` | Hard-coded credential tespiti |
| OWASP Top 10 | `p/owasp-top-ten` | OWASP en yaygin 10 zafiyet |
