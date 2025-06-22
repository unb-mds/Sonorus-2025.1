import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './VozCadastro.css';

const LeituraVoz = () => {
  const [gravando, setGravando] = useState(false);
  const [mensagem, setMensagem] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timeoutRef = useRef(null);
  const timeoutAtingidoRef = useRef(false);
  const navigate = useNavigate();

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
  const token = localStorage.getItem('token_temporario');

  const iniciarGravacao = async () => {
    setMensagem('');
    setGravando(true);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        setGravando(false);
        clearTimeout(timeoutRef.current);

        if (mediaRecorderRef.current && mediaRecorderRef.current.stream) {
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
        }

        if (timeoutAtingidoRef.current) {
          timeoutAtingidoRef.current = false;
          navigate('/erroLeitura');
          return;
        }

        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        audioChunksRef.current = [];

        const formData = new FormData();
        formData.append('arquivo', audioBlob, 'voz.webm');

        try {
          const response = await fetch(`${API_URL}/registrar-voz`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
            },
            body: formData,
          });

          if (response.ok) {
            setMensagem('Voz registrada com sucesso!');
            setTimeout(() => {
              navigate('/login');
            }, 1000);
          } else {
            navigate('/erroLeitura');
          }
        } catch (error) {
          navigate('/erroLeitura');
        }
      };

      mediaRecorderRef.current.start();

      // Timeout de 30 segundos para parar automaticamente
      timeoutRef.current = setTimeout(() => {
        timeoutAtingidoRef.current = true;
        setMensagem('Tempo limite atingido');
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          mediaRecorderRef.current.stop();
        }
      }, 30000);

    } catch (err) {
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

  return (
    <div className="containerr">
      <div className="conteudo">
        <h2 className="titulo">Vamos cadastrar sua voz</h2>

        <div className="mic-wrapper">
          {gravando && (
            <div className="ondas lado-esquerdo">
              {Array.from({ length: 7 }).map((_, i) => (
                <div
                  key={`left-${i}`}
                  className="onda"
                  style={{
                    animationDelay: `${i * 0.1}s`,
                    height: `${10 + (i % 4) * 15}px`,
                  }}
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
              {Array.from({ length: 7 }).map((_, i) => (
                <div
                  key={`right-${i}`}
                  className="onda"
                  style={{
                    animationDelay: `${i * 0.1}s`,
                    height: `${10 + (i % 4) * 15}px`,
                  }}
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