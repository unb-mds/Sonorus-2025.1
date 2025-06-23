import { useState } from 'react';
import './Register.css';
import { useNavigate } from 'react-router-dom';

const API_URL = (process.env.REACT_APP_API_URL || "http://localhost:8000/api").replace(/\/$/, "");

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

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const checkEmailExists = async (email) => {
    try {
      const response = await fetch(`${API_URL}/check-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
      if (response.ok) {
        // E-mail disponível
        return false;
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao verificar email');
      }
    } catch (error) {
      if (error.message === 'E-mail já cadastrado no sistema') {
        return true;
      }
      return error.message;
    }
  };

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
    if (emailExists === true) {
      setEmailError('Esse email já está sendo usado');
      setIsEmailValid(false);
    } else if (typeof emailExists === 'string') {
      setEmailError(emailExists);
      setIsEmailValid(false);
    } else {
      setEmailError('');
      setIsEmailValid(true);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (name === 'email') {
      handleEmailValidation(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');
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
      const response = await fetch(`${API_URL}/registrar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nome: formData.nome,
          sobrenome: formData.sobrenome,
          email: formData.email,
          senha: formData.senha
        }),
        credentials: 'include'
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro no cadastro');
      }

      navigate('/cadastro-voz', { 
        state: { email: formData.email }
      });
    } catch (error) {
      console.error('Erro no cadastro:', error);
      navigate('/erroCadastro');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="register-container">
      <div className="container">
        <div className="left-panel">
          <h2>Olá!</h2>
          <p>Já tem cadastro? Entre agora!</p>
          <button className="btn-outline" onClick={handleLoginClick}>
            FAÇA LOGIN
          </button>
        </div>
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