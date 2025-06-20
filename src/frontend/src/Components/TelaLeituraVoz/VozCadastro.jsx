import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom'; 
import './VozCadastro.css';

const LeituraVoz = () => {
  const [gravando, setGravando] = useState(false);
  const [mensagem, setMensagem] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const navigate = useNavigate(); 

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
  const token = localStorage.getItem('token_temporario');

  const iniciarGravacao = async () => {
    if (gravando) return;

    setMensagem('');
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
          const erro = await response.json();
          setMensagem(erro.detail || 'Erro ao registrar voz.');
        }
      } catch (error) {
        setMensagem('Erro de conexão com o servidor.');
      }

      setGravando(false);
    };

    mediaRecorderRef.current.start();

    setTimeout(() => {
      mediaRecorderRef.current.stop();
    }, 4000);
  };

  return (
    <div className="containerr">
      <h2>Cadastro de Voz</h2>
      <button onClick={iniciarGravacao} disabled={gravando}>
        {gravando ? 'Gravando...' : 'Iniciar Gravação'}
      </button>
      {mensagem && <p>{mensagem}</p>}
    </div>
  );
};

export default LeituraVoz;