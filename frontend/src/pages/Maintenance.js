import React, { useState, useEffect } from 'react';
import { maintenanceService, vehicleService } from '../services/api';
import './Maintenance.css';

function Maintenance() {
  const [alerts, setAlerts] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    vehicle_id: '',
    type: 'service',
    description: '',
    due_date: '',
    status: 'pending'
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [alertsData, vehiclesData] = await Promise.all([
        maintenanceService.getAll(),
        vehicleService.getAll()
      ]);
      setAlerts(alertsData);
      setVehicles(vehiclesData);
      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת הנתונים');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await maintenanceService.update(editingId, formData);
      } else {
        await maintenanceService.create(formData);
      }
      setFormData({
        vehicle_id: '',
        type: 'service',
        description: '',
        due_date: '',
        status: 'pending'
      });
      setEditingId(null);
      loadData();
    } catch (err) {
      setError('שגיאה בשמירת התראה');
      console.error('Error saving alert:', err);
    }
  };

  const handleEdit = (alert) => {
    setFormData({
      vehicle_id: alert.vehicle_id,
      type: alert.type,
      description: alert.description,
      due_date: alert.due_date,
      status: alert.status
    });
    setEditingId(alert.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('האם אתה בטוח שברצונך למחוק התראה זו?')) {
      try {
        await maintenanceService.delete(id);
        loadData();
      } catch (err) {
        setError('שגיאה במחיקת ההתראה');
        console.error('Error deleting alert:', err);
      }
    }
  };

  const handleComplete = async (id) => {
    if (window.confirm('האם אתה בטוח שברצונך לסמן את ההתראה כהושלמה?')) {
      try {
        await maintenanceService.complete(id);
        loadData();
      } catch (err) {
        setError('שגיאה בסימון ההתראה כהושלמה');
        console.error('Error completing alert:', err);
      }
    }
  };

  const getTypeText = (type) => {
    switch (type) {
      case 'service':
        return 'טיפול שוטף';
      case 'repair':
        return 'תיקון';
      case 'inspection':
        return 'בדיקה';
      default:
        return type;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'pending':
        return 'ממתין';
      case 'in_progress':
        return 'בביצוע';
      case 'completed':
        return 'הושלם';
      default:
        return status;
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'pending':
        return 'status-pending';
      case 'in_progress':
        return 'status-in-progress';
      case 'completed':
        return 'status-completed';
      default:
        return '';
    }
  };

  if (loading) {
    return <div className="loading">טוען...</div>;
  }

  return (
    <div className="maintenance-page">
      <h1>ניהול תחזוקה</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="maintenance-form">
        <h2>{editingId ? 'עריכת התראה' : 'התראה חדשה'}</h2>
        
        <div className="form-group">
          <label htmlFor="vehicle_id">רכב:</label>
          <select
            id="vehicle_id"
            name="vehicle_id"
            value={formData.vehicle_id}
            onChange={handleChange}
            required
          >
            <option value="">בחר רכב</option>
            {vehicles.map(vehicle => (
              <option key={vehicle.id} value={vehicle.id}>
                {vehicle.make} {vehicle.model} - {vehicle.license_plate}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="type">סוג:</label>
          <select
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
          >
            <option value="service">טיפול שוטף</option>
            <option value="repair">תיקון</option>
            <option value="inspection">בדיקה</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="description">תיאור:</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="due_date">תאריך יעד:</label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="status">סטטוס:</label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            required
          >
            <option value="pending">ממתין</option>
            <option value="in_progress">בביצוע</option>
            <option value="completed">הושלם</option>
          </select>
        </div>

        <button type="submit" className="submit-button">
          {editingId ? 'עדכן התראה' : 'צור התראה'}
        </button>
        
        {editingId && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setFormData({
                vehicle_id: '',
                type: 'service',
                description: '',
                due_date: '',
                status: 'pending'
              });
            }}
            className="cancel-button"
          >
            ביטול עריכה
          </button>
        )}
      </form>

      <div className="maintenance-list">
        <h2>רשימת התראות</h2>
        <table>
          <thead>
            <tr>
              <th>רכב</th>
              <th>סוג</th>
              <th>תיאור</th>
              <th>תאריך יעד</th>
              <th>סטטוס</th>
              <th>פעולות</th>
            </tr>
          </thead>
          <tbody>
            {alerts.slice(0, 20).map(alert => {
              const vehicle = vehicles.find(v => v.id === alert.vehicle_id);
              return (
                <tr key={alert.id}>
                  <td>
                    {vehicle
                      ? `${vehicle.make} ${vehicle.model} (${vehicle.license_plate})`
                      : 'לא ידוע'}
                  </td>
                  <td>{getTypeText(alert.type)}</td>
                  <td>{alert.description}</td>
                  <td>{new Date(alert.due_date).toLocaleDateString()}</td>
                  <td>
                    <span className={`status-badge ${getStatusClass(alert.status)}`}>
                      {getStatusText(alert.status)}
                    </span>
                  </td>
                  <td>
                    {alert.status !== 'completed' && (
                      <button
                        onClick={() => handleComplete(alert.id)}
                        className="complete-button"
                      >
                        סיים
                      </button>
                    )}
                    <button
                      onClick={() => handleEdit(alert)}
                      className="edit-button"
                    >
                      ערוך
                    </button>
                    <button
                      onClick={() => handleDelete(alert.id)}
                      className="delete-button"
                    >
                      מחק
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Maintenance; 