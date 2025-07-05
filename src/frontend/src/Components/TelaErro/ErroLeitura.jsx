import './ErroLeitura.css';


const ErroLeitura = () => {
  return (
      <div className="erro-card">
        <h1 className="erro-title">Algo deu errado.</h1>
        <div className="erro-icon">
          <div className="circle">
            <span className="cruz">×</span>
          </div>
        </div>
        <p className="erro-message">Vamos tentar novamente.</p>
      </div>
  );
};

export default ErroLeitura;