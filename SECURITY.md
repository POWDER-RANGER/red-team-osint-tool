# Security Policy

## 🔐 Ethical Use Declaration

This tool is designed **exclusively** for authorized security assessments, penetration testing, and Open Source Intelligence (OSINT) gathering. By using this software, you acknowledge and agree to the following terms:

### ✅ Authorized Use Cases
- Security researchers conducting **authorized** infrastructure assessments
- Red team operators with explicit **written permission** from target organizations
- Bug bounty hunters operating within program scope and rules of engagement
- System administrators assessing **their own** infrastructure
- Educational and academic research in controlled environments
- Compliance auditors performing authorized security reviews

### ⛔ Prohibited Activities
**You may NOT use this tool for:**
- Gaining unauthorized access to systems, networks, or data
- Conducting reconnaissance without explicit permission from target owners
- Violating any applicable computer fraud, privacy, or data protection laws
- Circumventing security controls without legal authorization
- Harvesting or redistributing personal data in violation of regulations
- Preparing or facilitating malicious attacks or exploitation
- Any activities that violate terms of service of third-party APIs used by this tool

### ⚖️ Legal Compliance
Users are **solely responsible** for ensuring compliance with:
- Computer Fraud and Abuse Act (CFAA) and equivalent laws in their jurisdiction
- Data protection regulations (GDPR, CCPA, PIPEDA, etc.)
- Privacy statutes and content access restrictions
- Export control regulations and international compliance frameworks
- Terms of service for all third-party APIs (Shodan, Censys, SecurityTrails, etc.)

**Unauthorized use may result in civil and/or criminal penalties.**

---

## 🚨 Responsible Disclosure Policy

We take security vulnerabilities in this tool seriously. If you discover a security issue, we appreciate your cooperation in disclosing it responsibly.

### Reporting a Vulnerability

**Contact Method:**
- **Email:** [Your security contact email - e.g., security@yourdomain.com]
- **PGP Key:** [Optional - link to your PGP public key for encrypted communications]
- **GitHub Security Advisories:** [Preferred] Use the "Security" tab to privately report vulnerabilities

**What to Include in Your Report:**
1. Detailed description of the vulnerability
2. Steps to reproduce the issue
3. Potential impact assessment (CVSS score if applicable)
4. Proof-of-concept (if available) - **non-destructive only**
5. Suggested remediation (if you have recommendations)

### Our Commitment

When you report a vulnerability, we commit to:
- **Acknowledge receipt** within 48 hours (business days)
- **Validate and triage** the report within 7 business days
- **Provide regular updates** on remediation progress (at least weekly)
- **Coordinate disclosure** with you before any public announcement
- **Credit you** in release notes (if you wish) upon resolution

### Expected Disclosure Timeline
- **Critical vulnerabilities** (RCE, credential leakage): 30-day coordinated disclosure
- **High-severity issues** (privilege escalation, data exposure): 60-day disclosure
- **Medium/Low severity**: 90-day disclosure

We may request an extension if remediation is complex. We aim for transparency throughout the process.

### Safe Harbor Provisions

**We will NOT pursue legal action** against security researchers who:
- Comply with this responsible disclosure policy
- Make good-faith efforts to avoid privacy violations and service disruptions
- Do not modify, destroy, or exfiltrate data that does not belong to them
- Provide us reasonable time to remediate before public disclosure
- Do not exploit vulnerabilities beyond what is necessary for proof-of-concept

**Legal Safe Harbor:** By adhering to this policy, researchers are authorized to conduct security research on this tool and are exempt from CFAA and similar legal claims, provided activities remain within the bounds described above.

---

## 🛡️ Operational Security (OpSec) Warnings

### Third-Party Data Sharing
**CRITICAL:** This tool sends target identifiers (domains, IPs, email addresses) to **third-party APIs** including:
- Shodan, Censys, SecurityTrails, ZoomEye (infrastructure intelligence)
- Hunter.io, HaveIBeenPwned (email/breach data)
- Twitter/X, GitHub (social media/code intelligence)
- CertSpotter, VirusTotal (certificate/reputation services)

**Implications:**
1. Target identifiers are logged by third-party services (may be retained per their policies)
2. API keys link queries to your account (attribution risk)
3. Some services may share data with law enforcement or other parties
4. Rate limiting and quotas may create operational constraints

**Mitigation Strategies:**
- Use **dedicated API accounts** for red team operations (separate from personal accounts)
- Review each service's **data retention and privacy policies**
- Consider using **VPNs or proxy infrastructure** to obscure origin
- Disable unnecessary modules via `config.yml` to minimize data sharing
- For high-sensitivity engagements, prefer **passive-only modules** (WHOIS, DNS)

### Detection Considerations
While this tool emphasizes passive OSINT, be aware:
- Large volumes of API queries may trigger anomaly detection
- DNS queries to target domains may appear in their logs
- Some APIs may notify targets of lookups (e.g., certain breach notification services)
- GitHub/social media scraping may be detectable via access logs

**Best Practices:**
- Run scans from **isolated VMs or containers** (see Dockerfile)
- Space out scans with appropriate delays (configure `network.delay` in config)
- Review engagement rules of engagement (ROE) before execution
- Maintain audit logs of when/where scans were conducted

---

## 🔧 Security Best Practices for Users

### Configuration Security
1. **NEVER commit `config.yml`** with real API keys to version control
2. Store API keys in encrypted vaults (KeePass, 1Password, HashiCorp Vault)
3. Use environment variables for keys in CI/CD pipelines (avoid plaintext)
4. Rotate API keys periodically (especially after project completion)
5. Restrict file permissions: `chmod 600 config.yml` on Unix systems

### Dependency Security
- Run `pip-audit` or `safety check` regularly to scan for vulnerable dependencies
- Keep Python packages updated (especially `requests`, `urllib3`, `pyyaml`)
- Use virtual environments to isolate dependencies: `python3 -m venv osintenv`
- Review `requirements.txt` before installation for unexpected packages

### Output Handling
- JSON reports may contain **sensitive information** (exposed emails, breach data)
- Store reports in encrypted volumes or secure file systems
- Redact sensitive data before sharing reports externally
- Securely delete reports after engagement completion: `shred -vfz osint_report_*.json`

---

## 📋 Supported Versions

| Version | Supported          | Notes                          |
| ------- | ------------------ | ------------------------------ |
| 1.x     | :white_check_mark: | Active development             |
| < 1.0   | :x:                | Beta/prototype - not supported |

We recommend always using the latest release for security fixes and feature updates.

---

## 🌍 Community Guidelines

### Contributing Security Fixes
If you'd like to contribute a security patch:
1. **DO NOT** open a public pull request for security vulnerabilities
2. Follow the Responsible Disclosure process above first
3. Once coordinated, we'll work with you on a PR with appropriate credit

### Security-Focused Contributions Welcome
We encourage pull requests that:
- Improve input validation and sanitization
- Add security-focused unit tests
- Enhance error handling and logging security
- Implement additional OpSec features (e.g., request obfuscation)

---

## 📞 Contact & Support

**Project Maintainer:** POWDER-RANGER  
**GitHub Issues:** [For non-security bugs and features only]  
**Security Contact:** [Use Security tab for vulnerability reports]  

**Acknowledgments:** We appreciate the security research community's efforts in keeping this tool safe and effective.

---

**Last Updated:** January 3, 2026  
**Policy Version:** 1.0
