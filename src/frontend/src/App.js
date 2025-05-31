import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Components/Login/Login';
import Register from './Components/Registro/Register';
import ErroCadastro from './Components/TelaErro/ErroCadastro';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/erroCadastro" element={<ErroCadastro />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
