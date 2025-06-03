import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Components/Login/Login';
import Register from './Components/Registro/Register';
import ErroCadastro from './Components/TelaErro/ErroCadastro';
import SucessoCadastro from './Components/TelaFuncionou/SucessoCadastro';
import VozCadastrada from './Components/TelaFuncionou/VozCadastrada';
import VozCadastro from './Components/TelaLeituraVoz/VozCadastro';
import VozLogin from './Components/TelaLeituraVoz/VozLogin';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/erroCadastro" element={<ErroCadastro />} />
          <Route path="/sucessocadastro" element={<SucessoCadastro />} />
          <Route path="/vozcadastrada" element={<VozCadastrada />} />
          <Route path="/cadastro-voz" element={<VozCadastro />} />
          <Route path="/login-voz" element={<VozLogin />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
