import React, { useState, useEffect } from 'react';
import { rentalService, customerService, vehicleService } from '../services/api';
import './Rentals.css';

function Rentals() {
  const [rentals, setRentals] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    customer_id: '',
    vehicle_id: '',
    start_date: '',
    end_date: '',
    pickup_location: '',
    dropoff_location: '',
    notes: ''
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [rentalsData, customersData, vehiclesData] = await Promise.all([
        rentalService.getAll(),
        customerService.getAll(),
        vehicleService.getAll()
      ]);
      setRentals(rentalsData);
      setCustomers(customersData);
      setVehicles(vehiclesData.filter(v => v.status === 'available'));
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
        await rentalService.update(editingId, formData);
      } else {
        await rentalService.create(formData);
      }
      setFormData({
        customer_id: '',
        vehicle_id: '',
        start_date: '',
        end_date: '',
        pickup_location: '',
        dropoff_location: '',
        notes: ''
      });
      setEditingId(null);
      loadData();
    } catch (err) {
      setError('שגיאה בשמירת ההשכרה');
      console.error('Error saving rental:', err);
    }
  };

  const handleEdit = (rental) => {
    setFormData({
      customer_id: rental.customer_id,
      vehicle_id: rental.vehicle_id,
      start_date: rental.start_date,
      end_date: rental.end_date,
      pickup_location: rental.pickup_location || '',
      dropoff_location: rental.dropoff_location || '',
      notes: rental.notes || ''
    });
    setEditingId(rental.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('האם אתה בטוח שברצונך למחוק השכרה זו?')) {
      try {
        await rentalService.delete(id);
        loadData();
      } catch (err) {
        setError('שגיאה במחיקת ההשכרה');
        console.error('Error deleting rental:', err);
      }
    }
  };

  const handleReturn = async (id) => {
    if (window.confirm('האם אתה בטוח שברצונך להחזיר את הרכב?')) {
      try {
        await rentalService.returnVehicle(id);
        loadData();
      } catch (err) {
        setError('שגיאה בהחזרת הרכב');
        console.error('Error returning vehicle:', err);
      }
    }
  };

  const handleCancel = async (id) => {
    if (window.confirm('האם אתה בטוח שברצונך לבטל את ההשכרה?')) {
      try {
        await rentalService.cancel(id);
        loadData();
      } catch (err) {
        setError('שגיאה בביטול ההשכרה');
        console.error('Error cancelling rental:', err);
      }
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
    <div className="rentals-page">
      <h1>ניהול השכרות</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="rental-form">
        <h2>{editingId ? 'עריכת השכרה' : 'השכרה חדשה'}</h2>
        
        <div className="form-group">
          <label htmlFor="customer_id">לקוח:</label>
          <select
            id="customer_id"
            name="customer_id"
            value={formData.customer_id}
            onChange={handleChange}
            required
          >
            <option value="">בחר לקוח</option>
            {customers.map(customer => (
              <option key={customer.id} value={customer.id}>
                {customer.name} - {customer.phone}
              </option>
            ))}
          </select>
        </div>

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
          <label htmlFor="start_date">תאריך התחלה:</label>
          <input
            type="datetime-local"
            id="start_date"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="end_date">תאריך סיום:</label>
          <input
            type="datetime-local"
            id="end_date"
            name="end_date"
            value={formData.end_date}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="pickup_location">מיקום איסוף:</label>
          <input
            type="text"
            id="pickup_location"
            name="pickup_location"
            value={formData.pickup_location}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="dropoff_location">מיקום החזרה:</label>
          <input
            type="text"
            id="dropoff_location"
            name="dropoff_location"
            value={formData.dropoff_location}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="notes">הערות:</label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            rows="3"
          />
        </div>

        <button type="submit" className="submit-button">
          {editingId ? 'עדכן השכרה' : 'צור השכרה'}
        </button>
        
        {editingId && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setFormData({
                customer_id: '',
                vehicle_id: '',
                start_date: '',
                end_date: '',
                pickup_location: '',
                dropoff_location: '',
                notes: ''
              });
            }}
            className="cancel-button"
          >
            ביטול עריכה
          </button>
        )}
      </form>

      <div className="rentals-list">
        <h2>רשימת השכרות</h2>
        <table>
          <thead>
            <tr>
              <th>לקוח</th>
              <th>רכב</th>
              <th>תאריך התחלה</th>
              <th>תאריך סיום</th>
              <th>סטטוס</th>
              <th>פעולות</th>
            </tr>
          </thead>
          <tbody>
            {rentals.slice(0, 20).map(rental => {
              const customer = customers.find(c => c.id === rental.customer_id);
              const vehicle = vehicles.find(v => v.id === rental.vehicle_id);
              return (
                <tr key={rental.id}>
                  <td>{customer ? customer.name : 'לא ידוע'}</td>
                  <td>
                    {vehicle
                      ? `${vehicle.make} ${vehicle.model} (${vehicle.license_plate})`
                      : 'לא ידוע'}
                  </td>
                  <td>{new Date(rental.start_date).toLocaleString()}</td>
                  <td>{new Date(rental.end_date).toLocaleString()}</td>
                  <td>
                    <span className={`status-badge ${getStatusClass(rental.status)}`}>
                      {getStatusText(rental.status)}
                    </span>
                  </td>
                  <td>
                    {rental.status === 'active' && (
                      <>
                        <button
                          onClick={() => handleReturn(rental.id)}
                          className="return-button"
                        >
                          החזר
                        </button>
                        <button
                          onClick={() => handleCancel(rental.id)}
                          className="cancel-button"
                        >
                          בטל
                        </button>
                      </>
                    )}
                    <button
                      onClick={() => handleEdit(rental)}
                      className="edit-button"
                    >
                      ערוך
                    </button>
                    <button
                      onClick={() => handleDelete(rental.id)}
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

export default Rentals; 