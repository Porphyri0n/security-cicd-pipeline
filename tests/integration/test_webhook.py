"""
Webhook bildirim fonksiyonlarini test et.
Gercek webhook gondermez, payload olusturmayi test eder.
"""
import sys
import os
import json

# notifications modulunu import et
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'notifications'))

from send_alert import parse_semgrep_report, build_discord_payload, build_slack_payload


def test_parse_semgrep_report(tmp_path):
    """Semgrep raporu dogru parse edilmeli"""
    # Sahte rapor olustur
    fake_report = {
        "results": [
            {
                "check_id": "test-rule-1",
                "path": "test.py",
                "start": {"line": 10},
                "extra": {
                    "severity": "ERROR",
                    "message": "Test bulgusu"
                }
            },
            {
                "check_id": "test-rule-2",
                "path": "test2.py",
                "start": {"line": 20},
                "extra": {
                    "severity": "WARNING",
                    "message": "Test uyarisi"
                }
            }
        ]
    }

    report_path = tmp_path / "test-report.json"
    report_path.write_text(json.dumps(fake_report))

    summary = parse_semgrep_report(str(report_path))
    assert summary["total_findings"] == 2
    assert summary["errors"] == 1
    assert summary["warnings"] == 1
    assert len(summary["findings"]) == 2


def test_parse_missing_report():
    """Var olmayan rapor dosyasi bos sonuc donmeli"""
    summary = parse_semgrep_report("/nonexistent/report.json")
    assert summary["total_findings"] == 0


def test_discord_payload_structure():
    """Discord payload dogru formatta olmali"""
    summary = {
        "total_findings": 3,
        "errors": 2,
        "warnings": 1,
        "findings": [
            {"rule_id": "test", "severity": "ERROR", "file": "test.py", "line": 1, "message": "Test"}
        ]
    }
    payload = build_discord_payload(summary, alert_type="failure")
    assert "embeds" in payload
    assert len(payload["embeds"]) > 0
    embed = payload["embeds"][0]
    assert "title" in embed
    assert "fields" in embed
    assert embed["color"] == 16711680  # Kirmizi


def test_discord_success_payload():
    """Discord basari bildirimi dogru formatta olmali"""
    payload = build_discord_payload({}, alert_type="success")
    assert "embeds" in payload
    assert payload["embeds"][0]["color"] == 65280  # Yesil


def test_slack_payload_structure():
    """Slack payload dogru formatta olmali"""
    summary = {
        "total_findings": 2,
        "errors": 1,
        "warnings": 1,
        "findings": [
            {"rule_id": "test", "severity": "ERROR", "file": "test.py", "line": 1, "message": "Test"}
        ]
    }
    payload = build_slack_payload(summary, alert_type="failure")
    assert "blocks" in payload
    assert len(payload["blocks"]) > 0


def test_slack_success_payload():
    """Slack basari bildirimi dogru formatta olmali"""
    payload = build_slack_payload({}, alert_type="success")
    assert "blocks" in payload
