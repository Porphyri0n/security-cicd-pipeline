# Self-Verifying Secure CI/CD Pipeline

[![Security Pipeline](https://github.com/SenorTacco/security-cicd-pipeline/actions/workflows/security-pipeline.yml/badge.svg)](https://github.com/SenorTacco/security-cicd-pipeline/actions/workflows/security-pipeline.yml)

> Türkçe sürüm için: [README.tr.md](README.tr.md)

A CI/CD pipeline with automated security gates that prevent developers from
shipping vulnerable code to production — and that proves its own security
rules still work on every push.

## How It Works

Whenever a developer pushes code, the following checks run on GitHub Actions:

| Job | Purpose | On Failure |
|-----|---------|------------|
| **Security Gate** | Production code (`app/secure/`) is scanned with Semgrep | Deploy is blocked + an alert is sent to Discord/Slack |
| **Rule Verification** | The intentionally vulnerable demo code (`app/vulnerable/`) is scanned to prove the rules **do** catch vulnerabilities | The rule set is considered broken and the pipeline stops |
| **Tests** | Security and integration tests run with pytest | Pipeline stops |
| **Dependency Audit** | Dependencies are checked for known CVEs with pip-audit | Pipeline stops |
| **Docker Build** | The image is built only if every check above passes | Deploy is blocked |
| **Deploy** | Runs only on the `main` branch after a successful build | - |

This way the pipeline not only protects the production code, but also
verifies on every push that its own security rules are still effective.

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/SenorTacco/security-cicd-pipeline.git
cd security-cicd-pipeline

# 2. Run the setup script
bash scripts/setup.sh

# 3. Prepare environment variables (.env is NEVER committed)
cp .env.example .env

# 4. Watch the demo
bash scripts/demo.sh
```

For detailed setup instructions (webhooks, GitHub Secrets, etc.) see the
[Setup Guide](docs/SETUP_GUIDE.md).

## Features

- **Static Analysis:** SQL injection, command injection, and hard-coded
  secret detection with Semgrep
- **Automatic Blocking:** Code with security findings cannot be deployed
- **Self-Verification:** The rule set is tested against the vulnerable demo
  code on every push
- **Dependency Security:** CVE scanning with pip-audit, automated updates
  with Dependabot
- **Instant Notifications:** Discord/Slack alerts via webhooks
- **Docker Support:** Secure containerization (non-root user, minimal image)
- **Education-Focused:** Vulnerable and secure implementations side by side
- **Custom Rules:** Project-specific Semgrep rule set with CWE references

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python/Flask | Web API (vulnerable + secure versions) |
| Docker | Containerization |
| GitHub Actions | CI/CD automation |
| Semgrep | Static application security testing (SAST) |
| pip-audit | Dependency vulnerability scanning (SCA) |
| Webhooks | Discord/Slack notifications |

## Project Structure

```
security-cicd-pipeline/
├── app/
│   ├── vulnerable/    # Intentionally vulnerable code (demo - NEVER deployed)
│   └── secure/        # Secure production code (passes the security gate)
├── semgrep/
│   ├── custom/        # Custom Semgrep rules
│   └── rules/         # Reference for the registry rule sets
├── .github/
│   ├── workflows/     # CI/CD pipeline (security gate)
│   └── dependabot.yml # Automated dependency updates
├── docker/            # Dockerfile and compose
├── notifications/     # Webhook notification system
├── tests/             # Security and integration tests
├── scripts/           # Automation scripts
└── docs/              # Documentation
```

## Important Notes

- The `app/vulnerable/` directory contains vulnerabilities **on purpose**; it
  exists to prove that the Semgrep rules work. It is excluded from the Docker
  image (`.dockerignore`) and is not part of the security gate scan.
- The `.env` file is gitignored and must never be committed; see
  `.env.example` for the template.
- The AWS keys in the vulnerable code are the official AWS documentation
  examples — they are not real credentials.

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System architecture and flow diagram
- [Setup Guide](docs/SETUP_GUIDE.md) - Step-by-step installation
- [Security Rules](docs/SECURITY_RULES.md) - Semgrep rule explanations
- [Contributing](docs/CONTRIBUTING.md) - Development guide

Note: the in-code comments and the documents above are written in Turkish.

## License

[MIT](LICENSE)
