from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import hashlib
import json

from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Text, JSON, UniqueConstraint, Index
)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True)
    source = Column(String(128), nullable=False)
    origin = Column(String(2048), nullable=False)
    title = Column(String(512), nullable=True)
    observed_at = Column(DateTime(timezone=True), nullable=False)
    content_hash = Column(String(128), nullable=False)
    snippet = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)
    regexes = Column(JSON, nullable=True)
    extra = Column(JSON, nullable=True)
    prev_hash = Column(String(64), nullable=True)
    evidence_hash = Column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint("source", "origin", "content_hash", name="uq_source_origin_hash"),
        Index("ix_evidence_observed_at", "observed_at"),
        Index("ix_evidence_source", "source"),
        Index("ix_evidence_origin", "origin"),
    )

class ContentHistory(Base):
    __tablename__ = "content_history"
    id = Column(Integer, primary_key=True)
    source = Column(String(128), nullable=False)
    origin = Column(String(2048), nullable=False)
    observed_at = Column(DateTime(timezone=True), nullable=False)
    content_hash = Column(String(128), nullable=False)
    content_text = Column(Text, nullable=False)

    __table_args__ = (
        Index("ix_hist_source_origin", "source", "origin"),
        Index("ix_hist_observed_at", "observed_at"),
    )


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj or {}, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_evidence_hash(
    *,
    source: str,
    origin: str,
    title: Optional[str],
    observed_at_iso: str,
    content_hash: str,
    prev_hash: Optional[str],
    snippet: Optional[str],
    keywords: List[str],
    regexes: List[str],
    extra: Dict[str, Any],
) -> str:
    payload = {
        "v": 1,
        "source": source,
        "origin": origin,
        "title": title,
        "observed_at": observed_at_iso,
        "content_hash": content_hash,
        "prev_hash": prev_hash,
        "snippet": snippet,
        "keywords": keywords or [],
        "regexes": regexes or [],
        "extra": extra or {},
    }
    blob = _canonical_json(payload).encode("utf-8", errors="replace")
    return hashlib.sha256(blob).hexdigest()


@dataclass
class DB:
    db_path: str

    def __post_init__(self) -> None:
        self.engine = create_engine(f"sqlite:///{self.db_path}", future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)

    def upsert_evidence(
        self,
        *,
        source: str,
        origin: str,
        title: Optional[str],
        content_hash: str,
        snippet: Optional[str],
        keywords: List[str],
        regexes: List[str],
        extra: Optional[Dict[str, Any]] = None,
        content_text: Optional[str] = None,
    ) -> bool:
        now = datetime.now(timezone.utc)
        observed_iso = now.isoformat()
        with self.Session() as s:
            exists = s.query(Evidence).filter(
                Evidence.source == source,
                Evidence.origin == origin,
                Evidence.content_hash == content_hash,
            ).first()
            if exists:
                return False

            last = s.query(Evidence.evidence_hash).order_by(Evidence.id.desc()).first()
            prev_hash = last[0] if last else None

            ev = Evidence(
                source=source,
                origin=origin,
                title=title,
                observed_at=now,
                content_hash=content_hash,
                snippet=snippet,
                keywords=keywords,
                regexes=regexes,
                extra=extra or {},
                prev_hash=prev_hash,
                evidence_hash=compute_evidence_hash(
                    source=source,
                    origin=origin,
                    title=title,
                    observed_at_iso=observed_iso,
                    content_hash=content_hash,
                    prev_hash=prev_hash,
                    snippet=snippet,
                    keywords=keywords,
                    regexes=regexes,
                    extra=extra or {},
                ),
            )
            s.add(ev)

            if content_text is not None:
                hist = ContentHistory(
                    source=source,
                    origin=origin,
                    observed_at=now,
                    content_hash=content_hash,
                    content_text=content_text,
                )
                s.add(hist)

            s.commit()
            return True
