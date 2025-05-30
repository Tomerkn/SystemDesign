import sqlite3  # מייבא את הספרייה שעובדת עם מסד נתונים

def init_database():  # פונקציה שמייצרת את מסד הנתונים
    conn = sqlite3.connect('rental_system.db')  # יוצר חיבור למסד
    c = conn.cursor()  # יוצר סמן לעבודה עם המסד

    # יוצר טבלת לקוחות
    c.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    ''')

    # יוצר טבלת רכבים
    c.execute('''
        CREATE TABLE IF NOT EXISTS Vehicle (
            licensePlate TEXT PRIMARY KEY,
            brand TEXT,
            model TEXT,
            status TEXT DEFAULT 'available'
        )
    ''')

    # יוצר טבלת השכרות
    c.execute('''
        CREATE TABLE IF NOT EXISTS Rental (
            rentalId INTEGER PRIMARY KEY AUTOINCREMENT,
            customerId TEXT,
            vehicleId TEXT,
            startDate TEXT,
            endDate TEXT,
            totalPrice TEXT,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (customerId) REFERENCES Customer(id),
            FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)
        )
    ''')

    # יוצר טבלת נתוני נהיגה
    c.execute('''
        CREATE TABLE IF NOT EXISTS DrivingData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicleId TEXT,
            date TEXT,
            avgSpeed REAL,
            harshBrakes INTEGER,
            FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)
        )
    ''')

    # יוצר טבלת התראות טיפול
    c.execute('''
        CREATE TABLE IF NOT EXISTS MaintenanceAlert (
            alertId INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicleId TEXT,
            dueDate TEXT,
            type TEXT,
            FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)
        )
    ''')

    conn.commit()  # שומר את השינויים במסד
    conn.close()   # סוגר את החיבור למסד

if __name__ == "__main__":  # בודק אם הקובץ מופעל ישירות
    init_database()  # מפעיל את הפונקציה שמייצרת את המסד
    print("Database initialized successfully!")  # מדפיס הודעת הצלחה 