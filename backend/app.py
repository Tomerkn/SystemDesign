from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# נתיב בדיקה פשוט
@app.route('/')
def test():
    return "השרת עובד!"

# הגדרת חיבור לבסיס הנתונים
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# מודלים
class Customer(db.Model):
    id = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    rentals = db.relationship('Rental', backref='customer', lazy=True)

class Vehicle(db.Model):
    license_plate = db.Column(db.String(20), primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    status = db.Column(db.String(20), default='available')
    rentals = db.relationship('Rental', backref='vehicle', lazy=True)

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(9), db.ForeignKey('customer.id'), nullable=False)
    vehicle_id = db.Column(db.String(20), db.ForeignKey('vehicle.license_plate'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')

class MaintenanceAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(20), db.ForeignKey('vehicle.license_plate'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')

# נתיבים
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'email': c.email
    } for c in customers])

@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.json
    try:
        customer = Customer(
            id=data['id'],
            name=data['name'],
            phone=data['phone'],
            email=data['email']
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'Customer added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/customers/<customer_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
def customer_detail(customer_id):
    if request.method == 'OPTIONS':
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if request.method == 'PUT':
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

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'license_plate': v.license_plate,
        'brand': v.brand,
        'model': v.model,
        'year': v.year,
        'status': v.status
    } for v in vehicles])

@app.route('/api/vehicles', methods=['POST'])
def add_vehicle():
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
    if request.method == 'OPTIONS':
        response = app.make_response(('', 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if request.method == 'PUT':
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

@app.route('/api/rentals', methods=['GET'])
def get_rentals():
    rentals = Rental.query.all()
    return jsonify([{
        'id': r.id,
        'customer_id': r.customer_id,
        'vehicle_id': r.vehicle_id,
        'start_date': r.start_date.isoformat(),
        'end_date': r.end_date.isoformat(),
        'total_price': r.total_price,
        'status': r.status
    } for r in rentals])

@app.route('/api/rentals', methods=['POST'])
def add_rental():
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

@app.route('/api/maintenance/alerts', methods=['GET'])
def get_maintenance_alerts():
    alerts = MaintenanceAlert.query.all()
    return jsonify([{
        'id': alert.id,
        'vehicle_id': alert.vehicle_id,
        'due_date': alert.due_date.isoformat(),
        'type': alert.type,
        'status': alert.status
    } for alert in alerts])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True) 