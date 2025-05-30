import React, { useState } from 'react';
import { vehicleService, customerService } from '../services/api';
import './BookingForm.css';

const BookingForm = () => {
  const [formData, setFormData] = useState({
    pickupLocation: '',
    dropoffLocation: '',
    pickupDate: '',
    dropoffDate: '',
    carType: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // כאן נוסיף את הלוגיקה לשמירת ההזמנה
      console.log('Booking form submitted:', formData);
    } catch (error) {
      console.error('Error submitting booking:', error);
    }
  };

  return (
    <form className="booking-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>מיקום איסוף</label>
        <input
          type="text"
          name="pickupLocation"
          value={formData.pickupLocation}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      
      <div className="form-group">
        <label>מיקום החזרה</label>
        <input
          type="text"
          name="dropoffLocation"
          value={formData.dropoffLocation}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      
      <div className="form-group">
        <label>תאריך איסוף</label>
        <input
          type="datetime-local"
          name="pickupDate"
          value={formData.pickupDate}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      
      <div className="form-group">
        <label>תאריך החזרה</label>
        <input
          type="datetime-local"
          name="dropoffDate"
          value={formData.dropoffDate}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      
      <div className="form-group">
        <label>סוג רכב</label>
        <select
          name="carType"
          value={formData.carType}
          onChange={handleChange}
          className="form-control"
          required
        >
          <option value="">בחר סוג רכב</option>
          <option value="economy">כלכלי</option>
          <option value="compact">קומפקטי</option>
          <option value="midsize">בינוני</option>
          <option value="luxury">יוקרתי</option>
          <option value="suv">שטח</option>
        </select>
      </div>
      
      <button type="submit" className="btn btn-success">
        הזמן עכשיו
      </button>
    </form>
  );
};

export default BookingForm; 