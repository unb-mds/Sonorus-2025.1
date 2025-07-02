import { useState } from 'react';
import './ErroLeitura.css';
import { useNavigate } from 'react-router-dom';

const ErroLeitura = () => {
  const navigate = useNavigate();

  const handleVoltarLogin = () => {
    navigate('/login');
  };

  return (
    <div className="erro-card2">
      <h1 className="erro-title2">Algo deu errado.</h1>
      <div className="erro-icon2">
        <div className="circle2">
          <span className="cruz2">×</span>
        </div>
      </div>
      <button
        className="botao-voltar-login2"
        onClick={handleVoltarLogin}
      >
        Voltar para o Login
      </button>
    </div>
  );
};

export default ErroLeitura;