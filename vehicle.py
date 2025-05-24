import sqlite3
# ייבוא ספריית בסיס הנתונים
from datetime import datetime, timedelta
# ייבוא ספריות לעבודה עם תאריכים
from vehicle_monitoring import DrivingData, MaintenanceAlert
# ייבוא מחלקות ניטור רכב והתראות תחזוקה

DB_PATH = "rental_system.db"
# הגדרת נתיב לקובץ בסיס הנתונים


class Vehicle:
    # מחלקה המייצגת רכב במערכת
    def __init__(self, license_plate, brand=None, model=None):
        # אתחול אובייקט רכב חדש
        self.license_plate = license_plate
        # מספר רישוי
        self.brand = brand
        # יצרן הרכב
        self.model = model
        # דגם הרכב
        self.status = 'available'
        # סטטוס הרכב - זמין כברירת מחדל
        
        # טעינת נתוני רכב מבסיס הנתונים אם לא סופקו
        if brand is None or model is None:
            self._load_from_db()

    def _load_from_db(self):
        # טעינת נתוני רכב מבסיס הנתונים
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT brand, model, status 
            FROM Vehicle 
            WHERE licensePlate = ?
        """, (self.license_plate,))
        
        result = c.fetchone()
        if result:
            self.brand = result[0]
            self.model = result[1]
            self.status = result[2]
        
        conn.close()

    def update_status(self, new_status):
        # עדכון סטטוס הרכב
        if new_status not in ['available', 'rented', 'maintenance']:
            raise ValueError("Invalid status")
            
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            UPDATE Vehicle 
            SET status = ? 
            WHERE licensePlate = ?
        """, (new_status, self.license_plate))
        
        conn.commit()
        conn.close()
        self.status = new_status

    def schedule_maintenance(self, maintenance_type, days_until_due=30):
        # תזמון טיפול לרכב
        alert = MaintenanceAlert(self.license_plate)
        alert.generate_alert(maintenance_type, days_until_due)
        
        # עדכון סטטוס הרכב לתחזוקה אם הטיפול מיידי
        if days_until_due == 0:
            self.update_status('maintenance')
        
        # שליחת התראה למנהל
        alert.notify_manager()

    def get_driving_data(self):
        # קבלת היסטוריית נתוני נהיגה של הרכב
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT date, avgSpeed, harshBrakes 
            FROM DrivingData 
            WHERE vehicleId = ?
            ORDER BY date DESC
        """, (self.license_plate,))
        
        data = c.fetchall()
        conn.close()
        return data

    def get_maintenance_alerts(self):
        # קבלת רשימת התראות תחזוקה לרכב
        return MaintenanceAlert.get_pending_alerts(self.license_plate)

    def record_driving_data(self, avg_speed, harsh_brakes):
        # תיעוד נתוני נהיגה חדשים
        data = DrivingData(self.license_plate)
        data.avg_speed = avg_speed
        data.harsh_brakes = harsh_brakes
        data.save()
        
        # חישוב ציון נהיגה ותזמון טיפול במידת הצורך
        score = data.calculate_score()
        if score < 60:  # אם ציון הנהיגה נמוך, תזמון בדיקת רכב
            self.schedule_maintenance("בדיקת ציון נהיגה נמוך", 7) 