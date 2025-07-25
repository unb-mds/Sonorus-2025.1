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
  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  // Validação de domínio usando Cloudflare DNS (com CORS habilitado)
  const validateEmailDomain = async (email) => {
    try {
      const domain = email.split('@')[1];
      const DNS_API_URL = process.env.REACT_APP_DNS_API_URL;
      const response = await fetch(`${DNS_API_URL}?name=${domain}&type=MX`, {
        headers: {
          'Accept': 'application/dns-json'
        }
      });
      const data = await response.json();
      return data.Answer && data.Answer.length > 0;
    } catch (error) {
      console.error('Erro ao verificar domínio:', error);
      // Em caso de erro na validação DNS, permite o email passar
      // para que seja validado pelo backend
      return true;
    }
  };

  // Verifica se o email já existe na API
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
        const data = await response.json();
        return data.exists || false;
      } else {
        const errorData = await response.json();
        return errorData.detail || 'Erro ao verificar email';
      }
    } catch (error) {
      console.error('Erro na requisição checkEmailExists:', error);
      return 'Erro de conexão ao verificar email';
    }
  };

  const handleEmailValidation = async (email) => {
    if (email === '') {
      setEmailError('');
      setIsEmailValid(false);
      return;
    }

    // Primeiro, valida o formato do email
    if (!validateEmail(email)) {
      setEmailError('Insira um endereço de email válido');
      setIsEmailValid(false);
      return;
    }

    // Segunda validação: domínio via DNS
    const isDomainValid = await validateEmailDomain(email);
    if (!isDomainValid) {
      setEmailError('O domínio do email não existe ou não está configurado para receber emails');
      setIsEmailValid(false);
      return;
    }

    // Terceira validação: verifica no backend se email já existe
    const emailCheck = await checkEmailExists(email);
    
    if (emailCheck === true) {
      setEmailError('Esse email já está sendo usado');
      setIsEmailValid(false);
    } else if (typeof emailCheck === 'string') {
      setEmailError(emailCheck);
      setIsEmailValid(false);
    } else {
      setEmailError('');
      setIsEmailValid(true);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (name === 'email') handleEmailValidation(value);
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

      navigate('/cadastro-voz', { state: { email: formData.email } });
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
          <img src="/sonorus_ed.png" alt="Logo Sonorus" className="left-panel-icon" />
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

            {/* Campo Senha */}
            <div className="password-input">
              <input
                type={showSenha ? 'text' : 'password'}
                name="senha"
                placeholder="Senha"
                value={formData.senha}
                onChange={handleChange}
                required
                minLength="6"
              />
              <span
                className="password-toggle"
                onClick={() => setShowSenha(!showSenha)}
              >
                {showSenha ? <EyeOff size={18} /> : <Eye size={18} />}
              </span>
            </div>

            <div className="password-input">
              <input
                type={showConfirmacaoSenha ? 'text' : 'password'}
                name="confirmacaoSenha"
                placeholder="Confirme a senha"
                value={formData.confirmacaoSenha}
                onChange={handleChange}
                required
              />
              <span
                className="password-toggle"
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