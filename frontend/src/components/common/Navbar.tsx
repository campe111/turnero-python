// src/components/common/Navbar.tsx
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useState, useEffect } from 'react';

export const Navbar = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className={`navbar navbar-expand-lg navbar-dark bg-primary custom-navbar ${isScrolled ? 'scrolled' : ''}`}>
      <div className="container-fluid container-lg">
        <Link className="navbar-brand" to="/">
          <i className="fas fa-clock me-2"></i>
          <span className="brand-text">Sistema de Turnos</span>
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Alternar navegación"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto align-items-center">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                <i className="fas fa-home me-1"></i>
                <span className="nav-text">Inicio</span>
              </Link>
            </li>
            {isAuthenticated && isAdmin && (
              <li className="nav-item">
                <Link className="nav-link" to="/admin">
                  <i className="fas fa-cog me-1"></i>
                  <span className="nav-text">Panel Admin</span>
                </Link>
              </li>
            )}
            {!isAuthenticated ? (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">
                    <i className="fas fa-sign-in-alt me-1"></i>
                    <span className="nav-text">Iniciar Sesión</span>
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link btn-nav-register" to="/register">
                    <i className="fas fa-user-plus me-1"></i>
                    <span className="nav-text">Registrarse</span>
                  </Link>
                </li>
              </>
            ) : (
              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle user-dropdown"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <i className="fas fa-user-circle me-1"></i>
                  <span className="nav-text user-name">{user?.nombre}</span>
                </a>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li>
                    <a className="dropdown-item" href="#" onClick={(e) => { e.preventDefault(); handleLogout(); }}>
                      <i className="fas fa-sign-out-alt me-2"></i>
                      Cerrar Sesión
                    </a>
                  </li>
                </ul>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

