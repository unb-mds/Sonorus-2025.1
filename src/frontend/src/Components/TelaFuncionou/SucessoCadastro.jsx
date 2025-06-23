import React from 'react';
import './SucessoCadastro.css';
import { useNavigate } from 'react-router-dom';

const SucessoCadastro = () => {
  const navigate = useNavigate();

  const handleVoltarLogin = () => {
    navigate('/login'); 
  };

  return (
    <div className="sucesso-card">
      <h1 className="sucesso-title">Autenticação realizada!</h1>
      <div className="sucesso-icon">
        <div className="circle">
          <span className="check">✓</span>
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

export default SucessoCadastro;