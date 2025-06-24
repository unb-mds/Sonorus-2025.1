import React, { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';

const Login = () => {
    const navigate = useNavigate();
    const [showSenha, setShowSenha] = useState(false);

    const handleCadastro = () => {
        navigate('/register');
    };

    return (
        <div className='blocoPreto'>
            <div className='form-box Entrar'>
                <form action=''>
                    <h1>Entrar</h1>
                    <div className="input-box">
                        <input type="text" placeholder='Email' required />
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
                        <a href="#">Esqueceu sua senha?</a>
                    </div>
                    <button type="submit" className='btn'>LOGIN</button>
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
