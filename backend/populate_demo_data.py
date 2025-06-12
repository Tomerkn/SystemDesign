import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = 'rental_system.db'

# נתוני דוגמה
first_names = [
    'דוד', 'יוסי', 'משה', 'רונית', 'אורית', 'אייל', 'נועה', 'שירה', 'אורי', 'רועי',
    'איילת', 'גדי', 'אורן', 'טל', 'דנה', 'רוני', 'איתי', 'עדי', 'לירון', 'שחר'
]
last_names = [
    'כהן', 'לוי', 'מזרחי', 'פרץ', 'דוד', 'אברהם', 'ביטון', 'חדד', 'מלכה', 'חיים',
    'סבן', 'סויסה', 'אלבז', 'בן דוד', 'שטרית', 'אזולאי', 'עמר', 'אליהו', 'סבן', 'ברק'
]
car_brands = [
    ('טויוטה', 'קורולה'), ('יונדאי', 'איוניק'), ('קיה', 'ספורטאז'), ('סיאט', 'לאון'),
    ('מאזדה', '3'), ('פיג׳ו', '208'), ('רנו', 'קליאו'), ('פולקסווגן', 'גולף'),
    ('סקודה', 'אוקטביה'), ('הונדה', 'סיוויק'), ('ניסאן', 'קשקאי'), ('סובארו', 'XV'),
    ('פיאט', '500'), ('סיטרואן', 'C3'), ('שברולט', 'ספארק'), ('פורד', 'פוקוס'),
    ('אופל', 'אסטרה'), ('סוזוקי', 'סוויפט'), ('מיצובישי', 'אאוטלנדר'), ('יונדאי', 'טוסון')
]

# יצירת 20 לקוחות
customers = []
for i in range(20):
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    id_num = str(300000000 + i)  # ת.ז פיקטיבית
    phone = f"05{random.randint(0,9)}-{random.randint(1000000,9999999)}"
    email = f"{first.lower()}.{last.lower()}@gmail.com"
    customers.append((id_num, name, phone, email))

# יצירת 20 רכבים
vehicles = []
for i, (brand, model) in enumerate(car_brands):
    license_plate = f"{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(10,99)}"
    vehicles.append((license_plate, brand, model, 'available'))

# יצירת 20 השכרות
rentals = []
for i in range(20):
    customer_id = customers[i][0]
    vehicle_id = vehicles[i][0]
    start_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d')
    total_price = random.randint(500, 2500)
    status = 'active'
    rentals.append((customer_id, vehicle_id, start_date, end_date, total_price, status))

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# הכנסת לקוחות
for cid, name, phone, email in customers:
    c.execute("INSERT OR IGNORE INTO Customer (id, name, phone, email) VALUES (?, ?, ?, ?)", (cid, name, phone, email))

# הכנסת רכבים
for license_plate, brand, model, status in vehicles:
    c.execute("INSERT OR IGNORE INTO Vehicle (licensePlate, brand, model, status) VALUES (?, ?, ?, ?)", (license_plate, brand, model, status))

# הכנסת השכרות
for customer_id, vehicle_id, start_date, end_date, total_price, status in rentals:
    c.execute("INSERT INTO Rental (customerId, vehicleId, startDate, endDate, totalPrice, status) VALUES (?, ?, ?, ?, ?, ?)", (customer_id, vehicle_id, start_date, end_date, total_price, status))

conn.commit()
conn.close()

print("הוזנו 20 לקוחות, 20 רכבים ו-20 השכרות לדוגמה!") 