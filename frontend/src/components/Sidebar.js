import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

function Sidebar() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <img src="/logo.png" alt="גלגל עומר" />
          <h1>גלגל עומר</h1>
        </div>
      </div>

      <nav className="sidebar-nav">
        <Link to="/" className={`nav-item ${isActive('/') ? 'active' : ''}`}>
          <i className="fas fa-home"></i>
          <span>לוח בקרה</span>
        </Link>

        <Link to="/customers" className={`nav-item ${isActive('/customers') ? 'active' : ''}`}>
          <i className="fas fa-users"></i>
          <span>לקוחות</span>
        </Link>

        <Link to="/cars" className={`nav-item ${isActive('/cars') ? 'active' : ''}`}>
          <i className="fas fa-car"></i>
          <span>רכבים</span>
        </Link>

        <Link to="/rentals" className={`nav-item ${isActive('/rentals') ? 'active' : ''}`}>
          <i className="fas fa-key"></i>
          <span>השכרות</span>
        </Link>

        <Link to="/maintenance" className={`nav-item ${isActive('/maintenance') ? 'active' : ''}`}>
          <i className="fas fa-tools"></i>
          <span>תחזוקה</span>
        </Link>
      </nav>

      <div className="sidebar-footer">
        <div className="user-info">
          <i className="fas fa-user-circle"></i>
          <span>משתמש מערכת</span>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;