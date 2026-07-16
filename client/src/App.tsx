import { useState } from "react";
import { ChatWindow } from "./components/Chat/ChatWindow";
import { Login } from "./components/Login/Login";
import { NetworkGraph } from "./components/NetworkGraph/NetworkGraph";
import { AuditLogs } from "./components/Admin/AuditLogs";
import { Dashboard } from "./components/Analytics/Dashboard";
import { t, type Language } from "./i18n/strings";
import { setDevAuth } from "./api/queryClient";
import "./App.css";

export default function App() {
  const [language, setLanguage] = useState<Language>("en");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState("");
  const [currentView, setCurrentView] = useState<"chat" | "audit" | "dashboard">("chat");

  const handleLogin = (role: string, stationId: string, districtId: string) => {
    setDevAuth(role, stationId, districtId);
    setUserRole(role);
    setIsAuthenticated(true);
  };

  const isAdmin = userRole === "System Admin";

  return (
    <div className="app">
      <header>
        <h1>{t(language, "appTitle")}</h1>
        <div className="header-controls">
          {isAuthenticated && (
            <div className="admin-toggle">
              <button 
                className={currentView === "chat" ? "active" : ""} 
                onClick={() => setCurrentView("chat")}
              >
                Intelligence Chat
              </button>
              <button 
                className={currentView === "dashboard" ? "active" : ""} 
                onClick={() => setCurrentView("dashboard")}
              >
                Analytics Dashboard
              </button>
              {isAdmin && (
                <button 
                  className={currentView === "audit" ? "active" : ""} 
                  onClick={() => setCurrentView("audit")}
                >
                  Audit Logs
                </button>
              )}
            </div>
          )}
          <div className="language-toggle" role="group" aria-label="Language">
            <button
              aria-pressed={language === "en"}
              onClick={() => setLanguage("en")}
            >
              English
            </button>
            <button
              aria-pressed={language === "kn"}
              onClick={() => setLanguage("kn")}
            >
              ಕನ್ನಡ
            </button>
          </div>
        </div>
      </header>

      <main>
        {!isAuthenticated ? (
          <Login language={language} onLogin={handleLogin} />
        ) : currentView === "audit" && isAdmin ? (
          <AuditLogs language={language} />
        ) : currentView === "dashboard" ? (
          <Dashboard language={language} />
        ) : (
          <div className="app-split-layout">
            <div className="app-chat-pane">
              <ChatWindow language={language} />
            </div>
            <div className="app-graph-pane">
              <NetworkGraph language={language} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
