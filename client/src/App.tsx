import { useState } from "react";
import { ChatWindow } from "./components/Chat/ChatWindow";
import { Login } from "./components/Login/Login";
import { t, type Language } from "./i18n/strings";
import { setDevAuth } from "./api/queryClient";

export default function App() {
  const [language, setLanguage] = useState<Language>("en");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = (role: string, stationId: string, districtId: string) => {
    setDevAuth(role, stationId, districtId);
    setIsAuthenticated(true);
  };

  return (
    <div className="app">
      <header>
        <h1>{t(language, "appTitle")}</h1>
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
      </header>

      <main>
        {!isAuthenticated ? (
          <Login language={language} onLogin={handleLogin} />
        ) : (
          <ChatWindow language={language} />
        )}
      </main>
    </div>
  );
}
