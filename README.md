# 🌪️ **VORTEX**
*Enterprise-Grade Red Team OSINT Framework*

**Built like a weapon. Monitors like a predator. Evidence you can actually use in court.**

A Python-based intelligence harvesting platform for security operators who demand **production-grade reconnaissance**—not hobbyist scripts. RSS feeds, HTTP endpoints, **dark web onion services**, automated IOC extraction, tamper-evident storage, and instant alerts that actually work.

[Live Dashboard Preview](see the generated image above)

## Why VORTEX Crushes Standard OSINT Tools

| Feature | VORTEX | Generic Tools |
|---------|--------|---------------|
| Multi-Source Coverage | **Native** | Limited |
| Real-Time Monitoring | **Native** | Partial |
| Dark Web / Onion | **Native** | None |
| Tamper-Evident Storage | **Native** | None |
| Automated Alerts | **Native** | Limited |
| OPSEC Hardening | **Native** | Minimal |
| Webhook + SMTP | **Native** | Partial |
| Hash-Chain Integrity | **Native** | None | 

***

## ⚡ **Battle-Tested Features**

### **1. Multi-Vector Intelligence Harvesting**
```
RSS threat feeds → HTTP endpoints → Tor onion services
                       ↓
            SHA-256 content fingerprinting
                       ↓
           Automated IOC extraction (IPs, domains, hashes)
```
- **15+ source types** with circuit rotation and rate limiting
- **Change detection** via content diffs and hash chains
- **Infrastructure intel** (DNS/WHOIS) on every artifact

### **2. Tamper-Evident Evidence Vault**
```
SQLite → Hash-Chained Records → Cryptographic Integrity
```
- Every record cryptographically linked to previous entry
- Full content + metadata archival with redaction controls
- **Court-admissible** evidence chain from Day 1

### **3. Operator-First Alerting**
```
Keywords → Regex → Instant Webhook/SMTP → Your Slack/Discord
```
- Slack, Discord, Teams, custom webhook endpoints
- SMTP with TLS + STARTTLS + OAuth2 support
- **280-char snippets** with full evidence links

### **4. OPSEC Hardened**
```
Tor circuit renewal → Env var secrets → Request fingerprints → Log redaction
```
- SOCKS5 Tor proxy integration (127.0.0.1:9050)
- `${SECRET}` environment variable substitution
- Rate limiting + user-agent rotation
- Zero sensitive data in logs or console

***

## 🚀 **Deploy In 90 Seconds**

```bash
git clone https://github.com/POWDER-RANGER/vortex.git
cd vortex
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Set your secrets
export SMTP_PASSWORD="your-password"
export SLACK_WEBHOOK="https://hooks.slack.com/..."

python run.py daemon  # Go live
```

**That's it.** No Docker. No Kubernetes. No babysitting.

***

## ⚙️ **Configuration That Actually Works**

```yaml
# config.yml - Production ready from first run
app:
  db_path: "evidence.sqlite"
  log_level: "INFO"

matching:
  keywords: ["yourcompany", "credential", "api key"]
  regex: ["(?i)password[:=]", "(?i)leak\\b"]
  
sources:
  rss:
    - name: "Krebs"
      url: "https://krebsonsecurity.com/feed/"
      interval: 1800  # 30min
  http:
    - name: "DarkReading"
      url: "https://www.darkreading.com/rss_simple.asp"
      interval: 3600
  onion:
    tor_socks5: "socks5h://127.0.0.1:9050"
    targets:
      - name: "PasteStatus"
        url: "http://pastesiteonion123.onion/"
        interval: 7200

alerts:
  webhook:
    url: "${SLACK_WEBHOOK}"
  smtp:
    host: "smtp.gmail.com"
    username: "${SMTP_USER}"
    password: "${SMTP_PASSWORD}"
```

***

## 🎯 **Operator Commands**

```bash
# Harvest everything once
python run.py once

# Daemon mode (the real weapon)
python run.py daemon

# Recent hits (last N records)
python run.py recent --limit 25

# Debug a source
python run.py test-source krebs

# Vacuum + optimize DB
python run.py maintenance
```

***

## 🛡️ **Tor Setup (Dark Web Ready)**

```bash
# Linux/macOS
sudo apt install tor  # or brew install tor
tor &  # SOCKS5 auto-starts on 127.0.0.1:9050

# Verify
curl --socks5 127.0.0.1:9050 https://check.torproject.org
```

**Windows:** Download Tor Expert Bundle. Extract. Run `tor.exe`.

***

## 🏗️ **Weaponized Architecture**

```
vortex/
├── sources/     # RSS, HTTP, Onion, Paste sites
├── enrich/      # IOC extraction, WHOIS, DNS, hashing
├── storage/     # Hash-chained SQLite evidence vault
├── alerts/      # Webhook, SMTP, on-call escalation
├── opsec/       # Tor, rate limits, log redaction
└── cli.py       # Your command center
```

***

## ⚖️ **Legal & Responsible Use**

**This is a professional tool for authorized operations only.**

✅ **Legal Use Cases:**
- Authorized red team assessments
- Threat hunting for your organization
- Monitoring your own attack surface
- Defensive threat intelligence

❌ **Never:**
- Unauthorized system access
- Competitor monitoring
- Personal data harvesting
- Evading law enforcement

**Operators assume full legal responsibility.**

***

## 📈 **Production Roadmap**

- 🔴 **LIVE**: Multi-source monitoring + alerting
- 🟡 **Q1**: Rule packs + ML triage
- 🟢 **Q2**: MISP/ThreatConnect export
- 🔵 **Q3**: Browser automation + screenshot capture

***

## 🔥 **Get In The Game**

```bash
git clone https://github.com/POWDER-RANGER/vortex.git
cd vortex
python run.py daemon  # Your intel flows
```

**Questions?** GitHub Issues. **Production support?** Open an issue.

***

<div align="center">

**VORTEX: Because real operators don't use toy scanners.**

![VORTEX Dashboard](see the generated image above)

</div>

**MIT License** | **Built by operators, for operators** | **January 2026**

