import axios from 'axios';

const API_URL = 'http://localhost:5001/api';

// הגדרת axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// שירות לקוחות
export const customerService = {
  getAll: () => api.get('/customers').then(res => res.data),
  getById: (id) => api.get(`/customers/${id}`).then(res => res.data),
  create: (data) => api.post('/customers', data).then(res => res.data),
  update: (id, data) => api.put(`/customers/${id}`, data).then(res => res.data),
  delete: (id) => api.delete(`/customers/${id}`).then(res => res.data)
};

// שירות רכבים
export const vehicleService = {
  getAll: () => api.get('/vehicles').then(res => res.data),
  getById: (id) => api.get(`/vehicles/${id}`).then(res => res.data),
  create: (data) => api.post('/vehicles', data).then(res => res.data),
  update: (id, data) => api.put(`/vehicles/${id}`, data).then(res => res.data),
  delete: (id) => api.delete(`/vehicles/${id}`).then(res => res.data),
  updateStatus: (id, status) => api.patch(`/vehicles/${id}/status`, { status }).then(res => res.data)
};

// שירות השכרות
export const rentalService = {
  getAll: () => api.get('/rentals').then(res => res.data),
  getById: (id) => api.get(`/rentals/${id}`).then(res => res.data),
  create: (data) => api.post('/rentals', data).then(res => res.data),
  update: (id, data) => api.put(`/rentals/${id}`, data).then(res => res.data),
  delete: (id) => api.delete(`/rentals/${id}`).then(res => res.data),
  returnVehicle: (id) => api.post(`/rentals/${id}/return`).then(res => res.data),
  cancel: (id) => api.post(`/rentals/${id}/cancel`).then(res => res.data)
};

// שירות תחזוקה
export const maintenanceService = {
  getAll: () => api.get('/maintenance/alerts').then(res => res.data),
  getById: (id) => api.get(`/maintenance/alerts/${id}`).then(res => res.data),
  create: (data) => api.post('/maintenance/alerts', data).then(res => res.data),
  update: (id, data) => api.put(`/maintenance/alerts/${id}`, data).then(res => res.data),
  delete: (id) => api.delete(`/maintenance/alerts/${id}`).then(res => res.data),
  complete: (id) => api.post(`/maintenance/alerts/${id}/complete`).then(res => res.data)
};

export default {
  customerService,
  vehicleService,
  rentalService,
  maintenanceService
}; 