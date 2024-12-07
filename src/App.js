import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import ChatbotPage from './components/ChatbotPage';
import Navbar from './components/Navbar';
import './styles.css';

function App() {
    const [user, setUser] = useState(null);

    return (
        <Router>
            <Navbar />
            <Routes>
                <Route
                    path="/"
                    element={<LoginPage setUser={setUser} />}
                />
                <Route
                    path="/chatbot"
                    element={user ? <ChatbotPage user={user} /> : <p>Please log in first.</p>}
                />
            </Routes>
        </Router>
    );
}

export default App;
