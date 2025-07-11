import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './VozCadastro.css';

const LeituraVoz = () => {
  const [gravando, setGravando] = useState(false);
  const [mensagem, setMensagem] = useState('');
  const [waveHeights, setWaveHeights] = useState(Array(7).fill(10));
  const [instrucaoBotao, setInstrucaoBotao] = useState('Clique no botão para gravar sua voz');

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timeoutRef = useRef(null);
  const timeoutAtingidoRef = useRef(false);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameIdRef = useRef(null);
  const streamRef = useRef(null);

  const navigate = useNavigate();
  const API_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');

  const limparRecursos = () => {
    if (animationFrameIdRef.current) cancelAnimationFrame(animationFrameIdRef.current);
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') audioContextRef.current.close();
    if (streamRef.current) streamRef.current.getTracks().forEach(track => track.stop());
    setWaveHeights(Array(7).fill(10));
  };

  const iniciarGravacao = async () => {
    setMensagem('');
    setGravando(true);
    setInstrucaoBotao('Após falar a frase, clique novamente no botão para concluir');
    timeoutAtingidoRef.current = false;
    audioChunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

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
        
        const newWaveHeights = Array.from({ length: 7 }, (_, i) => {
          const step = Math.floor(bufferLength / 7);
          const value = dataArray[i * step];
          return 10 + (value / 255) * 50;
        });
        setWaveHeights(newWaveHeights);
        animationFrameIdRef.current = requestAnimationFrame(animateWaves);
      };
      animateWaves();

      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (event) => audioChunksRef.current.push(event.data);

      mediaRecorderRef.current.onstop = async () => {
        limparRecursos();
        setGravando(false);
        setInstrucaoBotao('Clique no botão para gravar sua voz');

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

      timeoutRef.current = setTimeout(() => {
        timeoutAtingidoRef.current = true;
        setMensagem('Tempo limite atingido');
        if (mediaRecorderRef.current?.state === 'recording') {
          mediaRecorderRef.current.stop();
        }
      }, 30000);

    } catch (err) {
      limparRecursos();
      setMensagem('Permissão do microfone negada ou erro ao acessar o microfone.');
      setGravando(false);
      setInstrucaoBotao('Clique no botão para gravar sua voz');
    }
  };

  const pararGravacao = () => {
    if (mediaRecorderRef.current?.state === 'recording') {
      clearTimeout(timeoutRef.current);
      mediaRecorderRef.current.stop();
    }
  };

  const handleMicClick = () => {
    gravando ? pararGravacao() : iniciarGravacao();
  };

  useEffect(() => {
    return () => {
      limparRecursos();
      if(timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  return (
    <div className="containerr">
      <div className="conteudo">
        <h2 className="titulo">Vamos cadastrar sua voz</h2>

        <div className="mic-wrapper">
          {gravando && (
            <div className="ondas lado-esquerdo">
              {waveHeights.map((height, i) => <div key={`left-${i}`} className="onda" style={{ height: `${height}px` }} />)}
            </div>
          )}
          
          {/* Container que agrupa a instrução e o botão para garantir a centralização */}
          <div className="mic-action-area">
            <p className="instrucao-botao">{instrucaoBotao}</p>
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
          </div>

          {gravando && (
            <div className="ondas lado-direito">
              {waveHeights.map((height, i) => <div key={`right-${i}`} className="onda" style={{ height: `${height}px` }} />)}
            </div>
          )}
        </div>

        <p className="instrucao">Diga seu nome completo</p>
        {mensagem && <p style={{ marginTop: 30, fontWeight: 600 }}>{mensagem}</p>}
      </div>
    </div>
  );
};

export default LeituraVoz;