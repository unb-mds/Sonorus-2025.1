import { useState } from 'react';
import './ErroCadastro.css';


const ErroCadastro = () => {
  return (
      <div className="erro-card">
        <h1 className="erro-title">Houve um erro no cadastro!</h1>
        <div className="erro-icon">
          <div className="circle">
            <span className="cruz">×</span>
          </div>
        </div>
        <p className="erro-message">Vamos tentar novamente.</p>
      </div>
  );
};

export default ErroCadastro;