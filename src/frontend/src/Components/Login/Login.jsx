import React from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';
const Login = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [mensagemErro, setMensagemErro] = useState('');
    const [loading, setLoading] = useState(false);

    // Validação simples de e-mail
    const validarEmail = (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    };
const armazenarToken = (token) => {
    if (token) {
        localStorage.setItem('access_token', token);
    }
};
    const handleSubmit = async (e) => {
        e.preventDefault();
        setMensagemErro('');

        // Validação frontend
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
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok && data.access_token) {
                 armazenarToken(data.access_token);
                // Redireciona para dashboard
                navigate('/dashboard');
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
                            type="text"
                            placeholder='Email'
                            required
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="input-box">
                        <input
                            type="password"
                            placeholder='Senha'
                            required
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />
                    </div>
                    <div className="esqueceu">
                        <a href="#">Esqueceu sua senha?</a>
                    </div>
                    {mensagemErro && <div className="erro">{mensagemErro}</div>}
                    <button type="submit" className='btn' disabled={loading}>
                        {loading ? 'Entrando...' : 'LOGIN'}
                    </button>
                </form>
            </div>
            <div className='blocoAzul'>
                <div className='secao Registro'>
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
