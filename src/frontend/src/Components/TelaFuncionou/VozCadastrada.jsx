import React from 'react';
import './VozCadastrada.css';
import { useNavigate } from 'react-router-dom';

const VozCadastrada = () => {
  const navigate = useNavigate();

  const handleVoltarLogin = () => {
    navigate('/login');
  };

  return (
    <div className="sucesso-card2">
      <h1 className="sucesso-title2">Sua voz foi cadastrada!</h1>
      <div className="sucesso-icon2">
        <div className="circle2">
          <span className="check2">✓</span>
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

export default VozCadastrada;
