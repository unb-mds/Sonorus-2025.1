import React from 'react';
import './ErroCadastro.css';
import { useNavigate } from 'react-router-dom';

const ErroCadastro = () => {
  const navigate = useNavigate();

  const handleVoltarLogin = () => {
    navigate('/login');
  };

  return (
    <div className="erro-card">
      <h1 className="erro-title">Houve um erro no cadastro!</h1>
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

export default ErroCadastro;