#!/bin/bash
# Semgrep ile lokal tarama yapar ve sonuclari gosterir

echo "Semgrep Taramasi Basliyor..."
echo "================================"
echo ""

echo "--- Zafiyetli Kod Taramasi ---"
semgrep --config p/python --config p/flask --config p/secrets \
  --config semgrep/custom/ \
  app/vulnerable/ \
  --json --output semgrep-report.json 2>/dev/null

# Sonuclari oku ve ozetle
python3 -c "
import json
with open('semgrep-report.json') as f:
    data = json.load(f)
results = data.get('results', [])
print(f'Toplam bulgu: {len(results)}')
for r in results:
    sev = r.get('extra', {}).get('severity', '?')
    path = r.get('path', '?')
    line = r.get('start', {}).get('line', '?')
    msg = r.get('extra', {}).get('message', '?')[:80]
    icon = 'HATA' if sev == 'ERROR' else 'UYARI'
    print(f'  [{icon}] [{sev}] {path}:{line} - {msg}')
"

echo ""
echo "--- Guvenli Kod Taramasi ---"
semgrep --config semgrep/custom/ --config p/python --config p/flask --config p/secrets app/secure/ 2>/dev/null
echo "Guvenli kod taramasi tamamlandi"
