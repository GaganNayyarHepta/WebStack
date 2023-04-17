import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import HomePage from './pages/HomePage/HomePage';
import Footer from './components/Footer';
import './App.css';

function App() {
  return (
    <Router>
      <main>
        <Container>
          <Routes>
            <Route path='/' element={<HomePage />}></Route>
          </Routes>
        </Container>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
