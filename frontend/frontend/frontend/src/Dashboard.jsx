import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Dashboard.css";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5000/api";

function Dashboard() {
  const [stats, setStats] = useState({});
  const [sources, setSources] = useState([]);
  const [evidence, setEvidence] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [search, setSearch] = useState("");
  const [activeTab, setActiveTab] = useState("evidence");

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(false);
        
        const [statsRes, sourcesRes, evidenceRes, alertsRes] = await Promise.all([
          axios.get(`${API_BASE}/stats`),
          axios.get(`${API_BASE}/sources`),
          axios.get(`${API_BASE}/evidence?search=${search}`),
          axios.get(`${API_BASE}/alerts`),
        ]);
        
        setStats(statsRes.data);
        setSources(sourcesRes.data);
        setEvidence(evidenceRes.data);
        setAlerts(alertsRes.data);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, [search]);

  const getSeverityColor = (severity) => {
    const colors = {
      critical: "#dc2626",
      high: "#ea580c",
      medium: "#f59e0b",
      low: "#10b981",
      info: "#6b7280"
    };
    return colors[severity] || colors.info;
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🔍 OSINT Intelligence Dashboard</h1>
        <div className="header-status">
          {error && <span className="status-badge error">⚠️ Connection Error</span>}
          {loading && <span className="status-badge loading">⟳ Loading...</span>}
          {!loading && !error && <span className="status-badge success">✓ Connected</span>}
        </div>
      </header>

      <section className="stats-grid">
        <div className="stat-card">
          <h3>Total Evidence</h3>
          <p className="stat-value">{stats.total_evidence || 0}</p>
        </div>
        <div className="stat-card">
          <h3>High Severity</h3>
          <p className="stat-value critical">{stats.high_severity_count || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Active Sources</h3>
          <p className="stat-value">{stats.active_sources || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Recent Activity (24h)</h3>
          <p className="stat-value">{stats.recent_activity || 0}</p>
        </div>
      </section>

      <div className="tabs">
        <button
          className={activeTab === "evidence" ? "tab active" : "tab"}
          onClick={() => setActiveTab("evidence")}
        >
          Evidence ({evidence.length})
        </button>
        <button
          className={activeTab === "sources" ? "tab active" : "tab"}
          onClick={() => setActiveTab("sources")}
        >
          Sources ({sources.length})
        </button>
        <button
          className={activeTab === "alerts" ? "tab active" : "tab"}
          onClick={() => setActiveTab("alerts")}
        >
          Alerts ({alerts.length})
        </button>
      </div>

      {activeTab === "evidence" && (
        <section className="evidence-section">
          <div className="search-bar">
            <input
              type="text"
              placeholder="🔎 Search evidence..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="evidence-list">
            {evidence.map((item) => (
              <div key={item.id} className="evidence-card">
                <div className="evidence-header">
                  <h4>{item.title}</h4>
                  <span
                    className="severity-badge"
                    style={{ backgroundColor: getSeverityColor(item.severity) }}
                  >
                    {item.severity.toUpperCase()}
                  </span>
                </div>
                <p className="evidence-snippet">{item.snippet || "No preview available"}</p>
                <div className="evidence-meta">
                  <span>📡 {item.source}</span>
                  <span>🔗 {item.origin}</span>
                  <span>🕒 {new Date(item.observed_at).toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {activeTab === "sources" && (
        <section className="sources-section">
          <div className="sources-list">
            {sources.map((source, idx) => (
              <div key={idx} className="source-card">
                <h4>{source.name}</h4>
                <div className="source-info">
                  <span className={`status-dot ${source.status}`}></span>
                  <span>{source.status}</span>
                  <span>Evidence: {source.evidence_count}</span>
                  {source.last_run && (
                    <span>Last Run: {new Date(source.last_run).toLocaleString()}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {activeTab === "alerts" && (
        <section className="alerts-section">
          <div className="alerts-list">
            {alerts.map((alert) => (
              <div key={alert.id} className="alert-card">
                <div className="alert-header">
                  <span
                    className="severity-badge"
                    style={{ backgroundColor: getSeverityColor(alert.severity) }}
                  >
                    {alert.severity.toUpperCase()}
                  </span>
                  <span className="alert-time">
                    {new Date(alert.
