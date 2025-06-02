import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = 'rental_system.db'

# מילון המרה משמות בעברית לאנגלית
hebrew_to_english = {
    # שמות פרטיים
    'אברהם': 'abraham',
    'יצחק': 'isaac',
    'יעקב': 'jacob',
    'משה': 'moshe',
    'דוד': 'david',
    'שלמה': 'shlomo',
    'יוסף': 'joseph',
    'דניאל': 'daniel',
    'איתן': 'eitan',
    'נועם': 'noam',
    'שרה': 'sarah',
    'רבקה': 'rebecca',
    'רחל': 'rachel',
    'לאה': 'leah',
    'מרים': 'miriam',
    'חנה': 'hannah',
    'רות': 'ruth',
    'אסתר': 'esther',
    'תמר': 'tamar',
    'נועה': 'noa',
    'עומר': 'omer',
    'איתי': 'itay',
    'אלון': 'alon',
    'גיל': 'gil',
    'רון': 'ron',
    'ליאור': 'lior',
    'עידן': 'idan',
    'טל': 'tal',
    'יובל': 'yuval',
    'אורי': 'uri',
    'מיכל': 'michal',
    'יעל': 'yael',
    'שירה': 'shira',
    'אביגיל': 'abigail',
    'הדר': 'hadar',
    'עדי': 'adi',
    'שני': 'shani',
    'רוני': 'roni',
    'דנה': 'dana',
    'ליאת': 'liat',
    # שמות משפחה
    'כהן': 'cohen',
    'לוי': 'levi',
    'מזרחי': 'mizrachi',
    'פרץ': 'peretz',
    'ביטון': 'biton',
    'דהן': 'dahan',
    'אברהם': 'abraham',
    'פרידמן': 'friedman',
    'גולדשטיין': 'goldstein',
    'רוזנברג': 'rosenberg',
    'אזולאי': 'azulay',
    'אוחיון': 'ochion',
    'מלכה': 'malka',
    'חדד': 'hadad',
    'גבאי': 'gabay',
    'אדרי': 'edry',
    'אלבז': 'elbaz',
    'בוזגלו': 'bouzaglo',
    'אמסלם': 'amsalem',
    'דוידוב': 'davidov',
    'שפירא': 'shapira',
    'ברקוביץ׳': 'berkovich',
    'גרינברג': 'greenberg',
    'רבינוביץ׳': 'rabinovich',
    'וייס': 'weiss',
    'קליין': 'klein',
    'הורוביץ': 'horowitz',
    'פלדמן': 'feldman',
    'שטרן': 'stern',
    'קצב': 'katzav'
}

# מערכים של שמות ישראליים נפוצים
first_names = [
    'אברהם', 'יצחק', 'יעקב', 'משה', 'דוד', 'שלמה', 'יוסף', 'דניאל', 'איתן',
    'נועם', 'שרה', 'רבקה', 'רחל', 'לאה', 'מרים', 'חנה', 'רות', 'אסתר', 'תמר',
    'נועה', 'עומר', 'איתי', 'אלון', 'גיל', 'רון', 'ליאור', 'עידן', 'טל',
    'יובל', 'אורי', 'מיכל', 'יעל', 'שירה', 'אביגיל', 'הדר', 'עדי', 'שני',
    'רוני', 'דנה', 'ליאת'
]

last_names = [
    'כהן', 'לוי', 'מזרחי', 'פרץ', 'ביטון', 'דהן', 'אברהם', 'פרידמן',
    'גולדשטיין', 'רוזנברג', 'אזולאי', 'אוחיון', 'מלכה', 'חדד', 'גבאי', 'אדרי',
    'אלבז', 'בוזגלו', 'אמסלם', 'דוידוב', 'שפירא', 'ברקוביץ׳', 'גרינברג',
    'רבינוביץ׳', 'וייס', 'קליין', 'הורוביץ', 'פלדמן', 'שטרן', 'קצב'
]

# רכבים נפוצים בחברות השכרה בישראל
rental_cars = [
    # (יצרן, דגם, שנה, מחיר ליום)
    ('טויוטה', 'קורולה', 2023, 200),
    ('יונדאי', 'איוניק', 2023, 220),
    ('קיה', 'פיקנטו', 2023, 160),
    ('סקודה', 'אוקטביה', 2023, 240),
    ('טויוטה', 'יאריס', 2023, 180),
    ('יונדאי', 'i10', 2023, 150),
    ('קיה', 'סטוניק', 2023, 220),
    ('סיאט', 'איביזה', 2023, 180),
    ('פיג׳ו', '208', 2023, 190),
    ('רנו', 'קליאו', 2023, 180),
    ('מאזדה', '2', 2023, 190),
    ('סוזוקי', 'סוויפט', 2023, 170),
    ('פולקסווגן', 'פולו', 2023, 200),
    ('שברולט', 'ספארק', 2023, 150),
    ('מיצובישי', 'ספייס-סטאר', 2023, 160),
    # רכבים משפחתיים
    ('טויוטה', 'RAV4', 2023, 350),
    ('קיה', 'ספורטאז׳', 2023, 320),
    ('יונדאי', 'טוסון', 2023, 330),
    ('סקודה', 'קאמיק', 2023, 300),
    ('פיג׳ו', '3008', 2023, 340)
]

def generate_israeli_phone():
    """יצירת מספר טלפון ישראלי תקין"""
    prefixes = ['050', '052', '053', '054', '055', '058']
    return f"{random.choice(prefixes)}-{random.randint(1000000,9999999)}"

def generate_israeli_id():
    """יצירת ת.ז ישראלית תקינה"""
    # יצירת מספר ת.ז בסיסי שמתחיל ב-2-3 ספרות אקראיות ואחריהן 5-6 ספרות אקראיות
    # מספרים שמתחילים ב-2 או 3 נפוצים בת.ז ישראליות
    first_digits = random.randint(200, 399)  
    # שאר הספרות
    rest_digits = random.randint(10000, 999999)  
    
    # יצירת המספר המלא (ללא ספרת ביקורת)
    n = int(f"{first_digits}{rest_digits:06d}")
    
    # חישוב ספרת ביקורת
    total = 0
    for i, digit in enumerate(str(n)):
        digit = int(digit)
        if i % 2 == 0:  # מיקום זוגי
            digit *= 1
        else:  # מיקום אי-זוגי
            digit *= 2
            if digit > 9:
                digit = digit % 10 + digit // 10
        total += digit
    
    check_digit = (10 - (total % 10)) % 10
    return f"{n}{check_digit}"

def generate_license_plate():
    """יצירת מספר רישוי ישראלי בפורמט החדש"""
    nums = [
        random.randint(10, 99),
        random.randint(100, 999),
        random.randint(10, 99)
    ]
    return f"{nums[0]}-{nums[1]}-{nums[2]}"

# יצירת נתונים
customers = []
for _ in range(40):  # 40 לקוחות
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    id_num = generate_israeli_id()
    phone = generate_israeli_phone()
    # המרת השמות לאנגלית לצורך כתובת האימייל
    first_eng = hebrew_to_english[first]
    last_eng = hebrew_to_english[last]
    email = f"{first_eng}.{last_eng}@gmail.com"
    customers.append((id_num, name, phone, email))

# יצירת רכבים
vehicles = []
for brand, model, year, daily_price in rental_cars:
    license_plate = generate_license_plate()
    vehicles.append((license_plate, brand, model, 'available'))

# יצירת השכרות
rentals = []
for _ in range(30):  # 30 השכרות
    customer = random.choice(customers)
    vehicle = random.choice(vehicles)
    # תאריכי השכרה בטווח של החודש האחרון עד החודש הבא
    start_date = datetime.now() - timedelta(days=random.randint(-30, 30))
    duration = random.randint(1, 14)  # השכרה של 1-14 ימים
    end_date = start_date + timedelta(days=duration)
    
    # מחיר ההשכרה - מחיר יומי * מספר ימים
    car_price = next(
        price for b, m, y, price in rental_cars
        if b == vehicle[1] and m == vehicle[2]
    )
    total_price = car_price * duration
    
    # סטטוס ההשכרה
    if end_date < datetime.now():
        status = 'completed'
    elif start_date > datetime.now():
        status = 'pending'
    else:
        status = 'active'
    
    rentals.append((
        customer[0],  # customer_id
        vehicle[0],   # vehicle_id
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        total_price,
        status
    ))

# הכנסת הנתונים לבסיס הנתונים
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# מחיקת נתונים קיימים
c.execute("DELETE FROM Rental")
c.execute("DELETE FROM Customer")
c.execute("DELETE FROM Vehicle")

# הכנסת לקוחות
for customer in customers:
    c.execute("""
        INSERT OR REPLACE INTO Customer (id, name, phone, email)
        VALUES (?, ?, ?, ?)
    """, customer)

# הכנסת רכבים
for vehicle in vehicles:
    c.execute("""
        INSERT OR REPLACE INTO Vehicle (licensePlate, brand, model, status)
        VALUES (?, ?, ?, ?)
    """, vehicle)

# הכנסת השכרות
for rental in rentals:
    c.execute("""
        INSERT OR REPLACE INTO Rental 
        (customerId, vehicleId, startDate, endDate, totalPrice, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rental)

conn.commit()
conn.close()

print(f"""הנתונים הוזנו בהצלחה למערכת:
- {len(customers)} לקוחות
- {len(vehicles)} רכבים
- {len(rentals)} השכרות""") 