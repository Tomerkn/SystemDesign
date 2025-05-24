# Car Rental Management System

A simple car rental management system with a graphical user interface built using Python and SQLite.

## Features

- Customer registration
- Vehicle rental
- Vehicle return
- Rental history viewing
- Right-to-left (RTL) interface support for Hebrew

## Requirements

- Python 3.x
- tkinter (usually comes with Python)
- sqlite3 (usually comes with Python)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Initialize the database:
```bash
python init_db.py
```
4. Run the application:
```bash
python rental_app.py
```

## Usage

The application has four main tabs:

1. **Customer Registration (רישום לקוח)**
   - Enter customer ID, name, phone, and email
   - Click "Add Customer" to register

2. **Rent Vehicle (השכרת רכב)**
   - Enter customer ID, vehicle license plate, start date, and end date
   - Click "Rent Vehicle" to process the rental

3. **Return Vehicle (החזרת רכב)**
   - Enter vehicle license plate
   - Click "Return Vehicle" to process the return

4. **Rental List (רשימת השכרות)**
   - View all rentals
   - Click "Refresh" to update the list

## Sample Vehicles

The system comes with three sample vehicles pre-loaded:
- License Plate: 123-456-78
- License Plate: 234-567-89
- License Plate: 345-678-90

## Date Format

Enter dates in YYYY-MM-DD format (e.g., 2024-03-20) 