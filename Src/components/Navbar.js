import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <Link to="/">Login</Link>
      <Link to="/chatbot">Chatbot</Link>
    </nav>
  );
};

export default Navbar;
