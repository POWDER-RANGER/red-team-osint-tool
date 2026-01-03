
# 🌪️ **VORTEX** <span style="background: linear-gradient(135deg, #0ea5e9 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">Enterprise Red Team OSINT</span>

<div align="center">
<img src="https://user-gen-media-assets.s3.amazonaws.com/seedream_images/302b35bc-b0df-4432-a992-50029f017db0.png" alt="VORTEX Dashboard" width="100%" style="border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); margin: 2rem 0; max-width: 1200px;">
</div>

**Built like a weapon. Monitors like a predator. Evidence you can actually use in court.**

[![Feature Matrix](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/6e301f4effeea55d6bd9d50f20b5cdd2/a6f082f9-c449-4964-8b7d-f41207dc88a7/f9380c3a.png)](https://github.com/POWDER-RANGER/vortex)

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

## ⚡ **Weaponized Intelligence Platform**

| **Capability** | **Status** | **Detail** |
|---|---|---|
| 🔍 **Multi-Vector Harvest** | ✅ **Native** | RSS + HTTP + **Tor Onion** |
| 🛡️ **Tamper-Evident Vault** | ✅ **Native** | Hash-chained SQLite evidence |
| 🔔 **Instant Alerts** | ✅ **Native** | Slack/Discord/Teams/SMTP |
| 🕵️ **Dark Web Ready** | ✅ **Native** | SOCKS5 + circuit rotation |
| 🔒 **OPSEC Hardened** | ✅ **Native** | Env vars + rate limits + log redaction |

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

## ⚙️ **Configuration (Production Ready)**

<div style="background: #0f172a; border-radius: 16px; padding: 2rem; border: 1px solid #334155; margin: 2rem 0; font-family: 'SF Mono', monospace;">

```yaml
matching:
  keywords: ["yourcompany", "credential", "api key"]
  regex: ["(?i)password[:=]", "(?i)leak\\b"]

sources:
  rss:
    - name: "Krebs"
      url: "https://krebsonsecurity.com/feed/"
  onion:
    tor_socks5: "socks5h://127.0.0.1:9050"
    targets:
      - name: "PasteSite"
        url: "http://pastesite.onion/"

alerts:
  webhook: "${SLACK_WEBHOOK}"
  smtp:
    username: "${SMTP_USER}"
    password: "${SMTP_PASSWORD}"
```

</div>

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
|---|---|
| `python run.py daemon` | **Live monitoring** (the real weapon) |
| `python run.py once` | One-time intelligence harvest |
| `python run.py recent --limit 25` | **Latest hits** from your vault |
| `python run.py test-source krebs` | Validate individual source |

---

## 🏗️ **Battle-Tested Architecture**

```
vortex/
├── sources/     # RSS, HTTP, Onion 🕸️
├── storage/     # Hash-chained SQLite 🔗
├── alerts/      # Slack/Email webhooks 📱
├── opsec/       # Tor + rate limits 🛡️
└── cli.py       # Your command center 🎯
```

---

## ⚖️ **Legal & Responsible Disclosure**

<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-left: 4px solid #ef4444; padding: 1.5rem; border-radius: 12px; margin: 2rem 0;">

**🔴 PROFESSIONAL TOOL FOR AUTHORIZED OPERATIONS ONLY**

✅ **Legal:** Red team assessments, threat hunting, attack surface monitoring  
❌ **Illegal:** Unauthorized access, competitor intel, personal data harvesting

**Operators assume full legal responsibility.**

</div>

---

## 📈 **Production Roadmap**

| **Phase** | **Feature** | **Status** |
|---|---|---|
| Q1 2026 | Multi-source + alerting | ✅ **LIVE** |
| Q2 2026 | ML triage + rule packs | 🔄 **Building** |
| Q3 2026 | MISP/ThreatConnect export | 🔵 **Planned** |

---

<div align="center" style="margin: 4rem 0; padding: 3rem; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 24px; border: 1px solid #334155;">

<h2 style="font-family: 'Orbitron', monospace; background: linear-gradient(135deg, #0ea5e9 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 900; margin-bottom: 1rem;">🚀 DEPLOY VORTEX NOW</h2>

```bash
git clone https://github.com/POWDER-RANGER/vortex.git
cd vortex && pip install -r requirements.txt
python run.py daemon
```

**Your intel flows in 90 seconds.**

<a href="https://github.com/POWDER-RANGER/vortex" style="display: inline-block; background: linear-gradient(135deg, #0ea5e9 0%, #ec4899 100%); color: white; padding: 1rem 2.5rem; border-radius: 50px; font-weight: 700; font-size: 1.2rem; text-decoration: none; box-shadow: 0 10px 30px rgba(14, 165, 233, 0.4); transition: all 0.3s ease;">
⭐ Star on GitHub
</a>

</div>

<div align="center" style="color: #64748b; font-size: 0.9rem; margin-top: 3rem;">
**VORTEX: Because real operators don't use toy scanners.**<br>
MIT License | January 2026 | Built by operators, for operators
</div>
