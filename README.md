
# 🌪️ **VORTEX** <span style="background: linear-gradient(135deg, #0ea5e9 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">Enterprise Red Team OSINT</span>

<div align="center">
<img src="https://user-gen-media-assets.s3.amazonaws.com/seedream_images/302b35bc-b0df-4432-a992-50029f017db0.png" alt="VORTEX Dashboard" width="100%" style="border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); margin: 2rem 0; max-width: 1200px;">
</div>

**Built like a weapon. Monitors like a predator. Evidence you can actually use in court.**

> **VORTEX doesn't collect data. It *harvests intel*.**

---

## 🚀 **Deploy In 90 Seconds**

```bash
git clone https://github.com/POWDER-RANGER/vortex.git
cd vortex
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export SLACK_WEBHOOK="your-webhook"
python run.py daemon  # Your intel flows live
```

**That's it.** No Docker. No Kubernetes. No babysitting.

---

## ⚡ **VORTEX vs Standard OSINT Tools**

<div align="center">

| Feature | VORTEX | Generic Tools |
|:--------|:------:|:-------------:|
| **Multi-Source Coverage** | ✅ Native | ⚠️ Limited |
| **Real-Time Monitoring** | ✅ Native | ⚠️ Partial |
| **Dark Web / Onion** | ✅ Native | ❌ None |
| **Tamper-Evident Storage** | ✅ Native | ❌ None |
| **Automated Alerts** | ✅ Native | ⚠️ Limited |
| **OPSEC Hardening** | ✅ Native | ⚠️ Minimal |
| **Webhook + SMTP** | ✅ Native | ⚠️ Partial |
| **Hash-Chain Integrity** | ✅ Native | ❌ None |

**VORTEX dominates every category.**

</div>

---

## 🎯 **Live Intelligence Flow**

```
Threat Feeds → IOC Extraction → Hash Fingerprinting → Alert Pipeline
     ↓                    ↓                    ↓                 ↓
Krebs RSS    IPs/Hashes/Domains    SHA-256 Chains    Slack + Email    ✅ COURT ADMISSIBLE
Dark Reading     ↓                    ↓                 ↓
Onion Pastes  Content Diffs    Tamper-Evident    280-char Intel
```

---

## 💎 **Battle-Tested Features**

### **🔍 Multi-Vector Intelligence Harvesting**
- **RSS threat feeds** with custom intervals
- **HTTP endpoint scraping** with rate limiting
- **Tor onion services** with circuit rotation
- **IOC extraction** (IPs, domains, hashes, emails)
- **Content fingerprinting** (SHA-256) for change detection

### **🛡️ Tamper-Evident Evidence Vault**
- Hash-chained SQLite records
- Cryptographic integrity verification
- Full content + metadata archival
- **Court-admissible** evidence chain

### **🔔 Operator-First Alerting**
- Slack, Discord, Teams webhooks
- SMTP with TLS/STARTTLS/OAuth2
- Keyword + regex matching
- 280-char intel snippets with full evidence links

### **🕵️ OPSEC Hardened**
- SOCKS5 Tor proxy integration
- Environment variable secrets (`${SECRET}`)
- Request rate limiting + fingerprint rotation
- Sensitive data redaction in logs

---

## ⚙️ **Configuration (Production Ready)**

```yaml
matching:
  keywords: ["yourcompany", "credential", "api key"]
  regex: ["(?i)password[:=]", "(?i)leak\\b"]

sources:
  rss:
    - name: "Krebs"
      url: "https://krebsonsecurity.com/feed/"
      interval_seconds: 1800
  http:
    - name: "DarkReading"
      url: "https://www.darkreading.com/rss_simple.asp"
      interval_seconds: 3600
  onion:
    tor_socks5: "socks5h://127.0.0.1:9050"
    targets:
      - name: "PasteSite"
        url: "http://pastesite.onion/"
        interval_seconds: 7200

alerts:
  webhook:
    enabled: true
    url: "${SLACK_WEBHOOK}"
  smtp:
    enabled: true
    host: "smtp.gmail.com"
    port: 587
    username: "${SMTP_USER}"
    password: "${SMTP_PASSWORD}"
    from_addr: "osint@yourcompany.com"
    to_addrs:
      - "security@yourcompany.com"
```

---

## 🛡️ **Tor Setup (Dark Web Access)**

```bash
# Linux/macOS
sudo apt install tor && tor &

# Verify connection
curl --socks5 127.0.0.1:9050 https://check.torproject.org
```

**Windows:** [Tor Expert Bundle](https://www.torproject.org/download/tor/)

---

## 🎮 **Operator Commands**

| Command | Purpose |
|---------|---------|
| `python run.py daemon` | **Live monitoring** (the real weapon) |
| `python run.py once` | One-time intelligence harvest |
| `python run.py recent --limit 25` | **Latest hits** from your vault |
| `python run.py test-source krebs` | Validate individual source |

---

## 🏗️ **Battle-Tested Architecture**

```
vortex/
├── sources/       # RSS, HTTP, Onion collectors 🕸️
├── enrich/        # IOC extraction, WHOIS, DNS, hashing 🔍
├── storage/       # Hash-chained SQLite evidence vault 🔗
├── alerts/        # Webhook, SMTP notification handlers 📱
├── opsec/         # Tor integration, rate limits, redaction 🛡️
├── scheduler.py   # APScheduler job runner ⏰
└── cli.py         # Your command center 🎯
```

---

## ⚖️ **Legal & Responsible Disclosure**

> **🔴 PROFESSIONAL TOOL FOR AUTHORIZED OPERATIONS ONLY**

✅ **Legal Use Cases:**
- Authorized red team assessments
- Threat hunting for your organization
- Monitoring your own attack surface
- Defensive threat intelligence collection

❌ **Never Use For:**
- Unauthorized system access
- Competitor monitoring
- Personal data harvesting
- Evading law enforcement

**Operators assume full legal responsibility.**

---

## 📈 **Production Roadmap**

| **Phase** | **Feature** | **Status** |
|-----------|-------------|------------|
| Q1 2026 | Multi-source + alerting + hash-chain storage | ✅ **LIVE** |
| Q2 2026 | ML triage + automated rule packs | 🔄 **Building** |
| Q3 2026 | MISP/ThreatConnect export | 🔵 **Planned** |
| Q4 2026 | Browser automation + screenshot capture | 🔵 **Planned** |

---

## 🔥 **Get In The Game**

<div align="center">

### **Deploy VORTEX in 90 seconds:**

```bash
git clone https://github.com/POWDER-RANGER/vortex.git
cd vortex && pip install -r requirements.txt
python run.py daemon
```

**Your intel flows.**

<br>

[![⭐ Star on GitHub](https://img.shields.io/badge/⭐_Star_on_GitHub-100000?style=for-the-badge&logo=github&logoColor=white&labelColor=0ea5e9&color=ec4899)](https://github.com/POWDER-RANGER/vortex)

</div>

---

<div align="center">

**VORTEX: Because real operators don't use toy scanners.**

MIT License | January 2026 | Built by operators, for operators

</div>
```

