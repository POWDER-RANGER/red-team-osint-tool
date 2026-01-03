-- schema.sql - OSINT Database Schema
-- Creates tables for sources, evidence, and alerts with integrity constraints

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK(type IN ('rss', 'http', 'tor', 'dns', 'whois', 'ct_log', 'twitter', 'telegram')),
    url TEXT,
    status TEXT DEFAULT 'idle' CHECK(status IN ('idle', 'active', 'error', 'disabled')),
    last_run TIMESTAMP,
    last_success TIMESTAMP,
    error_count INTEGER DEFAULT 0,
    config_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT,
    severity TEXT DEFAULT 'info' CHECK(severity IN ('info', 'low', 'medium', 'high', 'critical')),
    matched BOOLEAN DEFAULT 0,
    iocs_json TEXT,  -- JSON array of indicators: IPs, domains, hashes, emails
    tags_json TEXT,  -- JSON array of tags/categories
    hash TEXT UNIQUE,  -- SHA256 of content for deduplication
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id INTEGER NOT NULL,
    channel TEXT NOT NULL CHECK(channel IN ('webhook', 'email', 'sms', 'discord', 'slack')),
    recipient TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'sent', 'failed')),
    error_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evidence_id) REFERENCES evidence(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_evidence_timestamp ON evidence(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_evidence_severity ON evidence(severity);
CREATE INDEX IF NOT EXISTS idx_evidence_matched ON evidence(matched);
CREATE INDEX IF NOT EXISTS idx_evidence_source ON evidence(source_id);
CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);

-- Views for dashboard queries
CREATE VIEW IF NOT EXISTS recent_critical AS
SELECT e.*, s.name as source_name
FROM evidence e
JOIN sources s ON e.source_id = s.id
WHERE e.severity IN ('high', 'critical')
ORDER BY e.timestamp DESC
LIMIT 50;

CREATE VIEW IF NOT EXISTS matched_evidence AS
SELECT e.*, s.name as source_name
FROM evidence e
JOIN sources s ON e.source_id = s.id
WHERE e.matched = 1
ORDER BY e.timestamp DESC
LIMIT 100;
