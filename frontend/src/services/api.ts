import axios from 'axios';

const API_URL = 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Customer {
  id: string;
  name: string;
  phone: string;
  email: string;
}

export interface Vehicle {
  licensePlate: string;
  brand: string;
  model: string;
  status: 'available' | 'rented' | 'maintenance';
}

export interface Rental {
  id: string;
  customer_id: string;
  vehicle_id: string;
  start_date: string; // ISO string
  end_date: string;   // ISO string
  total_price: number;
  status: 'active' | 'completed' | 'cancelled';
}

// Customer API calls
export const getCustomers = () => api.get<Customer[]>('/customers');
export const createCustomer = (customer: Omit<Customer, 'id'>) =>
  api.post<Customer>('/customers', customer);

// Vehicle API calls
export const getVehicles = () => api.get<Vehicle[]>('/vehicles');
export const createVehicle = (vehicle: Omit<Vehicle, 'id'>) =>
  api.post<Vehicle>('/vehicles', vehicle);

// Rental API calls
export const getRentals = () => api.get<Rental[]>('/rentals');
export const createRental = (rental: Omit<Rental, 'id'>) =>
  api.post<Rental>('/rentals', rental);

export default api; 