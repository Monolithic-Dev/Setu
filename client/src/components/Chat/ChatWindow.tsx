import { useState, useCallback } from "react";
import { submitQuery, flagAnswer, transcribeAudio, type QueryResponse, type Language } from "../../api/queryClient";
import { VoiceCapture } from "./VoiceCapture";
import { ConnectivityBanner } from "../ConnectivityBanner/ConnectivityBanner";
import { t } from "../../i18n/strings";
import "./ChatWindow.css";

// Implements docs/UX.md's "Answer View" and "Connectivity State" (added Phase 7 review):
// answer + sources + reasoning trail + feedback control, plus a visible
// reconnecting state instead of a silent failure (NFR-10).

interface ChatTurn {
  id: string;
  queryText: string;
  response: QueryResponse | null;
  status: "pending" | "done" | "reconnecting" | "error";
}

export function ChatWindow({ language }: { language: Language }) {
  const [turns, setTurns] = useState<ChatTurn[]>([
    {
      id: "welcome",
      queryText: "System Initialization",
      status: "done",
      response: {
        answer: "Welcome to Setu Intelligence Platform. ZCQL Data Store connected. QuickML Knowledge Base online. Awaiting query...",
        sources: [],
        audit_id: "init",
        language: "en"
      }
    }
  ]);
  const [inputText, setInputText] = useState("");
  const [sessionId] = useState(() => crypto.randomUUID());
  const [feedbackGiven, setFeedbackGiven] = useState<Record<string, boolean>>({});
  const [isRetrying, setIsRetrying] = useState(false);

  const handleSend = useCallback(async () => {
    const text = inputText.trim();
    if (!text) return;

    const turnId = crypto.randomUUID();
    setTurns((prev) => [...prev, { id: turnId, queryText: text, response: null, status: "pending" }]);
    setInputText("");

    let attempt = 0;
    const maxAttempts = 3;

    const trySubmit = async () => {
      try {
        const response = await submitQuery({ session_id: sessionId, text, language });
        setIsRetrying(false);
        setTurns((prev) =>
          prev.map((turn) => (turn.id === turnId ? { ...turn, response, status: "done" } : turn))
        );
      } catch (err) {
        attempt++;
        if (attempt >= maxAttempts) {
          setIsRetrying(false);
          setTurns((prev) =>
            prev.map((turn) => (turn.id === turnId ? { ...turn, status: "error" } : turn))
          );
          console.error("Query failed after retries:", err);
        } else {
          setIsRetrying(true);
          setTurns((prev) =>
            prev.map((turn) => (turn.id === turnId ? { ...turn, status: "reconnecting" } : turn))
          );
          // Exponential backoff
          await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
          await trySubmit();
        }
      }
    };

    await trySubmit();
  }, [inputText, language, sessionId]);

  const handleAudioCaptured = useCallback(async (audioBlob: Blob) => {
    try {
      setInputText("Transcribing..."); // In real app, we'd use a localized string or spinner
      const result = await transcribeAudio(audioBlob);
      setInputText(result.text);
    } catch (err) {
      console.error("Transcription failed:", err);
      alert("Failed to transcribe audio.");
      setInputText("");
    }
  }, []);

  const handleFeedback = useCallback((auditId: string, wasHelpful: boolean) => {
    flagAnswer(auditId, wasHelpful).catch((err) => console.error("Failed to record feedback:", err));
    setFeedbackGiven(prev => ({ ...prev, [auditId]: true }));
  }, []);

  return (
    <div className="chat-window">
      <ConnectivityBanner isVisible={isRetrying} />
      <div className="chat-header-actions">
        <button className="export-pdf-btn" onClick={() => window.print()} title={t(language, "exportPdf") || "Export to PDF"}>
          📄 Export to PDF
        </button>
      </div>
      <div className="chat-history">
        {turns.map((turn) => (
          <div key={turn.id} className="chat-turn">
            <p className="query">{turn.queryText}</p>

            {turn.status === "pending" && <p className="status">…</p>}

            {turn.status === "reconnecting" && (
              <p className="status status-reconnecting">{t(language, "reconnecting")}</p>
            )}

            {turn.status === "done" && turn.response && (
              <div className="answer">
                <p>{turn.response.answer}</p>

                {turn.response.sources.length > 0 && (
                  <details className="sources">
                    <summary>{t(language, "sources")}</summary>
                    <ul>
                      {turn.response.sources.map((s) => (
                        <li key={s.case_id}>
                          {s.case_id} ({s.relevance})
                        </li>
                      ))}
                    </ul>
                  </details>
                )}

                <div className="feedback-control">
                  {feedbackGiven[turn.response!.audit_id] ? (
                    <span className="feedback-thanks">Thanks, noted.</span>
                  ) : (
                    <>
                      <span>{t(language, "wasHelpful")}</span>
                      <button onClick={() => handleFeedback(turn.response!.audit_id, true)}>
                        👍 {t(language, "yes")}
                      </button>
                      <button onClick={() => handleFeedback(turn.response!.audit_id, false)}>
                        👎 {t(language, "no")}
                      </button>
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <VoiceCapture language={language} onAudioCaptured={handleAudioCaptured} />
        <input
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder={t(language, "askPlaceholder")}
        />
        <button onClick={handleSend}>{t(language, "send")}</button>
      </div>
    </div>
  );
}
