# Version 1.1 - Firmware Update
# הספריות שאנחנו צריכים בשביל לעקוב אחרי הרכבים
import sqlite3
from datetime import datetime, timedelta

# איפה שומרים את כל המידע
DB_PATH = "rental_system.db"


class DrivingData:
    # עוקב אחרי איך נוהגים ברכב - מהירות, בלימות וכו'
    def __init__(self, vehicle_id):
        # כשמתחילים לעקוב אחרי רכב חדש
        self.vehicle_id = vehicle_id      # איזה רכב זה
        self.date = datetime.now()        # מתי הנסיעה התחילה
        self.avg_speed = 0.0              # כמה מהר נסעו בממוצע
        self.harsh_brakes = 0             # כמה פעמים בלמו חזק מדי

    def calculate_score(self):
        # נותן ציון לנהיגה - 100 זה מושלם, 0 זה ממש גרוע
        score = 100  # מתחילים מציון מושלם
        
        # מורידים נקודות אם נסעו מהר מדי (מעל 100 קמ"ש)
        if self.avg_speed > 100:
            score -= (self.avg_speed - 100) * 0.5
        
        # מורידים נקודות על כל בלימת חירום
        score -= self.harsh_brakes * 5
        
        # מחזירים ציון בין 0 ל-100
        return max(0, min(100, score))

    def save(self):
        # שומר את כל הנתונים על הנסיעה בבסיס הנתונים
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
    # מטפל בכל ההתראות על טיפולים שצריך לעשות לרכבים
    def __init__(self, vehicle_id):
        # כשיוצרים התראה חדשה על טיפול
        self.vehicle_id = vehicle_id      # לאיזה רכב צריך לעשות את הטיפול
        self.alert_id = None              # מספר מזהה להתראה
        self.due_date = None              # עד מתי צריך לעשות את הטיפול
        self.type = None                  # איזה סוג של טיפול צריך

    def generate_alert(self, alert_type, days_until_due=30):
        # יוצר התראה חדשה על טיפול שצריך לעשות
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
        # שולח הודעה למנהל על טיפול שצריך לעשות
        # בעתיד נוסיף פה שליחת מייל או הודעה בטלפון
        print(f"התראת תחזוקה: רכב {self.vehicle_id}")
        print(f"סוג טיפול: {self.type}")
        print(f"תאריך יעד: {self.due_date.strftime('%Y-%m-%d')}")

    @staticmethod
    def get_pending_alerts(vehicle_id=None):
        # מביא את כל הטיפולים שעוד לא נעשו
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if vehicle_id:
            # אם ביקשו טיפולים של רכב ספציפי
            c.execute("""
                SELECT alertId, vehicleId, dueDate, type 
                FROM MaintenanceAlert 
                WHERE vehicleId = ?
                ORDER BY dueDate
            """, (vehicle_id,))
        else:
            # אם רוצים לראות את כל הטיפולים של כל הרכבים
            c.execute("""
                SELECT alertId, vehicleId, dueDate, type 
                FROM MaintenanceAlert 
                ORDER BY dueDate
            """)
            
        alerts = c.fetchall()
        conn.close()
        return alerts 