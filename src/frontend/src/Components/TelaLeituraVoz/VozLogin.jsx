import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import GravadorWav from '../GravadorWav';
import './VozLogin.css';

const LeituraVoz = () => {
  const [mensagem, setMensagem] = useState('');
  const API_URL = (process.env.REACT_APP_API_URL || "http://localhost:8000/api").replace(/\/$/, "");
  const navigate = useNavigate();

  const handleAudioReady = async (blob) => {
    setMensagem('Enviando áudio...');
    const formData = new FormData();
    formData.append('arquivo', blob, 'voz.wav');
    try {
      const response = await fetch(`${API_URL}/autenticar-voz`, {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });

      if (response.ok) {
        setMensagem('Autenticação realizada!');
        setTimeout(() => {
          navigate('/sucessoCadastro');
        }, 1000);
      } else {
        navigate('/erroLeitura');
      }
    } catch (error) {
      navigate('/erroLeitura');
    }
  };

  return (
    <div className="containerr2">
      <div className="conteudo2">
        <h2 className="titulo2">Autenticação por voz</h2>
        <GravadorWav contexto="login" onAudioReady={handleAudioReady}>
          <p className="instrucao2">Diga "Esta é a minha voz"</p>
          {mensagem && <p style={{ marginTop: 30, fontWeight: 600 }}>{mensagem}</p>}
        </GravadorWav>
      </div>
    </div>
  );
};

export default LeituraVoz;