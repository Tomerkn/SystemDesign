import sqlite3
# ייבוא ספריית בסיס הנתונים
from datetime import datetime, timedelta
# ייבוא ספריות לעבודה עם תאריכים

DB_PATH = "rental_system.db"
# הגדרת נתיב לקובץ בסיס הנתונים


class DrivingData:
    # מחלקה לניהול נתוני נהיגה של רכב
    def __init__(self, vehicle_id):
        # אתחול אובייקט נתוני נהיגה
        self.vehicle_id = vehicle_id
        # מספר רישוי הרכב
        self.date = datetime.now()
        # תאריך הנסיעה
        self.avg_speed = 0.0
        # מהירות ממוצעת
        self.harsh_brakes = 0
        # מספר בלימות חדות

    def calculate_score(self):
        # חישוב ציון נהיגה על בסיס המדדים
        score = 100
        # ציון התחלתי מקסימלי
        
        # הורדת נקודות על מהירות גבוהה (מעל 100 קמ"ש)
        if self.avg_speed > 100:
            score -= (self.avg_speed - 100) * 0.5
        
        # הורדת נקודות על בלימות חדות
        score -= self.harsh_brakes * 5
        
        # החזרת ציון בטווח 0-100
        return max(0, min(100, score))

    def save(self):
        # שמירת נתוני הנהיגה בבסיס הנתונים
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO DrivingData (vehicleId, date, avgSpeed, harshBrakes)
            VALUES (?, ?, ?, ?)
        """, (self.vehicle_id, self.date.strftime('%Y-%m-%d'),
              self.avg_speed, self.harsh_brakes))
        conn.commit()
        conn.close()


class MaintenanceAlert:
    # מחלקה לניהול התראות תחזוקה
    def __init__(self, vehicle_id):
        # אתחול אובייקט התראת תחזוקה
        self.vehicle_id = vehicle_id
        # מספר רישוי הרכב
        self.alert_id = None
        # מזהה ההתראה
        self.due_date = None
        # תאריך יעד לטיפול
        self.type = None
        # סוג הטיפול הנדרש

    def generate_alert(self, alert_type, days_until_due=30):
        # יצירת התראת תחזוקה חדשה
        self.type = alert_type
        self.due_date = datetime.now() + timedelta(days=days_until_due)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO MaintenanceAlert (vehicleId, dueDate, type)
            VALUES (?, ?, ?)
        """, (self.vehicle_id, self.due_date.strftime('%Y-%m-%d'), self.type))
        
        self.alert_id = c.lastrowid
        conn.commit()
        conn.close()

    def notify_manager(self):
        # שליחת התראה למנהל המערכת
        # במערכת אמיתית, כאן תהיה שליחת מייל או התראה
        print(f"התראת תחזוקה: רכב {self.vehicle_id}")
        print(f"סוג טיפול: {self.type}")
        print(f"תאריך יעד: {self.due_date.strftime('%Y-%m-%d')}")

    @staticmethod
    def get_pending_alerts(vehicle_id=None):
        # קבלת רשימת התראות תחזוקה פתוחות
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if vehicle_id:
            # קבלת התראות לרכב ספציפי
            c.execute("""
                SELECT alertId, vehicleId, dueDate, type 
                FROM MaintenanceAlert 
                WHERE vehicleId = ?
                ORDER BY dueDate
            """, (vehicle_id,))
        else:
            # קבלת כל ההתראות במערכת
            c.execute("""
                SELECT alertId, vehicleId, dueDate, type 
                FROM MaintenanceAlert 
                ORDER BY dueDate
            """)
            
        alerts = c.fetchall()
        conn.close()
        return alerts 