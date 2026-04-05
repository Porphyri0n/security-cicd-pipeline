"""
Semgrep'in zafiyetli kodu yakalayip guvenli kodu gecirdigini dogrula.
Bu test subprocess ile semgrep calistirir ve ciktiyi kontrol eder.
"""
import subprocess
import json
import pytest


def test_semgrep_catches_vulnerable_code():
    """Zafiyetli kod tarandiginda EN AZ 5 bulgu olmali"""
    result = subprocess.run(
        ["semgrep", "--config", "semgrep/custom/", "--config", "p/python",
         "--config", "p/flask", "--config", "p/secrets",
         "--json", "app/vulnerable/"],
        capture_output=True, text=True, encoding="utf-8", timeout=120
    )
    report = json.loads(result.stdout)
    findings = report.get("results", [])
    assert len(findings) >= 5, f"Beklenen en az 5 bulgu, bulunan: {len(findings)}"


def test_semgrep_passes_secure_code():
    """Guvenli kod tarandiginda SIFIR ERROR bulgusu olmali"""
    result = subprocess.run(
        ["semgrep", "--config", "semgrep/custom/", "--config", "p/python",
         "--config", "p/flask", "--config", "p/secrets",
         "--json", "app/secure/"],
        capture_output=True, text=True, encoding="utf-8", timeout=120
    )
    report = json.loads(result.stdout)
    errors = [r for r in report.get("results", [])
              if r.get("extra", {}).get("severity") == "ERROR"]
    assert len(errors) == 0, f"Guvenli kodda {len(errors)} ERROR bulundu!"


def test_semgrep_detects_sql_injection():
    """SQL Injection pattern'i spesifik olarak yakalanmali"""
    result = subprocess.run(
        ["semgrep", "--config", "semgrep/custom/", "--json",
         "app/vulnerable/database.py"],
        capture_output=True, text=True, encoding="utf-8", timeout=120
    )
    report = json.loads(result.stdout)
    rule_ids = [r.get("check_id", "") for r in report.get("results", [])]
    sql_rules = [r for r in rule_ids if "sql" in r.lower()]
    assert len(sql_rules) > 0, "SQL Injection kurali tetiklenmedi!"


def test_semgrep_detects_hardcoded_secrets():
    """Hard-coded secret pattern'i yakalanmali"""
    result = subprocess.run(
        ["semgrep", "--config", "semgrep/custom/", "--json",
         "app/vulnerable/config.py"],
        capture_output=True, text=True, encoding="utf-8", timeout=120
    )
    report = json.loads(result.stdout)
    assert len(report.get("results", [])) > 0, "Hard-coded secret tespit edilemedi!"


def test_semgrep_detects_command_injection():
    """Command Injection pattern'i yakalanmali"""
    result = subprocess.run(
        ["semgrep", "--config", "semgrep/custom/", "--json",
         "app/vulnerable/app.py"],
        capture_output=True, text=True, encoding="utf-8", timeout=120
    )
    report = json.loads(result.stdout)
    rule_ids = [r.get("check_id", "") for r in report.get("results", [])]
    cmd_rules = [r for r in rule_ids if "popen" in r.lower() or "command" in r.lower()]
    assert len(cmd_rules) > 0, "Command Injection kurali tetiklenmedi!"
