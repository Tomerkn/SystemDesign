# ייבוא הספריות הנדרשות
from flask import Flask, request, jsonify, render_template  # הוספת render_template
from flask_cors import CORS  # ייבוא ספריית CORS לאפשר גישה מדומיינים שונים
from flask_sqlalchemy import SQLAlchemy  # ייבוא ספריית ORM לעבודה עם בסיס הנתונים
from datetime import datetime  # ייבוא ספריית תאריכים
import os  # ייבוא ספריית מערכת ההפעלה
import sqlite3  # ייבוא ספריית בסיס הנתונים SQLite

# יצירת אפליקציית Flask
app = Flask(__name__)
# הגדרת CORS לאפשר גישה מכל דומיין
CORS(app, resources={r"/*": {"origins": "*"}})

# נתיב בדיקה פשוט לוודא שהשרת עובד
@app.route('/')
def test():
    return "השרת עובד!"

# הגדרת הגדרות חיבור לבסיס הנתונים
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_system.db'  # נתיב לקובץ בסיס הנתונים
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # ביטול מעקב אחר שינויים לשיפור ביצועים
db = SQLAlchemy(app)  # יצירת אובייקט בסיס הנתונים

# הגדרת מודל לקוח
class Customer(db.Model):
    id = db.Column(db.String(9), primary_key=True)  # מספר ת.ז כמפתח ראשי
    name = db.Column(db.String(100), nullable=False)  # שם מלא - שדה חובה
    phone = db.Column(db.String(20), nullable=False)  # מספר טלפון - שדה חובה
    email = db.Column(db.String(100), nullable=False)  # כתובת אימייל - שדה חובה
    rentals = db.relationship('Rental', backref='customer', lazy=True)  # קשר להשכרות של הלקוח

# הגדרת מודל רכב
class Vehicle(db.Model):
    license_plate = db.Column(db.String(20), primary_key=True)  # מספר רישוי כמפתח ראשי
    brand = db.Column(db.String(50), nullable=False)  # יצרן הרכב - שדה חובה
    model = db.Column(db.String(50), nullable=False)  # דגם הרכב - שדה חובה
    year = db.Column(db.Integer)  # שנת ייצור
    status = db.Column(db.String(20), default='available')  # סטטוס הרכב - ברירת מחדל: זמין
    rentals = db.relationship('Rental', backref='vehicle', lazy=True)  # קשר להשכרות של הרכב

# הגדרת מודל השכרה
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # מזהה ייחודי להשכרה
    customer_id = db.Column(db.String(9), db.ForeignKey('customer.id'), nullable=False)  # מפתח זר ללקוח
    vehicle_id = db.Column(db.String(20), db.ForeignKey('vehicle.license_plate'), nullable=False)  # מפתח זר לרכב
    start_date = db.Column(db.DateTime, nullable=False)  # תאריך התחלת ההשכרה
    end_date = db.Column(db.DateTime, nullable=False)  # תאריך סיום ההשכרה
    total_price = db.Column(db.Float)  # מחיר כולל להשכרה
    status = db.Column(db.String(20), default='active')  # סטטוס ההשכרה - ברירת מחדל: פעיל

# הגדרת מודל התראת תחזוקה
class MaintenanceAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # מזהה ייחודי להתראה
    vehicle_id = db.Column(db.String(20), db.ForeignKey('vehicle.license_plate'), nullable=False)  # מפתח זר לרכב
    due_date = db.Column(db.DateTime, nullable=False)  # תאריך יעד לטיפול
    type = db.Column(db.String(50), nullable=False)  # סוג הטיפול הנדרש
    status = db.Column(db.String(20), default='pending')  # סטטוס ההתראה - ברירת מחדל: ממתין

# נתיב לקבלת כל הלקוחות
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()  # שליפת כל הלקוחות מבסיס הנתונים
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'email': c.email
    } for c in customers])

# נתיב להוספת לקוח חדש
@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.json  # קבלת נתוני הלקוח מהבקשה
    try:
        # יצירת אובייקט לקוח חדש
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

# נתיב לעדכון או מחיקת לקוח ספציפי
@app.route('/api/customers/<customer_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
def customer_detail(customer_id):
    # טיפול בבקשת OPTIONS (נדרש ל-CORS)
    if request.method == 'OPTIONS':
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # עדכון פרטי לקוח
    if request.method == 'PUT':
        try:
            data = request.json  # קבלת נתוני העדכון
            customer = Customer.query.get(customer_id)  # מציאת הלקוח
            if not customer:
                return jsonify({'error': 'Customer not found'}), 404
            # עדכון הפרטים
            customer.name = data.get('name', customer.name)
            customer.phone = data.get('phone', customer.phone)
            customer.email = data.get('email', customer.email)
            db.session.commit()  # שמירת השינויים
            return jsonify({'message': 'Customer updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # מחיקת לקוח
    if request.method == 'DELETE':
        try:
            customer = Customer.query.get(customer_id)  # מציאת הלקוח
            if not customer:
                return jsonify({'error': 'Customer not found'}), 404
            db.session.delete(customer)  # מחיקת הלקוח
            db.session.commit()  # שמירת השינויים
            return jsonify({'message': 'Customer deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Method not allowed'}), 405

# נתיב לקבלת כל הרכבים
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()  # שליפת כל הרכבים
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'license_plate': v.license_plate,
        'brand': v.brand,
        'model': v.model,
        'year': v.year,
        'status': v.status
    } for v in vehicles])

# נתיב להוספת רכב חדש
@app.route('/api/vehicles', methods=['POST'])
def add_vehicle():
    data = request.json  # קבלת נתוני הרכב מהבקשה
    try:
        # יצירת אובייקט רכב חדש
        vehicle = Vehicle(
            license_plate=data['license_plate'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            status=data.get('status', 'available')
        )
        db.session.add(vehicle)  # הוספה לבסיס הנתונים
        db.session.commit()  # שמירת השינויים
        return jsonify({'message': 'Vehicle added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# נתיב לעדכון או מחיקת רכב ספציפי
@app.route('/api/vehicles/<license_plate>', methods=['PUT', 'DELETE', 'OPTIONS'])
def vehicle_detail(license_plate):
    # טיפול בבקשת OPTIONS
    if request.method == 'OPTIONS':
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # עדכון פרטי רכב
    if request.method == 'PUT':
        try:
            data = request.json  # קבלת נתוני העדכון
            vehicle = Vehicle.query.get(license_plate)  # מציאת הרכב
            if not vehicle:
                return jsonify({'error': 'Vehicle not found'}), 404
            # עדכון הפרטים
            vehicle.brand = data.get('brand', vehicle.brand)
            vehicle.model = data.get('model', vehicle.model)
            vehicle.year = data.get('year', vehicle.year)
            vehicle.status = data.get('status', vehicle.status)
            db.session.commit()  # שמירת השינויים
            return jsonify({'message': 'Vehicle updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # מחיקת רכב
    if request.method == 'DELETE':
        try:
            vehicle = Vehicle.query.get(license_plate)  # מציאת הרכב
            if not vehicle:
                return jsonify({'error': 'Vehicle not found'}), 404
            db.session.delete(vehicle)  # מחיקת הרכב
            db.session.commit()  # שמירת השינויים
            return jsonify({'message': 'Vehicle deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Method not allowed'}), 405

# נתיב לעדכון סטטוס רכב
@app.route('/api/vehicles/<license_plate>/status', methods=['PATCH', 'OPTIONS'])
def update_vehicle_status(license_plate):
    # טיפול בבקשת OPTIONS
    if request.method == 'OPTIONS':
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PATCH, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    try:
        data = request.json  # קבלת נתוני העדכון
        vehicle = Vehicle.query.get(license_plate)  # מציאת הרכב
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        if 'status' not in data:
            return jsonify({'error': 'Missing status field'}), 400
        vehicle.status = data['status']  # עדכון הסטטוס
        db.session.commit()  # שמירת השינויים
        return jsonify({'message': 'Vehicle status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# נתיב לקבלת כל ההשכרות
@app.route('/api/rentals', methods=['GET'])
def get_rentals():
    rentals = Rental.query.all()  # שליפת כל ההשכרות
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'id': r.id,
        'customer_id': r.customer_id,
        'vehicle_id': r.vehicle_id,
        'start_date': r.start_date.isoformat(),
        'end_date': r.end_date.isoformat(),
        'total_price': r.total_price,
        'status': r.status
    } for r in rentals])

# נתיב להוספת השכרה חדשה
@app.route('/api/rentals', methods=['POST'])
def add_rental():
    data = request.json  # קבלת נתוני ההשכרה מהבקשה
    try:
        # יצירת אובייקט השכרה חדש
        rental = Rental(
            customer_id=data['customer_id'],
            vehicle_id=data['vehicle_id'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            total_price=data['total_price'],
            status=data.get('status', 'active')
        )
        db.session.add(rental)  # הוספה לבסיס הנתונים
        db.session.commit()  # שמירת השינויים
        return jsonify({'message': 'Rental added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# נתיב לקבלת כל התראות התחזוקה
@app.route('/api/maintenance/alerts', methods=['GET'])
def get_maintenance_alerts():
    alerts = MaintenanceAlert.query.all()  # שליפת כל ההתראות
    return jsonify([{  # המרת הנתונים לפורמט JSON
        'id': alert.id,
        'vehicle_id': alert.vehicle_id,
        'due_date': alert.due_date.isoformat(),
        'type': alert.type,
        'status': alert.status
    } for alert in alerts])

# נתיב לקבלת כל הרכבים הפנויים להשכרה
@app.route('/api/vehicles/available', methods=['GET'])
def get_available_vehicles():
    # שליפת כל הרכבים שסטטוס שלהם הוא 'available'
    available_vehicles = Vehicle.query.filter_by(status='available').all()
    
    # המרת הנתונים לפורמט JSON
    return jsonify([{
        'license_plate': v.license_plate,
        'brand': v.brand,
        'model': v.model,
        'year': v.year,
        'status': v.status
    } for v in available_vehicles])

# נתיב לבדיקת זמינות רכב בתאריכים מסוימים
@app.route('/api/vehicles/check-availability', methods=['POST'])
def check_vehicle_availability():
    data = request.json  # קבלת נתוני הבקשה
    
    try:
        # המרת התאריכים מסטרינג לאובייקט תאריך
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
        
        # בדיקה שהתאריכים הגיוניים
        if start_date >= end_date:
            return jsonify({'error': 'תאריך התחלה חייב להיות לפני תאריך סיום'}), 400
            
        if start_date < datetime.now():
            return jsonify({'error': 'לא ניתן להזמין רכב בתאריך שעבר'}), 400
        
        # מציאת כל הרכבים שפנויים בטווח התאריכים המבוקש
        busy_vehicles = Rental.query.filter(
            Rental.status != 'cancelled',  # לא כולל השכרות שבוטלו
            Rental.vehicle_id == Vehicle.license_plate,  # חיבור לטבלת רכבים
            # בדיקת חפיפה בין התאריכים המבוקשים להשכרות קיימות
            ((Rental.start_date <= end_date) & (Rental.end_date >= start_date))
        ).with_entities(Rental.vehicle_id).distinct().all()
        
        # המרה לרשימת מספרי רישוי
        busy_vehicle_ids = [v[0] for v in busy_vehicles]
        
        # שליפת כל הרכבים הפנויים
        available_vehicles = Vehicle.query.filter(
            Vehicle.status == 'available',  # רק רכבים במצב 'זמין'
            ~Vehicle.license_plate.in_(busy_vehicle_ids)  # לא כולל רכבים תפוסים
        ).all()
        
        return jsonify([{
            'license_plate': v.license_plate,
            'brand': v.brand,
            'model': v.model,
            'year': v.year
        } for v in available_vehicles])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# נתיב לקבלת רכבים זמינים מקובצים לפי דגם
@app.route('/api/vehicles/available-by-model', methods=['GET'])
def get_available_vehicles_by_model():
    # שליפת כל הרכבים הזמינים
    available_vehicles = Vehicle.query.filter_by(status='available').all()
    
    # יצירת מילון לקיבוץ הרכבים לפי דגם
    vehicles_by_model = {}
    
    for vehicle in available_vehicles:
        # יצירת מפתח מדגם הרכב
        model_key = f"{vehicle.brand} {vehicle.model} ({vehicle.year})"
        
        # אם הדגם לא קיים במילון, יוצרים רשימה חדשה
        if model_key not in vehicles_by_model:
            vehicles_by_model[model_key] = []
            
        # הוספת הרכב לרשימת הרכבים מאותו דגם
        vehicles_by_model[model_key].append({
            'license_plate': vehicle.license_plate,
            'brand': vehicle.brand,
            'model': vehicle.model,
            'year': vehicle.year,
            'status': vehicle.status
        })
    
    # המרת המילון לרשימה של דגמים עם הרכבים שלהם
    result = []
    for model_key, vehicles in vehicles_by_model.items():
        result.append({
            'model_name': model_key,
            'vehicles': vehicles,
            'count': len(vehicles)  # כמה רכבים זמינים מדגם זה
        })
    
    return jsonify(result)

# נתיב ליצירת השכרה חדשה עם בדיקת זמינות
@app.route('/api/rentals/create-with-availability', methods=['POST'])
def create_rental_with_availability():
    data = request.json  # קבלת נתוני ההשכרה מהבקשה
    
    try:
        # המרת התאריכים מסטרינג לאובייקט תאריך
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
        
        # בדיקה שהתאריכים הגיוניים
        if start_date >= end_date:
            return jsonify({'error': 'תאריך התחלה חייב להיות לפני תאריך סיום'}), 400
            
        if start_date < datetime.now():
            return jsonify({'error': 'לא ניתן להזמין רכב בתאריך שעבר'}), 400
        
        # בדיקה שהרכב המבוקש זמין בתאריכים אלו
        vehicle = Vehicle.query.get(data['vehicle_id'])
        if not vehicle:
            return jsonify({'error': 'הרכב המבוקש לא נמצא'}), 404
            
        if vehicle.status != 'available':
            return jsonify({'error': 'הרכב המבוקש אינו זמין להשכרה'}), 400
            
        # בדיקה שאין השכרות חופפות לרכב זה
        existing_rental = Rental.query.filter(
            Rental.vehicle_id == data['vehicle_id'],
            Rental.status != 'cancelled',
            ((Rental.start_date <= end_date) & (Rental.end_date >= start_date))
        ).first()
        
        if existing_rental:
            return jsonify({'error': 'הרכב כבר מושכר בתאריכים אלו'}), 400
            
        # חישוב מחיר ההשכרה (לדוגמה: 200 ש"ח ליום)
        days = (end_date - start_date).days
        total_price = days * 200
        
        # יצירת השכרה חדשה
        rental = Rental(
            customer_id=data['customer_id'],
            vehicle_id=data['vehicle_id'],
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='active'
        )
        
        # עדכון סטטוס הרכב ל'מושכר'
        vehicle.status = 'rented'
        
        # שמירת השינויים בבסיס הנתונים
        db.session.add(rental)
        db.session.commit()
        
        return jsonify({
            'message': 'ההשכרה נוצרה בהצלחה',
            'rental_id': rental.id,
            'total_price': total_price,
            'days': days
        }), 201
        
    except Exception as e:
        db.session.rollback()  # ביטול השינויים במקרה של שגיאה
        return jsonify({'error': str(e)}), 400

# נתיב לדף הוספת השכרה חדשה
@app.route('/add-rental')
def add_rental_page():
    return render_template('add_rental.html')

# הפעלת השרת
if __name__ == '__main__':
    with app.app_context():  # יצירת הקשר אפליקציה
        db.create_all()  # יצירת כל הטבלאות בבסיס הנתונים
    app.run(host='0.0.0.0', port=5001, debug=True)  # הפעלת השרת בפורט 5001 עם מצב דיבאג