import { useState } from "react";
import { ChatWindow } from "./components/Chat/ChatWindow";
import { t, type Language } from "./i18n/strings";

export default function App() {
  const [language, setLanguage] = useState<Language>("en");

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
        <ChatWindow language={language} />
      </main>
    </div>
  );
}
