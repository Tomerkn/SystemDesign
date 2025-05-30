import React, { useState, useEffect } from 'react';
import { customerService } from '../services/api';
import './Customers.css';

function Customers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    phone: '',
    email: ''
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      const data = await customerService.getAll();
      setCustomers(data);
      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת הלקוחות');
      console.error('Error loading customers:', err);
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
        await customerService.update(editingId, formData);
      } else {
        await customerService.create(formData);
      }
      setFormData({ id: '', name: '', phone: '', email: '' });
      setEditingId(null);
      loadCustomers();
    } catch (err) {
      setError('שגיאה בשמירת הלקוח');
      console.error('Error saving customer:', err);
    }
  };

  const handleEdit = (customer) => {
    setFormData({
      id: customer.id,
      name: customer.name,
      phone: customer.phone,
      email: customer.email
    });
    setEditingId(customer.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('האם אתה בטוח שברצונך למחוק לקוח זה?')) {
      try {
        await customerService.delete(id);
        loadCustomers();
      } catch (err) {
        setError('שגיאה במחיקת הלקוח');
        console.error('Error deleting customer:', err);
      }
    }
  };

  if (loading) {
    return <div className="loading">טוען...</div>;
  }

  return (
    <div className="customers-page">
      <h1>ניהול לקוחות</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="customer-form">
        <h2>{editingId ? 'עריכת לקוח' : 'הוספת לקוח חדש'}</h2>
        
        <div className="form-group">
          <label htmlFor="id">תעודת זהות:</label>
          <input
            type="text"
            id="id"
            name="id"
            value={formData.id}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="name">שם מלא:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="phone">טלפון:</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">דוא"ל:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" className="submit-button">
          {editingId ? 'עדכן לקוח' : 'הוסף לקוח'}
        </button>
        
        {editingId && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setFormData({ id: '', name: '', phone: '', email: '' });
            }}
            className="cancel-button"
          >
            ביטול עריכה
          </button>
        )}
      </form>

      <div className="customers-list">
        <h2>רשימת לקוחות</h2>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>שם</th>
                <th>טלפון</th>
                <th>דוא"ל</th>
                <th>פעולות</th>
              </tr>
            </thead>
            <tbody>
              {customers.length === 0 ? (
                <tr>
                  <td colSpan="5" className="no-data">אין לקוחות להצגה</td>
                </tr>
              ) : (
                customers.slice(0, 20).map(customer => (
                  <tr key={customer.id}>
                    <td>{customer.name}</td>
                    <td>{customer.phone}</td>
                    <td>{customer.email}</td>
                    <td className="actions-cell">
                      <button
                        onClick={() => handleEdit(customer)}
                        className="edit-button"
                        title="ערוך לקוח"
                      >
                        <i className="fas fa-edit"></i>
                      </button>
                      <button
                        onClick={() => handleDelete(customer.id)}
                        className="delete-button"
                        title="מחק לקוח"
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

export default Customers; 