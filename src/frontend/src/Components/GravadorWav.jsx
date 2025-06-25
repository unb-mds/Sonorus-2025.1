import React, { useRef, useState } from "react";
import WavEncoder from "wav-encoder";
import { ReactComponent as MicIcon } from "../assets/mic.svg";
import "./TelaLeituraVoz/VozCadastro.css";
import "./TelaLeituraVoz/VozLogin.css";

const GravadorWav = ({
  onAudioReady,
  children,
  tempoMaximo = 30,
  contexto = "cadastro" // ou "login"
}) => {
  const [gravando, setGravando] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const [ondas, setOndas] = useState([0.5, 0.7, 0.4, 0.8, 0.6]);
  const audioContextRef = useRef(null);
  const bufferRef = useRef([]);
  const streamRef = useRef(null);
  const processorRef = useRef(null);
  const rafRef = useRef(null);
  const timeoutRef = useRef(null);

  // Define classes conforme contexto
  const micWrapperClass = contexto === "login" ? "mic-wrapper2" : "mic-wrapper";
  const micButtonClass = contexto === "login" ? "mic-button2" : "mic-button";
  const micIconClass = contexto === "login" ? "mic-icon2" : "mic-icon";
  const ondasClass = contexto === "login" ? "ondas2" : "ondas";
  const ondaClass = contexto === "login" ? "onda2" : "onda";

  // Animação das ondas
  const animarOndas = (inputLevel = 0.5) => {
    setOndas((prev) =>
      prev.map(() => Math.max(0.3, Math.min(1, inputLevel + (Math.random() - 0.5) * 0.5)))
    );
    if (gravando) rafRef.current = requestAnimationFrame(() => animarOndas(inputLevel));
  };

  const startRecording = async () => {
    setAudioUrl(null);
    bufferRef.current = [];
    setGravando(true);

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    streamRef.current = stream;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audioContext = new AudioContext();
    audioContextRef.current = audioContext;
    const source = audioContext.createMediaStreamSource(stream);
    const processor = audioContext.createScriptProcessor(4096, 1, 1);

    processor.onaudioprocess = (e) => {
      bufferRef.current.push(new Float32Array(e.inputBuffer.getChannelData(0)));
      const input = e.inputBuffer.getChannelData(0);
      const rms = Math.sqrt(input.reduce((sum, v) => sum + v * v, 0) / input.length);
      animarOndas(rms * 2);
    };

    source.connect(processor);
    processor.connect(audioContext.destination);
    processorRef.current = processor;

    timeoutRef.current = setTimeout(() => {
      stopRecording();
    }, tempoMaximo * 1000);
  };

  const stopRecording = async () => {
    setGravando(false);
    clearTimeout(timeoutRef.current);
    cancelAnimationFrame(rafRef.current);

    const audioContext = audioContextRef.current;
    const stream = streamRef.current;
    const processor = processorRef.current;

    if (processor) processor.disconnect();
    if (stream) stream.getTracks().forEach((track) => track.stop());
    if (audioContext) audioContext.close();

    const flatBuffer = Float32Array.from(bufferRef.current.flat());

    // Resample para 16kHz se necessário
    let resampled = flatBuffer;
    let sampleRate = audioContextRef.current?.sampleRate || 44100;
    if (sampleRate !== 16000) {
      const ratio = 16000 / sampleRate;
      const newLength = Math.round(flatBuffer.length * ratio);
      resampled = new Float32Array(newLength);
      for (let i = 0; i < newLength; i++) {
        const idx = i / ratio;
        const idx0 = Math.floor(idx);
        const idx1 = Math.min(idx0 + 1, flatBuffer.length - 1);
        const frac = idx - idx0;
        resampled[i] = flatBuffer[idx0] * (1 - frac) + flatBuffer[idx1] * frac;
      }
      sampleRate = 16000;
    }

    const wavData = await WavEncoder.encode({
      sampleRate: 16000,
      channelData: [resampled],
    });

    const blob = new Blob([wavData], { type: "audio/wav" });
    setAudioUrl(URL.createObjectURL(blob));
    if (onAudioReady) onAudioReady(blob);
  };

  return (
    <div>
      <div className={micWrapperClass}>
        <button
          className={micButtonClass}
          onClick={gravando ? stopRecording : startRecording}
          disabled={gravando}
          aria-label={gravando ? "Parar gravação" : "Iniciar gravação"}
        >
          <MicIcon className={micIconClass} />
        </button>
        <div className={ondasClass}>
          {ondas.map((h, i) => (
            <div
              key={i}
              className={ondaClass}
              style={{
                height: `${h * 40 + 20}px`,
                background: gravando ? "#3b82f6" : "#888",
                transition: "height 0.2s",
              }}
            />
          ))}
        </div>
      </div>
      {audioUrl && (
        <div style={{ margin: "10px 0" }}>
          <audio src={audioUrl} controls />
          <a href={audioUrl} download="gravacao.wav" style={{ marginLeft: 10 }}>
            Baixar WAV
          </a>
        </div>
      )}
      {children}
    </div>
  );
};

export default GravadorWav;