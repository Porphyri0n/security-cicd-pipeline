"""
Guvenlik Uyari Bildirim Sistemi
================================
CI/CD pipeline'indan cagrilarak Semgrep bulgularini
Discord veya Slack webhook'una gonderir.

Kullanim:
  python send_alert.py --report semgrep-report.json --webhook-url <URL>
  python send_alert.py --type success --message "Deploy OK" --webhook-url <URL>
"""

import json
import sys
import argparse
import logging
from datetime import datetime, timezone

# Loglama yapilandirmasi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# requests kutuphanesi yoksa urllib kullan
try:
    import requests
    USE_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    USE_REQUESTS = False


def parse_semgrep_report(report_path):
    """
    Semgrep JSON raporunu oku ve ozetini cikar.
    """
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error("Rapor dosyasi bulunamadi: %s", report_path)
        return {"total_findings": 0, "errors": 0, "warnings": 0, "findings": []}
    except json.JSONDecodeError:
        logger.error("Rapor dosyasi gecerli JSON degil: %s", report_path)
        return {"total_findings": 0, "errors": 0, "warnings": 0, "findings": []}

    results = data.get("results", [])
    findings = []

    for result in results:
        severity = result.get("extra", {}).get("severity", "WARNING")
        finding = {
            "rule_id": result.get("check_id", "unknown"),
            "severity": severity,
            "file": result.get("path", "unknown"),
            "line": result.get("start", {}).get("line", 0),
            "message": result.get("extra", {}).get("message", "Aciklama yok")
        }
        findings.append(finding)

    errors = [f for f in findings if f["severity"] == "ERROR"]
    warnings = [f for f in findings if f["severity"] == "WARNING"]

    summary = {
        "total_findings": len(findings),
        "errors": len(errors),
        "warnings": len(warnings),
        "findings": findings
    }

    logger.info(
        "Rapor ozeti: %d toplam, %d hata, %d uyari",
        summary["total_findings"], summary["errors"], summary["warnings"]
    )
    return summary


def build_discord_payload(report_summary, alert_type="failure"):
    """
    Discord Embed formatinda mesaj olustur.
    """
    now = datetime.now(timezone.utc).isoformat()

    if alert_type == "success":
        return {
            "embeds": [{
                "title": "Deploy Basarili",
                "color": 65280,  # Yesil
                "description": "Tum guvenlik kontrolleri gecti ve deploy basariyla tamamlandi.",
                "footer": {"text": "CI/CD Guvenlik Boru Hatti"},
                "timestamp": now
            }]
        }

    # Basarisizlik (guvenlik uyarisi) bildirimi
    findings = report_summary.get("findings", [])

    # Bulgu detaylarini olustur (maksimum 10 bulgu)
    details_lines = []
    for finding in findings[:10]:
        severity_icon = "HATA" if finding["severity"] == "ERROR" else "UYARI"
        short_msg = finding["message"].strip().split("\n")[0][:100]
        details_lines.append(
            f"**{finding['file']}:{finding['line']}** — [{severity_icon}] {short_msg}"
        )

    if len(findings) > 10:
        details_lines.append(f"...ve {len(findings) - 10} bulgu daha")

    description = "\n".join(details_lines) if details_lines else "Detay bulunamadi."

    return {
        "embeds": [{
            "title": "GUVENLIK UYARISI — Pipeline Durduruldu",
            "color": 16711680,  # Kirmizi
            "fields": [
                {"name": "Toplam Bulgu", "value": str(report_summary["total_findings"]), "inline": True},
                {"name": "Kritik (ERROR)", "value": str(report_summary["errors"]), "inline": True},
                {"name": "Uyari (WARNING)", "value": str(report_summary["warnings"]), "inline": True}
            ],
            "description": description,
            "footer": {"text": "CI/CD Guvenlik Boru Hatti"},
            "timestamp": now
        }]
    }


def build_slack_payload(report_summary, alert_type="failure"):
    """
    Slack Block Kit formatinda mesaj olustur.
    """
    if alert_type == "success":
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "Deploy Basarili"}
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Tum guvenlik kontrolleri gecti ve deploy basariyla tamamlandi."
                    }
                }
            ]
        }

    # Basarisizlik bildirimi
    findings = report_summary.get("findings", [])

    # Bulgu detaylarini olustur
    details_lines = []
    for finding in findings[:10]:
        severity_icon = "HATA" if finding["severity"] == "ERROR" else "UYARI"
        short_msg = finding["message"].strip().split("\n")[0][:100]
        details_lines.append(f"*{finding['file']}:{finding['line']}* — [{severity_icon}] {short_msg}")

    if len(findings) > 10:
        details_lines.append(f"...ve {len(findings) - 10} bulgu daha")

    details_text = "\n".join(details_lines) if details_lines else "Detay bulunamadi."

    return {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "GUVENLIK UYARISI — Pipeline Durduruldu"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Toplam Bulgu:* {report_summary['total_findings']}"},
                    {"type": "mrkdwn", "text": f"*Kritik:* {report_summary['errors']}"},
                    {"type": "mrkdwn", "text": f"*Uyari:* {report_summary['warnings']}"}
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": details_text}
            }
        ]
    }


def _try_send(webhook_url, payload):
    """Tek bir webhook gonderme denemesi yapar. Basarida True doner."""
    json_payload = json.dumps(payload)
    if USE_REQUESTS:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if 200 <= response.status_code < 300:
            return True
        logger.error("Webhook hatasi: HTTP %d — %s", response.status_code, response.text)
        return False
    else:
        req = urllib.request.Request(
            webhook_url,
            data=json_payload.encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            if 200 <= status < 300:
                return True
            logger.error("Webhook hatasi: HTTP %d", status)
            return False


def send_webhook(webhook_url, payload):
    """
    Webhook URL'ine POST istegi gonder.
    Basarisiz olursa bir kez daha dener.
    """
    logger.info("Webhook'a bildirim gonderiliyor: %s", webhook_url[:50] + "...")

    for attempt in range(1, 3):
        try:
            if _try_send(webhook_url, payload):
                logger.info("Bildirim basariyla gonderildi (deneme %d)", attempt)
                return True
        except Exception as e:
            logger.error("Deneme %d basarisiz: %s", attempt, str(e))
        if attempt < 2:
            logger.info("Tekrar deneniyor...")

    return False


def main():
    """
    Komut satiri arguemanlari ile bildirim gonder.
    """
    parser = argparse.ArgumentParser(description="CI/CD Guvenlik Bildirimi")
    parser.add_argument("--report", help="Semgrep rapor dosyasi yolu")
    parser.add_argument("--webhook-url", required=True, help="Webhook URL")
    parser.add_argument("--type", default="failure", choices=["failure", "success"])
    parser.add_argument("--message", default="", help="Ozel mesaj")
    parser.add_argument("--platform", default="discord", choices=["discord", "slack"])

    args = parser.parse_args()

    # Webhook URL bossa veya placeholder ise sessizce cik
    if not args.webhook_url or args.webhook_url.startswith("$"):
        print("Webhook URL yapilandirilmamis, bildirim atlaniyor.")
        sys.exit(0)

    payload = None

    if args.type == "failure" and args.report:
        summary = parse_semgrep_report(args.report)
        if args.platform == "slack":
            payload = build_slack_payload(summary, alert_type="failure")
        else:
            payload = build_discord_payload(summary, alert_type="failure")
    elif args.type == "success":
        if args.platform == "slack":
            payload = build_slack_payload({}, alert_type="success")
        else:
            payload = build_discord_payload({}, alert_type="success")

    if payload:
        success = send_webhook(args.webhook_url, payload)
        if success:
            print("Bildirim basariyla gonderildi.")
        else:
            print("Bildirim gonderilemedi, ancak pipeline devam ediyor.")
    else:
        print("Olusturulacak bildirim bulunamadi.")


if __name__ == "__main__":
    main()
