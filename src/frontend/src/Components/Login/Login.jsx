import { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';

const Login = () => {
    const navigate = useNavigate();
    const [showSenha, setShowSenha] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [mensagemErro, setMensagemErro] = useState('');
    const [loading, setLoading] = useState(false);

    const validarEmail = (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMensagemErro('');

        if (!email || !password) {
            setMensagemErro('Preencha todos os campos.');
            return;
        }
        if (!validarEmail(email)) {
            setMensagemErro('Formato de e-mail inválido.');
            return;
        }

        setLoading(true);

        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);

        try {
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/login`, {
                method: 'POST',
                body: formData,
                credentials: 'include', // ESSENCIAL para cookies HttpOnly
            });

            const data = await response.json();

            if (response.ok) {
                navigate('/login-voz');
            } else if (data.detail) {
                setMensagemErro(data.detail);
            } else {
                setMensagemErro('Erro ao fazer login');
            }
        } catch (error) {
            setMensagemErro('Erro de conexão com o servidor');
        } finally {
            setLoading(false);
        }
    };

    const handleCadastro = () => {
        navigate('/register');
    };

    return (
        <div className='blocoPreto'>
            <div className='form-box Entrar'>
                <form onSubmit={handleSubmit}>
                    <h1>Entrar</h1>
                    <div className="input-box">
                        <input
                            type="email"
                            placeholder='Email'
                            required
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />
                    </div>

                    {/* Campo de Senha com olho */}
                    <div className="input-box password-input">
                        <input
                            type={showSenha ? 'text' : 'password'}
                            placeholder='Senha'
                            required
                        />
                        <span
                            className="password-toggle"
                            onClick={() => setShowSenha(!showSenha)}
                        >
                            {showSenha ? <EyeOff size={18} /> : <Eye size={18} />}
                        </span>
                    </div>

                    <div className="esqueceu">
                        <button 
                            type="button" 
                            className="link-button"
                            onClick={() => setMensagemErro('Funcionalidade em desenvolvimento')}
                        >
                            Esqueceu sua senha?
                        </button>
                    </div>
                    {mensagemErro && <div className="erro">{mensagemErro}</div>}
                    <button type="submit" className='btn' disabled={loading}>
                        {loading ? 'Entrando...' : 'LOGIN'}
                    </button>
                </form>
            </div>
            <div className='blocoAzul'>
                <div className='secao Registro'>
                    <img src="/sonorus_ed.png" alt="Logo Sonorus" className="left-panel-icon2" />
                    <h1>Bem-vindo</h1>
                    <p>Primeira vez? Faça seu cadastro!</p>
                    <button className='btntransp-outline' onClick={handleCadastro}>
                        CADASTRE-SE
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Login;