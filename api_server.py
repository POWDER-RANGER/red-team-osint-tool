"""
Flask API Server for OSINT Tool
Provides REST endpoints for React dashboard integration
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import desc, func
from sqlalchemy.orm import sessionmaker
from osinttool.db import Evidence, ContentHistory, create_engine
import os

app = Flask(__name__)
CORS(app)

# Database configuration
DB_PATH = os.getenv("OSINT_DB_PATH", "osint.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "database": DB_PATH})

@app.route("/api/stats")
def get_stats():
    """Get dashboard statistics"""
    session = Session()
    try:
        total_evidence = session.query(func.count(Evidence.id)).scalar()
        high_severity = session.query(func.count(Evidence.id)).filter(
            Evidence.title.contains("CRITICAL") | Evidence.title.contains("HIGH")
        ).scalar()
        
        # Get unique sources
        unique_sources = session.query(func.count(func.distinct(Evidence.source))).scalar()
        
        # Recent activity (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent = session.query(func.count(Evidence.id)).filter(
            Evidence.observed_at >= yesterday
        ).scalar()
        
        return jsonify({
            "total_evidence": total_evidence or 0,
            "high_severity_count": high_severity or 0,
            "active_sources": unique_sources or 0,
            "recent_activity": recent or 0
        })
    finally:
        session.close()

@app.route("/api/sources")
def get_sources():
    """Get list of sources with their stats"""
    session = Session()
    try:
        # Group evidence by source
        source_stats = session.query(
            Evidence.source,
            func.count(Evidence.id).label('count'),
            func.max(Evidence.observed_at).label('last_run')
        ).group_by(Evidence.source).all()
        
        sources = []
        for source, count, last_run in source_stats:
            sources.append({
                "name": source,
                "type": "rss",  # You can enhance this by storing type in config
                "status": "active" if count > 0 else "idle",
                "evidence_count": count,
                "last_run": last_run.isoformat() if last_run else None
            })
        
        return jsonify(sources)
    finally:
        session.close()

@app.route("/api/evidence")
def get_evidence():
    """Get evidence with optional search and filtering"""
    session = Session()
    try:
        search = request.args.get("search", "")
        severity = request.args.get("severity", "")
        source = request.args.get("source", "")
        limit = int(request.args.get("limit", 100))
        
        query = session.query(Evidence).order_by(desc(Evidence.observed_at))
        
        if search:
            query = query.filter(
                Evidence.title.contains(search) | Evidence.snippet.contains(search)
            )
        
        if severity:
            query = query.filter(Evidence.title.contains(severity.upper()))
        
        if source:
            query = query.filter(Evidence.source == source)
        
        evidence = query.limit(limit).all()
        
        results = []
        for ev in evidence:
            results.append({
                "id": ev.id,
                "source": ev.source,
                "origin": ev.origin,
                "title": ev.title,
                "snippet": ev.snippet,
                "observed_at": ev.observed_at.isoformat() if ev.observed_at else None,
                "content_hash": ev.content_hash,
                "severity": "high" if any(kw in (ev.title or "").upper() for kw in ["CRITICAL", "HIGH", "URGENT"]) else "info"
            })
        
        return jsonify(results)
    finally:
        session.close()

@app.route("/api/evidence/<int:evidence_id>")
def get_evidence_detail(evidence_id):
    """Get detailed evidence by ID"""
    session = Session()
    try:
        ev = session.query(Evidence).filter_by(id=evidence_id).first()
        if not ev:
            return jsonify({"error": "Evidence not found"}), 404
        
        # Get content history
        history = session.query(ContentHistory).filter_by(
            source=ev.source,
            origin=ev.origin
        ).order_by(desc(ContentHistory.observed_at)).limit(5).all()
        
        return jsonify({
            "id": ev.id,
            "source": ev.source,
            "origin": ev.origin,
            "title": ev.title,
            "snippet": ev.snippet,
            "observed_at": ev.observed_at.isoformat() if ev.observed_at else None,
            "content_hash": ev.content_hash,
            "history": [
                {
                    "content_hash": h.content_hash,
                    "observed_at": h.observed_at.isoformat() if h.observed_at else None,
                    "content_text": h.content_text[:500] if h.content_text else None
                }
                for h in history
            ]
        })
    finally:
        session.close()

@app.route("/api/alerts")
def get_alerts():
    """Get recent alerts (from high-severity evidence)"""
    session = Session()
    try:
        # Get critical/high severity evidence as alerts
        alerts = session.query(Evidence).filter(
            Evidence.title.contains("CRITICAL") | Evidence.title.contains("HIGH")
        ).order_by(desc(Evidence.observed_at)).limit(50).all()
        
        results = []
        for alert in alerts:
            results.append({
                "id": alert.id,
                "message": f"High severity evidence from {alert.source}: {alert.title}",
                "severity": "critical" if "CRITICAL" in (alert.title or "") else "high",
                "timestamp": alert.observed_at.isoformat() if alert.observed_at else None,
                "source": alert.source
            })
        
        return jsonify(results)
    finally:
        session.close()

if __name__ == "__main__":
    print(f"[*] Starting OSINT API Server")
    print(f"[*] Database: {DB_PATH}")
    print(f"[*] API running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
