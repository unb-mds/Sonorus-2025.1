import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './VozLogin.css';

const LeituraVoz = () => {
  const [gravando, setGravando] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timeoutRef = useRef(null);
  const API_URL = (process.env.REACT_APP_API_URL || "http://localhost:8000/api").replace(/\/$/, "");
  const navigate = useNavigate();

  const iniciarGravacao = async () => {
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
        clearTimeout(timeoutRef.current);
        setGravando(false);

        if (mediaRecorderRef.current && mediaRecorderRef.current.stream) {
          mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
        }

        if (audioChunksRef.current.length === 0) {
          navigate('/erroLeitura');
          return;
        }

        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        audioChunksRef.current = [];

        const formData = new FormData();
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

      timeoutRef.current = setTimeout(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          mediaRecorderRef.current.stop();
          navigate('/erroLeitura');
        }
      }, 30000);

    } catch (err) {
      setGravando(false);
      navigate('/erroLeitura');
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

  return (
    <div className="containerr2">
      <div className="conteudo2">
        <h2 className="titulo2">Autenticação por voz</h2>

        <div className="mic-wrapper2">
          {gravando && (
            <div className="ondas2 lado-esquerdo2">
              {Array.from({ length: 7 }).map((_, i) => (
                <div
                  key={`left-${i}`}
                  className="onda2"
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
              {Array.from({ length: 7 }).map((_, i) => (
                <div
                  key={`right-${i}`}
                  className="onda2"
                  style={{
                    animationDelay: `${i * 0.1}s`,
                    height: `${10 + (i % 4) * 15}px`,
                  }}
                />
              ))}
            </div>
          )}
        </div>

        <p className="instrucao2">Diga "Esta é a minha voz"</p>
      </div>
    </div>
  );
};

export default LeituraVoz;