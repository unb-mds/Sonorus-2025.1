import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Components/LoginRegistro/Login';
import Register from './Components/LoginRegistro/Register';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
