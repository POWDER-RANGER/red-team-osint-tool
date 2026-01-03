from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
import os
import re
import yaml

# Pattern for environment variable placeholders like ${VAR}
_ENV_RX = re.compile(r"^\$\{([A-Z0-9_]+)\}$")

def _resolve_env(value: Any) -> Any:
    """Resolve ${VAR} placeholders to environment values."""
    if isinstance(value, str):
        m = _ENV_RX.match(value.strip())
        if m:
            return os.getenv(m.group(1), "")
    return value

@dataclass
class AppConfig:
    db_path: str
    log_level: str

@dataclass
class MatchingConfig:
    keywords: List[str]
    regex: List[str]
    max_snippet_chars: int

@dataclass
class AlertsConfig:
    webhook: Dict[str, Any]
    smtp: Dict[str, Any]

@dataclass
class Config:
    app: AppConfig
    matching: MatchingConfig
    sources: Dict[str, Any]
    alerts: AlertsConfig

def load_config(path: str) -> Config:
    """Load configuration from a YAML file and resolve environment variables."""
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    def resolve(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: resolve(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [resolve(x) for x in obj]
        return _resolve_env(obj)

    app_cfg = raw.get("app", {})
    matching_cfg = raw.get("matching", {})
    alerts_cfg = raw.get("alerts", {})

    alerts_resolved = resolve(alerts_cfg)

    return Config(
        app=AppConfig(
            db_path=app_cfg.get("db_path", "evidence.sqlite"),
            log_level=app_cfg.get("log_level", "INFO"),
        ),
        matching=MatchingConfig(
            keywords=matching_cfg.get("keywords", []) or [],
            regex=matching_cfg.get("regex", []) or [],
            max_snippet_chars=int(matching_cfg.get("max_snippet_chars", 280)),
        ),
        sources=raw.get("sources", {}) or {},
        alerts=AlertsConfig(
            webhook=alerts_resolved.get("webhook", {}) or {},
            smtp=alerts_resolved.get("smtp", {}) or {},
        ),
    )
