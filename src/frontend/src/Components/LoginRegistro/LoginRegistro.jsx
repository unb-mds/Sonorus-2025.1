import React from 'react';
import './LoginRegistro.css';

const LoginRegistro = () => {
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
        </div>
    );
};

export default LoginRegistro;