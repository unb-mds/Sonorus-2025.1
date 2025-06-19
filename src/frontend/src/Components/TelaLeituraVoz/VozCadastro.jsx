import React, { useState, useRef } from 'react';
import './VozCadastro.css';

const LeituraVoz = () => {
  const [gravando, setGravando] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const iniciarGravacao = async () => {
    if (gravando) return;

    setGravando(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
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

      setGravando(false);
    };

    mediaRecorderRef.current.start();

    setTimeout(() => {
      mediaRecorderRef.current.stop();
    }, 4000); // grava por 4 segundos (ajuste conforme necessário)
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
      </div>
    </div>
  );
};

export default LeituraVoz;
