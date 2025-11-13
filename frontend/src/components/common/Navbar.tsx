// src/components/common/Navbar.tsx
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const Navbar = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand" to="/">
          <i className="fas fa-clock me-2"></i>
          Sistema de Turnos
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-label="Alternar navegación"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                <i className="fas fa-home me-1"></i>
                Inicio
              </Link>
            </li>
            {isAuthenticated && isAdmin && (
              <li className="nav-item">
                <Link className="nav-link" to="/admin">
                  <i className="fas fa-cog me-1"></i>
                  Panel Admin
                </Link>
              </li>
            )}
            {!isAuthenticated ? (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">
                    <i className="fas fa-sign-in-alt me-1"></i>
                    Iniciar Sesión
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/register">
                    <i className="fas fa-user-plus me-1"></i>
                    Registrarse
                  </Link>
                </li>
              </>
            ) : (
              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <i className="fas fa-user me-1"></i>
                  {user?.nombre}
                </a>
                <ul className="dropdown-menu">
                  <li>
                    <a className="dropdown-item" href="#" onClick={handleLogout}>
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

