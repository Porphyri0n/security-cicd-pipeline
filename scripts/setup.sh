#!/bin/bash
# Projeyi sifirdan kurar: bagimliliklar, veritabani, vb.

set -e  # Hata olursa dur

echo "Python bagimliliklari yukleniyor..."
pip install -r app/requirements.txt
pip install semgrep pytest pytest-cov

echo "Veritabani olusturuluyor..."
cd app/vulnerable && python -c "from database import init_db; init_db()" && cd ../..

echo "Kurulum tamamlandi!"
echo ""
echo "Simdi sunlari yapabilirsin:"
echo "  1. Zafiyetli uygulamayi calistir:  python app/vulnerable/app.py"
echo "  2. Lokal Semgrep taramasi:          bash scripts/run_local_scan.sh"
echo "  3. Tam demo:                        bash scripts/demo.sh"
