# ------------------------------------------------------
# ייבוא הספריות הנדרשות
# ------------------------------------------------------
from flask import (
    Flask, request, jsonify, render_template, redirect, url_for, session  # ייבוא רכיבי Flask: אפליקציה, בקשות, JSON, תבניות, הפניות, session
)
from flask_cors import CORS  # ייבוא ספריית CORS לאפשר גישה מדומיינים שונים
from flask_sqlalchemy import SQLAlchemy  # ייבוא ספריית ORM לעבודה עם בסיס הנתונים
from datetime import datetime  # ייבוא ספריית תאריכים
import sqlite3  # ייבוא ספריית בסיס הנתונים SQLite

# ------------------------------------------------------
# יצירת אפליקציית Flask והגדרות ראשוניות
# ------------------------------------------------------
app = Flask(__name__)
# הגדרת CORS לאפשר גישה מכל דומיין (לצורך עבודה עם פרונטנד נפרד)
CORS(app, resources={r"/*": {"origins": "*"}})

# ------------------------------------------------------
# נתיב בדיקה פשוט לוודא שהשרת עובד
# ------------------------------------------------------
@app.route('/')
def test():
    # מחזיר טקסט פשוט כדי לבדוק שהשרת פועל
    return "השרת עובד!"

# ------------------------------------------------------
# הגדרות חיבור לבסיס הנתונים
# ------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_system.db'  # נתיב לקובץ בסיס הנתונים
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # ביטול מעקב אחר שינויים לשיפור ביצועים
# יצירת אובייקט בסיס הנתונים
# (מאפשר עבודה עם ORM של SQLAlchemy)
db = SQLAlchemy(app)

# ------------------------------------------------------
# הגדרת מודלים (טבלאות) של בסיס הנתונים
# ------------------------------------------------------
class Customer(db.Model):
    # טבלת לקוחות
    id = db.Column(db.String(9), primary_key=True)  # מספר ת.ז כמפתח ראשי
    name = db.Column(db.String(100), nullable=False)  # שם מלא - שדה חובה
    phone = db.Column(db.String(20), nullable=False)  # מספר טלפון - שדה חובה
    email = db.Column(db.String(100), nullable=False)  # כתובת אימייל - שדה חובה
    rentals = db.relationship('Rental', backref='customer', lazy=True)  # קשר להשכרות של הלקוח

class Vehicle(db.Model):
    # טבלת רכבים
    license_plate = db.Column(db.String(20), primary_key=True)  # מספר רישוי כמפתח ראשי
    brand = db.Column(db.String(50), nullable=False)  # יצרן הרכב - שדה חובה
    model = db.Column(db.String(50), nullable=False)  # דגם הרכב - שדה חובה
    year = db.Column(db.Integer)  # שנת ייצור
    status = db.Column(db.String(20), default='available')  # סטטוס הרכב - ברירת מחדל: זמין
    rentals = db.relationship('Rental', backref='vehicle', lazy=True)  # קשר להשכרות של הרכב

class Rental(db.Model):
    # טבלת השכרות
    id = db.Column(db.Integer, primary_key=True)  # מזהה ייחודי להשכרה
    customer_id = db.Column(db.String(9), db.ForeignKey('customer.id'), nullable=False)  # מפתח זר ללקוח
    vehicle_id = db.Column(db.String(20), db.ForeignKey('vehicle.license_plate'), nullable=False)  # מפתח זר לרכב
    start_date = db.Column(db.DateTime, nullable=False)  # תאריך התחלת ההשכרה
    end_date = db.Column(db.DateTime, nullable=False)  # תאריך סיום ההשכרה
    total_price = db.Column(db.Float)  # מחיר כולל להשכרה
    status = db.Column(db.String(20), default='active')  # סטטוס ההשכרה - ברירת מחדל: פעיל

class MaintenanceAlert(db.Model):
    # טבלת התראות תחזוקה
    id = db.Column(db.Integer, primary_key=True)  # מזהה ייחודי להתראה
    vehicle_id = db.Column(db.String(20), db.ForeignKey('vehicle.license_plate'), nullable=False)  # מפתח זר לרכב
    due_date = db.Column(db.DateTime, nullable=False)  # תאריך יעד לטיפול
    type = db.Column(db.String(50), nullable=False)  # סוג הטיפול הנדרש
    status = db.Column(db.String(20), default='pending')  # סטטוס ההתראה - ברירת מחדל: ממתין

# ------------------------------------------------------
# API - לקוחות
# ------------------------------------------------------
@app.route('/api/customers', methods=['GET'])
def get_customers():
    # שליפת כל הלקוחות מבסיס הנתונים
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'email': c.email
    } for c in Customer.query.all()])

@app.route('/api/customers', methods=['POST'])
def add_customer():
    # הוספת לקוח חדש
    data = request.json  # קבלת נתוני הלקוח מהבקשה
    try:
        customer = Customer(
            id=data['id'],
            name=data['name'],
            phone=data['phone'],
            email=data['email']
        )
        db.session.add(customer)  # הוספה לבסיס הנתונים
        db.session.commit()  # שמירת השינויים
        return jsonify({'message': 'Customer added successfully'}), 201  # החזרת הודעת הצלחה
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # החזרת הודעת שגיאה במקרה של כישלון

@app.route('/api/customers/<customer_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
def customer_detail(customer_id):
    # עדכון או מחיקת לקוח ספציפי
    if request.method == 'OPTIONS':
        # טיפול בבקשת OPTIONS (נדרש ל-CORS)
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if request.method == 'PUT':
        # עדכון פרטי לקוח
        try:
            data = request.json
            customer = Customer.query.get(customer_id)
            if not customer:
                return jsonify({'error': 'Customer not found'}), 404
            customer.name = data.get('name', customer.name)
            customer.phone = data.get('phone', customer.phone)
            customer.email = data.get('email', customer.email)
            db.session.commit()
            return jsonify({'message': 'Customer updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    if request.method == 'DELETE':
        # מחיקת לקוח
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                return jsonify({'error': 'Customer not found'}), 404
            db.session.delete(customer)
            db.session.commit()
            return jsonify({'message': 'Customer deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Method not allowed'}), 405

# ------------------------------------------------------
# API - רכבים
# ------------------------------------------------------
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    # שליפת כל הרכבים
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'licensePlate': v.license_plate,
        'brand': v.brand,
        'model': v.model,
        'status': v.status
    } for v in Vehicle.query.all()])

@app.route('/api/vehicles', methods=['POST'])
def add_vehicle():
    # הוספת רכב חדש
    data = request.json
    try:
        vehicle = Vehicle(
            license_plate=data['license_plate'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            status=data.get('status', 'available')
        )
        db.session.add(vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vehicles/<license_plate>', methods=['PUT', 'DELETE', 'OPTIONS'])
def vehicle_detail(license_plate):
    # עדכון או מחיקת רכב ספציפי
    if request.method == 'OPTIONS':
        # טיפול בבקשת OPTIONS
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if request.method == 'PUT':
        # עדכון פרטי רכב
        try:
            data = request.json
            vehicle = Vehicle.query.get(license_plate)
            if not vehicle:
                return jsonify({'error': 'Vehicle not found'}), 404
            vehicle.brand = data.get('brand', vehicle.brand)
            vehicle.model = data.get('model', vehicle.model)
            vehicle.year = data.get('year', vehicle.year)
            vehicle.status = data.get('status', vehicle.status)
            db.session.commit()
            return jsonify({'message': 'Vehicle updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    if request.method == 'DELETE':
        # מחיקת רכב
        try:
            vehicle = Vehicle.query.get(license_plate)
            if not vehicle:
                return jsonify({'error': 'Vehicle not found'}), 404
            db.session.delete(vehicle)
            db.session.commit()
            return jsonify({'message': 'Vehicle deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/api/vehicles/<license_plate>/status', methods=['PATCH', 'OPTIONS'])
def update_vehicle_status(license_plate):
    # עדכון סטטוס רכב
    if request.method == 'OPTIONS':
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PATCH, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    try:
        data = request.json
        vehicle = Vehicle.query.get(license_plate)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        if 'status' not in data:
            return jsonify({'error': 'Missing status field'}), 400
        vehicle.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Vehicle status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------------------------
# API - השכרות
# ------------------------------------------------------
@app.route('/api/rentals', methods=['GET'])
def get_rentals():
    # שליפת כל ההשכרות
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'id': r.id,
        'customerId': r.customer_id,
        'vehicleId': r.vehicle_id,
        'startDate': r.start_date.isoformat(),
        'endDate': r.end_date.isoformat(),
        'totalPrice': r.total_price,
        'status': r.status
    } for r in Rental.query.all()])

@app.route('/api/rentals', methods=['POST'])
def add_rental():
    # הוספת השכרה חדשה
    data = request.json
    try:
        rental = Rental(
            customer_id=data['customer_id'],
            vehicle_id=data['vehicle_id'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            total_price=data['total_price'],
            status=data.get('status', 'active')
        )
        db.session.add(rental)
        db.session.commit()
        return jsonify({'message': 'Rental added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------------------------
# API - התראות תחזוקה
# ------------------------------------------------------
@app.route('/api/maintenance/alerts', methods=['GET'])
def get_maintenance_alerts():
    # שליפת כל התראות התחזוקה
    alerts = MaintenanceAlert.query.all()
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'id': alert.id,
        'vehicle_id': alert.vehicle_id,
        'due_date': alert.due_date.isoformat(),
        'type': alert.type,
        'status': alert.status
    } for alert in alerts])

# ------------------------------------------------------
# API - רכבים פנויים
# ------------------------------------------------------
@app.route('/api/vehicles/available', methods=['GET'])
def get_available_vehicles():
    # שליפת כל הרכבים שסטטוס שלהם הוא 'available'
    available_vehicles = Vehicle.query.filter_by(status='available').all()
    return jsonify([{
        'license_plate': v.license_plate,
        'brand': v.brand,
        'model': v.model,
        'year': v.year,
        'status': v.status
    } for v in available_vehicles])

@app.route('/api/vehicles/check-availability', methods=['POST'])
def check_vehicle_availability():
    # בדיקת זמינות רכב בתאריכים מסוימים
    data = request.json
    try:
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
        if start_date >= end_date:
            return jsonify({'error': 'תאריך התחלה חייב להיות לפני תאריך סיום'}), 400
        if start_date < datetime.now():
            return jsonify({'error': 'לא ניתן להזמין רכב בתאריך שעבר'}), 400
        busy_vehicles = Rental.query.filter(
            Rental.status != 'cancelled',
            Rental.vehicle_id == Vehicle.license_plate,
            ((Rental.start_date <= end_date) & (Rental.end_date >= start_date))
        ).with_entities(Rental.vehicle_id).distinct().all()
        busy_vehicle_ids = [v[0] for v in busy_vehicles]
        available_vehicles = Vehicle.query.filter(
            Vehicle.status == 'available',
            ~Vehicle.license_plate.in_(busy_vehicle_ids)
        ).all()
        return jsonify([{
            'license_plate': v.license_plate,
            'brand': v.brand,
            'model': v.model,
            'year': v.year
        } for v in available_vehicles])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vehicles/available-by-model', methods=['GET'])
def get_available_vehicles_by_model():
    # קיבוץ רכבים זמינים לפי דגם
    available_vehicles = Vehicle.query.filter_by(status='available').all()
    vehicles_by_model = {}
    for vehicle in available_vehicles:
        model_key = f"{vehicle.brand} {vehicle.model} ({vehicle.year})"
        if model_key not in vehicles_by_model:
            vehicles_by_model[model_key] = []
        vehicles_by_model[model_key].append({
            'license_plate': vehicle.license_plate,
            'brand': vehicle.brand,
            'model': vehicle.model,
            'year': vehicle.year,
            'status': vehicle.status
        })
    result = []
    for model_key, vehicles in vehicles_by_model.items():
        result.append({
            'model_name': model_key,
            'vehicles': vehicles,
            'count': len(vehicles)
        })
    return jsonify(result)

@app.route('/api/rentals/create-with-availability', methods=['POST'])
def create_rental_with_availability():
    # יצירת השכרה חדשה עם בדיקת זמינות
    data = request.json
    try:
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
        if start_date >= end_date:
            return jsonify({'error': 'תאריך התחלה חייב להיות לפני תאריך סיום'}), 400
        if start_date < datetime.now():
            return jsonify({'error': 'לא ניתן להזמין רכב בתאריך שעבר'}), 400
        vehicle = Vehicle.query.get(data['vehicle_id'])
        if not vehicle:
            return jsonify({'error': 'הרכב המבוקש לא נמצא'}), 404
        if vehicle.status != 'available':
            return jsonify({'error': 'הרכב המבוקש אינו זמין להשכרה'}), 400
        existing_rental = Rental.query.filter(
            Rental.vehicle_id == data['vehicle_id'],
            Rental.status != 'cancelled',
            ((Rental.start_date <= end_date) & (Rental.end_date >= start_date))
        ).first()
        if existing_rental:
            return jsonify({'error': 'הרכב כבר מושכר בתאריכים אלו'}), 400
        days = (end_date - start_date).days
        total_price = days * 200
        rental = Rental(
            customer_id=data['customer_id'],
            vehicle_id=data['vehicle_id'],
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='active'
        )
        vehicle.status = 'rented'
        db.session.add(rental)
        db.session.commit()
        return jsonify({
            'message': 'ההשכרה נוצרה בהצלחה',
            'rental_id': rental.id,
            'total_price': total_price,
            'days': days
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ------------------------------------------------------
# דפי HTML (למשל דף הוספת השכרה)
# ------------------------------------------------------
@app.route('/add-rental')
def add_rental_page():
    # החזרת דף HTML להוספת השכרה
    return render_template('add_rental.html')

# ------------------------------------------------------
# התחברות (Login) - API + דף HTML
# ------------------------------------------------------
@app.route('/api/login', methods=['POST'])
def api_login():
    # התחברות דרך API (לשימוש פרונטנד)
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect('rental_system.db')
    c = conn.cursor()
    c.execute(
        "SELECT role FROM SystemUser WHERE username=? AND password=?",
        (username, password)
    )
    result = c.fetchone()
    conn.close()
    if result:
        return jsonify({'message': 'Login successful', 'role': result[0]}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/', methods=['GET'])
def root():
    # הפניה לדף התחברות HTML
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # דף התחברות HTML
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('rental_system.db')
        c = conn.cursor()
        c.execute(
            "SELECT role FROM SystemUser WHERE username=? AND password=?",
            (username, password)
        )
        result = c.fetchone()
        conn.close()
        if result:
            session['username'] = username
            session['role'] = result[0]
            return redirect(url_for('welcome'))
        else:
            error = 'שם משתמש או סיסמה שגויים'
    return render_template('login.html', error=error)

@app.route('/welcome')
def welcome():
    # דף ברוך הבא לאחר התחברות
    if not session.get('username'):
        return redirect(url_for('root_login'))
    return f"<h2>ברוך הבא, {session['username']}!</h2>"

# ------------------------------------------------------
# הפעלת השרת
# ------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():  # יצירת הקשר אפליקציה
        db.create_all()  # יצירת כל הטבלאות בבסיס הנתונים
    app.run(host='0.0.0.0', port=5001, debug=True)  # הפעלת השרת בפורט 5001 עם מצב דיבאג