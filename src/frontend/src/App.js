import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginRegistro from './Components/LoginRegistro/LoginRegistro';
import Register from './Components/LoginRegistro/Register';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LoginRegistro />} />
          <Route path="/login" element={<LoginRegistro />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
