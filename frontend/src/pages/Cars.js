import React, { useState, useEffect } from 'react';
import { vehicleService } from '../services/api';
import './Cars.css';

function Cars() {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const currentYear = new Date().getFullYear();
  const [formData, setFormData] = useState({
    license_plate: '',
    brand: '',
    model: '',
    year: currentYear,
    status: 'available'
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    loadVehicles();
  }, []);

  const loadVehicles = async () => {
    try {
      setLoading(true);
      const data = await vehicleService.getAll();
      setVehicles(data);
      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת הרכבים');
      console.error('Error loading vehicles:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'year' ? Number(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await vehicleService.update(editingId, formData);
      } else {
        await vehicleService.create(formData);
      }
      setFormData({
        license_plate: '',
        brand: '',
        model: '',
        year: currentYear,
        status: 'available'
      });
      setEditingId(null);
      loadVehicles();
    } catch (err) {
      setError('שגיאה בשמירת הרכב');
      console.error('Error saving vehicle:', err);
    }
  };

  const handleEdit = (vehicle) => {
    setFormData({
      license_plate: vehicle.license_plate,
      brand: vehicle.brand,
      model: vehicle.model,
      year: vehicle.year,
      status: vehicle.status
    });
    setEditingId(vehicle.license_plate);
  };

  const handleDelete = async (license_plate) => {
    if (window.confirm('האם אתה בטוח שברצונך למחוק רכב זה?')) {
      try {
        await vehicleService.delete(license_plate);
        loadVehicles();
      } catch (err) {
        setError('שגיאה במחיקת הרכב');
        console.error('Error deleting vehicle:', err);
      }
    }
  };

  const handleStatusChange = async (license_plate, newStatus) => {
    try {
      await vehicleService.updateStatus(license_plate, newStatus);
      loadVehicles();
    } catch (err) {
      setError('שגיאה בעדכון סטטוס הרכב');
      console.error('Error updating vehicle status:', err);
    }
  };

  if (loading) {
    return <div className="loading">טוען...</div>;
  }

  return (
    <div className="cars-page">
      <h1>ניהול רכבים</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="car-form">
        <h2>{editingId ? 'עריכת רכב' : 'הוספת רכב חדש'}</h2>
        
        <div className="form-group">
          <label htmlFor="license_plate">מספר רישוי:</label>
          <input
            type="text"
            id="license_plate"
            name="license_plate"
            value={formData.license_plate}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="brand">יצרן:</label>
          <input
            type="text"
            id="brand"
            name="brand"
            value={formData.brand}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="model">דגם:</label>
          <input
            type="text"
            id="model"
            name="model"
            value={formData.model}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="year">שנת ייצור:</label>
          <input
            type="number"
            id="year"
            name="year"
            value={formData.year}
            min="1900"
            max={currentYear}
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
          >
            <option value="available">זמין</option>
            <option value="rented">מושכר</option>
            <option value="maintenance">בטיפול</option>
          </select>
        </div>

        <button type="submit" className="submit-button">
          {editingId ? 'עדכן רכב' : 'הוסף רכב'}
        </button>
        
        {editingId && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setFormData({ license_plate: '', brand: '', model: '', year: currentYear, status: 'available' });
            }}
            className="cancel-button"
          >
            ביטול עריכה
          </button>
        )}
      </form>

      <div className="cars-list">
        <h2>רשימת רכבים</h2>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>יצרן</th>
                <th>דגם</th>
                <th>מספר רישוי</th>
                <th>סטטוס</th>
                <th>פעולות</th>
              </tr>
            </thead>
            <tbody>
              {vehicles.length === 0 ? (
                <tr>
                  <td colSpan="6" className="no-data">אין רכבים להצגה</td>
                </tr>
              ) : (
                vehicles.slice(0, 20).map(vehicle => (
                  <tr key={vehicle.license_plate}>
                    <td>{vehicle.brand}</td>
                    <td>{vehicle.model}</td>
                    <td>{vehicle.license_plate}</td>
                    <td>
                      <select
                        value={vehicle.status}
                        onChange={(e) => handleStatusChange(vehicle.license_plate, e.target.value)}
                        className={`status-select status-${vehicle.status}`}
                      >
                        <option value="available">זמין</option>
                        <option value="rented">מושכר</option>
                        <option value="maintenance">בתחזוקה</option>
                      </select>
                    </td>
                    <td className="actions-cell">
                      <button
                        onClick={() => handleEdit(vehicle)}
                        className="edit-button"
                        title="ערוך רכב"
                      >
                        <i className="fas fa-edit"></i>
                      </button>
                      <button
                        onClick={() => handleDelete(vehicle.license_plate)}
                        className="delete-button"
                        title="מחק רכב"
                      >
                        <i className="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Cars; 