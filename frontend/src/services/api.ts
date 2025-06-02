import axios from 'axios';

// כתובת בסיס ל-API
const API_URL = 'http://localhost:5000/api';

// יצירת מופע axios עם הגדרות בסיסיות
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ממשק עבור לקוח
export interface Customer {
  id: string;      // מזהה ייחודי
  name: string;    // שם מלא
  phone: string;   // מספר טלפון
  email: string;   // כתובת אימייל
}

// ממשק עבור רכב
export interface Vehicle {
  licensePlate: string;  // מספר רישוי
  brand: string;         // יצרן
  model: string;         // דגם
  status: 'available' | 'rented' | 'maintenance';  // סטטוס: זמין, מושכר, בתחזוקה
}

// ממשק עבור השכרה
export interface Rental {
  id: string;           // מזהה ייחודי
  customer_id: string;  // מזהה הלקוח
  vehicle_id: string;   // מזהה הרכב
  start_date: string;   // תאריך התחלה (מחרוזת ISO)
  end_date: string;     // תאריך סיום (מחרוזת ISO)
  total_price: number;  // מחיר כולל
  status: 'active' | 'completed' | 'cancelled';  // סטטוס: פעיל, הושלם, בוטל
}

// קריאות API ללקוחות
export const getCustomers = () => api.get<Customer[]>('/customers');  // קבלת כל הלקוחות
export const createCustomer = (customer: Omit<Customer, 'id'>) =>     // יצירת לקוח חדש
  api.post<Customer>('/customers', customer);

// קריאות API לרכבים
export const getVehicles = () => api.get<Vehicle[]>('/vehicles');    // קבלת כל הרכבים
export const createVehicle = (vehicle: Omit<Vehicle, 'id'>) =>       // יצירת רכב חדש
  api.post<Vehicle>('/vehicles', vehicle);

// קריאות API להשכרות
export const getRentals = () => api.get<Rental[]>('/rentals');       // קבלת כל ההשכרות
export const createRental = (rental: Omit<Rental, 'id'>) =>          // יצירת השכרה חדשה
  api.post<Rental>('/rentals', rental);

export default api; 