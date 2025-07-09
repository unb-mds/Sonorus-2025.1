import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './VozLogin.css';

const LeituraVoz = () => {
  // --- Estados e Refs combinados de ambas as branches ---
  const [gravando, setGravando] = useState(false);
  const [waveHeights, setWaveHeights] = useState(Array(7).fill(10));

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timeoutRef = useRef(null);
  
  // Refs para a Web Audio API da 'melhorias-na-UI'
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameIdRef = useRef(null);
  const streamRef = useRef(null);
  
  const navigate = useNavigate();
  // Usando a definição mais robusta de API_URL que remove a barra final
  const API_URL = (process.env.REACT_APP_API_URL || "http://localhost:8000/api").replace(/\/$/, "");

  // --- Função de Limpeza Centralizada ---
  // Combina a lógica de limpeza das duas branches para evitar repetição
  const limparRecursos = () => {
    if (animationFrameIdRef.current) {
      cancelAnimationFrame(animationFrameIdRef.current);
    }
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setWaveHeights(Array(7).fill(10));
  };

  // --- Funções de Controle da Gravação ---

  const iniciarGravacao = async () => {
    setGravando(true);
    audioChunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      // Início da lógica de visualização de áudio ('melhorias-na-UI')
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;
      const bufferLength = analyserRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const animateWaves = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);
        
        const newWaveHeights = [];
        const step = Math.floor(bufferLength / 7);
        for (let i = 0; i < 7; i++) {
          const value = dataArray[i * step];
          const height = 10 + (value / 255) * 50;
          newWaveHeights.push(height);
        }
        setWaveHeights(newWaveHeights);
        animationFrameIdRef.current = requestAnimationFrame(animateWaves);
      };
      animateWaves();
      // Fim da lógica de visualização

      // Lógica do MediaRecorder
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        clearTimeout(timeoutRef.current);
        setGravando(false);
        limparRecursos(); // Usa a função de limpeza

        if (audioChunksRef.current.length === 0) {
          navigate('/erroLeitura');
          return;
        }

        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const formData = new FormData();
        // Lógica de envio da 'main', que é mais robusta
        formData.append('arquivo', audioBlob, 'voz.webm');

        try {
          const response = await fetch(`${API_URL}/autenticar-voz`, {
            method: 'POST',
            credentials: 'include',
            body: formData,
          });

          if (response.ok) {
            navigate('/sucessoCadastro');
          } else {
            navigate('/erroLeitura');
          }
        } catch (error) {
          navigate('/erroLeitura');
        }
      };

      mediaRecorderRef.current.start();

      // Lógica de timeout da 'main'
      timeoutRef.current = setTimeout(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          mediaRecorderRef.current.stop();
        }
      }, 30000); // Timeout de 30 segundos

    } catch (err) {
      setGravando(false);
      limparRecursos(); // Garantir que recursos sejam limpos antes de navegar
      navigate('/erroLeitura'); // Tratamento de erro da 'main'
    }
  };

  const pararGravacao = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  };

  const handleMicClick = () => {
    if (!gravando) {
      iniciarGravacao();
    } else {
      pararGravacao();
    }
  };

  // Efeito para limpar tudo caso o componente seja desmontado
  useEffect(() => {
    return () => {
      limparRecursos();
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return (
    <div className="containerr2">
      <div className="conteudo2">
        <h2 className="titulo2">Autenticação por voz</h2>

        <div className="mic-wrapper2">
          {gravando && (
            <div className="ondas2 lado-esquerdo2">
              {waveHeights.map((height, i) => (
                <div
                  key={`left-${i}`}
                  className="onda2"
                  style={{ height: `${height}px` }}
                />
              ))}
            </div>
          )}

          <button
            onClick={handleMicClick}
            className={`mic-button2 ${gravando ? 'gravando' : ''}`}
            aria-label={gravando ? "Parar gravação" : "Iniciar gravação"}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="mic-icon2" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 16a4 4 0 0 0 4-4V6a4 4 0 0 0-8 0v6a4 4 0 0 0 4 4z"/>
              <path d="M19 12a1 1 0 1 0-2 0 5 5 0 0 1-10 0 1 1 0 1 0-2 0 7 7 0 0 0 6 6.83V21a1 1 0 1 0 2 0v-2.17A7 7 0 0 0 19 12z"/>
            </svg>
          </button>

          {gravando && (
            <div className="ondas2 lado-direito2">
              {waveHeights.map((height, i) => (
                <div
                  key={`right-${i}`}
                  className="onda2"
                  style={{ height: `${height}px` }}
                />
              ))}
            </div>
          )}
        </div>

        <p className="instrucao2">Diga seu nome completo</p>
      </div>
    </div>
  );
};

export default LeituraVoz;
