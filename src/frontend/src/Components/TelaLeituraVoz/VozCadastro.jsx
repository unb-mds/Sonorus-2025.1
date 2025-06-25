import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import GravadorWav from '../GravadorWav';
import './VozCadastro.css';

const LeituraVoz = () => {
  const [mensagem, setMensagem] = useState('');
  const navigate = useNavigate();
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  const handleAudioReady = async (blob) => {
    setMensagem('Enviando áudio...');
    const formData = new FormData();
    formData.append('arquivo', blob, 'voz.wav');
    try {
      const response = await fetch(`${API_URL}/registrar-voz`, {
        method: 'POST',
        credentials: 'include',
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

  return (
    <div className="containerr">
      <div className="conteudo">
        <h2 className="titulo">Vamos cadastrar sua voz</h2>
        <GravadorWav contexto="cadastro" onAudioReady={handleAudioReady}>
          <p className="instrucao">Diga "Esta é a minha voz"</p>
          {mensagem && <p style={{ marginTop: 30, fontWeight: 600 }}>{mensagem}</p>}
        </GravadorWav>
      </div>
    </div>
  );
};

export default LeituraVoz;