import { useEffect, useState } from "react";
import { fetchAuditLogs, AuditLogEntry } from "../../api/queryClient";
import { t, type Language } from "../../i18n/strings";
import "./AuditLogs.css";

interface AuditLogsProps {
  language: Language;
}

export function AuditLogs({ language }: AuditLogsProps) {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadLogs() {
      try {
        const data = await fetchAuditLogs();
        setLogs(data);
      } catch (err: any) {
        setError(err.message || "Failed to load audit logs.");
      } finally {
        setLoading(false);
      }
    }
    loadLogs();
  }, []);

  if (loading) {
    return <div className="audit-loading">Loading audit logs...</div>;
  }

  if (error) {
    return <div className="audit-error">{error}</div>;
  }

  return (
    <div className="audit-logs-container">
      <h2>System Audit Logs</h2>
      <p className="audit-subtitle">Confidential system access records.</p>
      
      <div className="table-responsive">
        <table className="audit-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>User ID</th>
              <th>Language</th>
              <th>Sources Used</th>
              <th>Query / Answer Summary</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.audit_id}>
                <td className="time-col">{new Date(log.timestamp).toLocaleString()}</td>
                <td className="user-col">{log.user_id}</td>
                <td className="lang-col">{log.language.toUpperCase()}</td>
                <td className="sources-col">
                  {log.sources_used.length > 0 ? (
                    <ul className="source-list">
                      {log.sources_used.map(src => (
                        <li key={src}>{src}</li>
                      ))}
                    </ul>
                  ) : (
                    <span className="no-sources">None</span>
                  )}
                </td>
                <td className="summary-col">
                  <strong>Query:</strong> {log.query_text} <br/>
                  <span className="answer-summary">
                    <strong>Answer:</strong> {log.answer_summary}
                  </span>
                </td>
              </tr>
            ))}
            {logs.length === 0 && (
              <tr>
                <td colSpan={5} className="empty-state">No audit logs found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
