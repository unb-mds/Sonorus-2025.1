import React from 'react';
import './ErroLeitura.css';
import { useNavigate } from 'react-router-dom';

const ErroLeitura = () => {
  const navigate = useNavigate();

  const handleVoltarLogin = () => {
    navigate('/login');
  };

  return (
    <div className="erro-card">
      <h1 className="erro-title">Algo deu errado.</h1>
      <div className="erro-icon">
        <div className="circle">
          <span className="cruz">×</span>
        </div>
      </div>
      <button
        className="botao-voltar-login"
        onClick={handleVoltarLogin}
      >
        Voltar para o Login
      </button>
    </div>
  );
};

export default ErroLeitura;