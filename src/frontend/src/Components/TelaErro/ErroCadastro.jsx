import './ErroCadastro.css';
import { useNavigate } from 'react-router-dom';

const ErroCadastro = () => {
  const navigate = useNavigate();

  const handleVoltarRegister = () => {
    navigate('/Register');
  };

  return (
    <div className="erro-card1">
      <h1 className="erro-title1">Houve um erro no cadastro!</h1>
      <div className="erro-icon1">
        <div className="circle1">
          <span className="cruz1">×</span>
        </div>
      </div>
      <button
        className="botao-voltar-Register"
        onClick={handleVoltarRegister}
      >
        Voltar para o Cadastro
      </button>
    </div>
  );
};

export default ErroCadastro;