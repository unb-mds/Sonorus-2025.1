import React, { useState } from 'react';
import './Register.css';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({
    nome: '',
    sobrenome: '',
    email: '',
    senha: '',
    confirmacaoSenha: ''
  });
  
  const [emailError, setEmailError] = useState('');
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  // validação do email
  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  // verifica se o email já existe na API
  const checkEmailExists = async (email) => {
    try {
      const response = await fetch('http://localhost:8000/api/check-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
      
      if (!response.ok) {
        throw new Error('Erro ao verificar email');
      }
      
      const data = await response.json();
      return data.exists;
    } catch (error) {
      console.error('Erro na verificação de email:', error);
      return false;
    }
  };

  // manipulador de mudanças nos campos
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // validação em tempo real apenas para o email
    if (name === 'email') {
      handleEmailValidation(value);
    }
  };

  // validação do email
  const handleEmailValidation = async (email) => {
    if (email === '') {
      setEmailError('');
      setIsEmailValid(false);
      return;
    }
    
    if (!validateEmail(email)) {
      setEmailError('Insira um endereço de email válido');
      setIsEmailValid(false);
      return;
    }
    
    const emailExists = await checkEmailExists(email);
    if (emailExists) {
      setEmailError('Esse email já está sendo usado');
      setIsEmailValid(false);
    } else {
      setEmailError('');
      setIsEmailValid(true);
    }
  };

  // envio do formulário para o FastAPI
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');
    
    // validação adicional da senha
    if (formData.senha !== formData.confirmacaoSenha) {
      setSubmitError('As senhas não coincidem');
      return;
    }
    
    if (!isEmailValid) {
      setSubmitError('Por favor, corrija os erros no formulário');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          first_name: formData.nome,
          last_name: formData.sobrenome,
          email: formData.email,
          password: formData.senha
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro no cadastro');
      }
      
      // redireciona para a etapa de biometria por voz
      navigate('/cadastro-voz', { 
        state: { 
          email: formData.email,
          userId: (await response.json()).user_id // supondo que a API retorne o ID
        } 
      });
    } catch (error) {
      console.error('Erro no cadastro:', error);
      setSubmitError(error.message || 'Erro ao processar cadastro');
    } finally {
      setIsSubmitting(false);
    }
  };

  // navegação para a página de login
  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="register-container">
      <div className="container">
        {/* Painel da Esquerda (Login) */}
        <div className="left-panel">
          <h2>Olá!</h2>
          <p>Já tem cadastro? Entre agora!</p>
          <button 
            className="btn-outline"
            onClick={handleLoginClick}
          >
            FAÇA LOGIN
          </button>
        </div>

        {/* Painel da Direita (Formulário de cadastro) */}
        <div className="right-panel">
          <h2>Cadastre-se</h2>
          {submitError && <div className="submit-error">{submitError}</div>}
          <form onSubmit={handleSubmit}>
            <div className="input-row">
              <input
                type="text"
                name="nome"
                placeholder="Nome"
                value={formData.nome}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="sobrenome"
                placeholder="Sobrenome"
                value={formData.sobrenome}
                onChange={handleChange}
                required
              />
            </div>
            <div className="input-with-error">
              <input
                type="email"
                name="email"
                placeholder="Seu melhor e-mail"
                value={formData.email}
                onChange={handleChange}
                className={emailError ? 'input-error' : ''}
                required
              />
              {emailError && <span className="error-message">{emailError}</span>}
            </div>
            <input
              type="password"
              name="senha"
              placeholder="Senha"
              value={formData.senha}
              onChange={handleChange}
              required
              minLength="6"
            />
            <input
              type="password"
              name="confirmacaoSenha"
              placeholder="Confirme a senha"
              value={formData.confirmacaoSenha}
              onChange={handleChange}
              required
            />
            <button
              type="submit"
              className="btn-solid"
              disabled={!isEmailValid || isSubmitting}
            >
              {isSubmitting ? 'PROCESSANDO...' : 'CONTINUAR'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;