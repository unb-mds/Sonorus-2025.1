import { useState } from 'react';
import './SucessoCadastro.css';
import { useNavigate } from 'react-router-dom';

const SucessoCadastro = () => {
  const navigate = useNavigate();

  const handleVoltarLogin = () => {
    navigate('/login'); 
  };

  return (
    <div className="sucesso-card1">
      <h1 className="sucesso-title1">Autenticação realizada!</h1>
      <div className="sucesso-icon1">
        <div className="circle1">
          <span className="check1">✓</span>
        </div>
      </div>
      <button
        className="botao-voltar-login1"
        onClick={handleVoltarLogin}
      >
        Voltar para o Login
      </button>
    </div>
  );
};

export default SucessoCadastro;