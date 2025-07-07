import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './VozCadastro.css';

const LeituraVoz = () => {
  // --- Estados e Refs combinados de ambas as branches ---
  const [gravando, setGravando] = useState(false);
  const [mensagem, setMensagem] = useState('');
  const [waveHeights, setWaveHeights] = useState(Array(7).fill(10)); // Estado para as ondas

  // Refs para a gravação e lógica da 'main'
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timeoutRef = useRef(null);
  const timeoutAtingidoRef = useRef(false);

  // Refs para a visualização de áudio da 'melhorias-na-UI'
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameIdRef = useRef(null);
  const streamRef = useRef(null); // Ref unificada para a stream

  const navigate = useNavigate();
  const API_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');

  // --- Função para limpar todos os recursos de áudio e visualização ---
  // Unifica a lógica de limpeza que estava espalhada
  const limparRecursos = () => {
    // Limpeza da visualização de áudio
    if (animationFrameIdRef.current) {
      cancelAnimationFrame(animationFrameIdRef.current);
    }
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close();
    }
    // Para as tracks do microfone
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    // Reseta o estado visual
    setWaveHeights(Array(7).fill(10));
  };


  // --- Funções de controle da gravação (Estrutura da 'main' com funcionalidades da 'melhorias-na-UI') ---

  const iniciarGravacao = async () => {
    setMensagem('');
    setGravando(true);
    timeoutAtingidoRef.current = false;
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

      // Início da lógica do MediaRecorder
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      // onstop agora contém a lógica de envio de áudio robusta da 'main'
      mediaRecorderRef.current.onstop = async () => {
        limparRecursos(); // Usa a função de limpeza centralizada

        if (timeoutAtingidoRef.current) {
          navigate('/erroCadastro');
          return;
        }

        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('arquivo', audioBlob, 'voz.webm');

        try {
          const response = await fetch(`${API_URL}/registrar-voz`, {
            method: 'POST',
            credentials: 'include',
            body: formData,
          });

          if (response.ok) {
            setMensagem('Voz registrada com sucesso!');
            setTimeout(() => navigate('/login'), 1000);
          } else {
            navigate('/erroCadastro');
          }
        } catch (error) {
          navigate('/erroCadastro');
        }
      };

      mediaRecorderRef.current.start();

      // Lógica de timeout da 'main', mais robusta
      timeoutRef.current = setTimeout(() => {
        timeoutAtingidoRef.current = true;
        setMensagem('Tempo limite atingido');
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          mediaRecorderRef.current.stop();
        }
      }, 30000);

    } catch (err) {
      limparRecursos();
      setMensagem('Permissão do microfone negada ou erro ao acessar o microfone.');
      setGravando(false);
    }
  };

  const pararGravacao = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      clearTimeout(timeoutRef.current);
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

  // Efeito para limpar recursos caso o componente seja desmontado
  useEffect(() => {
    return () => {
      limparRecursos();
      if(timeoutRef.current) {
        clearTimeout(timeoutRef.current);
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
            onClick={handleMicClick}
            className={`mic-button ${gravando ? 'gravando' : ''}`}
            aria-label={gravando ? "Parar gravação" : "Iniciar gravação"}
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
        {mensagem && <p style={{ marginTop: 30, fontWeight: 600 }}>{mensagem}</p>}
      </div>
    </div>
  );
};

export default LeituraVoz;