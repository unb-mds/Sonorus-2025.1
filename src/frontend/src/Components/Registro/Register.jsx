// src/Components/Registro/Register.jsx
import { useState } from 'react';
import './Register.css';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';

const API_URL = (process.env.REACT_APP_API_URL || "http://localhost:8000/api").replace(/\/$/, "");

const Register = () => {
  const [formData, setFormData] = useState({
    nome: '',
    sobrenome: '',
    email: '',
    senha: '',
    confirmacaoSenha: ''
  });

  const [showSenha, setShowSenha] = useState(false);
  const [showConfirmacaoSenha, setShowConfirmacaoSenha] = useState(false);
  const [emailError, setEmailError] = useState('');
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  // Validação do formato do email
  const validateEmail = email => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  // Validação de domínio usando Cloudflare DNS (com CORS habilitado)
  const validateEmailDomain = async email => {
    try {
      const domain = email.split('@')[1];
      const DNS_API_URL = process.env.REACT_APP_DNS_API_URL;
      const response = await fetch(`${DNS_API_URL}?name=${domain}&type=MX`, {
        headers: { 'Accept': 'application/dns-json' }
      });
      const data = await response.json();
      return data.Answer && data.Answer.length > 0;
    } catch (err) {
      console.error('Erro ao verificar domínio:', err);
      // Em caso de erro na validação DNS, permite passar para validação backend
      return true;
    }
  };

  // Verifica se o email já existe na API
  const checkEmailExists = async email => {
    try {
      const res = await fetch(`${API_URL}/check-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      return res.ok ? (data.exists || false) : data.detail;
    } catch (err) {
      console.error('Erro na requisição checkEmailExists:', err);
      return 'Erro de conexão ao verificar email';
    }
  };

  const handleEmailValidation = async email => {
    if (!email) {
      setEmailError(''); setIsEmailValid(false);
      return;
    }
    if (!validateEmail(email)) {
      setEmailError('Insira um endereço de email válido');
      setIsEmailValid(false);
      return;
    }
    const domainOk = await validateEmailDomain(email);
    if (!domainOk) {
      setEmailError('O domínio do email não existe ou não está configurado para receber emails');
      setIsEmailValid(false);
      return;
    }
    const existsCheck = await checkEmailExists(email);
    if (existsCheck === true) {
      setEmailError('Esse email já está sendo usado');
      setIsEmailValid(false);
    } else if (typeof existsCheck === 'string') {
      setEmailError(existsCheck);
      setIsEmailValid(false);
    } else {
      setEmailError('');
      setIsEmailValid(true);
    }
  };

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(f => ({ ...f, [name]: value }));
    if (name === 'email') handleEmailValidation(value);
  };

  const handleSubmit = async e => {
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
      const res = await fetch(`${API_URL}/registrar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          nome: formData.nome,
          sobrenome: formData.sobrenome,
          email: formData.email,
          senha: formData.senha
        })
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Erro no cadastro');
      }
      navigate('/cadastro-voz', { state: { email: formData.email } });
    } catch (err) {
      console.error('Erro no cadastro:', err);
      navigate('/erroCadastro');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="register-container">
      <div className="container">
        <div className="left-panel">
          <img src="/sonorus_ed.png" alt="Logo Sonorus" className="left-panel-icon" />
          <h2>Olá!</h2>
          <p>Já tem cadastro? Entre agora!</p>
          <button className="btn-outline" onClick={() => navigate('/login')}>
            FAÇA LOGIN
          </button>
        </div>
        <div className="right-panel">
          <h2>Cadastre-se</h2>
          {submitError && <div className="submit-error">{submitError}</div>}
          <form onSubmit={handleSubmit}>
            <div className="input-row">
              <input
                name="nome"
                placeholder="Nome"
                required
                value={formData.nome}
                onChange={handleChange}
              />
              <input
                name="sobrenome"
                placeholder="Sobrenome"
                required
                value={formData.sobrenome}
                onChange={handleChange}
              />
            </div>
            <div className="input-with-error">
              <input
                name="email"
                type="email"
                placeholder="Seu melhor e-mail"
                required
                value={formData.email}
                onChange={handleChange}
                className={emailError ? 'input-error' : ''}
              />
              {emailError && <span className="error-message">{emailError}</span>}
            </div>
            <div className="password-input">
              <input
                name="senha"
                type={showSenha ? 'text' : 'password'}
                placeholder="Senha"
                required
                minLength="6"
                value={formData.senha}
                onChange={handleChange}
              />
              <span
                className="password-toggle"
                aria-label="toggle password visibility"
                onClick={() => setShowSenha(!showSenha)}
              >
                {showSenha ? <EyeOff size={18} /> : <Eye size={18} />}
              </span>
            </div>
            <div className="password-input">
              <input
                name="confirmacaoSenha"
                type={showConfirmacaoSenha ? 'text' : 'password'}
                placeholder="Confirme a senha"
                required
                value={formData.confirmacaoSenha}
                onChange={handleChange}
              />
              <span
                className="password-toggle"
                aria-label="toggle password visibility"
                onClick={() => setShowConfirmacaoSenha(!showConfirmacaoSenha)}
              >
                {showConfirmacaoSenha ? <EyeOff size={18} /> : <Eye size={18} />}
              </span>
            </div>
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
