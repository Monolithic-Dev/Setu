import { useEffect, useState } from "react";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from "recharts";
import { Activity, AlertTriangle, CheckCircle } from "lucide-react";
import "./Dashboard.css";
import { Language } from "../../i18n/strings";

interface DashboardProps {
  language: Language;
}

export function Dashboard({ }: DashboardProps) {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:3000/api/dashboard/stats")
      .then(res => res.json())
      .then(data => setStats(data.data))
      .catch(console.error);
  }, []);

  if (!stats) {
    return <div className="dashboard-loading">Loading Analytics...</div>;
  }

  const COLORS = ["#0ea5e9", "#a855f7", "#f43f5e", "#34d399"];

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Intelligence Analytics Dashboard</h2>
        <span className="live-badge">LIVE DATA</span>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon"><Activity size={24} color="#0ea5e9" /></div>
          <div className="stat-info">
            <h4>Total Cases Analyzed</h4>
            <p className="stat-value">{stats.totalCases.toLocaleString()}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><AlertTriangle size={24} color="#f43f5e" /></div>
          <div className="stat-info">
            <h4>Active Hotspots</h4>
            <p className="stat-value danger">{stats.activeHotspots}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><CheckCircle size={24} color="#34d399" /></div>
          <div className="stat-info">
            <h4>Resolved Cases</h4>
            <p className="stat-value success">{stats.resolvedCases.toLocaleString()}</p>
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Crime Trend (Last 6 Months)</h3>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={stats.monthlyTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="month" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)' }} />
                <Line type="monotone" dataKey="crimes" stroke="#a855f7" strokeWidth={3} dot={{ r: 4, fill: '#a855f7' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="chart-card">
          <h3>Crime Distribution by Type</h3>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.crimeTypes}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  fill="#8884d8"
                  paddingAngle={5}
                  dataKey="value"
                >
                  {stats.crimeTypes.map((_: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      <div className="alerts-grid">
        <div className="chart-card">
          <h3>Active Hotspot Alerts</h3>
          {stats.hotspotAlerts && stats.hotspotAlerts.length > 0 ? (
            <div className="alerts-list">
              {stats.hotspotAlerts.map((alert: any) => (
                <div key={alert.cluster_id} className="alert-card">
                  <div className="alert-header">
                    <span className="alert-district">{alert.district}</span>
                    <span className="alert-count">{alert.case_count} Cases</span>
                  </div>
                  <p className="alert-explanation">{alert.explanation}</p>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>No active hotspots detected.</p>
          )}
        </div>
      </div>
    </div>
  );
}
