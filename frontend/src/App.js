import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import HomePage from './pages/HomePage/HomePage';
import Footer from './components/Footer';
import './App.css';
import Header from './components/Header';
import LoginPage from './pages/LoginPage/LoginPage';

function App() {
  return (
    <Router>
      <Header />
      <main>
        <Container>
          <Routes>
            <Route path='/' element={<HomePage />}></Route>
            <Route path='/login' element={<LoginPage />}></Route>
          </Routes>
        </Container>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
