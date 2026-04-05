#!/bin/bash
# Projenin tum akisini bastan sona gosterir

echo "CI/CD Guvenlik Boru Hatti - DEMO"
echo "======================================"
echo ""

echo "[ADIM 1/5] Zafiyetli uygulama baslatiliyor..."
cd app/vulnerable && python app.py &
APP_PID=$!
cd ../..
sleep 2

echo "[ADIM 2/5] Zafiyetli endpoint'ler test ediliyor..."
echo "  Normal sorgu:"
curl -s http://localhost:5000/api/user?username=admin | python3 -m json.tool
echo ""
echo "  SQL Injection denemesi:"
curl -s "http://localhost:5000/api/user?username=' OR '1'='1" | python3 -m json.tool
echo ""

echo "[ADIM 3/5] Semgrep guvenlik taramasi..."
bash scripts/run_local_scan.sh

echo "[ADIM 4/5] Zafiyetli uygulama durduruluyor..."
kill $APP_PID 2>/dev/null

echo "[ADIM 5/5] Testler calistiriliyor..."
pytest tests/ -v --tb=short

echo ""
echo "Demo tamamlandi!"
echo "Sonuc: Semgrep zafiyetleri yakaladi -> Pipeline durdurulur -> Bildirim gonderilir"
