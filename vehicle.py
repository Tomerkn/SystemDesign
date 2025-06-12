# Version 1.1 - Firmware Update
import sqlite3
# מייבא את הספריות שאנחנו צריכים
from vehicle_monitoring import DrivingData, MaintenanceAlert
# ייבוא מחלקות ניטור רכב והתראות תחזוקה

# איפה נמצא בסיס הנתונים שלנו
DB_PATH = "rental_system.db"


class Vehicle:
    # כל רכב במערכת מיוצג על ידי המחלקה הזו
    def __init__(self, license_plate, brand=None, model=None):
        # כשיוצרים רכב חדש, צריך לפחות את מספר הרישוי שלו
        self.license_plate = license_plate  # מספר הרישוי
        self.brand = brand                  # איזה יצרן (טויוטה, הונדה וכו')
        self.model = model                  # איזה דגם ספציפי
        self.status = 'available'           # האם הרכב פנוי להשכרה
        
        # אם לא נתנו לנו את כל הפרטים, ננסה למצוא אותם בבסיס הנתונים
        if brand is None or model is None:
            self._load_from_db()

    def _load_from_db(self):
        # מנסה למצוא את פרטי הרכב בבסיס הנתונים
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
        # משנה את המצב של הרכב (פנוי, מושכר, בטיפול)
        if new_status not in ['available', 'rented', 'maintenance']:
            raise ValueError("סטטוס לא חוקי")
            
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
        # קובע תור לטיפול ברכב
        # אפשר לקבוע טיפול למועד עתידי או לטיפול מיידי
        alert = MaintenanceAlert(self.license_plate)
        alert.generate_alert(maintenance_type, days_until_due)
        
        # אם זה טיפול דחוף, הרכב עובר למצב "בטיפול" מיד
        if days_until_due == 0:
            self.update_status('maintenance')
        
        # שולח הודעה למנהל על הטיפול המתוכנן
        alert.notify_manager()

    def get_driving_data(self):
        # מביא את כל הנתונים על איך נהגו ברכב לאחרונה
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
        # מביא את כל ההתראות על טיפולים שצריך לעשות לרכב
        return MaintenanceAlert.get_pending_alerts(self.license_plate)

    def record_driving_data(self, avg_speed, harsh_brakes):
        # שומר מידע חדש על נסיעה שנעשתה ברכב
        data = DrivingData(self.license_plate)
        data.avg_speed = avg_speed
        data.harsh_brakes = harsh_brakes
        data.save()
        
        # בודק אם הנהיגה הייתה בעייתית ואולי צריך לבדוק את הרכב
        score = data.calculate_score()
        if score < 60:  # אם הציון נמוך מדי
            # קובע בדיקה תוך שבוע
            self.schedule_maintenance("בדיקה בגלל נהיגה בעייתית", 7) 