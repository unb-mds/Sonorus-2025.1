import React from 'react';
import './Register.css';

const Register = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Lógica de cadastro aqui
  };

  return (
    <div className="register-container">
      <div className="container">
        {/* Painel da Esquerda (Imagem de fundo) */}
        <div className="left-panel">
          <h2>Olá!</h2>
          <p>Já tem cadastro? Entre agora!</p>
          <button className="btn-outline">FAÇA LOGIN</button>
        </div>

        {/* Painel da Direita (Formulário de cadastro) */}
        <div className="right-panel">
          <h2>Cadastre-se</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-row">
              <input type="text" placeholder="Nome" required />
              <input type="text" placeholder="Último nome" required />
            </div>
            <input type="email" placeholder="Seu melhor email" required />
            <input type="password" placeholder="Senha" required />
            <input type="password" placeholder="Confirme a senha" required />
            <button type="submit" className="btn-solid">CONTINUAR</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;