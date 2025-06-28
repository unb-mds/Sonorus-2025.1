import React, { useState, useRef, useEffect } from 'react';
import './VozCadastro.css';

const LeituraVoz = () => {
  const [gravando, setGravando] = useState(false);
  const [waveHeights, setWaveHeights] = useState(Array(7).fill(10)); // Estado para alturas das ondas

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  
  // Refs para a Web Audio API
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameIdRef = useRef(null);
  const streamRef = useRef(null);

  const iniciarGravacao = async () => {
    if (gravando) return;

    try {
      setGravando(true);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      // --- Início da lógica da Web Audio API ---
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;
      const bufferLength = analyserRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      // --- Fim da lógica da Web Audio API ---

      // --- Início da função de animação ---
      const animateWaves = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);
        
        const newWaveHeights = [];
        const step = Math.floor(bufferLength / 7);
        for (let i = 0; i < 7; i++) {
          const value = dataArray[i * step];
          // Mapeia o valor de 0-255 para uma altura de 10px a 60px
          const height = 10 + (value / 255) * 50;
          newWaveHeights.push(height);
        }
        setWaveHeights(newWaveHeights);
        animationFrameIdRef.current = requestAnimationFrame(animateWaves);
      };
      animateWaves();
      // --- Fim da função de animação ---

      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        audioChunksRef.current = [];

        const formData = new FormData();
        formData.append('audio', audioBlob);

        await fetch('http://localhost:8000/enviar-audio', {
          method: 'POST',
          body: formData,
        });

        // Limpeza após parar
        cancelAnimationFrame(animationFrameIdRef.current);
        if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
          audioContextRef.current.close();
        }
        streamRef.current.getTracks().forEach(track => track.stop()); // Para o microfone
        setWaveHeights(Array(7).fill(10)); // Reseta as ondas
        setGravando(false);
      };

      mediaRecorderRef.current.start();

      setTimeout(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
        }
      }, 4000);
    } catch (error) {
        console.error("Erro ao acessar o microfone:", error);
        setGravando(false);
    }
  };

  // Efeito para limpar recursos caso o componente seja desmontado
  useEffect(() => {
    return () => {
      cancelAnimationFrame(animationFrameIdRef.current);
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        audioContextRef.current.close();
      }
      if(streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div className="containerr">
      <div className="conteudo">
        <h2 className="titulo">Vamos cadastrar sua voz</h2>

        <div className="mic-wrapper">
          {gravando && (
            <div className="ondas lado-esquerdo">
              {waveHeights.map((height, i) => (
                <div
                  key={`left-${i}`}
                  className="onda"
                  style={{ height: `${height}px` }}
                />
              ))}
            </div>
          )}

          <button
            onClick={iniciarGravacao}
            className={`mic-button ${gravando ? 'gravando' : ''}`}
            disabled={gravando}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="mic-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 16a4 4 0 0 0 4-4V6a4 4 0 0 0-8 0v6a4 4 0 0 0 4 4z"/>
              <path d="M19 12a1 1 0 1 0-2 0 5 5 0 0 1-10 0 1 1 0 1 0-2 0 7 7 0 0 0 6 6.83V21a1 1 0 1 0 2 0v-2.17A7 7 0 0 0 19 12z"/>
            </svg>
          </button>

          {gravando && (
            <div className="ondas lado-direito">
              {waveHeights.map((height, i) => (
                <div
                  key={`right-${i}`}
                  className="onda"
                  style={{ height: `${height}px` }}
                />
              ))}
            </div>
          )}
        </div>

        <p className="instrucao">Diga "Esta é a minha voz"</p>
      </div>
    </div>
  );
};

export default LeituraVoz;