# 🔍 Red Team OSINT Tool

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Policy](https://img.shields.io/badge/Security-Policy-red.svg)](https://github.com/POWDER-RANGER/red-team-osint-tool/security/policy)

> **Advanced Intelligence Gathering Framework for Authorized Security Assessments**

A Python-based red-team OSINT (Open Source Intelligence) tool designed for **authorized security assessments** and reconnaissance pipelines. Built with modularity, automation, and comprehensive threat surface mapping in mind.

---

## 🎉 Intent Routing Matrix

| Use Case | Module | Output | Time |
|----------|--------|--------|------|
| Domain reconnaissance | `whois_profiler` | Registrant, DNS records, ASN data | ~2s |
| Email discovery | `email_harvester` | Valid addresses, metadata | ~15s |
| Subdomain enumeration | `subdomain_scanner` | Active subdomains, IP ranges | ~30s |
| Web scraping & content analysis | `web_crawler` | Tech stack, metadata, vulnerabilities | ~60s |
| Social engineering intel | `social_profiler` | Public profiles, linked accounts, connections | ~45s |
| Dark web monitoring | `dark_monitor` | Mentions, leaks, threat intel | ~120s |
| Threat synthesis & reporting | `report_generator` | Executive summary, risk scores, actionable intel | ~10s |

---

## 📋 Sample Assessment Report Output

```
╔════════════════════════════════════════════════════════════════════════╗
║           RED TEAM OSINT ASSESSMENT REPORT                             ║
║           Target: example-corp.com                                     ║
║           Assessment Date: 2026-02-24                                  ║
║           Authorization: Verified (signed contract on file)            ║
╚════════════════════════════════════════════════════════════════════════╝

─ EXECUTIVE SUMMARY ─────────────────────────────────────────────────────

Identified 47 information disclosure points across web properties and
public sources. Risk elevation: MEDIUM. 12 remediation actions recommended.

─ DOMAIN INTELLIGENCE ───────────────────────────────────────────────────

Registrant:      REDACTED (privacy service active)
Domain Age:      8 years
Nameservers:     4 (AWS Route53)
MX Records:      3 (Microsoft 365 configured)
DNSSEC:          ✓ Enabled
WHOIS Privacy:   ✓ Protected
ASN:             AS16509 (Amazon Web Services)

─ WEB FINGERPRINTING ────────────────────────────────────────────────────

Server:          Apache/2.4.48 (Ubuntu)
Python Framework: Django 3.2.5
Frontend:        React 17.0.2
CDN:             CloudFlare (Pro tier)
CMS Detected:    WordPress 5.9.1 (outdated)
Plugins Exposed: 23 (6 with known CVEs)

Vulnerabilities Found:
  • CVE-2021-39195 (WP Plugin: Slider Revolution) - CRITICAL
  • CVE-2022-0897  (WP Plugin: Insert Headers/Footers) - HIGH
  • Publicly exposed .git directory - HIGH
  • Backup files indexed by Google - MEDIUM

─ EMAIL INTELLIGENCE ────────────────────────────────────────────────────

Valid Addresses Found:  18
Executive Accounts:     5
  • cto@example-corp.com (LinkedIn: confirmed)
  • engineering-lead@example-corp.com (GitHub: active)
  • security@example-corp.com (responds to emails)

Compromised in Breaches: 3 addresses (Have I Been Pwned)

─ SOCIAL ENGINEERING VECTORS ────────────────────────────────────────────

LinkedIn Profiles:     34 employees identified
GitHub Public Repos:   8 (exposed API keys in 2 repos)
Twitter Accounts:      4 official accounts + 12 employee accounts
Public Slack History:  Exposed via Google Cache (fixed)
Job Postings (Stack): Technical requirements reveal tech stack details

─ DARK WEB & THREAT INTEL ───────────────────────────────────────────────

Mentions:        4 credible sources
Data Breaches:   Company email addresses in 2 paste sites (2021, 2023)
Phishing Threats: 2 active phishing sites mimicking login portal
Ransom Mentions: None detected
Forum Activity:  Hackers discussing vulnerabilities in private forums

─ REMEDIATION CHECKLIST ─────────────────────────────────────────────────

[ ] Update WordPress to latest version (5.9.2)
[ ] Remove/disable 6 vulnerable plugins
[ ] Remove publicly exposed .git repository
[ ] Implement robots.txt to block sensitive paths
[ ] Enable rate limiting on email discovery endpoints
[ ] Rotate potentially compromised employee credentials
[ ] Enable multi-factor authentication for AWS/Microsoft 365
[ ] Configure SIEM alerts for external reconnaissance activity
[ ] Conduct security awareness training (social engineering)
[ ] Review and restrict GitHub secret access

═══════════════════════════════════════════════════════════════════════════
```

---

## 🛡️ Capability Matrix

| Capability | Scope | Access Gate | Status |
|------------|-------|-------------|--------|
| Whois Profiling | Domain & ASN data | **REQUIRED** | ✓ Production |
| Email Enumeration | Company & personal | **REQUIRED** | ✓ Production |
| Subdomain Discovery | DNS records | **REQUIRED** | ✓ Production |
| Web Content Scraping | Public sites | **REQUIRED** | ✓ Production |
| Social Media Analysis | Public profiles only | **REQUIRED** | ✓ Production |
| Dark Web Monitoring | Paste sites, forums | **REQUIRED** | ✓ Production |
| Report Generation | Assessment synthesis | **REQUIRED** | ✓ Production |

---

## 🔐 Authorization Gate

**CRITICAL**: This tool is designed exclusively for authorized security assessments.

```python
from osint_tool import AuthorizedAssessment

# Initialize with authorization verification
assessment = AuthorizedAssessment(
    target="example.com",
    client_name="ABC Corporation",
    contract_path="./contracts/signed_engagement_2026.pdf",
    scope="web properties, DNS, social media",
    authorized_personnel=["john.doe@redteam.io", "jane.smith@redteam.io"],
    assessment_date="2026-02-24"
)

# Authorization is VERIFIED before any modules execute
if not assessment.verify_authorization():
    raise PermissionError("Engagement not authorized. Aborting.")

# Run assessment
report = assessment.execute_full_scan()
print(report.to_markdown())
```

All modules check this gate before execution. No bypasses.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/POWDER-RANGER/red-team-osint-tool.git
cd red-team-osint-tool
pip install -r requirements.txt
```

### Basic Usage

```bash
python osint_tool.py --target example.com --scope full --contract ./engagement.pdf
```

### With Authorization File

```bash
python osint_tool.py \
  --target example.com \
  --client "ABC Corporation" \
  --contract ./signed_engagement.pdf \
  --authorized-users "john@redteam.io" "jane@redteam.io" \
  --scope "domain,email,web,social" \
  --output ./reports/example-com-assessment.md
```

---

## 📄 License

MIT License - [LICENSE](./LICENSE)

---

## 📢 Legal & Compliance Notice

**AUTHORIZATION REQUIRED**: This tool is designed exclusively for authorized security assessments conducted under signed engagement agreements. Unauthorized use against systems you do not own or have explicit written permission to test is illegal.

Users are solely responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/POWDER-RANGER/red-team-osint-tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/POWDER-RANGER/red-team-osint-tool/discussions)
