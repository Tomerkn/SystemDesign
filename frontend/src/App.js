import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Cars from './pages/Cars';
import Rentals from './pages/Rentals';
import Maintenance from './pages/Maintenance';
import Booking from './pages/Booking';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/cars" element={<Cars />} />
            <Route path="/rentals" element={<Rentals />} />
            <Route path="/maintenance" element={<Maintenance />} />
            <Route path="/booking" element={<Booking />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App; 