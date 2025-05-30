import React, { useState, useEffect } from 'react';
import { customerService, vehicleService, rentalService } from '../services/api';
import './Booking.css';

function Booking() {
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

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [customersData, vehiclesData] = await Promise.all([
        customerService.getAll(),
        vehicleService.getAll()
      ]);
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
      await rentalService.create(formData);
      setFormData({
        customer_id: '',
        vehicle_id: '',
        start_date: '',
        end_date: '',
        pickup_location: '',
        dropoff_location: '',
        notes: ''
      });
      alert('ההשכרה נוצרה בהצלחה!');
    } catch (err) {
      setError('שגיאה ביצירת ההשכרה');
      console.error('Error creating rental:', err);
    }
  };

  if (loading) {
    return <div className="loading">טוען...</div>;
  }

  return (
    <div className="booking-page">
      <h1>הזמנת רכב</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="booking-form">
        <div className="form-section">
          <h2>פרטי לקוח</h2>
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
        </div>

        <div className="form-section">
          <h2>פרטי רכב</h2>
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
        </div>

        <div className="form-section">
          <h2>פרטי השכרה</h2>
          <div className="form-row">
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
          </div>

          <div className="form-row">
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
        </div>

        <button type="submit" className="submit-button">
          צור השכרה
        </button>
      </form>
    </div>
  );
}

export default Booking; 