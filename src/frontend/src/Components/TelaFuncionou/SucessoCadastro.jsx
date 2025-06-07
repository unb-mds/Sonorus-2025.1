import React from 'react';
import './SucessoCadastro.css';

const SucessoCadastro = () => {
  return (
    <div className="sucesso-card">
      <h1 className="sucesso-title">Autenticação realizada!</h1>
      <div className="sucesso-icon">
        <div className="circle">
          <span className="check">✓</span>
        </div>
      </div>
      <p className="sucesso-message">Bem-vindo!</p>
    </div>
  );
};

export default SucessoCadastro;

