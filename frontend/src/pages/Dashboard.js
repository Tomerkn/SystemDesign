import React, { useState, useEffect } from 'react';
import { customerService, vehicleService, rentalService, maintenanceService } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    totalCustomers: 0,
    totalVehicles: 0,
    activeRentals: 0,
    pendingMaintenance: 0
  });
  const [recentRentals, setRecentRentals] = useState([]);
  const [upcomingMaintenance, setUpcomingMaintenance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [
        customers,
        vehicles,
        rentals,
        maintenance
      ] = await Promise.all([
        customerService.getAll(),
        vehicleService.getAll(),
        rentalService.getAll(),
        maintenanceService.getAll()
      ]);

      // חישוב סטטיסטיקות
      const activeRentals = rentals.filter(r => r.status === 'active');
      const pendingMaintenance = maintenance.filter(m => m.status !== 'completed');

      setStats({
        totalCustomers: customers.length,
        totalVehicles: vehicles.length,
        activeRentals: activeRentals.length,
        pendingMaintenance: pendingMaintenance.length
      });

      // השכרות אחרונות
      const sortedRentals = [...rentals]
        .sort((a, b) => new Date(b.start_date) - new Date(a.start_date))
        .slice(0, 5);
      setRecentRentals(sortedRentals);

      // תחזוקה קרובה
      const sortedMaintenance = [...maintenance]
        .filter(m => m.status !== 'completed')
        .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
        .slice(0, 5);
      setUpcomingMaintenance(sortedMaintenance);

      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת הנתונים');
      console.error('Error loading dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active':
        return 'פעיל';
      case 'completed':
        return 'הוחזר';
      case 'cancelled':
        return 'בוטל';
      default:
        return status;
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'active':
        return 'status-active';
      case 'completed':
        return 'status-completed';
      case 'cancelled':
        return 'status-cancelled';
      default:
        return '';
    }
  };

  if (loading) {
    return <div className="loading">טוען...</div>;
  }

  return (
    <div className="dashboard-page">
      <h1>לוח בקרה</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>לקוחות</h3>
          <div className="stat-value">{stats.totalCustomers}</div>
        </div>
        
        <div className="stat-card">
          <h3>רכבים</h3>
          <div className="stat-value">{stats.totalVehicles}</div>
        </div>
        
        <div className="stat-card">
          <h3>השכרות פעילות</h3>
          <div className="stat-value">{stats.activeRentals}</div>
        </div>
        
        <div className="stat-card">
          <h3>תחזוקה ממתינה</h3>
          <div className="stat-value">{stats.pendingMaintenance}</div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h2>השכרות אחרונות</h2>
          <table>
            <thead>
              <tr>
                <th>לקוח</th>
                <th>רכב</th>
                <th>תאריך התחלה</th>
                <th>סטטוס</th>
              </tr>
            </thead>
            <tbody>
              {recentRentals.map(rental => (
                <tr key={rental.id}>
                  <td>{rental.customer_name}</td>
                  <td>{rental.vehicle_info}</td>
                  <td>{new Date(rental.start_date).toLocaleDateString()}</td>
                  <td>
                    <span className={`status-badge ${getStatusClass(rental.status)}`}>
                      {getStatusText(rental.status)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="dashboard-card">
          <h2>תחזוקה קרובה</h2>
          <table>
            <thead>
              <tr>
                <th>רכב</th>
                <th>סוג</th>
                <th>תאריך יעד</th>
                <th>סטטוס</th>
              </tr>
            </thead>
            <tbody>
              {upcomingMaintenance.map(alert => (
                <tr key={alert.id}>
                  <td>{alert.vehicle_info}</td>
                  <td>{alert.type}</td>
                  <td>{new Date(alert.due_date).toLocaleDateString()}</td>
                  <td>
                    <span className={`status-badge ${getStatusClass(alert.status)}`}>
                      {getStatusText(alert.status)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard; 