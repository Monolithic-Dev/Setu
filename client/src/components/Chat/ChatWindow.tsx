import { useState, useCallback } from "react";
import { submitQuery, flagAnswer, transcribeAudio, exportConversationPdf, synthesizeAudio, type QueryResponse, type Language } from "../../api/queryClient";
import { VoiceCapture } from "./VoiceCapture";
import { t } from "../../i18n/strings";
import "./ChatWindow.css";

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
  const [isExporting, setIsExporting] = useState(false);
  const [playingAudioId, setPlayingAudioId] = useState<string | null>(null);

  const handleSend = useCallback(async () => {
    const text = inputText.trim();
    if (!text) return;

    const turnId = crypto.randomUUID();
    setTurns((prev) => [...prev, { id: turnId, queryText: text, response: null, status: "pending" }]);
    setInputText("");

    try {
      const response = await submitQuery({ session_id: sessionId, text, language });
      setTurns((prev) =>
        prev.map((turn) => (turn.id === turnId ? { ...turn, response, status: "done" } : turn))
      );
    } catch (err) {
      setTurns((prev) =>
        prev.map((turn) => (turn.id === turnId ? { ...turn, status: "reconnecting" } : turn))
      );
      console.error("Query failed, entering reconnecting state:", err);
    }
  }, [inputText, language, sessionId]);

  const handleAudioCaptured = useCallback(async (audioBlob: Blob) => {
    try {
      setInputText("Transcribing...");
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
  }, []);

  const handleExportPdf = useCallback(async () => {
    const lastTurn = turns[turns.length - 1];
    if (!lastTurn || !lastTurn.response) {
      alert("No completed conversation to export yet!");
      return;
    }
    
    setIsExporting(true);
    try {
      const conversation = {
        query_text: lastTurn.queryText,
        answer: lastTurn.response.answer,
        sources: lastTurn.response.sources.map(s => s.case_id),
        audit_id: lastTurn.response.audit_id,
        timestamp: new Date().toISOString()
      };
      
      const blob = await exportConversationPdf(sessionId, conversation);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Setu_Report_${sessionId.substring(0, 8)}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Failed to export PDF", err);
      alert("Failed to export PDF.");
    } finally {
      setIsExporting(false);
    }
  }, [turns, sessionId]);

  const handlePlayAudio = useCallback(async (turnId: string, text: string) => {
    setPlayingAudioId(turnId);
    try {
      const result = await synthesizeAudio(text, language);
      const audio = new Audio("data:audio/wav;base64," + result.audio);
      audio.onended = () => setPlayingAudioId(null);
      await audio.play();
    } catch (err) {
      console.error("Audio synthesis failed:", err);
      alert("Failed to play audio.");
      setPlayingAudioId(null);
    }
  }, [language]);

  return (
    <div className="chat-window">
      <div className="chat-header-actions">
        <button className="export-pdf-btn" onClick={handleExportPdf} disabled={isExporting} title={t(language, "exportPdf") || "Export to PDF"}>
          {isExporting ? "⏳ Exporting..." : "📄 Export to PDF"}
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
                
                <div style={{ marginTop: "10px" }}>
                  <button onClick={() => handlePlayAudio(turn.id, turn.response!.answer)} disabled={playingAudioId === turn.id} style={{ background: "transparent", border: "1px solid var(--primary-color)", color: "var(--primary-color)", borderRadius: "12px", padding: "4px 10px", cursor: "pointer", fontSize: "0.85rem" }}>
                    {playingAudioId === turn.id ? "🔊 Playing..." : "🔊 Read Aloud"}
                  </button>
                </div>

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
                  <span>{t(language, "wasHelpful")}</span>
                  <button onClick={() => handleFeedback(turn.response!.audit_id, true)}>
                    {t(language, "yes")}
                  </button>
                  <button onClick={() => handleFeedback(turn.response!.audit_id, false)}>
                    {t(language, "no")}
                  </button>
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
