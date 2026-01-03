# red-team-osint-tool

A Python-based red-team OSINT framework with automation and dark web monitoring capabilities. Built for security researchers conducting authorized reconnaissance operations.

## Features

- **Multi-Source Intelligence Gathering**
  - RSS feed monitoring (security blogs, threat intel feeds)
  - HTTP endpoint scraping with rate limiting
  - Tor/onion service monitoring with circuit renewal
  
- **Automated Enrichment**
  - IOC extraction (IPs, domains, URLs, emails, hashes)
  - Content hashing (SHA-256) for change detection
  - Diff computation for monitoring content modifications
  - DNS and WHOIS lookups for infrastructure intelligence

- **Tamper-Evident Evidence Storage**
  - SQLite database with hash-chained evidence records
  - Cryptographic integrity verification
  - Full content and metadata archival

- **Flexible Alerting**
  - Webhook notifications (Slack, Discord, custom endpoints)
  - SMTP email alerts with configurable recipients
  - Keyword and regex-based matching rules

- **Operational Security**
  - Environment variable substitution for secrets
  - Request rate limiting to avoid detection
  - Tor integration for anonymized monitoring
  - Sensitive data redaction in logs

## Installation

```bash
git clone https://github.com/POWDER-RANGER/red-team-osint-tool.git
cd red-team-osint-tool
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Edit `config.yml` to customize your monitoring setup:

### Basic Settings

```yaml
app:
  db_path: "evidence.sqlite"
  log_level: "INFO"
```

### Matching Rules

Define keywords and regex patterns to detect in collected content:

```yaml
matching:
  keywords:
    - "yourcompany"
    - "credential"
    - "api key"
  regex:
    - "(?i)password\\s*[:=]"
    - "(?i)api[_-]?key\\s*[:=]"
    - "(?i)leak(ed)?\\b"
  max_snippet_chars: 280
```

### Data Sources

**RSS Feeds:**
```yaml
sources:
  rss:
    - name: "KrebsOnSecurity"
      url: "https://krebsonsecurity.com/feed/"
      interval_seconds: 1800
```

**HTTP Endpoints:**
```yaml
  http:
    - name: "ExampleBlog"
      url: "https://example.com/security"
      interval_seconds: 3600
```

**Tor Onion Services:**
```yaml
  onion_allowlist:
    tor_socks5: "socks5h://127.0.0.1:9050"
    targets:
      - name: "OnionStatusPage"
        url: "http://exampleonionaddressonion.onion/"
        interval_seconds: 3600
```

### Alerting

**Webhook (Slack/Discord):**
```yaml
alerts:
  webhook:
    enabled: true
    url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**SMTP Email:**
```yaml
  smtp:
    enabled: true
    host: "smtp.example.com"
    port: 587
    username: "user@example.com"
    password: "${SMTP_PASSWORD}"  # Use environment variable
    from_addr: "osint@example.com"
    to_addrs:
      - "security@example.com"
```

**Environment Variables:**  
Use `${VARIABLE_NAME}` syntax in config.yml for secrets:
```bash
export SMTP_PASSWORD="your-secure-password"
```

## Usage

### One-Time Scan
Run all configured sources once and exit:
```bash
python run.py once
```

### Continuous Monitoring Daemon
Run sources on scheduled intervals:
```bash
python run.py daemon
```

### View Recent Evidence
Display recent collected items from the database:
```bash
python run.py recent --limit 50
```

### Custom Configuration File
```bash
python run.py --config custom-config.yml once
```

## Tor Setup

For monitoring .onion services:

1. **Install Tor:**
   - Linux: `sudo apt-get install tor`
   - macOS: `brew install tor`
   - Windows: Download [Tor Browser Bundle](https://www.torproject.org/download/)

2. **Start Tor Service:**
   ```bash
   tor  # Default SOCKS5 proxy: 127.0.0.1:9050
   ```

3. **Configure in config.yml:**
   ```yaml
   onion_allowlist:
     tor_socks5: "socks5h://127.0.0.1:9050"
   ```

## Architecture

```
osinttool/
├── sources/       # Data collection modules (RSS, HTTP, onion)
├── enrich/        # Content enrichment (IOC, hashing, diff, WHOIS)
├── alerts/        # Notification handlers (webhook, SMTP)
├── utils/         # Utilities (logging, rate limiting, redaction)
├── config.py      # YAML config loader with env var resolution
├── db.py          # SQLite with tamper-evident hash chain
├── scheduler.py   # APScheduler job runner
└── cli.py         # CLI commands (once, daemon, recent)
```

## Security & Legal Notice

**This tool is intended for authorized security research and reconnaissance only.**

- Only monitor systems and data you have explicit permission to access
- Respect robots.txt and website terms of service
- Comply with all applicable laws and regulations
- Use Tor responsibly and ethically
- Do not use for unauthorized access, data theft, or malicious purposes

The authors assume no liability for misuse of this tool.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please:
- Open an issue to discuss major changes
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed

## Troubleshooting

**Import errors after installation:**
```bash
# Ensure all dependencies installed
pip install -r requirements.txt --upgrade
```

**Tor connection failures:**
```bash
# Verify Tor is running
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org
```

**Permission denied errors:**
```bash
# Check file permissions
chmod +x run.py
```

## Roadmap

- [ ] Diff-based change detection with configurable thresholds
- [ ] Rule pack system for automated triage
- [ ] Config validation with pydantic schemas
- [ ] Health checks and self-monitoring
- [ ] Additional source types (Twitter/X API, Pastebin, GitHub)
- [ ] Export formats (JSON, CSV, MISP)

---

**For questions or issues, please open a GitHub issue.**
