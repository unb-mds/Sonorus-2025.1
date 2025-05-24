import React from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();

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
                    <div className="input-box">
                        <input type="password" placeholder='Senha' required />
                    </div>
                    <div className="esqueceu">
                        <a href="#">Esqueceu sua senha?</a>
                    </div>
                    <button type="submit" className='btn'>LOGIN</button>
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
