import React from 'react';
import './LoginRegistro.css';

const LoginRegistro = () => {
    return (
        <div className='Wrapper'>
            <div className='form-box Entrar'>
                <form action=''>
                    <h1>Entrar</h1>
                        <div className="input-box">
                            <input type="text" placeholder='Usuário' required />
                        </div>
                        <div className="input-box">
                            <input type="password" placeholder='Senha' required />
                        </div>

                        <div className="remember-forgot">
                            <label>
                                <input type="checkbox"/>
                                Lembre de mim
                            </label>
                            <a href="#">Esqueceu sua senha?</a>
                        </div>
                        <button type="submit" className='btn'>Login</button>

                        <div className="register-link">
                            <p>Primeira vez? Faça seu cadastro! <a href="#">
                                <button type="submit" className='btn'>Cadastre-se</button></a>
                            </p>
                        </div>
                </form>
            </div>
        </div>
    );
};

export default LoginRegistro;