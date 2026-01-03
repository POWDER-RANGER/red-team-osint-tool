from __future__ import annotations

import argparse
import logging
import time
from dataclasses import asdict
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

from .config import load_config, Config
from .db import DB
from .utils.logging import setup_logging
from .utils.text import find_matches, make_snippet
from .utils.redact import redact_text
from .enrich.hashing import sha256_text
from .enrich.whois_dns import extract_domain, dns_lookup, whois_lookup
from .enrich.ioc import extract_iocs
from .enrich.diff import compute_diff
from .sources import RssSource, HttpPageSource, OnionAllowlistSource
from .scheduler import JobRunner
from .alerts import send_webhook, send_email

console = Console()
log = logging.getLogger("osinttool")


def _alert(alerts_cfg: Dict[str, Any], event: Dict[str, Any]) -> None:
    """Dispatch alerts via webhook and email if configured."""
    webhook_cfg = alerts_cfg.get("webhook", {}) or {}
    if webhook_cfg.get("enabled") and webhook_cfg.get("url"):
        try:
            send_webhook(webhook_cfg["url"], event)
        except Exception as e:
            log.warning(f"Webhook alert failed: {e}")
    smtp_cfg = alerts_cfg.get("smtp", {}) or {}
    if smtp_cfg.get("enabled"):
        try:
            send_email(
                host=smtp_cfg["host"],
                port=int(smtp_cfg.get("port", 587)),
                username=smtp_cfg["username"],
                password=smtp_cfg["password"],
                from_addr=smtp_cfg["from_addr"],
                to_addrs=list(smtp_cfg.get("to_addrs", [])),
                subject=f"[OSINT HIT] {event.get('source')} :: {event.get('title') or event.get('origin')}",
                body=str(event),
            )
        except Exception as e:
            log.warning(f"SMTP alert failed: {e}")


def _process_source(db: DB, cfg: Config, source_obj) -> None:
    """Fetch items from a source, analyze, store evidence and send alerts."""
    items = list(source_obj.fetch())
    for it in items:
        # keyword and regex matches
        kw_hits, rx_hits = find_matches(it.text, cfg.matching.keywords, cfg.matching.regex)
        # compute content hash and snippet
        content_hash = sha256_text(it.text)
        snippet = make_snippet(it.text, cfg.matching.max_snippet_chars)
        # build extra metadata
        extra: Dict[str, Any] = dict(it.extra or {})
        domain = extract_domain(it.origin)
        if domain and not domain.endswith(".onion"):
            extra["dns"] = dns_lookup(domain)
            extra["whois"] = whois_lookup(domain)
        # indicator of compromise extraction
        iocs = extract_iocs(it.text)
        if iocs:
            extra["iocs"] = iocs
        # insert evidence
        inserted = db.upsert_evidence(
            source=source_obj.name,
            origin=it.origin,
            title=it.title,
            content_hash=content_hash,
            snippet=snippet,
            keywords=kw_hits,
            regexes=rx_hits,
            extra=extra,
        )
        if inserted:
            log.info(f"NEW: {source_obj.name} :: {it.origin}")
        # send alert if any match or ioc
        if kw_hits or rx_hits or iocs:
            event = {
                "source": source_obj.name,
                "origin": it.origin,
                "title": it.title,
                "keywords": kw_hits,
                "regexes": rx_hits,
                "iocs": iocs,
                "snippet": redact_text(snippet),
            }
            _alert(asdict(cfg.alerts), event)
            log.warning(
                f"HIT: {source_obj.name} :: {it.origin} :: kw={kw_hits} rx={len(rx_hits)} ioc={bool(iocs)}"
            )


def run_once(config_path: str) -> None:
    """Run all sources once and exit."""
    cfg = load_config(config_path)
    setup_logging(cfg.app.log_level)
    db = DB(cfg.app.db_path)
    # build sources
    sources: List[Any] = []
    for entry in cfg.sources.get("rss", []) or []:
        sources.append(RssSource(entry["name"], entry["url"]))
    for entry in cfg.sources.get("http", []) or []:
        sources.append(HttpPageSource(entry["name"], entry["url"]))
    onion_cfg = cfg.sources.get("onion_allowlist", {}) or {}
    tor = onion_cfg.get("tor_socks5", "socks5h://127.0.0.1:9050")
    renew = bool(onion_cfg.get("renew_circuit", False))
    ctrl_port = int(onion_cfg.get("tor_control_port", 9051))
    for entry in onion_cfg.get("targets", []) or []:
        sources.append(OnionAllowlistSource(entry["name"], entry["url"], tor, ctrl_port, renew))
    for s in sources:
        _process_source(db, cfg, s)


def run_daemon(config_path: str) -> None:
    """Run all sources at configured intervals until interrupted."""
    cfg = load_config(config_path)
    setup_logging(cfg.app.log_level)
    db = DB(cfg.app.db_path)
    runner = JobRunner()
    # schedule rss
    for entry in cfg.sources.get("rss", []) or []:
        src = RssSource(entry["name"], entry["url"])
        interval = int(entry.get("interval_seconds", 1800))
        runner.add_interval_job(lambda s=src: _process_source(db, cfg, s), interval, f"rss:{src.name}")
    # schedule http
    for entry in cfg.sources.get("http", []) or []:
        src = HttpPageSource(entry["name"], entry["url"])
        interval = int(entry.get("interval_seconds", 3600))
        runner.add_interval_job(lambda s=src: _process_source(db, cfg, s), interval, f"http:{src.name}")
    # schedule onion allowlist
    onion_cfg = cfg.sources.get("onion_allowlist", {}) or {}
    tor = onion_cfg.get("tor_socks5", "socks5h://127.0.0.1:9050")
    renew = bool(onion_cfg.get("renew_circuit", False))
    ctrl_port = int(onion_cfg.get("tor_control_port", 9051))
    for entry in onion_cfg.get("targets", []) or []:
        src = OnionAllowlistSource(entry["name"], entry["url"], tor, ctrl_port, renew)
        interval = int(entry.get("interval_seconds", 3600))
        runner.add_interval_job(lambda s=src: _process_source(db, cfg, s), interval, f"onion:{src.name}")
    runner.start()
    console.print("[bold green]OSINT daemon running. Press Ctrl+C to stop.[/bold green]")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        runner.shutdown()


def show_recent(db_path: str, limit: int = 25) -> None:
    """Display a table of the most recent evidence records."""
    from sqlalchemy import desc
    from .db import Evidence
    db = DB(db_path)
    with db.Session() as s:
        rows = s.query(Evidence).order_by(desc(Evidence.observed_at)).limit(int(limit)).all()
    table = Table(title=f"Recent Evidence (limit={limit})")
    table.add_column("When", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Title/Origin", overflow="fold")
    table.add_column("Hits", style="yellow")
    for r in rows:
        hits: List[str] = []
        if r.keywords:
            hits.append(f"kw:{len(r.keywords)}")
        if r.regexes:
            hits.append(f"rx:{len(r.regexes)}")
        extra = r.extra or {}
        if extra.get("iocs"):
            hits.append(f"ioc:{len(extra['iocs'])}")
        table.add_row(
            str(r.observed_at).replace("+00:00", "Z"),
            r.source,
            (r.title or r.origin)[:160],
            " ".join(hits) or "-",
        )
    console.print(table)
