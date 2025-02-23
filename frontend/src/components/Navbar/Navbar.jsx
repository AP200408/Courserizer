import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  // Optional: If you want to close the menu after clicking a link
  const handleLinkClick = () => setMenuOpen(false);

  return (
    <header>
      <h1 style={{ color: "black" }}>Courserizer</h1>
      {/* Hamburger Toggle Button */}
      <button
        className="toggle-button"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        <span className="bar"></span>
        <span className="bar"></span>
        <span className="bar"></span>
      </button>
      {/* Navigation Menu */}
      <nav className={`nav ${menuOpen ? "active" : ""}`}>
        <Link className="ele" to="/" onClick={handleLinkClick}>
          Home
        </Link>
        <Link className="ele" to="/Korsy" onClick={handleLinkClick}>
          KorsyAI
        </Link>
        <div className="ele dropdown">
          <span>Get Started</span>
          <ul className="dropdown-content">
            <li>
              <Link to="/howtouse" onClick={handleLinkClick}>
                How to Use
              </Link>
            </li>
            <li>
              <Link to="/services" onClick={handleLinkClick}>
                Our Services
              </Link>
            </li>
            <li>
              <Link to="/procedures" onClick={handleLinkClick}>
                Procedures
              </Link>
            </li>
          </ul>
        </div>
        <Link className="ele" to="/about" onClick={handleLinkClick}>
          About
        </Link>
        <Link className="ele" to="/contact" onClick={handleLinkClick}>
          Contact
        </Link>
      </nav>
    </header>
  );
}

export default Navbar;
