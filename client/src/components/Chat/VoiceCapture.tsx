import { useState, useRef, useCallback } from "react";
import { t, type Language } from "../../i18n/strings";
import "./VoiceCapture.css";

interface VoiceCaptureProps {
  language: Language;
  onAudioCaptured: (audioBlob: Blob) => void;
}

export function VoiceCapture({ language, onAudioCaptured }: VoiceCaptureProps) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: "audio/webm" });
        onAudioCaptured(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert(t(language, "micError") || "Could not access microphone.");
    }
  }, [language, onAudioCaptured]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

  return (
    <button
      className={`voice-capture-btn ${isRecording ? "recording" : ""}`}
      onClick={isRecording ? stopRecording : startRecording}
      title={isRecording ? "Stop recording" : "Start voice recording"}
    >
      {isRecording ? "⏹" : "🎤"}
    </button>
  );
}
