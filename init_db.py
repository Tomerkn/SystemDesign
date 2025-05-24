import sqlite3  # מייבא את הספרייה שעובדת עם מסד נתונים

def init_database():  # פונקציה שמייצרת את מסד הנתונים
    conn = sqlite3.connect('rental_system.db')  # יוצר חיבור למסד
    c = conn.cursor()  # יוצר סמן לעבודה עם המסד

    # יוצר טבלת לקוחות
    c.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            id TEXT PRIMARY KEY,  # ת.ז כמפתח ראשי
            name TEXT NOT NULL,   # שם (חובה למלא)
            phone TEXT,           # טלפון
            email TEXT            # אימייל
        )
    ''')

    # יוצר טבלת רכבים
    c.execute('''
        CREATE TABLE IF NOT EXISTS Vehicle (
            licensePlate TEXT PRIMARY KEY,  # מספר רישוי כמפתח ראשי
            brand TEXT,                     # יצרן
            model TEXT,                     # דגם
            status TEXT DEFAULT 'available'  # סטטוס (ברירת מחדל: פנוי)
        )
    ''')

    # יוצר טבלת השכרות
    c.execute('''
        CREATE TABLE IF NOT EXISTS Rental (
            rentalId INTEGER PRIMARY KEY AUTOINCREMENT,  # מספר השכרה (עולה אוטומטית)
            customerId TEXT,                             # ת.ז של הלקוח
            vehicleId TEXT,                              # מספר רישוי של הרכב
            startDate TEXT,                              # תאריך התחלה
            endDate TEXT,                                # תאריך סיום
            totalPrice TEXT,                             # מחיר כולל
            status TEXT DEFAULT 'active',                # סטטוס (ברירת מחדל: פעיל)
            FOREIGN KEY (customerId) REFERENCES Customer(id),          # קישור ללקוח
            FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)   # קישור לרכב
        )
    ''')

    # יוצר טבלת נתוני נהיגה
    c.execute('''
        CREATE TABLE IF NOT EXISTS DrivingData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # מזהה ייחודי
            vehicleId TEXT,                        # מספר רישוי של הרכב
            date TEXT,                             # תאריך הנסיעה
            avgSpeed REAL,                         # מהירות ממוצעת
            harshBrakes INTEGER,                   # מספר בלימות חזקות
            FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)  # קישור לרכב
        )
    ''')

    # יוצר טבלת התראות טיפול
    c.execute('''
        CREATE TABLE IF NOT EXISTS MaintenanceAlert (
            alertId INTEGER PRIMARY KEY AUTOINCREMENT,  # מזהה התראה
            vehicleId TEXT,                             # מספר רישוי של הרכב
            dueDate TEXT,                               # תאריך יעד לטיפול
            type TEXT,                                  # סוג הטיפול
            FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)  # קישור לרכב
        )
    ''')

    conn.commit()  # שומר את השינויים במסד
    conn.close()   # סוגר את החיבור למסד

if __name__ == "__main__":  # בודק אם הקובץ מופעל ישירות
    init_database()  # מפעיל את הפונקציה שמייצרת את המסד
    print("Database initialized successfully!")  # מדפיס הודעת הצלחה 