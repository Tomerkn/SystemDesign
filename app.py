from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify
)
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_system.db'
db = SQLAlchemy(app)

# פונקציות לעבודה עם בסיס הנתונים

def get_stats():
    # מביא את כל הנתונים הכלליים של המערכת - כמה רכבים יש, כמה לקוחות, וכו'
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Vehicle")
    cars = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Customer")
    customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Rental WHERE endDate >= date('now')")
    active_rentals = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Vehicle WHERE status = 'available'")
    available = c.fetchone()[0]
    conn.close()
    return cars, customers, active_rentals, available

def get_customers():
    # מביא את כל הלקוחות שלנו מהמערכת
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    c.execute("SELECT id, name, phone, email FROM Customer")
    customers = c.fetchall()
    conn.close()
    return customers

def get_vehicles():
    # מביא את כל הרכבים שיש לנו במערכת
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    c.execute("SELECT licensePlate, brand, model, status FROM Vehicle")
    vehicles = c.fetchall()
    conn.close()
    return vehicles

def get_rentals():
    # מביא את כל ההשכרות שיש במערכת, כולל שם הלקוח ומספר הרכב
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    c.execute("""
        SELECT r.rentalId, c.name, v.licensePlate, r.startDate, r.endDate 
        FROM Rental r
        JOIN Customer c ON r.customerId = c.id
        JOIN Vehicle v ON r.vehicleId = v.licensePlate
        ORDER BY r.startDate DESC
    """)
    rentals = c.fetchall()
    conn.close()
    return rentals

# הדפים השונים באתר

@app.route('/')
def index():
    # דף הבית - מציג סטטיסטיקות כלליות על המערכת
    cars, customers, active_rentals, available = get_stats()
    return render_template(
        'index.html',
        cars=cars,
        customers=customers,
        active_rentals=active_rentals,
        available=available
    )

@app.route('/customers')
def customers():
    # דף הלקוחות - מציג את כל הלקוחות במערכת
    customers_list = get_customers()
    return render_template('customers.html', customers=customers_list)

@app.route('/vehicles')
def vehicles():
    # דף הרכבים - מציג את כל הרכבים במערכת
    vehicles_list = get_vehicles()
    return render_template('vehicles.html', vehicles=vehicles_list)

@app.route('/rentals')
def rentals():
    # דף ההשכרות - מציג את כל ההשכרות הפעילות והישנות
    rentals_list = get_rentals()
    today = date.today().isoformat()
    return render_template('rentals.html', rentals=rentals_list, today=today)

# פעולות שאפשר לעשות במערכת

@app.route('/add_customer', methods=['POST'])
def add_customer():
    # הוספת לקוח חדש למערכת
    # אם הלקוח כבר קיים (לפי תעודת זהות), נקבל הודעת שגיאה
    customer_id = request.form.get('id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO Customer (id, name, phone, email) VALUES (?, ?, ?, ?)",
            (customer_id, name, phone, email)
        )
        conn.commit()
        flash('הלקוח נוסף בהצלחה', 'success')
    except sqlite3.IntegrityError:
        flash('הלקוח כבר קיים במערכת', 'error')
    finally:
        conn.close()
    return redirect(url_for('customers'))

@app.route('/add_rental', methods=['POST'])
def add_rental():
    # הוספת השכרה חדשה
    # בודקים שהרכב פנוי ושהתאריכים הגיוניים
    customer_id = request.form.get('customer_id')
    vehicle_id = request.form.get('vehicle_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO Rental (customerId, vehicleId, startDate, endDate) 
            VALUES (?, ?, ?, ?)
        """, (customer_id, vehicle_id, start_date, end_date))
        c.execute("UPDATE Vehicle SET status = 'rented' WHERE licensePlate = ?", 
                 (vehicle_id,))
        conn.commit()
        flash('ההשכרה נוספה בהצלחה', 'success')
    except sqlite3.Error as e:
        flash(f'שגיאה בהוספת ההשכרה: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('rentals'))

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    license_plate = request.form.get('license_plate')
    brand = request.form.get('brand')
    model = request.form.get('model')
    
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        c.execute(
            """
            INSERT INTO Vehicle (licensePlate, brand, model, status)
            VALUES (?, ?, ?, 'available')
            """,
            (license_plate, brand, model)
        )
        conn.commit()
        flash('הרכב נוסף בהצלחה', 'success')
    except sqlite3.IntegrityError:
        flash('רכב עם מספר רישוי זה כבר קיים במערכת', 'error')
    finally:
        conn.close()
    return redirect(url_for('vehicles'))

@app.route('/delete_vehicle', methods=['POST'])
def delete_vehicle():
    license_plate = request.form.get('license_plate')
    
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        # Check if vehicle is currently rented
        c.execute(
            """
            SELECT COUNT(*) FROM Rental
            WHERE vehicleId = ? AND endDate >= date('now')
            """,
            (license_plate,)
        )
        active_rentals = c.fetchone()[0]
        
        if active_rentals > 0:
            flash('לא ניתן למחוק רכב שנמצא בהשכרה פעילה', 'error')
        else:
            c.execute("DELETE FROM Vehicle WHERE licensePlate = ?", (license_plate,))
            conn.commit()
            flash('הרכב נמחק בהצלחה', 'success')
    except sqlite3.Error as e:
        flash(f'שגיאה במחיקת הרכב: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('vehicles'))

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    customer_id = request.form.get('customer_id')
    
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        # Check if customer has active rentals
        c.execute(
            """
            SELECT COUNT(*) FROM Rental
            WHERE customerId = ? AND endDate >= date('now')
            """,
            (customer_id,)
        )
        active_rentals = c.fetchone()[0]
        
        if active_rentals > 0:
            flash('לא ניתן למחוק לקוח עם השכרות פעילות', 'error')
        else:
            c.execute("DELETE FROM Customer WHERE id = ?", (customer_id,))
            conn.commit()
            flash('הלקוח נמחק בהצלחה', 'success')
    except sqlite3.Error as e:
        flash(f'שגיאה במחיקת הלקוח: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('customers'))

@app.route('/end_rental', methods=['POST'])
def end_rental():
    rental_id = request.form.get('rental_id')
    
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        # Get the vehicle ID for this rental
        c.execute("SELECT vehicleId FROM Rental WHERE rentalId = ?", (rental_id,))
        vehicle_id = c.fetchone()[0]
        
        # Update rental end date to today
        c.execute(
            """
            UPDATE Rental
            SET endDate = date('now')
            WHERE rentalId = ?
            """,
            (rental_id,)
        )
        
        # Update vehicle status to available
        c.execute(
            """
            UPDATE Vehicle
            SET status = 'available'
            WHERE licensePlate = ?
            """,
            (vehicle_id,)
        )
        
        conn.commit()
        flash('ההשכרה הסתיימה בהצלחה', 'success')
    except sqlite3.Error as e:
        flash(f'שגיאה בסיום ההשכרה: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('rentals'))

@app.route('/add_rental_page')
def add_rental_page():
    return render_template('add_rental.html')

@app.route('/api/vehicles/available')
def get_available_vehicles():
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        # בדיקה אם קיימת עמודת year בטבלה
        c.execute("PRAGMA table_info(Vehicle)")
        columns = [column[1] for column in c.fetchall()]
        has_year = 'year' in columns
        
        # בניית השאילתה בהתאם לקיום עמודת year
        if has_year:
            query = """
                SELECT licensePlate, brand, model, year 
                FROM Vehicle 
                WHERE status = 'available'
                ORDER BY brand, model
            """
        else:
            query = """
                SELECT licensePlate, brand, model 
                FROM Vehicle 
                WHERE status = 'available'
                ORDER BY brand, model
            """
        
        c.execute(query)
        vehicles = c.fetchall()
        
        # ארגון הרכבים לפי דגם
        vehicles_by_model = {}
        for vehicle in vehicles:
            model_key = f"{vehicle[1]} {vehicle[2]}"  # brand + model
            if model_key not in vehicles_by_model:
                vehicles_by_model[model_key] = []
            
            vehicle_data = {
                'license_plate': vehicle[0],
                'brand': vehicle[1],
                'model': vehicle[2]
            }
            
            # הוספת שנה רק אם היא קיימת
            if has_year and len(vehicle) > 3:
                vehicle_data['year'] = vehicle[3]
            
            vehicles_by_model[model_key].append(vehicle_data)
        
        # המרה לפורמט הרצוי
        result = []
        for model_name, vehicles in vehicles_by_model.items():
            result.append({
                'model_name': model_name,
                'vehicles': vehicles
            })
        
        return jsonify(result)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/customer/<customer_id>')
def get_customer_by_id(customer_id):
    conn = sqlite3.connect("rental_system.db")
    c = conn.cursor()
    try:
        c.execute("SELECT name FROM Customer WHERE id = ?", (customer_id,))
        customer = c.fetchone()
        if customer:
            return jsonify({'name': customer[0]})
        else:
            return jsonify({'error': 'לקוח לא נמצא'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(port=5000, debug=True) 