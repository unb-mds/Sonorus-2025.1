import { useState } from 'react';
import './VozCadastrada.css';

const VozCadastrada = () => {
  return (
    <div className="sucesso-card">
      <h1 className="sucesso-title">Sua voz foi cadastrada!</h1>
      <div className="sucesso-icon">
        <div className="circle">
          <span className="check">✓</span>
        </div>
      </div>
      <p className="sucesso-message">Agora você pode usar a voz para logar!</p>
    </div>
  );
};

export default VozCadastrada;
